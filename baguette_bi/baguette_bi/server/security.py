from fastapi import Depends, Form, Request, status

from baguette_bi.server import exc, models, settings
from baguette_bi.server.db import Session, get_db


def check_credentials(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
) -> models.User:
    user: models.User = db.query(models.User).get(username)
    if user is None or not user.check_password(password):
        raise exc.WebException(status.HTTP_401_UNAUTHORIZED)
    return user


def do_login(request: Request, user: models.User = Depends(check_credentials)):
    request.session["username"] = user.username
    request.session["counter"] = user.session_counter
    return user


def maybe_user(
    request: Request,
    db: Session = Depends(get_db),
):
    if not settings.auth:
        return None
    username = request.session.get("username")
    if username is None:
        return None
    user: models.User = db.query(models.User).get(username)
    counter = request.session.get("counter")
    try:
        counter = int(counter)
    except ValueError:
        return None
    if (
        user is None
        or counter is None
        or not user.is_active
        or counter != user.session_counter
    ):
        return None
    return user


def authenticated(request: Request, user: models.User = Depends(maybe_user)):
    if settings.auth and user is None:
        raise exc.WebException(status.HTTP_401_UNAUTHORIZED)


def authenticated_api(user: models.User = Depends(maybe_user)):
    if settings.auth and user is None:
        raise exc.APIException(status.HTTP_401_UNAUTHORIZED)
