from contextlib import contextmanager
from pathlib import Path

from baguette_bi.server import models, settings, static
from baguette_bi.server.db import get_db
from baguette_bi.server.project import get_project


def print_ascii():
    import locale

    from baguette_bi import __version__

    loc, _ = locale.getlocale()
    logo = "baguette_moscow.txt" if loc == "ru_RU" else "baguette.txt"
    path = Path(static.__file__).parent / logo
    print(path.read_text().replace("__version__", __version__))


def create_default_admin(db):
    pass


def ensure_admin_user():
    pass


def run():
    print_ascii()
    ensure_admin_user()
