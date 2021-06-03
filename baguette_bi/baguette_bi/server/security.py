from typing import Optional

from fastapi import Depends, Form, Request

from baguette_bi.server import models, settings
from baguette_bi.server.db import Session, get_db
from baguette_bi.server.exc import Unauthorized
from baguette_bi.server.project import Project, get_project


def check_credentials(
    username: str = Form(...),
    password: str = Form(...),
    project: Project = Depends(get_project),
    db: Session = Depends(get_db),
):
    user: models.User = db.query(models.User).get(username)
    if user is None or user.username not in project.users:
        Unauthorized().raise_for_view()
    if user.check_password(password):
        return project.users.get(user.username)
    Unauthorized().raise_for_view()


def do_login(request: Request, user: models.User = Depends(check_credentials)):
    request.session["username"] = user.username
    return user


def maybe_user(
    request: Request,
    project: Project = Depends(get_project),
    db: Session = Depends(get_db),
):
    if not settings.auth:
        return None
    username = request.session.get("username")
    if username is None:
        return None
    db_user: models.User = db.query(models.User).get(username)
    if db_user is None or db_user.username not in project.users:
        return None
    user = project.users.get(db_user.username)
    if not user.is_active:
        return None
    return user


def current_user(user: Optional[models.User] = Depends(maybe_user)):
    if user is None:
        Unauthorized().raise_for_api()
    return user
