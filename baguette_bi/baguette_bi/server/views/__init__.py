from types import SimpleNamespace
from typing import Callable, Dict, Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from jinja2.exceptions import TemplateNotFound
from markdown import Markdown

from baguette_bi.core import RenderContext
from baguette_bi.server import exc, models, security, settings
from baguette_bi.server.project import Project, get_project
from baguette_bi.server.views.utils import (
    get_locale_definition,
    template_context,
    templates,
)

router = APIRouter()

md = Markdown(extensions=["fenced_code", "codehilite", "toc"])

router = APIRouter()

locale = get_locale_definition()


@router.get("/", dependencies=[Depends(security.authenticated)])
def index(
    request: Request,
    project: Project = Depends(get_project),
    context: Dict = Depends(template_context),
    render: Callable = Depends(templates),
):
    return get_page(
        "index",
        project=project,
        context=context,
        render=render,
        request=request,
    )


@router.get("/pages/{path:path}", dependencies=[Depends(security.authenticated)])
def get_page(
    path: str,
    request: Request,
    project: Project = Depends(get_project),
    context: Dict = Depends(template_context),
    render: Callable = Depends(templates),
):
    try:
        template = project.pages.get_template(f"{path}.md.j2")
    except TemplateNotFound:
        raise exc.WebException(404)
    _embed = request.query_params._dict.pop("_embed", None) is not None
    context.update(
        {
            "DataFrame": _get_dataframe(project, request.query_params),
            "params": SimpleNamespace(**request.query_params),
            "page": path,
        }
    )
    page = md.convert(template.render(context))
    return render("pages.html.j2", page=page, _embed=_embed, locale=locale)


@router.get("/login/")
def get_login(
    request: Request,
    render: Callable = Depends(templates),
    user: Optional[models.User] = Depends(security.maybe_user),
):
    if not settings.auth or user is not None:
        return RedirectResponse(request.url_for("index"), status.HTTP_302_FOUND)
    return render("login.html.j2")


@router.post("/login/", dependencies=[Depends(security.do_login)])
def post_login(request: Request):
    return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)


@router.get("/logout/")
def get_logout(request: Request):
    request.session["username"] = ""
    return RedirectResponse(request.url_for("get_login"))


def _get_dataframe(project: Project, parameters: Dict):
    def DataFrame(name: str, **kwargs):
        ctx = RenderContext(parameters=parameters)
        dataset = project.datasets[name]()
        return dataset.get_data(ctx)

    return DataFrame
