import typer
import uvicorn


app = typer.Typer()


@app.command()
def version():
    from baguette_bi import __version__

    typer.echo(f"Baguette BI v{__version__}")


@app.command()
def server(reload: bool = False):
    uvicorn.run("baguette_bi.server.app:app", reload=reload)
