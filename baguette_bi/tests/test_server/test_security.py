from unittest.mock import MagicMock, PropertyMock

import pytest

from baguette_bi.core import User
from baguette_bi.server import security, settings
from baguette_bi.server.exc import HTTPException, WebException
from baguette_bi.server.project import get_project

project = get_project()


def test_check_credentials_no_db_user():
    db = MagicMock()
    db.query.return_value.get.return_value = None
    with pytest.raises(WebException) as exc:
        security.check_credentials("no user", "pass", project=project, db=db)
    assert exc.value.status_code == 401


def test_check_credentials_no_project_user():
    db = MagicMock()
    db.query.return_value.get.return_value.username = "test"
    with pytest.raises(WebException) as exc:
        security.check_credentials("test", "test", project=project, db=db)
    assert exc.value.status_code == 401


def test_check_credentials_incorrect_password(monkeypatch):
    monkeypatch.setattr(project, "users", {"test": User("test")})
    db = MagicMock()
    user = db.query.return_value.get.return_value
    user.username = "test"
    user.check_password.return_value = False
    with pytest.raises(WebException) as exc:
        security.check_credentials("test", "incorrect", project=project, db=db)
    assert exc.value.status_code == 401


def test_check_credentials_success(monkeypatch):
    user = User("test")
    monkeypatch.setattr(project, "users", {"test": user})
    db = MagicMock()
    db.query.return_value.get.return_value = user
    user.username = "test"
    user.check_password = MagicMock(return_value=True)
    returned_user = security.check_credentials("test", "test", project=project, db=db)
    assert returned_user is user


def test_do_login_sets_session():
    request = MagicMock()
    request.session = {}
    user = MagicMock()
    user.username = "test"
    assert security.do_login(request, user) == user
    assert request.session["username"] == user.username


def test_maybe_user_no_auth(monkeypatch):
    monkeypatch.setattr(settings, "auth", False)
    assert security.maybe_user(None) is None


def test_maybe_user_empty_session(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    request = MagicMock()
    request.session.get.return_value = None
    assert security.maybe_user(request) is None
    assert request.session.get.call_count == 1


def test_maybe_user_no_db_user(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    db = MagicMock()
    db.query.return_value.get.return_value = None
    request = MagicMock()
    request.session.get.return_value = "no user"
    assert security.maybe_user(request, project=project, db=db) is None
    assert request.session.get.call_count == 1


def test_maybe_user_no_project_user(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    request = MagicMock()
    request.session.get.return_value = "test"
    db = MagicMock()
    username = PropertyMock(return_value="test")
    type(db.query.return_value.get.return_value).username = username
    assert security.maybe_user(request, project=project, db=db) is None
    assert request.session.get.call_count == 1
    assert username.call_count == 1


def test_maybe_user_inactive_active(monkeypatch):
    monkeypatch.setattr(settings, "auth", True)
    users = MagicMock()
    users.get.return_value.is_active = False
    users.get.return_value.username = "test"
    users.__contains__.return_value = True
    monkeypatch.setattr(project, "users", users)
    request = MagicMock()
    request.session.get.return_value = "test"
    db = MagicMock()
    db.query.return_value.get.return_value.username = "test"
    assert security.maybe_user(request, project=project, db=db) is None
    assert users.get.call_count == 1
    users.get.return_value.is_active = True
    assert security.maybe_user(request, project=project, db=db) is not None


def test_current_user_raises_unauthorized():
    with pytest.raises(HTTPException) as exc:
        security.current_user(None)
    assert exc.value.status_code == 401


def test_current_user_success():
    assert security.current_user(1) == 1
