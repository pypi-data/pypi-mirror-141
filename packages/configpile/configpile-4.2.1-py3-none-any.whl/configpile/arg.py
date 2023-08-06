from __future__ import annotations

import abc
import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from .collector import Collector
from .errors import Err, Result
from .types import ParamType

if TYPE_CHECKING:
    from .config import Config
    from .sources import Source

T = TypeVar("T", covariant=True)  #: Item type

W = TypeVar("W", covariant=True)  #: Wrapped item type


class AutoName(Enum):
    """
    Describes automatic handling of an argument name
    """

    #: The argument should not be present in the corresponding source
    FORBIDDEN = 0

    #: Derives the argument name from the original Python identifier (default)
    DERIVED = 1

    @staticmethod
    def derive_long_flag_name(name: str) -> str:
        if name.endswith("_command"):
            name = name[:-8]
        return "--" + name.replace("_", "-")

    @staticmethod
    def derive_env_var_name(name: str, prefix: Optional[str]) -> str:
        if prefix is not None:
            return prefix + "_" + name.upper()
        else:
            return name.upper()

    @staticmethod
    def derive_config_key_name(name: str) -> str:
        return name.replace("_", "-")


ArgName = Union[str, AutoName]

A = TypeVar("A", bound="Arg")


@dataclass(frozen=True)
class Arg(abc.ABC):
    """
    Base class for all kinds of arguments
    """

    help: Optional[str] = None  #: Help for the argument

    #: Short option name, used in command line parsing, prefixed by a single hyphen
    short_flag_name: Optional[str] = None

    #: Long option name used in command line argument parsing
    #:
    #: It is lowercase, prefixed with ``--`` and words are separated by hyphens
    long_flag_name: ArgName = AutoName.DERIVED

    def all_flags(self) -> Sequence[str]:
        """
        Returns a sequence of all forms of command line flags
        """
        res: List[str] = []
        if self.short_flag_name is not None:
            res.append(self.short_flag_name)
        assert self.long_flag_name != AutoName.DERIVED
        if isinstance(self.long_flag_name, str):
            res.append(self.long_flag_name)
        return res

    def update_dict_(self, name: str, help: str, env_prefix: Optional[str]) -> Mapping[str, Any]:
        """
        Returns updated values for this argument, used during :class:`.App` construction

        Args:
            name: Argument field name
            help: Argument docstring which describes the argument role
            env_prefix: Uppercase prefix for all environment variables

        Returns:

        """
        res = {"help": help}
        if self.long_flag_name == AutoName.DERIVED:
            res["long_flag_name"] = AutoName.derive_long_flag_name(name)
        return res

    def updated(self: A, name: str, help: str, env_prefix: Optional[str]) -> A:
        return dataclasses.replace(self, **self.update_dict_(name, help, env_prefix))

    def argparse_argument_kwargs(self) -> Mapping[str, Any]:
        """
        Returns the keyword arguments for use with argparse.ArgumentParser.add_argument

        Returns:
            Keyword arguments mapping
        """
        return {"help": self.help}


@dataclass(frozen=True)
class Cmd(Arg):
    # Base class for command arguments
    pass


@dataclass(frozen=True)
class HelpCmd(Cmd):
    """
    Command-line argument that displays a help message and exits
    """


@dataclass(frozen=True)
class Expander(Cmd):
    """
    Command-line argument that expands into a flag/value pair
    """

    new_flag: str = ""  #: Inserted flag in the command line
    new_value: str = ""  #: Inserted value in the command line

    def inserts(self) -> Tuple[str, str]:
        """
        Returns the flag/value pair that is inserted when this command flag is present
        """
        return (self.new_flag, self.new_value)

    @staticmethod
    def make(
        new_flag: str,
        new_value: str,
        *,
        short_flag_name: Optional[str],
        long_flag_name: ArgName = AutoName.DERIVED,
    ) -> Expander:
        """
        Constructs an expander that inserts a flag/value pair in the command line

        At least one of ``short_flag_name`` or ``long_flag_name`` must be defined.

        Args:
            new_flag: Inserted flag, including the hyphen prefix
            new_value: String value to insert following the flag
            short_flag_name: Short flag name of this command flag
            long_flag_name: Long flag name of this command flag
        """
        res = Expander(
            new_flag=new_flag,
            new_value=new_value,
            short_flag_name=short_flag_name,
            long_flag_name=long_flag_name,
        )
        assert res.all_flags(), "Provide at least one of short_flag_name or long_flag_name"
        return res


class Positional(Enum):
    """
    Describes the positional behavior of a parameter
    """

    FORBIDDEN = 0  #: The argument is not positional
    ONCE = 1  #: The argument parses a single positional value
    ZERO_OR_MORE = 2  #: The argument parses the remaining positional value
    ONE_OR_MORE = 3  #: The argument parses at least one remaining positional value

    def should_be_last(self) -> bool:
        """
        Returns whether a positional parameter should be the last one
        """
        return self in {Positional.ZERO_OR_MORE, Positional.ONE_OR_MORE}

    def is_positional(self) -> bool:
        """
        Returns whether a parameter is positional
        """
        return self != Positional.FORBIDDEN


@dataclass(frozen=True)
class Instance(Generic[T]):
    """
    Parameter instance
    """

    value: T  #: Value parsed from string
    string: str  #: Parsed string
    source: Source  #: Parameter source

    @staticmethod
    def parse(s: str, param_type: ParamType[T], source: Source) -> Result[Instance[T]]:
        """
        Parses a string using a parameter type and constructs a parameter instance

        Args:
            s: String to parse
            param_type: Parameter type used as a parser
            source: Source of the string

        Returns:
            A parameter instance or an error
        """
        res = param_type.parse(s)
        if isinstance(res, Err):
            return res
        else:
            return Instance(res, s, source)


