import typer
from typer.testing import CliRunner

runner = CliRunner()

app = typer.Typer()


@app.command()
def cmd(
    arg1: float,
    arg2: str = typer.Argument("bar"),
    opt1: str = typer.Option("foo"),
    opt2: bool = typer.Option(False),
    opt3: int = typer.Option(1),
):
    """
    Some command

    :param opt1: First option
    :param opt2: Second option
    :param opt3:
        Third
        option
    :param arg1: First argument
    :param arg2: Second argument
    """


@app.callback()
def main(global_opt: bool = False):
    """
    Callback

    :param global_opt: Global option
    """


def test_help_main():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Callback" in result.output
    assert ":param" not in result.output
    assert "--global-opt / --no-global-opt" in result.output
    assert "Global option" in result.output
    assert "[default: no-global-opt]" in result.output


def test_help_cmd():
    result = runner.invoke(app, ["cmd", "--help"])
    assert result.exit_code == 0
    assert "Some command" in result.output
    assert ":param" not in result.output
    assert "ARG1" in result.output
    assert "First argument" in result.output
    assert "[required]" in result.output
    assert "[ARG2]" in result.output
    assert "Second argument" in result.output
    assert "[default: bar]" in result.output
    assert "--opt1 TEXT" in result.output
    assert "First option" in result.output
    assert "[default: foo]" in result.output
    assert "--opt2 / --no-opt2" in result.output
    assert "Second option" in result.output
    assert "[default: no-opt2]" in result.output
    assert "--opt3 INTEGER" in result.output
    assert "Third option" in result.output
    assert "[default: 1]" in result.output
