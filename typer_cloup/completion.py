import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import click
import click.exceptions
import click.shell_completion
from click.shell_completion import (
    BashComplete,
    FishComplete,
    ZshComplete,
    get_completion_class,
)

from .models import ParamMeta
from .params import Option
from .utils import get_params_from_function

try:
    import shellingham
except ImportError:  # pragma: no cover
    shellingham = None


Shells = Enum(  # type: ignore[misc]
    "Shells",
    names={shell: shell for shell in click.shell_completion._available_shells.keys()},
    type=str,
)


def get_completion_script(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: str,
    shell: str,
) -> str:
    comp_cls = get_completion_class(shell)
    if comp_cls is None:  # pragma: no cover
        click.echo(f"Shell '{shell}' is not supported.", err=True)
        sys.exit(1)

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    return comp.source()


def install_bash(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: str,
    shell: str,
) -> Path:
    # Ref: https://github.com/scop/bash-completion#faq
    # It seems bash-completion is the official completion system for bash:
    # Ref: https://www.gnu.org/software/bash/manual/html_node/A-Programmable-Completion-Example.html
    # But installing in the locations from the docs doesn't seem to have effect
    completion_path = Path.home() / f".bash_completions/{prog_name}.sh"

    rc_path = Path.home() / ".bashrc"
    rc_path.parent.mkdir(parents=True, exist_ok=True)
    rc_content = ""
    if rc_path.is_file():
        rc_content = rc_path.read_text()

    completion_init_lines = [f"source {completion_path}"]
    for line in completion_init_lines:
        if line not in rc_content:  # pragma: no cover
            rc_content += f"\n{line}"

    rc_content += "\n"
    rc_path.write_text(rc_content)

    # Install completion
    completion_path.parent.mkdir(parents=True, exist_ok=True)
    script_content = get_completion_script(
        cli, ctx_args, prog_name, complete_var, shell
    )
    completion_path.write_text(script_content)

    return completion_path


def install_zsh(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: str,
    shell: str,
) -> Path:
    # Set up Z shell and load `~/.zfunc``
    zshrc_path = Path.home() / ".zshrc"
    zshrc_path.parent.mkdir(parents=True, exist_ok=True)
    zshrc_content = ""
    if zshrc_path.is_file():
        zshrc_content = zshrc_path.read_text()

    completion_init_lines = [
        "autoload -Uz compinit",
        "compinit",
        "zstyle ':completion:*' menu select",
        "fpath+=~/.zfunc",
    ]
    for line in completion_init_lines:
        if line not in zshrc_content:  # pragma: no cover
            zshrc_content += f"\n{line}"

    zshrc_content += "\n"
    zshrc_path.write_text(zshrc_content)

    # Install completion under `~/.zfunc/``
    path_obj = Path.home() / f".zfunc/_{prog_name}"
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    script_content = get_completion_script(
        cli, ctx_args, prog_name, complete_var, shell
    )
    path_obj.write_text(script_content)

    return path_obj


def install_fish(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: str,
    shell: str,
) -> Path:
    path_obj = Path.home() / f".config/fish/completions/{prog_name}.fish"
    parent_dir: Path = path_obj.parent
    parent_dir.mkdir(parents=True, exist_ok=True)

    script_content = get_completion_script(
        cli, ctx_args, prog_name, complete_var, shell
    )
    path_obj.write_text(f"{script_content}\n")

    return path_obj


def install(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    shell: Optional[str] = None,
    prog_name: Optional[str] = None,
    complete_var: Optional[str] = None,
) -> Tuple[str, Path]:
    prog_name = prog_name or click.get_current_context().find_root().info_name
    assert prog_name

    if complete_var is None:
        complete_var = "_{}_COMPLETE".format(prog_name.replace("-", "_").upper())

    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if shell is None and shellingham is not None and not test_disable_detection:
        shell, _ = shellingham.detect_shell()

    if shell == BashComplete.name:
        installed_path = install_bash(cli, ctx_args, prog_name, complete_var, shell)
    elif shell == ZshComplete.name:
        installed_path = install_zsh(cli, ctx_args, prog_name, complete_var, shell)
    elif shell == FishComplete.name:
        installed_path = install_fish(cli, ctx_args, prog_name, complete_var, shell)
    else:
        click.echo(f"Shell '{shell}' is not supported.")
        raise click.exceptions.Exit(1)

    return shell, installed_path


def get_completion_inspect_parameters() -> Tuple[ParamMeta, ParamMeta]:
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if shellingham and not test_disable_detection:
        parameters = get_params_from_function(_install_completion_placeholder_function)
    else:
        parameters = get_params_from_function(
            _install_completion_no_auto_placeholder_function
        )
    install_param, show_param = parameters.values()
    return install_param, show_param


def install_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma no cover
    if isinstance(value, str):
        shell, path = install(ctx.command, {}, shell=value)
    else:
        shell, path = install(ctx.command, {})
    click.secho(f"{shell} completion installed at `{path}`", fg="green")
    click.echo("Completion will take effect once you restart the terminal")
    sys.exit(0)


def show_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma no cover
    prog_name = ctx.find_root().info_name
    assert prog_name
    complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()
    shell = ""
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if isinstance(value, str):
        shell = value
    elif shellingham and not test_disable_detection:
        shell, _ = shellingham.detect_shell()
    script_content = get_completion_script(
        ctx.command, {}, prog_name, complete_var, shell
    )
    click.echo(script_content)
    sys.exit(0)


# Create a fake command function to extract the completion parameters
def _install_completion_placeholder_function(
    install_completion: bool = Option(
        None,
        "--install-completion",
        is_flag=True,
        callback=install_callback,
        expose_value=False,
        help="Install completion for the current shell.",
    ),
    show_completion: bool = Option(
        None,
        "--show-completion",
        is_flag=True,
        callback=show_callback,
        expose_value=False,
        help="Show completion for the current shell, to copy it or customize the installation.",
    ),
) -> Any:
    pass  # pragma no cover


def _install_completion_no_auto_placeholder_function(
    install_completion: Shells = Option(
        None,
        callback=install_callback,
        expose_value=False,
        help="Install completion for the specified shell.",
    ),
    show_completion: Shells = Option(
        None,
        callback=show_callback,
        expose_value=False,
        help="Show completion for the specified shell, to copy it or customize the installation.",
    ),
) -> Any:
    pass  # pragma no cover


# Re-implement `shell_complete` to add error messages.
def shell_complete(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: str,
    instruction: str,
) -> int:
    if "_" not in instruction:
        click.echo("Invalid completion instruction.", err=True)
        return 1

    shell, _, instruction = instruction.partition("_")
    comp_cls = get_completion_class(shell)
    if comp_cls is None:
        click.echo(f"Shell '{shell}' is not supported.", err=True)
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    if instruction == "source":
        click.echo(comp.source())
        return 0
    elif instruction == "complete":
        click.echo(comp.complete())
        return 0

    click.echo(f"Completion instruction '{instruction}' is not supported.", err=True)
    return 1
