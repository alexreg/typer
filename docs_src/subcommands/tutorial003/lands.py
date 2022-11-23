import typer_cloup as typer

import reigns
import towns

app = typer.Typer()
app.add_sub(reigns.app, name="reigns")
app.add_sub(towns.app, name="towns")

if __name__ == "__main__":
    app()
