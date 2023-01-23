import pytest

import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_version():
    app = typer.Typer()

    @app.command()
    def main(
        version: bool = typer.VersionOption(version="1.0.0", prog_name="test-version")
    ):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "--version"])
    assert result.exit_code == 0
    assert "test-version, version 1.0.0" in result.output


def test_version_package():
    app = typer.Typer()

    @app.command()
    def main(version: bool = typer.VersionOption(package_name=typer.__package__)):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "--version"])
    assert result.exit_code == 0
    assert f"main, version {typer.__version__}" in result.output


def test_version_package_not_installed():
    app = typer.Typer()

    @app.command()
    def main(version: bool = typer.VersionOption()):
        pass  # pragma: no cover

    with pytest.raises(RuntimeError) as exc_info:
        result = runner.invoke(app, ["main", "--version"], catch_exceptions=False)
    assert (
        exc_info.value.args[0]
        == "'tests' is not installed. Try passing 'package_name' instead."
    )
