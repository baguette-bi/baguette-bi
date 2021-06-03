import traceback
from contextlib import contextmanager

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from baguette_bi.core import User
from baguette_bi.server import schema, security
from baguette_bi.server.exc import BaguetteException
from baguette_bi.server.project import Project, get_project

router = APIRouter()


@contextmanager
def handle_project_exceptions():
    try:
        yield
    except BaguetteException as exc:
        exc.raise_for_api()


@router.get("/{pk}/", response_model=schema.ChartRead)
def read_chart(
    pk: str,
    project: Project = Depends(get_project),
    user: User = Depends(security.maybe_user),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk, user)
        return schema.ChartRead.from_orm(chart)


@router.post("/{pk}/render/")
def render_chart(
    pk: str,
    render_context: schema.RenderContext,
    project: Project = Depends(get_project),
    user: User = Depends(security.maybe_user),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk, user)()
        try:
            return chart.get_definition(render_context)
        except Exception:
            tb = traceback.format_exc()
            return JSONResponse({"traceback": tb}, status_code=400)
