import subprocess

from docs_src.subcommands.callback_override import tutorial004 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = mod.app


def test_cli():
    result = runner.invoke(app, ["users", "create", "Camila"])
    assert result.exit_code == 0
    assert "Running a users command" not in result.output
    assert "Callback override, running users command" not in result.output
    assert "I have the high land! Running users command" in result.output
    assert "Creating user: Camila" in result.output


def test_for_coverage():
    mod.default_callback()
    mod.user_callback()


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
