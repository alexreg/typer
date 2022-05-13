import typer
from typer.testing import CliRunner, columns_match

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
    assert columns_match(
        result.output,
        "--global-opt / --no-global-opt",
        "Global option  [default: no-global-opt]",
    )


def test_help_cmd():
    result = runner.invoke(app, ["cmd", "--help"])
    assert result.exit_code == 0
    assert "Some command" in result.output
    assert ":param" not in result.output
    assert columns_match(result.output, "ARG1", "First argument  [required]")
    assert columns_match(result.output, "[ARG2]", "Second argument  [default: bar]")
    assert columns_match(result.output, "--opt1 TEXT", "First option  [default: foo]")
    assert columns_match(
        result.output, "--opt2 / --no-opt2", "Second option  [default: no-opt2]"
    )
    assert columns_match(result.output, "--opt3 INTEGER", "Third option  [default: 1]")
