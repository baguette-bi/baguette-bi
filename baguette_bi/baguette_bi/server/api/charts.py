import traceback
from contextlib import contextmanager
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from baguette_bi.core.context import RenderContext
from baguette_bi.exc import NotFound
from baguette_bi.server import schema, security
from baguette_bi.server.models import User
from baguette_bi.server.project import Project, get_project

router = APIRouter()


@contextmanager
def handle_project_exceptions():
    try:
        yield
    except NotFound:
        raise HTTPException(404)


@router.post("/{pk}/render/", dependencies=[Depends(security.authenticated_api)])
def render_chart(
    pk: str,
    render_context: schema.RenderContext,
    project: Project = Depends(get_project),
    user: Optional[User] = Depends(security.maybe_user),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk)()
        try:
            return chart.get_definition(RenderContext(**render_context.dict()))
        except Exception:
            traceback.print_exc()
            res = {}
            if user is None or user.is_admin:
                tb = traceback.format_exc()
                res["traceback"] = tb
            return JSONResponse(res, status_code=500)
