import traceback
from contextlib import contextmanager

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from baguette_bi.server import schema
from baguette_bi.server.exc import ServerException
from baguette_bi.server.project import Project, get_project

router = APIRouter()


@contextmanager
def handle_project_exceptions():
    try:
        yield
    except ServerException as exc:
        exc.raise_for_api()


@router.post("/{pk}/render/")
def render_chart(
    pk: str,
    render_context: schema.RenderContext,
    project: Project = Depends(get_project),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk)()
        try:
            return chart.get_definition(render_context)
        except Exception:
            tb = traceback.format_exc()
            return JSONResponse({"traceback": tb}, status_code=400)
