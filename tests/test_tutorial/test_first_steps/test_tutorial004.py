import subprocess

import typer_cloup as typer
from docs_src.first_steps import tutorial004 as mod
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Arguments:" in result.output
    assert columns_match(result.output, "NAME", "[required]")
    assert columns_match(result.output, "LASTNAME", "[required]")
    assert "--formal / --no-formal" in result.output


def test_1():
    result = runner.invoke(app, ["Camila", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_formal_1():
    result = runner.invoke(app, ["Camila", "Gutiérrez", "--formal"])
    assert result.exit_code == 0
    assert "Good day Ms. Camila Gutiérrez." in result.output


def test_formal_2():
    result = runner.invoke(app, ["Camila", "--formal", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Good day Ms. Camila Gutiérrez." in result.output


def test_formal_3():
    result = runner.invoke(app, ["--formal", "Camila", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Good day Ms. Camila Gutiérrez." in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
