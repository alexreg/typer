import inspect
import os
import sys
from gettext import gettext as _
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import click
import click.core
import click.formatting
import click.parser
import click.types
import cloup

if TYPE_CHECKING:  # pragma: no cover
    import click.shell_completion


class TyperArgument(cloup.Argument):
    def __init__(
        self,
        *,
        # Parameter
        param_decls: List[str],
        type: Optional[Any] = None,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        callback: Optional[Callable[..., Any]] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        # TyperArgument
        show_default: Union[bool, str] = True,
        show_choices: bool = True,
        show_envvar: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
    ):
        super().__init__(
            param_decls=param_decls,
            type=type,
            required=required,
            default=default,
            callback=callback,
            nargs=nargs,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
        )

        self.help = help
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar
        self.hidden = hidden

    def get_help_record(self, ctx: click.Context) -> Tuple[str, str]:
        # Modified version of click.core.Option.get_help_record()
        # to support arguments

        name = self.make_metavar()
        help = self.help or ""
        extra = []
        if self.show_envvar:
            envvar = self.envvar
            # allow_from_autoenv is currently not supported in Typer for CLI Arguments
            if envvar is not None:
                var_str = (
                    ", ".join(str(d) for d in envvar)
                    if isinstance(envvar, (list, tuple))
                    else envvar
                )
                extra.append(f"env var: {var_str}")
        if self.default is not None and (self.show_default or ctx.show_default):
            if isinstance(self.show_default, str):
                default_string = f"({self.show_default})"
            elif isinstance(self.default, (list, tuple)):
                default_string = ", ".join(str(d) for d in self.default)
            elif inspect.isfunction(self.default):
                default_string = "(dynamic)"
            else:
                default_string = str(self.default)
            extra.append(f"default: {default_string}")
        if self.required:
            extra.append("required")
        if extra:
            extra_str = ";".join(extra)
            help = f"{help}  [{extra_str}]" if help else f"[{extra_str}]"
        return name, help

    def make_metavar(self) -> str:
        # Modified version of click.core.Argument.make_metavar()
        # to include Argument name
        if self.metavar is not None:
            return self.metavar
        var = (self.name or "").upper()
        if not self.required:
            var = "[{}]".format(var)
        type_var = self.type.get_metavar(self)
        if type_var:
            var += f":{type_var}"
        if self.nargs != 1:
            var += "..."
        return var

    def shell_complete(
        self, ctx: click.Context, incomplete: str
    ) -> List["click.shell_completion.CompletionItem"]:
        return super().shell_complete(ctx, incomplete)


