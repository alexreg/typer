import typer_cloup as typer

app = typer.Typer()


def old_callback():
    """
    Old callback help.
    """


users_app = typer.Typer(callback=old_callback)


def new_users():
    """
    I have the highland! Create some users.
    """


app.add_sub(users_app, callback=new_users)


@users_app.callback()
def users():
    """
    Manage users in the app.
    """


@users_app.command()
def create(name: str):
    typer.echo(f"Creating user: {name}")


if __name__ == "__main__":
    app()
