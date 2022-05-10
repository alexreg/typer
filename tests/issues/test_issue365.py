import typer
from typer.testing import CliRunner

TERMINAL_WIDTH = 800
ARG_HELP_TEXT = "This is an argument with a very long help text. " * 10

runner = CliRunner()

app = typer.Typer(
    context_settings=dict(
        max_content_width=TERMINAL_WIDTH,
        terminal_width=TERMINAL_WIDTH,
    )
)


@app.command()
def main(
    arg: str = typer.Argument(..., help=ARG_HELP_TEXT),
):
    pass


def test_help_output():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert ARG_HELP_TEXT in result.output
