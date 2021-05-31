from typing import Optional

from fastapi import Depends, Form, HTTPException, Request, status

from baguette_bi import core
from baguette_bi.server import models, settings
from baguette_bi.server.db import Session, get_db
from baguette_bi.server.project import project


def check_credentials(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user: models.User = db.query(models.User).get(username)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if user.check_password(password):
        return user
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)


def do_login(request: Request, user: models.User = Depends(check_credentials)):
    request.session["username"] = user.username
    return user


def maybe_user(request: Request, db: Session = Depends(get_db)):
    if not settings.auth:
        return None
    username = request.session.get("username")
    if username is None:
        return None
    db_user: models.User = db.query(models.User).get(username)
    if db_user is None:
        return None
    if db_user.username == "admin":
        return core.User("admin", is_admin=True)
    if db_user is not None:
        user = project.users.get(db_user.username)
        if user is None or not user.is_active:
            return None
    return user


def current_user(user: Optional[models.User] = Depends(maybe_user)):
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user
