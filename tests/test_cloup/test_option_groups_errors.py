from typing import Optional

import pytest
import typer
from cloup import OptionGroup
from typer import option_group
from typer.testing import CliRunner

runner = CliRunner()


def test_no_option():
    app = typer.Typer()

    with pytest.raises(ValueError) as exc_info:

        @app.command()
        @option_group("Some group")
        def main(foo: Optional[str] = typer.Option(None)):  # pragma: no cover
            pass

    assert exc_info.value.args[0] == "you must provide at least one option"


def test_invalid_group_name():
    app = typer.Typer()

    with pytest.raises(TypeError) as exc_info:

        @app.command()
        @option_group(None)
        def main(foo: Optional[str] = typer.Option(None)):  # pragma: no cover
            pass

    assert (
        exc_info.value.args[0]
        == "the first argument of `@option_group` must be its title, a string; you probably forgot it"
    )


def test_not_parameter():
    app = typer.Typer()

    @app.command()
    @option_group("Some group", "bar")
    def main(foo: Optional[str] = typer.Option(None)):
        pass  # pragma: no cover

    with pytest.raises(ValueError) as exc_info:
        runner.invoke(app, ["--foo", "foo"])
    assert exc_info.value.args[0] == "`bar` is not a parameter"


def test_not_option():
    app = typer.Typer()

    @app.command()
    @option_group("Some group", "foo")
    def main(foo: str = typer.Argument(...)):
        pass  # pragma: no cover

    with pytest.raises(TypeError) as exc_info:
        runner.invoke(app, ["--foo", "foo"])
    assert (
        exc_info.value.args[0]
        == "only parameter of type `Option` can be added to option groups"
    )


def test_double_assignment():
    app = typer.Typer()

    another_group = OptionGroup("Another group")

    @app.command()
    @option_group("Some group", "foo")
    def main(
        foo: str = typer.Option(None, group=another_group),
    ):
        pass  # pragma: no cover

    with pytest.raises(ValueError) as exc_info:
        runner.invoke(app, ["--foo", "foo"])
    assert (
        exc_info.value.args[0]
        == "`<TyperOption foo>` was first assigned to `OptionGroup('Another group', options=[])` and then passed as argument to `@option_group('Some group', ...)`"
    )
