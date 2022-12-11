from typing import Any

import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_typer_unprocessed():
    app = typer.Typer()

    @app.command()
    def main(name: Any):
        assert isinstance(name, bytes) and name == b"\xa1"

    result = runner.invoke(app, [b"\xa1"])
    assert result.exit_code == 0
