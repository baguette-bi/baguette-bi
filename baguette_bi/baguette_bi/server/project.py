import importlib
import inspect
import pkgutil
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Dict, Optional

from baguette_bi.core import AltairChart, Folder, Permissions, User
from baguette_bi.core.chart import Chart
from baguette_bi.server import settings
from baguette_bi.server.exc import Forbidden, NotFound


@contextmanager
def syspath(path):
    sys.path.append(path)
    yield
    sys.path.pop()


def get_submodules(mod):
    for sub in pkgutil.walk_packages(mod.__path__, prefix=mod.__name__ + "."):
        yield importlib.import_module(sub.name)


def _import_path(fp: str):
    path = Path(fp)
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path.is_dir() and not (path / "__init__.py").is_file():
        raise FileNotFoundError(
            f"{path} is a directory, but isn't a valid python package"
        )
    parent = str(path.parent)
    name = path.stem
    # TODO: user-readable errors
    with syspath(parent):
        mod = importlib.import_module(name)
        if path.is_dir():
            return [mod] + list(get_submodules(mod))
        return [mod]


def is_chart(obj):
    return (
        inspect.isclass(obj)
        and issubclass(obj, Chart)
        and obj not in (Chart, AltairChart)
    )


def is_folder(obj):
    return isinstance(obj, Folder)


def is_user(obj):
    return isinstance(obj, User)


def check_permissions(obj, user: Optional[User]):
    if obj.permissions == Permissions.public or not settings.auth:
        return True
    if obj.permissions == Permissions.inherit:
        return check_permissions(obj.parent, user)
    if user is None:
        return False
    if user.is_admin:
        return True
    if obj.permissions == Permissions.authenticated:
        return True
    if isinstance(obj.permissions, (list, set)):
        return any(user.username == u.username for u in obj.permissions)
    return False


@dataclass
class Project:
    root: Folder
    folders: Dict[str, Folder]
    charts: Dict[str, Chart]
    users: Dict[str, User]

    @classmethod
    @cache  # import only once
    def import_path(cls, path: Path) -> "Project":
        root = Folder("__root__", permissions=settings.root_permissions)
        folders = {}
        charts = {}
        users = {}
        for module in _import_path(path):
            for _, folder in inspect.getmembers(module, is_folder):
                folders[folder.id] = folder
                if folder.parent is not None and folder not in folder.parent.children:
                    folder.parent.children.append(folder)
                if folder.parent is None and folder not in root.children:
                    folder.parent = root
                    root.children.append(folder)
            for _, chart in inspect.getmembers(module, is_chart):
                charts[chart.id] = chart
                if chart.folder is None and chart not in root.charts:
                    chart.folder = root
                    root.charts.append(chart)
            for _, user in inspect.getmembers(module, is_user):
                users[user.username] = user
        return cls(root=root, folders=folders, charts=charts, users=users)

    def get_root(self, user: Optional[User]):
        if check_permissions(self.root, user):
            f = Folder(self.root.name, permissions=self.root.permissions)
            f.charts = [c for c in self.root.charts if check_permissions(c, user)]
            f.children = [c for c in self.root.children if check_permissions(c, user)]
            return f
        raise Forbidden

    def get_folder(self, pk: str, user: Optional[User]):
        folder = self.folders.get(pk)
        if folder is None:
            raise NotFound
        if check_permissions(folder, user):
            f = Folder(
                folder.name, parent=folder.parent, permissions=folder.permissions
            )
            f.charts = [c for c in folder.charts if check_permissions(c, user)]
            f.children = [c for c in folder.children if check_permissions(c, user)]
            return f
        raise Forbidden

    def get_chart(self, pk: str, user: Optional[User]):
        chart = self.charts.get(pk)
        if chart is None:
            raise NotFound
        if check_permissions(chart, user):
            return chart
        raise Forbidden


@cache
def get_project():
    return Project.import_path(settings.project)
