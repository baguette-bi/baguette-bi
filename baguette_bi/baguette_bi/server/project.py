import importlib
import inspect
import pkgutil
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from baguette_bi.core.chart import AltairChart, Chart, ChartMeta
from baguette_bi.core.folder import Folder
from baguette_bi.settings import settings


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


@dataclass
class Project:
    root: Folder
    folders: Dict[str, Folder]
    charts: Dict[str, ChartMeta]

    @classmethod
    def import_path(cls, path: Path) -> "Project":
        root = Folder("__root__")
        folders = {}
        charts = {}
        for module in _import_path(path):
            for _, folder in inspect.getmembers(module, is_folder):
                folders[folder.id] = folder
                if folder.parent is None and folder not in root.children:
                    root.children.append(folder)
            for _, chart in inspect.getmembers(module, is_chart):
                charts[chart.id] = chart
                if chart.folder is None and chart not in root.charts:
                    root.charts.append(chart)
        return cls(root=root, folders=folders, charts=charts)


project = Project.import_path(settings.project)
