from typing import List

import typer_cloup as typer

app = typer.Typer()


@app.command()
def main(name: List[str] = typer.Option(["World"], help="The name to say hi to.")):
    for each_name in name:
        typer.echo(f"Hello {each_name}")


if __name__ == "__main__":
    app()
