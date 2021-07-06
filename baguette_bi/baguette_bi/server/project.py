import importlib
import inspect
import pkgutil
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Dict

from baguette_bi.core import AltairChart, Dataset
from baguette_bi.core.chart import Chart
from baguette_bi.exc import NotFound
from baguette_bi.server import settings
from baguette_bi.server.templating import Environment, pages


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


def is_dataset(obj):
    return inspect.isclass(obj) and issubclass(obj, Dataset) and obj is not Dataset


@dataclass
class Project:
    datasets: Dict[str, Dataset]
    charts: Dict[str, Chart]
    pages: Environment

    @classmethod
    @cache  # import only once
    def import_path(cls, path: Path) -> "Project":
        charts = {}
        datasets = {}
        for module in _import_path(path):
            for _, chart in inspect.getmembers(module, is_chart):
                charts[chart.id] = chart
            for _, dataset in inspect.getmembers(module, is_dataset):
                datasets[dataset.id] = dataset
        return cls(
            charts=charts,
            pages=pages,
            datasets=datasets,
        )

    def get_chart(self, pk: str):
        chart = self.charts.get(pk)
        if chart is None:
            raise NotFound
        return chart


@cache
def get_project():
    return Project.import_path(settings.project)
