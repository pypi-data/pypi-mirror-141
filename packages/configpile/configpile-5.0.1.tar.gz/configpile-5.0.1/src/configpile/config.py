from __future__ import annotations

import abc
import argparse
import os
import sys
import textwrap
from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Annotated, get_args, get_origin, get_type_hints

from . import arg, types
from .arg import Arg, Cmd, Expander, HelpCmd, Param, Positional
from .collector import Instance
from .errors import ArgErr, Err, ManyErr, Result, collect
from .sources import (
    CommandLine,
    DefaultValue,
    EnvironmentVariables,
    IniSection,
    IniSectionSource,
    Source,
)
from .util import ClassDoc, filter_types_single

C = TypeVar("C", bound="Config")


@dataclass(frozen=True)
class ConfigProcessor(Generic[C]):
    """
    Process command-line arguments

    """

    cs: ConfigStructure[C]
    cwd: Path
    args: Sequence[str]
    env: Mapping[str, str]

    def command_line(self) -> Result[CommandLine]:
        """
        Constructs a command line source

        Returns:
            A source or an error
        """
        exp_flags = {flag: cmd.inserts() for (flag, cmd) in self.cs.cl_expanders.items()}
        val_flags = frozenset(self.cs.cl_flag_params.keys())
        cmd_flags = frozenset(self.cs.cl_non_expander_cmds.keys())
        return CommandLine.make(
            args=self.args,
            expanding_flags=exp_flags,
            flags_followed_by_value=val_flags,
            command_flags=cmd_flags,
        )

    def environment_variables(self) -> Result[EnvironmentVariables]:
        """
        Constructs a source from environment variables

        Returns:
            A source or an error
        """
        return EnvironmentVariables(self.env)

    def process(self) -> Result[Union[C, Cmd]]:
        """
        Runs the processing

        Returns:
            A parsed configuration or an error
        """
        cs = self.cs
        config_sources: Result[Tuple[CommandLine, EnvironmentVariables]] = collect(
            self.command_line(), self.environment_variables()
        )
        if isinstance(config_sources, Err):
            return config_sources
        cl, env = config_sources

        for flag, cmd in cs.cl_non_expander_cmds.items():
            if flag in cl.commands:
                return cmd

        ini_from_env: Result[Sequence[Instance[Sequence[Path]]]] = env[cs.ini_files]
        if isinstance(ini_from_env, Err):
            return ini_from_env
        ini_from_cl: Result[Sequence[Instance[Sequence[Path]]]] = cl[cs.ini_files]
        if isinstance(ini_from_cl, Err):
            return ini_from_cl
        default = DefaultValue()
        sources: List[Source] = [default, env]
        ini_instances: Sequence[Path] = [
            ins for instances in [*ini_from_env, *ini_from_cl] for ins in instances.value
        ]
        for fn in ini_instances:
            sections_res = IniSectionSource.from_file(
                self.cwd / fn, cs.ini_sections, cs.ini_params
            )
            if isinstance(sections_res, Err):
                return sections_res
            sources.extend(sections_res)
        sources.append(cl)
        values: List[Tuple[str, Any]] = []
        errs: List[Err] = []
        for name, arg in cs.params.items():
            res = Source.collect(sources, arg)
            if isinstance(res, Err):
                errs.append(ArgErr(arg, res))
            else:
                values.append((name, res))
        if errs:
            return ManyErr(errs)
        else:
            return cs.config(**dict(values))


