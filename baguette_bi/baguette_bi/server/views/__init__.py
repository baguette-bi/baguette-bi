from contextlib import contextmanager
from typing import Callable

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from baguette_bi.core import User
from baguette_bi.server import security
from baguette_bi.server.project import Forbidden, NotFound, project
from baguette_bi.server.views.exc import WebException
from baguette_bi.server.views.utils import templates

router = APIRouter()


@contextmanager
def handle_project_exceptions():
    try:
        yield
    except NotFound:
        raise WebException(status.HTTP_404_NOT_FOUND)
    except Forbidden:
        raise WebException(status.HTTP_403_FORBIDDEN)


@router.get("/")
def index(
    render: Callable = Depends(templates), user: User = Depends(security.maybe_user)
):
    with handle_project_exceptions():
        root = project.get_root(user)
        return render("tree.html.j2", dict(charts=root.charts, folders=root.children))


@router.get("/folders/{pk}/")
def folder_page(
    pk: str,
    user: User = Depends(security.maybe_user),
    render: Callable = Depends(templates),
):
    with handle_project_exceptions():
        folder = project.get_folder(pk, user)
        return render(
            "tree.html.j2", dict(charts=folder.charts, folders=folder.children)
        )


@router.get("/charts/{pk}/")
def chart_page(
    pk: str,
    user: User = Depends(security.maybe_user),
    render: Callable = Depends(templates),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk, user)
        return render("chart.html.j2", dict(chart=chart))


@router.get("/login/")
def get_login(render: Callable = Depends(templates)):
    return render("login.html.j2")


@router.post("/login/", dependencies=[Depends(security.do_login)])
def post_login():
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/logout/")
def get_logout(request: Request):
    request.session["username"] = ""
    return RedirectResponse(request.url_for("get_login"))
