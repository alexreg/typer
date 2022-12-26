import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_autoenv_prefix():
    app = typer.Typer(context_settings=dict(auto_envvar_prefix="TEST"))

    @app.command()
    def main(
        name: str = typer.Argument(..., allow_from_autoenv=True),
        lastname: str = typer.Option(...),
    ):
        typer.echo(f"Hello {name} {lastname}")

    result = runner.invoke(app, ["--help"])
    assert "[env var: TEST_NAME; required]" in result.stdout
    assert "[env var: TEST_LASTNAME; required]" in result.stdout

    result = runner.invoke(app, env={"TEST_NAME": "Joe", "TEST_LASTNAME": "Bloggs"})
    assert result.exit_code == 0
    assert "Hello Joe Bloggs" in result.output


def test_autoenv_prefix_empty():
    app = typer.Typer(context_settings=dict(auto_envvar_prefix=""))

    @app.command()
    def main(
        name: str = typer.Argument(..., allow_from_autoenv=True),
        lastname: str = typer.Option(...),
    ):
        typer.echo(f"Hello {name} {lastname}")

    result = runner.invoke(app, ["--help"])
    assert "[env var: NAME; required]" in result.stdout
    assert "[env var: LASTNAME; required]" in result.stdout

    result = runner.invoke(app, env={"NAME": "Joe", "LASTNAME": "Bloggs"})
    assert result.exit_code == 0
    assert "Hello Joe Bloggs" in result.output
