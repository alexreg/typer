import typer
from typer.testing import CliRunner

runner = CliRunner()

app = typer.Typer()


@app.command()
def test(count: int = typer.Option(1)):
    typer.echo(f"Count: {count}")


@app.command()
def dist(count: int = typer.Option(1)):
    app.forward(test)
    app.invoke(test, count=42)


def test_invocation():
    result = runner.invoke(app, ["dist", "--count", "2"])
    assert result.exit_code == 0
    assert "Count: 2\nCount: 42" in result.output
