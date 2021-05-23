from pathlib import Path

import pytest
from baguette_bi.examples import altair_examples, single_file
from baguette_bi.server.project import Project, _import_path, project


def test_altair_examples():
    assert len(project.charts) == 15
    assert len(project.folders) == 3
    assert len(project.root.charts) == 0
    assert len(project.root.children) == 1


def test_import_path_raises_file_not_found_when_no_such_path():
    with pytest.raises(FileNotFoundError, match=r"does not exist$"):
        _import_path("/no/such/path")


def test_import_path_raises_file_not_found_when_not_a_package(tmpdir):
    with pytest.raises(FileNotFoundError, match=r"isn't a valid python package$"):
        _import_path(tmpdir)


def test_import_path_ok():
    mods = _import_path(Path(altair_examples.__file__).parent)
    assert len(mods) == 19


def test_import_path_single_file():
    mods = _import_path(Path(single_file.__file__))
    assert len(mods) == 1


def test_project_import_path_single_file():
    proj = Project.import_path(single_file.__file__)
    assert len(proj.charts) == 1
    assert len(proj.root.charts) == 1
    assert len(proj.folders) == 0
    assert len(proj.root.children) == 0


def test_project_import_path_duplicate_bug():
    proj = Project.import_path(Path(altair_examples.__file__).parent)
    assert len(proj.root.children) == 1
