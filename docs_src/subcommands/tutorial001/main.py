import typer_cloup as typer

import items
import users

app = typer.Typer()
app.add_sub(users.app, name="users")
app.add_sub(items.app, name="items")

if __name__ == "__main__":
    app()
