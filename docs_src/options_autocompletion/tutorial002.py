import typer


def complete_name(ctx, param, incomplete):
    return ["Camila", "Carlos", "Sebastian"]


app = typer.Typer()


@app.command()
def main(
    name: str = typer.Option(
        "World", help="The name to say hi to.", shell_complete=complete_name
    )
):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    app()
