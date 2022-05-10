import typer
from typer.testing import CliRunner

runner = CliRunner()

app = typer.Typer(
    context_settings=dict(
        help_option_names=["-h", "--help"],
    )
)


@app.command()
def main():
    pass


def test_help_short_option():
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
