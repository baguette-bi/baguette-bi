from contextlib import contextmanager
from typing import Callable

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from baguette_bi.core import User
from baguette_bi.server import security
from baguette_bi.server.exc import BaguetteException
from baguette_bi.server.project import Project, get_project
from baguette_bi.server.views import pages
from baguette_bi.server.views.utils import templates

router = APIRouter()
router.include_router(pages.router, prefix="/pages")


@contextmanager
def handle_project_exceptions():
    try:
        yield
    except BaguetteException as exc:
        exc.raise_for_view()


@router.get("/")
def index(
    render: Callable = Depends(templates),
    project: Project = Depends(get_project),
    user: User = Depends(security.maybe_user),
):
    with handle_project_exceptions():
        root = project.get_root(user)
        return render("tree.html.j2", folder=root)


@router.get("/folders/{pk}/")
def folder_page(
    pk: str,
    project: Project = Depends(get_project),
    user: User = Depends(security.maybe_user),
    render: Callable = Depends(templates),
):
    with handle_project_exceptions():
        folder = project.get_folder(pk, user)
        return render("tree.html.j2", folder=folder)


@router.get("/charts/{pk}/")
def chart_page(
    pk: str,
    project: Project = Depends(get_project),
    user: User = Depends(security.maybe_user),
    render: Callable = Depends(templates),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk, user)
        return render("chart.html.j2", chart=chart)


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
