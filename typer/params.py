from typing import TYPE_CHECKING, Any, Callable, List, Optional, Type, Union, cast

import click
import cloup
import cloup.constraints

from .models import ArgumentInfo, CommandFunctionType, OptionInfo

if TYPE_CHECKING:  # pragma: no cover
    import click.shell_completion


def Option(
    # Parameter
    default: Optional[Any],
    *param_decls: str,
    callback: Optional[Callable[..., Any]] = None,
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
    # Option
    show_default: bool = True,
    prompt: Union[bool, str] = False,
    confirmation_prompt: bool = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = True,
    group: Optional[cloup.OptionGroup] = None,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[Union[List[str]]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, Type[str], Type[bytes]] = None,
) -> Any:
    return OptionInfo(
        # Parameter
        default=default,
        param_decls=param_decls,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        # Option
        show_default=show_default,
        prompt=prompt,
        confirmation_prompt=confirmation_prompt,
        prompt_required=prompt_required,
        hide_input=hide_input,
        is_flag=is_flag,
        flag_value=flag_value,
        count=count,
        allow_from_autoenv=allow_from_autoenv,
        help=help,
        hidden=hidden,
        show_choices=show_choices,
        show_envvar=show_envvar,
        group=group,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
    )


def Argument(
    # Parameter
    default: Optional[Any],
    *,
    callback: Optional[Callable[..., Any]] = None,
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
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[Union[List[str]]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, Type[str], Type[bytes]] = None,
) -> Any:
    return ArgumentInfo(
        # Parameter
        default=default,
        # Arguments can only have one param declaration
        # it will be generated from the param name
        param_decls=None,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        # TyperArgument
        show_default=show_default,
        show_choices=show_choices,
        show_envvar=show_envvar,
        help=help,
        hidden=hidden,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
    )


def option_group(
    title: str,
    *options: str,
    help: Optional[str] = None,
    constraint: Optional[cloup.constraints.Constraint] = None,
    hidden: bool = False,
) -> Callable[[CommandFunctionType], CommandFunctionType]:
    if not isinstance(title, str):
        raise TypeError(
            "the first argument of `@option_group` must be its title, a string; "
            "you probably forgot it"
        )

    if not options:
        raise ValueError("you must provide at least one option")

    def decorator(f: CommandFunctionType) -> CommandFunctionType:
        opt_group = cloup.OptionGroup(
            title, help=help, constraint=constraint, hidden=hidden
        )
        f_obj = cast(Any, f)
        if not hasattr(f, "__opt_groups"):
            f_obj.__opt_groups = []
        f_obj.__opt_groups.append((opt_group, options))
        return f

    return decorator


def constraint(
    constr: cloup.constraints.Constraint,
    *params: str,
) -> Callable[[CommandFunctionType], CommandFunctionType]:
    return cloup.constraint(constr, params)
