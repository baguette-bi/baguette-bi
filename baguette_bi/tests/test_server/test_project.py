from pathlib import Path
from unittest.mock import MagicMock

import pytest

from baguette_bi.core.permissions import Permissions
from baguette_bi.examples import altair_examples, single_file
from baguette_bi.server import settings
from baguette_bi.server.project import (
    Forbidden,
    NotFound,
    Project,
    _import_path,
    check_permissions,
    get_project,
)

project = get_project()


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
    assert len(mods) == 20


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
    assert len(project.root.children) == 1


def test_check_permissions_no_auth(monkeypatch):
    monkeypatch.setattr(settings, "auth", False)
    assert check_permissions(MagicMock(), None)


def test_check_permissions_public(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    obj = MagicMock()
    obj.permissions = Permissions.public
    assert check_permissions(obj, None)


def test_check_permission_user_none_permissions_authenticated(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    obj = MagicMock()
    obj.permissions = Permissions.authenticated
    assert not check_permissions(obj, None)


def test_check_permissions_admin_permissions_authenticated(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    obj = MagicMock()
    admin = MagicMock()
    admin.is_admin = True
    assert check_permissions(obj, admin)


def test_check_permissions_perm_list(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    obj = MagicMock()
    user = MagicMock()
    user.is_admin = False
    user.username = "user"
    obj.permissions = {user}
    assert check_permissions(obj, user)
    other = MagicMock()
    other.username = "other"
    other.is_admin = False
    assert not check_permissions(obj, other)


def test_check_permissions_inherit(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    obj = MagicMock()
    obj.permissions = Permissions.inherit
    obj.parent.permissions = Permissions.authenticated
    user = MagicMock()
    user.is_admin = False
    assert check_permissions(obj, user)
    assert not check_permissions(obj, None)
    obj.parent.permissions = Permissions.public
    assert check_permissions(obj, None)


def test_check_permissions_catchall_false(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    obj = MagicMock()
    obj.permissions = None
    user = MagicMock()
    user.is_admin = False
    assert not check_permissions(obj, user)


def test_project_get_root_raises_forbidden(monkeypatch):
    mock_check = MagicMock(return_value=False)
    monkeypatch.setattr("baguette_bi.server.project.check_permissions", mock_check)
    with pytest.raises(Forbidden):
        project.get_root(None)


def test_project_get_root_checks_permissions(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    monkeypatch.setattr(project.root, "permissions", Permissions.public)
    monkeypatch.setattr(
        project.root.children[0], "permissions", Permissions.authenticated
    )
    assert project.get_root(None).children == []
    monkeypatch.setattr(project.root.children[0], "permissions", Permissions.inherit)
    assert len(project.get_root(None).children) == 1


def test_project_get_folder_raises_notfound():
    with pytest.raises(NotFound):
        project.get_folder("not_found", None)


def test_project_get_folder_raises_forbidden(monkeypatch):
    mock_check = MagicMock(return_value=False)
    monkeypatch.setattr("baguette_bi.server.project.check_permissions", mock_check)
    with pytest.raises(Forbidden):
        project.get_folder(project.root.children[0].id, None)


def test_project_get_folder_checks_permissions(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    monkeypatch.setattr(project.root, "permissions", Permissions.public)
    monkeypatch.setattr(
        project.root.children[0].children[0], "permissions", Permissions.authenticated
    )
    monkeypatch.setattr(
        project.root.children[0].charts[0], "permissions", Permissions.authenticated
    )
    folder = project.get_folder(project.root.children[0].id, None)
    assert len(folder.children) == 1
    assert len(folder.charts) == 1


def test_get_chart_raises_notfound():
    with pytest.raises(NotFound):
        project.get_chart("not found", None)


def test_get_chart_raises_forbidden(monkeypatch):
    mock_check = MagicMock(return_value=False)
    monkeypatch.setattr("baguette_bi.server.project.check_permissions", mock_check)
    with pytest.raises(Forbidden):
        project.get_chart(project.root.children[0].charts[0].id, None)


def test_get_chart_ok():
    assert (
        project.get_chart(project.root.children[0].charts[0].id, None).name
        == "Bar Chart with Negative Values"
    )
