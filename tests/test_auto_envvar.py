import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_autoenv_prefix():
    app = typer.Typer(context_settings=dict(auto_envvar_prefix="TEST"))

    @app.command()
    def hello(
        name: str = typer.Argument(..., allow_from_autoenv=True),
        lastname: str = typer.Option(...),
    ):
        typer.echo(f"Hello {name} {lastname}")

    @app.command()
    def goodbye(
        name: str = typer.Argument(..., allow_from_autoenv=True),
        lastname: str = typer.Option(...),
    ):
        typer.echo(f"Goodbye {name} {lastname}")

    result = runner.invoke(app, ["hello", "--help"])
    assert "[env var: TEST_HELLO_NAME; required]" in result.stdout
    assert "[env var: TEST_HELLO_LASTNAME; required]" in result.stdout

    result = runner.invoke(app, ["goodbye", "--help"])
    assert "[env var: TEST_GOODBYE_NAME; required]" in result.stdout
    assert "[env var: TEST_GOODBYE_LASTNAME; required]" in result.stdout

    result = runner.invoke(
        app,
        ["hello"],
        env={"TEST_HELLO_NAME": "Joe", "TEST_HELLO_LASTNAME": "Bloggs"},
    )
    assert result.exit_code == 0
    assert "Hello Joe Bloggs" in result.output

    result = runner.invoke(
        app,
        ["goodbye"],
        env={"TEST_GOODBYE_NAME": "Joe", "TEST_GOODBYE_LASTNAME": "Bloggs"},
    )
    assert result.exit_code == 0
    assert "Goodbye Joe Bloggs" in result.output


def test_autoenv_prefix_empty():
    app = typer.Typer(context_settings=dict(auto_envvar_prefix=""))

    @app.command()
    def hello(
        name: str = typer.Argument(..., allow_from_autoenv=True),
        lastname: str = typer.Option(...),
    ):
        typer.echo(f"Hello {name} {lastname}")

    @app.command()
    def goodbye(
        name: str = typer.Argument(..., allow_from_autoenv=True),
        lastname: str = typer.Option(...),
    ):
        typer.echo(f"Goodbye {name} {lastname}")

    result = runner.invoke(app, ["hello", "--help"])
    assert "[env var: HELLO_NAME; required]" in result.stdout
    assert "[env var: HELLO_LASTNAME; required]" in result.stdout

    result = runner.invoke(app, ["goodbye", "--help"])
    assert "[env var: GOODBYE_NAME; required]" in result.stdout
    assert "[env var: GOODBYE_LASTNAME; required]" in result.stdout

    result = runner.invoke(
        app,
        ["hello"],
        env={"HELLO_NAME": "Joe", "HELLO_LASTNAME": "Bloggs"},
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Hello Joe Bloggs" in result.output

    result = runner.invoke(
        app,
        ["goodbye"],
        env={"GOODBYE_NAME": "Joe", "GOODBYE_LASTNAME": "Bloggs"},
    )
    assert result.exit_code == 0
    assert "Goodbye Joe Bloggs" in result.output
