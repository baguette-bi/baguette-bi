import pytest
from fastapi import HTTPException

from baguette_bi.server.api.folders import read_folder, read_root_folder
from baguette_bi.server.project import get_project

project = get_project()


def test_read_root_folder():
    root = read_root_folder(project=project)
    assert len(root.children) == 1
    assert root.name == "__root__"


def test_read_folder_raises_404():
    with pytest.raises(HTTPException) as exc:
        read_folder("no such folder", project=project)
    assert exc.value.status_code == 404


def test_read_folder():
    root = read_root_folder(project=project)
    pk = root.children[0].id
    f = read_folder(pk, project=project)
    assert len(f.charts) == 2
    assert len(f.children) == 2