@dataclass(frozen=True)
class ConfigStructure(Generic[C]):
    config: Type[C]

    prog: str  #: Program name
    description: Optional[str]  #: Text to display before the argument help
    env_prefix: Optional[str]  #: Prefix of environment variables

    ini_files: Param[Sequence[Path]]  #: Parameter describing INI files to parse

    ini_sections: Sequence[IniSection]  #: Sequence of INI sections to parse

    #: All parameters indexed by destination field
    params: Mapping[str, Param[Any]]

    #: All commands
    commands: Sequence[Cmd]

    #: Command-line commands that are not expanders
    cl_non_expander_cmds: Mapping[str, Cmd]

    #: Command-line commands that are expanders
    cl_expanders: Mapping[str, Expander]

    #: Parameters triggered by command-line flags, indexed by their flags
    cl_flag_params: Mapping[str, Param[Any]]

    #: Positional command-line parameters
    cl_positional: Optional[Param[Any]]

    #: Parameters present in configuration files, indexed by their key
    ini_params: Mapping[str, Param[Any]]

    #: Parameters present in environment variables, indexed by variable name
    env_params: Mapping[str, Param[Any]]

    @staticmethod
    def from_config(config_type: Type[C]) -> ConfigStructure[C]:

        # fill program name from script invocation
        prog = config_type.prog_
        if prog is None:
            prog = sys.argv[0]
        # fill description from class docstring
        description: Optional[str] = config_type.description_
        if description is None:
            description = config_type.__doc__
        env_prefix = config_type.env_prefix_
        ini_sections: Sequence[IniSection] = config_type.ini_sections_()

        args: List[Arg] = []
        params: Dict[str, Param[Any]] = {}
        commands: List[Cmd] = []
        cl_non_expander_cmds: Dict[str, Cmd] = {}
        cl_expanders: Dict[str, Expander] = {}
        cl_flag_params: Dict[str, Param[Any]] = {}
        cl_positional: Optional[Param[Any]] = None
        ini_files: Optional[Param[Sequence[Path]]] = None
        ini_params: Dict[str, Param[Any]] = {}
        env_params: Dict[str, Param[Any]] = {}

        docs: ClassDoc[C] = ClassDoc.make(config_type)

        th = get_type_hints(config_type, include_extras=True)
        for name, typ in th.items():
            arg: Optional[Arg] = None
            if get_origin(typ) is ClassVar:
                a = getattr(config_type, name)
                if isinstance(a, Arg):
                    assert isinstance(a, Cmd), "Only commands (Cmd) can be class attributes"
                    arg = a
            if get_origin(typ) is Annotated:
                param = filter_types_single(Param, get_args(typ))
                if param is not None:
                    arg = param
            if arg is not None:
                help_lines = docs[name]
                if help_lines is None:
                    help = ""
                else:
                    help = "\n".join(help_lines)
                arg = arg.updated(name, help, config_type.env_prefix_)
                args.append(arg)
                if name == "config":
                    assert isinstance(arg, Param)
                    ini_files = arg

        for arg in args:
            if isinstance(arg, Param):
                assert arg.name is not None
                params[arg.name] = arg
                if arg.positional != Positional.FORBIDDEN:
                    assert cl_positional is None, "Only one positional argument is allowed"
                    cl_positional = arg
                for flag in arg.all_flags():
                    cl_flag_params[flag] = arg
                for key in arg.all_config_key_names():
                    ini_params[key] = arg
                for name in arg.all_env_var_names():
                    env_params[name] = arg
            elif isinstance(arg, Cmd):
                commands.append(arg)
                for flag in arg.all_flags():
                    if isinstance(arg, Expander):
                        cl_expanders[flag] = arg
                    else:
                        cl_non_expander_cmds[flag] = arg
            else:
                raise ValueError(f"Not implemented, type: {type(arg)}")

        assert ini_files is not None

        return ConfigStructure(
            config_type,
            prog=prog,
            description=description,
            env_prefix=env_prefix,
            ini_files=ini_files,
            ini_sections=ini_sections,
            params=params,
            commands=commands,
            cl_non_expander_cmds=cl_non_expander_cmds,
            cl_expanders=cl_expanders,
            cl_flag_params=cl_flag_params,
            cl_positional=cl_positional,
            ini_params=ini_params,
            env_params=env_params,
        )

    def get_argument_parser(self) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(
            prog=self.prog,
            description=self.description,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False,
        )
        p._action_groups.pop()
        commands = p.add_argument_group("commands")
        required = p.add_argument_group("required arguments")
        optional = p.add_argument_group("optional arguments")
        for param in self.params.values():
            if param.is_required():
                required.add_argument(*param.all_flags(), **param.argparse_argument_kwargs())
            else:
                optional.add_argument(*param.all_flags(), **param.argparse_argument_kwargs())
        print(self.cl_expanders.values())
        print(self.cl_non_expander_cmds.values())
        for cmd in [*self.commands]:
            commands.add_argument(*cmd.all_flags(), action="help")
        return p


