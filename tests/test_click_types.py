from typing import Any, List

import typer_cloup as typer
from typer_cloup.param_types import SHELL_QUOTED_LIST
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_typer_unprocessed():
    app = typer.Typer()

    @app.command()
    def main(name: Any):
        assert isinstance(name, bytes) and name == b"\xa1"

    result = runner.invoke(app, [b"\xa1"])
    assert result.exit_code == 0


def test_shell_quoted_list():
    assert repr(SHELL_QUOTED_LIST) == "SHELL-QUOTED LIST"
    assert SHELL_QUOTED_LIST.convert(None, None, None) is None
    assert SHELL_QUOTED_LIST.convert(["foo", "bar"], None, None) == ["foo", "bar"]


def test_typer_shell_quoted_list():
    app = typer.Typer()

    @app.command()
    def main(
        names: List[str] = typer.Argument(..., shell_quoted_list=True, envvar="NAMES")
    ):
        for name in names:
            typer.echo(f"Hello {name}")

    result = runner.invoke(app, ["'Joe Bloggs' Camila"])
    assert "Hello Joe Bloggs" in result.stdout
    assert "Hello Camila" in result.stdout

    runner.env["NAMES"] = "'Joe Bloggs' Camila"
    result = runner.invoke(app)
    assert "Hello Joe Bloggs" in result.stdout
    assert "Hello Camila" in result.stdout
