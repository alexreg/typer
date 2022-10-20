import typer
from cloup import Section
from typer.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer(name="git", align_sections=True)


def f(**kwargs):
    """Dummy command callback"""
    print(**kwargs)


section1 = Section("Start a working area (see also: git help tutorial)")
section2 = Section("Work on the current change (see also: git help everyday)")
section3 = Section("Examine the history and state (see also: git help revisions)")


@app.command(section=section1, help="Clone a repository into a new directory")
def clone():
    pass  # pragma: no cover


@app.command(
    section=section1,
    help="Create an empty Git repository or reinitialize an existing one",
)
def init():
    pass  # pragma: no cover


@app.command(
    section=section2, help="Remove files from the working tree and from the index"
)
def rm():
    pass  # pragma: no cover


@app.command(section=section2, help="Initialize and modify the sparse-checkout")
def sparse_checkout():
    pass  # pragma: no cover


@app.command(section=section2, help="Move or rename a file, a directory, or a symlink")
def mv():
    pass  # pragma: no cover


@app.command(section=section3, help="Show the working tree status")
def status():
    pass  # pragma: no cover


@app.command(
    section=section3, help="Show changes between commits, commit and working tree, etc"
)
def diff():
    pass  # pragma: no cover


@app.command(
    section=section3, help="Use binary search to find the commit that introduced a bug"
)
def bisect():
    pass  # pragma: no cover


# The following commands will be added to the "default section" (a sorted Section)


@app.command(help="Fake command #2")
def fake_2():
    pass  # pragma: no cover


@app.command(help="Fake command #1")
def fake_1():
    pass  # pragma: no cover


def test_help():
    result = runner.invoke(app, ["--help"])
    print(result.output)
    assert result.exit_code == 0
    assert "Start a working area (see also: git help tutorial):" in result.output
    assert columns_match(
        result.output, "clone", "Clone a repository into a new directory"
    )
    assert columns_match(result.output, "init", "Create an empty Git repository")
    assert "Work on the current change (see also: git help everyday):" in result.output
    assert columns_match(
        result.output, "rm", "Remove files from the working tree and from the index"
    )
    assert columns_match(
        result.output, "sparse-checkout", "Initialize and modify the sparse-checkout"
    )
    assert columns_match(
        result.output, "mv", "Move or rename a file, a directory, or a symlink"
    )
    assert (
        "Examine the history and state (see also: git help revisions):" in result.output
    )
    assert columns_match(result.output, "status", "Show the working tree status")
    assert columns_match(result.output, "diff", "Show changes between commits")
    assert columns_match(
        result.output,
        "bisect",
        "Use binary search to find the commit that introduced a bug",
    )
