from contextlib import contextmanager

from baguette_bi.server import models, settings
from baguette_bi.server.db import engine, get_db
from baguette_bi.server.project import project


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
    if not settings.auth:
        return
    admins = [u.username for _, u in project.users.items() if u.is_admin]
    with contextmanager(get_db)() as db:
        if len(admins) == 0:
            create_default_admin(db)
            return
        admins_in_db = (
            db.query(models.User).filter(models.User.username.in_(admins)).count()
        )
        if admins_in_db == 0:
            create_default_admin(db)


def run():
    create_all()
    ensure_admin_user()