@dataclass(frozen=True)
class Config(abc.ABC):
    """
    Base class for dataclasses holding configuration data
    """

    #: Configuration file paths
    #:
    #: The paths are absolute or relative to the current working directory, and
    #: point to existing INI files containing configuration settings
    config: Annotated[Sequence[Path], Param.append(types.path.separated_by(","))]

    #: Display usage information and exits
    help: ClassVar[HelpCmd] = HelpCmd(short_flag_name="-h", long_flag_name="--help")

    #: Names of sections to parse in configuration files, with unknown keys ignored
    ini_relaxed_sections_: ClassVar[Sequence[str]] = ["Common", "COMMON", "common"]

    #: Names of additional sections to parse in configuration files, unknown keys error
    ini_strict_sections_: ClassVar[Sequence[str]] = []

    @classmethod
    def ini_sections_(cls) -> Sequence[IniSection]:
        """
        Returns a sequence of INI file sections to parse

        By default, this parses first the relaxed sections and then the strict ones.

        This method can be overridden.
        """
        relaxed = [IniSection(name, False) for name in cls.ini_relaxed_sections_]
        strict = [IniSection(name, True) for name in cls.ini_strict_sections_]
        return relaxed + strict

    prog_: ClassVar[Optional[str]] = None  #: Program name
    description_: ClassVar[Optional[str]] = None  #: Text to display before the argument help
    env_prefix_: ClassVar[Optional[str]] = None  #: Prefix for environment variables

    @classmethod
    def config_structure_(cls: Type[C]) -> ConfigStructure[C]:
        return ConfigStructure.from_config(cls)

    @classmethod
    def parse_command_line_(
        cls: Type[C],
        cwd: Path = Path.cwd(),
        args: Sequence[str] = sys.argv[1:],
        env: Mapping[str, str] = os.environ,
    ) -> Result[Union[C, Cmd]]:
        """
        Parses multiple information sources, returns a configuration, a command or an error

        Default values are taken from the current working directory, the script command line
        arguments, and the current environment variables.

        Args:
            cwd: Directory used as a base for the configuration file relative paths
            args: Command line arguments
            env: Environment variables

        Returns:
            A parsed configuration or an error
        """
        cs = cls.config_structure_()
        cp = ConfigProcessor(cs, cwd, args, env)
        return cp.process()

    @classmethod
    def from_command_line_(
        cls: Type[C],
        cwd: Path = Path.cwd(),
        args: Sequence[str] = sys.argv[1:],
        env: Mapping[str, str] = os.environ,
    ) -> C:
        """
        Parses multiple information sources into a configuration and display help on error

        Default values are taken from the current working directory, the script command line
        arguments, and the current environment variables.

        Args:
            cwd: Directory used as a base for the configuration file relative paths
            args: Command line arguments
            env: Environment variables

        Returns:
            A parsed configuration
        """
        res = cls.parse_command_line_(cwd, args, env)
        if isinstance(res, cls):
            return res
        if isinstance(res, Err):
            res.pretty_print()
            cls.get_argument_parser_().print_help()
            sys.exit(1)
        assert isinstance(res, Cmd)  # exhaustiveness checking does not work here
        # TODO: implement generic cmd mechanism
        assert isinstance(res, HelpCmd), "Only supported command is HelpCmd"
        cls.get_argument_parser_().print_help()
        sys.exit(0)

    @classmethod
    def get_argument_parser_(cls: Type[C]) -> argparse.ArgumentParser:
        """
        Returns an :class:`argparse.ArgumentParser` for documentation purposes
        """
        return cls.config_structure_().get_argument_parser()
