import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import uvicorn
from sqlalchemy import Table
from sqlalchemy.exc import IntegrityError

from baguette_bi.examples import docs
from baguette_bi.examples import new as _new
from baguette_bi.exc import Conflict, NotFound
from baguette_bi.server import db, models, settings

get_db = contextmanager(db.get_db)


def new(target: Path):
    if target.exists():
        raise ValueError(f"{target} already exists")
    src = Path(_new.__file__).parent
    shutil.copytree(src, target, ignore=shutil.ignore_patterns("__pycache__"))


def drop_all_tables():
    Table("alembic_version", models.Base.metadata)
    models.Base.metadata.drop_all(db.engine)


def run_migrations():
    from alembic import command
    from alembic.config import Config

    alembic_dir = Path(__file__).parent / "alembic"
    assert alembic_dir.is_dir()
    alembic_ini = alembic_dir / "alembic.ini"
    migrations_dir = alembic_dir / "migrations"

    config = Config(alembic_ini)
    config.set_main_option("script_location", str(migrations_dir))
    config.set_main_option("sqlalchemy.url", settings.database_url)

    command.upgrade(config, "head")


def create_default_admin():
    try:
        users_create("admin", settings.default_admin_password, is_admin=True)
    except Conflict:
        print("Default admin user already exists, skipping")


def generate_password(n: int = 12):
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


def server_run(project: Path):
    import subprocess

    os.environ["BAGUETTE_PROJECT"] = str(project)
    config = Path(__file__).parent / "server" / "gunicorn.conf.py"
    subprocess.call(["gunicorn", "-c", str(config)])


def develop(
    project: Path,
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
):
    os.environ["BAGUETTE_PROJECT"] = str(project)
    uvicorn.run(
        "baguette_bi.server.app:app",
        reload=reload,
        reload_dirs=[str(project)],
        host=host,
        port=port,
    )


def docs_run(
    reload: bool = False,
    browser: bool = True,
    host: str = "127.0.0.1",
    port: int = 8000,
):
    project = Path(docs.__file__).parent

    if browser:
        import webbrowser
        from threading import Timer

        t = Timer(
            interval=3, function=webbrowser.open, args=("http://localhost:8000/",)
        )
        t.start()

    develop(project=project, host=host, port=port, reload=reload)


def db_init():
    run_migrations()
    create_default_admin()


def db_upgrade():
    run_migrations()


def db_reset():
    drop_all_tables()
    db_init()


def users_create(username: str, password: str, is_admin: bool = False, **kwargs):
    with get_db() as db:
        user = models.User(username, is_admin=is_admin, **kwargs)
        user.set_password(password)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            raise Conflict(f"User {username} already exists")


def get_user(username: str, db) -> models.User:
    user: models.User = db.query(models.User).get(username)
    if user is None:
        raise NotFound(f"User {username} does not exist")
    return user


def users_delete(username: str):
    with get_db() as db:
        user = get_user(username, db)
        db.delete(user)
        db.commit()


def users_deactivate(username: str):
    with get_db() as db:
        user = get_user(username, db)
        user.is_active = False
        db.add(user)
        db.commit()


def users_activate(username: str):
    with get_db() as db:
        user = get_user(username, db)
        user.is_active = True
        db.add(user)
        db.commit()


def users_set_password(username: str, password: Optional[str] = None, n: int = 12):
    _password = generate_password(n) if password is None else password
    with get_db() as db:
        user = get_user(username, db)
        user.set_password(_password)
        db.add(user)
        db.commit()
    if password is None:
        return _password
