from pathlib import Path

import pytest

from baguette_bi.examples import single_file
from baguette_bi.server.project import NotFound, Project, _import_path, get_project

project = get_project()


def test_import_path_raises_file_not_found_when_no_such_path():
    with pytest.raises(FileNotFoundError, match=r"does not exist$"):
        _import_path("/no/such/path")


def test_import_path_raises_file_not_found_when_not_a_package(tmpdir):
    with pytest.raises(FileNotFoundError, match=r"isn't a valid python package$"):
        _import_path(tmpdir)


def test_import_path_single_file():
    mods = _import_path(Path(single_file.__file__))
    assert len(mods) == 1


def test_project_import_path_single_file():
    proj = Project.import_path(single_file.__file__)
    assert len(proj.charts) == 1


def test_get_chart_raises_notfound():
    with pytest.raises(NotFound):
        project.get_chart("not found")
