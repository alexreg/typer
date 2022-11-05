import typer

valid_names = ["Camila", "Carlos", "Sebastian"]


def complete_name(ctx, param, incomplete):
    completion = []
    for name in valid_names:
        if name.startswith(incomplete):
            completion.append(name)
    return completion


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
