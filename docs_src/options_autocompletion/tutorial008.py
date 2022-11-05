from typing import List

import typer
from click.shell_completion import CompletionItem

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_name(ctx, param, incomplete):
    typer.echo(f"{ctx.args}", err=True)
    completion = []
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            completion.append(CompletionItem(name, help=help_text))
    return completion


app = typer.Typer()


@app.command()
def main(
    name: List[str] = typer.Option(
        ["World"], help="The name to say hi to.", shell_complete=complete_name
    )
):
    for n in name:
        typer.echo(f"Hello {n}")


if __name__ == "__main__":
    app()
