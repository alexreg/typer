import subprocess

import typer_cloup as typer
from docs_src.parameter_types.datetime import tutorial001 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]" in result.output


def test_main():
    result = runner.invoke(app, ["1956-01-31T10:00:00"])
    assert result.exit_code == 0
    assert "Interesting day to be born: 1956-01-31 10:00:00" in result.output
    assert "Birth hour: 10" in result.output


def test_invalid():
    result = runner.invoke(app, ["july-19-1989"])
    assert result.exit_code != 0
    assert (
        "Error: Invalid value for 'BIRTH:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]': 'july-19-1989' does not match the formats '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'"
        in result.output
    )


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
