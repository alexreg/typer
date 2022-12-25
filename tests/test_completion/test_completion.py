import os
import subprocess
import sys
from pathlib import Path

from docs_src.commands.index import tutorial001 as mod


def test_show_completion():
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"{sys.executable}  -m coverage run {mod.__file__} --show-completion",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )
    assert "_TUTORIAL001.PY_COMPLETE=bash_complete" in result.stdout


def test_install_completion():
    bash_completion_path: Path = Path.home() / ".bashrc"
    text = ""
    if bash_completion_path.is_file():  # pragma: no cover
        text = bash_completion_path.read_text()
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"{sys.executable} -m coverage run {mod.__file__} --install-completion",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )
    new_text = bash_completion_path.read_text()
    bash_completion_path.write_text(text)
    assert "source" in new_text
    assert ".bash_completions/tutorial001.py.sh" in new_text
    assert "completion installed at" in result.stdout
    assert "Completion will take effect once you restart the terminal" in result.stdout


def test_completion_invalid_instruction():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bashsource",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode != 0
    assert "Invalid completion instruction." in result.stderr


def test_completion_source_bash():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "complete -o nosort -F _tutorial001py_completion tutorial001.py"
        in result.stdout
    )


def test_completion_source_invalid_shell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "xxx_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Shell 'xxx' is not supported." in result.stderr


def test_completion_source_invalid_instruction():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_explode",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Completion instruction 'explode' is not supported." in result.stderr


def test_completion_source_zsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "zsh_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "compdef _tutorial001py_completion tutorial001.py" in result.stdout


def test_completion_source_fish():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "fish_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "complete --no-files --command tutorial001.py" in result.stdout
