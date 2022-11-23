import typer_cloup as typer

import items
import lands
import users

app = typer.Typer()
app.add_sub(users.app, name="users")
app.add_sub(items.app, name="items")
app.add_sub(lands.app, name="lands")

if __name__ == "__main__":
    app()