@dataclass(frozen=True)
class Param(Arg, Generic[T]):
    """
    Describes an argument holding a value of a given type

    .. note::
        Instances of :class:`.Param` have two "states":

        * Initially, instances of :class:`.Param` are assigned to class attributes of
        subclasses of :class:`.app.App`. In that state, :attr:`.Param.name` is not set,
        and the other ``XXX_name`` attributes contain either a custom name provided by the user, or
        instructions about the derivation of the corresponding name.

        * When an instance of :class:`.App` is constructed, the :attr:`.name` attribute and the
          ``XXX_name`` attributes of the instance are updated.
    """

    #: Argument type, parser from string to value
    param_type: ParamType[T] = ParamType.invalid()  # type: ignore

    #: Argument collector
    collector: Collector[T] = Collector.invalid()  # type: ignore

    default_value: Optional[str] = None  #: Default value inserted as instance

    name: Optional[str] = None  #: Python identifier representing the argument

    positional: Positional = Positional.FORBIDDEN

    #: Configuration key name used in INI files
    #:
    #: It is lowercase, and words are separated by hyphens.
    config_key_name: ArgName = AutoName.DERIVED

    #: Environment variable name
    #:
    #: The environment variable name has an optional prefix, followed by the
    #: Python identifier in uppercase, with underscore as separator.
    #:
    #: This prefix is provided by :attr:`.App.env_prefix_`
    #:
    #: If a non-empty prefix is given, the name is prefixed with it
    #: (and an underscore).
    env_var_name: ArgName = AutoName.FORBIDDEN

    def update_dict_(self, name: str, help: str, env_prefix: Optional[str]) -> Mapping[str, Any]:
        r = {"name": name, **super().update_dict_(name, help, env_prefix)}
        if self.config_key_name == AutoName.DERIVED:
            r["config_key_name"] = AutoName.derive_config_key_name(name)
        if self.env_var_name == AutoName.DERIVED and env_prefix is not None:
            r["env_var_name"] = AutoName.derive_env_var_name(name, env_prefix)
        return r

    def all_config_key_names(self) -> Sequence[str]:
        """
        Returns a sequence of all forms of command line options

        Returns:
            Command line options
        """
        if isinstance(self.config_key_name, str):
            return [self.config_key_name]
        else:
            return []

    def all_env_var_names(self) -> Sequence[str]:
        """
        Returns a sequence of all forms of command line options

        Returns:
            Command line options
        """
        if isinstance(self.env_var_name, str):
            return [self.env_var_name]
        else:
            return []

    def is_required(self) -> bool:
        """
        Returns whether the argument is required
        """
        return self.default_value is None and self.collector.arg_required()

    def argparse_argument_kwargs(self) -> Mapping[str, Any]:
        res = super().argparse_argument_kwargs()
        if self.is_required():
            res = {**res, "required": True}
        return {
            **res,
            **self.collector.argparse_argument_kwargs(),
            **self.param_type.argparse_argument_kwargs(),
        }

    @staticmethod
    def store(
        param_type: ParamType[T],
        *,
        default_value: Optional[str] = None,
        positional: Positional = Positional.FORBIDDEN,
        short_flag_name: Optional[str] = None,
        long_flag_name: ArgName = AutoName.DERIVED,
        config_key_name: ArgName = AutoName.DERIVED,
        env_var_name: ArgName = AutoName.FORBIDDEN,
    ) -> Param[T]:
        """
        Creates a parameter that stores the last provided value

        If a default value is provided, the argument can be omitted. However,
        if the default_value ``None`` is given (default), then
        the parameter cannot be omitted.

        Args:
            param_type: Parser that transforms a string into a value
            default_value: Default value
            positional: Whether this parameter is present in positional arguments
            short_flag_name: Short option name (optional)
            long_flag_name: Long option name (auto. derived from fieldname by default)
            config_key_name: Config key name (auto. derived from fieldname by default)
            env_var_name: Environment variable name (forbidden by default)

        Returns:
            The constructed Param instance
        """

        return Param(
            param_type=param_type,
            collector=Collector.keep_last(),
            default_value=default_value,
            positional=positional,
            short_flag_name=short_flag_name,
            long_flag_name=long_flag_name,
            config_key_name=config_key_name,
            env_var_name=env_var_name,
        )

    @staticmethod
    def append(
        param_type: ParamType[Sequence[W]],
        *,
        positional: Positional = Positional.FORBIDDEN,
        short_flag_name: Optional[str] = None,
        long_flag_name: ArgName = AutoName.DERIVED,
        config_key_name: ArgName = AutoName.DERIVED,
        env_var_name: ArgName = AutoName.FORBIDDEN,
    ) -> Param[Sequence[W]]:
        """
        Creates an argument that stores the last provided value

        Args:
            param_type: Parser that transforms a string into a value
            positional: Whether this argument is present in positional arguments
            short_flag_name: Short option name (optional)
            long_flag_name: Long option name (auto. derived from fieldname by default)
            config_key_name: Config key name (auto. derived from fieldname by default)
            env_var_name: Environment variable name (forbidden by default)

        Returns:
            The constructed Arg instance
        """
        return Param(
            param_type=param_type,
            collector=Collector.append(),  # type: ignore
            default_value=None,
            positional=positional,
            short_flag_name=short_flag_name,
            long_flag_name=long_flag_name,
            config_key_name=config_key_name,
            env_var_name=env_var_name,
        )