class TyperOption(cloup.Option):
    def __init__(
        self,
        # click.Parameter
        param_decls: List[str],
        type: Optional[Union[click.types.ParamType, Any]] = None,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        callback: Optional[Callable[..., Any]] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        # click.Option
        show_default: Union[bool, str] = False,
        prompt: Union[bool, str] = False,
        confirmation_prompt: Union[bool, str] = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: Optional[bool] = None,
        flag_value: Optional[Any] = None,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        # cloup.Option
        group: Optional[cloup.OptionGroup] = None,
    ):
        super().__init__(
            param_decls=param_decls,
            type=type,
            required=required,
            default=default,
            callback=callback,
            nargs=nargs,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
            show_default=show_default,
            prompt=prompt,
            confirmation_prompt=confirmation_prompt,
            prompt_required=prompt_required,
            hide_input=hide_input,
            is_flag=is_flag,
            flag_value=flag_value,
            multiple=multiple,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            help=help,
            hidden=hidden,
            show_choices=show_choices,
            show_envvar=show_envvar,
            group=group,
        )

    def get_help_record(self, ctx: click.Context) -> Optional[Tuple[str, str]]:
        # Duplicate all of Click's logic only to modify a single line, to allow boolean
        # flags with only names for False values as it's currently supported by Typer
        # Ref: https://alexreg-typer.netlify.app/tutorial/parameter-types/bool/#only-names-for-false

        any_prefix_is_slash = False

        def _write_opts(opts: Sequence[str]) -> str:
            nonlocal any_prefix_is_slash

            rv, any_slashes = click.formatting.join_options(opts)

            if any_slashes:
                any_prefix_is_slash = True

            if not self.is_flag and not self.count:
                rv += f" {self.make_metavar()}"

            return rv

        rv = [_write_opts(self.opts)]

        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ""
        extra = []

        if self.show_envvar:
            envvar = self.envvar

            if envvar is None:
                if (
                    self.allow_from_autoenv
                    and ctx.auto_envvar_prefix is not None
                    and self.name is not None
                ):
                    envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"

            if envvar is not None:
                var_str = (
                    envvar
                    if isinstance(envvar, str)
                    else ", ".join(str(d) for d in envvar)
                )
                extra.append(_("env var: {var}").format(var=var_str))

        # Temporarily enable resilient parsing to avoid type casting
        # failing for the default. Might be possible to extend this to
        # help formatting in general.
        resilient = ctx.resilient_parsing
        ctx.resilient_parsing = True

        try:
            default_value = self.get_default(ctx, call=False)
        finally:
            ctx.resilient_parsing = resilient

        show_default_is_str = isinstance(self.show_default, str)

        if show_default_is_str or (
            default_value is not None and (self.show_default or ctx.show_default)
        ):
            if show_default_is_str:
                default_string = f"({self.show_default})"
            elif isinstance(default_value, (list, tuple)):
                default_string = ", ".join(str(d) for d in default_value)
            elif callable(default_value):
                default_string = _("(dynamic)")
            elif self.is_bool_flag and self.secondary_opts:
                # For boolean flags that have distinct True/False opts,
                # use the opt without prefix instead of the value.
                # Typer override, original commented
                # default_string = click.parser.split_opt(
                #     (self.opts if self.default else self.secondary_opts)[0]
                # )[1]
                if self.default:
                    if self.opts:
                        default_string = click.parser.split_opt(self.opts[0])[1]
                    else:
                        default_string = str(default_value)
                else:
                    default_string = click.parser.split_opt(self.secondary_opts[0])[1]
                # Typer override end
            elif self.is_bool_flag and not self.secondary_opts and not default_value:
                default_string = ""
            else:
                default_string = str(default_value)

            if default_string:
                extra.append(_("default: {default}").format(default=default_string))

        if isinstance(self.type, click.types._NumberRangeBase):
            range_str = self.type._describe_range()

            if range_str:
                extra.append(range_str)

        if self.required:
            extra.append(_("required"))

        if extra:
            extra_str = "; ".join(extra)
            help = f"{help}  [{extra_str}]" if help else f"[{extra_str}]"

        return ("; " if any_prefix_is_slash else " / ").join(rv), help

    def shell_complete(
        self, ctx: click.Context, incomplete: str
    ) -> List["click.shell_completion.CompletionItem"]:
        return super().shell_complete(ctx, incomplete)


def _typer_main_shell_completion(
    self: click.core.Command,
    *,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: Optional[str] = None,
) -> None:
    if complete_var is None:
        complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()

    instruction = os.environ.get(complete_var)

    if not instruction:
        return

    from .completion import shell_complete

    rv = shell_complete(self, ctx_args, prog_name, complete_var, instruction)
    sys.exit(rv)


class TyperCommand(cloup.Command):
    def _main_shell_completion(
        self,
        ctx_args: Dict[str, Any],
        prog_name: str,
        complete_var: Optional[str] = None,
    ) -> None:
        _typer_main_shell_completion(
            self, ctx_args=ctx_args, prog_name=prog_name, complete_var=complete_var
        )

    def get_arguments_help_section(
        self, ctx: click.Context
    ) -> Optional[cloup.HelpSection]:
        def is_arg_hidden(arg: click.Argument) -> bool:
            if isinstance(arg, TyperArgument):
                return arg.hidden
            return False

        if all(is_arg_hidden(arg) for arg in self.arguments):
            return None
        return cloup.HelpSection(
            heading="Arguments",
            definitions=[
                self.get_argument_help_record(arg, ctx)
                for arg in self.arguments
                if not is_arg_hidden(arg)
            ],
        )

    def get_default_option_group(
        self, ctx: click.Context, is_the_only_visible_option_group: bool = False
    ) -> cloup.OptionGroup:
        """
        Returns an ``OptionGroup`` instance for the options not explicitly
        assigned to an option group, eventually including the ``--help`` option.
        """
        default_group = cloup.OptionGroup("Options")
        default_group.options = self.get_ungrouped_options(ctx)
        return default_group


class TyperGroup(cloup.Group):
    def _main_shell_completion(
        self,
        ctx_args: Dict[str, Any],
        prog_name: str,
        complete_var: Optional[str] = None,
    ) -> None:
        _typer_main_shell_completion(
            self, ctx_args=ctx_args, prog_name=prog_name, complete_var=complete_var
        )
