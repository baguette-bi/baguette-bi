from types import SimpleNamespace
from typing import Callable, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from jinja2.exceptions import TemplateNotFound
from markdown import Markdown

from baguette_bi.core.context import RenderContext
from baguette_bi.server import security
from baguette_bi.server.project import Project, get_project
from baguette_bi.server.views.utils import template_context, templates

router = APIRouter()

md = Markdown(extensions=["fenced_code", "toc"])

router = APIRouter()


@router.get("/")
def index(
    request: Request,
    project: Project = Depends(get_project),
    context: Dict = Depends(template_context),
    render: Callable = Depends(templates),
):
    return get_page(
        "index.md", project=project, context=context, render=render, request=request
    )


@router.get("/{path:path}")
def get_page(
    path: str,
    request: Request,
    project: Project = Depends(get_project),
    context: Dict = Depends(template_context),
    render: Callable = Depends(templates),
):
    try:
        template = project.pages.get_template(path)
    except TemplateNotFound:
        raise HTTPException(404)
    if template is None:
        raise HTTPException(404)
    context.update(
        {
            "DataFrame": _get_dataframe(project, request.query_params),
            "params": SimpleNamespace(**request.query_params),
            "page": path,
        }
    )
    page = md.convert(template.render(context))
    return render("pages.html.j2", page=page)


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


def _get_dataframe(project: Project, parameters: Dict):
    def DataFrame(name: str):
        dataset = project.datasets[name]()
        return dataset.get_data(RenderContext(parameters=parameters))

    return DataFrame
