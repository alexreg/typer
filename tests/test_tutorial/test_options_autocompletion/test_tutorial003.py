import os
import subprocess

from docs_src.options_autocompletion import tutorial003 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_completion():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL003.PY_COMPLETE": "zsh_complete",
            "COMP_WORDS": "tutorial003.py --name Seb",
            "COMP_CWORD": "2",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Camila" not in result.stdout
    assert "Carlos" not in result.stdout
    assert "Sebastian" in result.stdout


def test_1():
    result = runner.invoke(mod.app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
