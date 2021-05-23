import os
from pathlib import Path

import typer
import uvicorn

app = typer.Typer()


@app.command()
def version():
    from baguette_bi import __version__

    typer.echo(f"Baguette BI v{__version__}")


@app.command()
def server(project: Path, reload: bool = False):
    os.environ["BAGUETTE_PROJECT"] = str(project)
    uvicorn.run("baguette_bi.server.app:app", reload=reload, reload_dirs=[str(project)])
