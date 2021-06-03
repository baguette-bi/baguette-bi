from contextlib import contextmanager
from pathlib import Path

from baguette_bi.core import User
from baguette_bi.server import models, settings, static
from baguette_bi.server.db import engine, get_db
from baguette_bi.server.project import get_project


def print_ascii():
    import locale

    from baguette_bi import __version__

    loc, _ = locale.getlocale()
    logo = "baguette_moscow.txt" if loc == "ru_RU" else "baguette.txt"
    path = Path(static.__file__).parent / logo
    print(path.read_text().replace("__version__", __version__))


def create_all():
    """Only one "migration"
    TODO: migrate to alembic, separate command
    """
    models.base.Base.metadata.create_all(engine)


def create_default_admin(db):
    admin = models.User(username="admin")
    admin.set_password(settings.default_admin_password)
    db.merge(admin)
    db.commit()


def ensure_admin_user():
    """If there is no admin user with a set password in the project,
    create a default 'admin' admin
    """
    if not settings.auth:
        return
    project = get_project()
    admins = [u.username for _, u in project.users.items() if u.is_admin]
    with contextmanager(get_db)() as db:
        admins_in_db = (
            db.query(models.User).filter(models.User.username.in_(admins)).count()
        )
        if admins_in_db == 0:
            create_default_admin(db)
            project.users["admin"] = User("admin", is_admin=True)


def run():
    print_ascii()
    create_all()
    ensure_admin_user()
