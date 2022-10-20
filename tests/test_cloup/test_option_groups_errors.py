import pytest
import typer
from cloup import OptionGroup
from typer import option_group
from typer.testing import CliRunner

runner = CliRunner()

app = typer.Typer()

another_group = OptionGroup("Another group")


@app.command()
@option_group(
    "Some group",
    "foo",
)
def main(
    foo: str = typer.Option(None, group=another_group),
):
    pass  # pragma: no cover


def test_double_assignment():
    with pytest.raises(ValueError) as exc_info:
        runner.invoke(app, ["--foo", "foo"])
        assert (
            exc_info.value.message
            == "<TyperOption foo>` was first assigned to `OptionGroup('Another group', options=[])` and then passed as argument to `@option_group('Some group', ...)"
        )
