import typer
from click.shell_completion import CompletionItem

app = typer.Typer()


def complete(ctx, param, incomplete):
    typer.echo(f"info name is: {ctx.info_name}", err=True)
    typer.echo(f"param is: {param.name}", err=True)
    typer.echo(f"incomplete is: {incomplete}", err=True)
    return [
        CompletionItem("Camila", help="The reader of books."),
        CompletionItem("Carlos", help="The writer of scripts."),
        CompletionItem("Sebastian", help="The type hints guy."),
    ]


@app.command()
def main(name: str = typer.Option("World", shell_complete=complete)):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    app()
