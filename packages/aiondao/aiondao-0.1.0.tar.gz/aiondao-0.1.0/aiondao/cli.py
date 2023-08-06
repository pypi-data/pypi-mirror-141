import typer

from .dev import run_dev

app = typer.Typer()


@app.callback()
def callback():
    """
    Crypto Currency Agent Based Model
    """


@app.command()
def dev():
    """
    Start running the model you want to live.
    """
    typer.secho("Run model", fg="green")
    run_dev()


@app.command()
def start():
    """
    Load the portal gun
    """
    typer.secho("Run model", styles="green")
