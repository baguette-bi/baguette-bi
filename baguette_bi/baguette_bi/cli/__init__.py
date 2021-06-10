import os
from pathlib import Path
from typing import Optional

import typer
import uvicorn

from baguette_bi.examples import altair_examples, docs

app = typer.Typer()


@app.command()
def version():
    from baguette_bi import __version__

    typer.echo(f"Baguette BI v{__version__}")


@app.command()
def server(project: Optional[Path] = typer.Argument(None), reload: bool = False):
    if project is None:
        project = Path(altair_examples.__file__).parent
    os.environ["BAGUETTE_PROJECT"] = str(project)
    uvicorn.run("baguette_bi.server.app:app", reload=reload, reload_dirs=[str(project)])


@app.command(name="docs")
def docs_cmd(reload: bool = False):
    project = Path(docs.__file__).parent
    os.environ["BAGUETTE_PROJECT"] = str(project)
    uvicorn.run("baguette_bi.server.app:app", reload=reload, reload_dirs=[str(project)])
