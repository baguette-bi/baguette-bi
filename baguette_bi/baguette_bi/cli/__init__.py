from contextlib import contextmanager
from functools import wraps
from typing import Optional

import typer
from typer import Option, Typer

from baguette_bi import actions
from baguette_bi.exc import BaguetteException
from baguette_bi.server.db import get_db

get_db = contextmanager(get_db)
app = typer.Typer()


def echo_exc(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except BaguetteException as exc:
            typer.secho(str(exc), fg="red")

    return wrapped


@app.command()
@echo_exc
def version():
    from baguette_bi import __version__

    typer.echo(f"Baguette BI v{__version__}")


new = app.command(name="new")(actions.new)
server = app.command(name="server")(actions.server_run)
develop = app.command(name="develop")(actions.develop)
docs_cmd = app.command(name="docs")(actions.docs_run)


db = typer.Typer()
init = db.command(name="init")(echo_exc(actions.db_init))
upgrade = db.command(name="upgrade")(echo_exc(actions.db_upgrade))


@db.command()
@echo_exc
def reset(yes: bool = Option(False, "--yes", "-y")):
    if yes or typer.confirm(
        "WARNING! This command will drop all existing tables and create empty ones "
        "instead. Continue?"
    ):
        actions.db_reset()
    else:
        typer.echo("Aborting db reset")


app.add_typer(db, name="db")


users = Typer()


@users.command()
@echo_exc
def create(
    username: str,
    password: str = Option(..., "--password", "-p"),
    is_admin: bool = Option(False, "--admin"),
    email: str = Option(None, "--email", "-e"),
    first_name: str = Option(None, "--first-name", "-f"),
    last_name: str = Option(None, "--last-name", "-l"),
):
    actions.users_create(
        username,
        password,
        is_admin=is_admin,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


users_activate = users.command(name="activate")(echo_exc(actions.users_activate))
users_deactivate = users.command(name="deactivate")(echo_exc(actions.users_deactivate))
users_delete = users.command(name="delete")(echo_exc(actions.users_delete))


@users.command(name="set-password")
@echo_exc
def users_set_password(
    username: str,
    password: Optional[str] = Option(None, "--password", "-p"),
    n: int = Option(
        12, "-n", help="Generated password length, if --password option is omitted."
    ),
):
    password = actions.users_set_password(username, password, n)
    if password is not None:
        typer.echo(password)


app.add_typer(users, name="users")
