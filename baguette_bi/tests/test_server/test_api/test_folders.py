import pytest
from baguette_bi.server.api.folders import read_folder, read_root_folder
from fastapi import HTTPException


def test_read_root_folder():
    root = read_root_folder()
    assert len(root.children) == 1
    assert root.name == "__root__"


def test_read_folder_raises_404():
    with pytest.raises(HTTPException) as exc:
        read_folder("no such folder")
    assert exc.value.status_code == 404


def test_read_folder():
    root = read_root_folder()
    pk = root.children[0].id
    f = read_folder(pk)
    assert len(f.charts) == 2
    assert len(f.children) == 2
