from contextlib import contextmanager

from fastapi import APIRouter, Depends, HTTPException, status

from baguette_bi.core import User
from baguette_bi.server import schema, security
from baguette_bi.server.project import Forbidden, NotFound, project

router = APIRouter()


@contextmanager
def handle_project_exceptions():
    try:
        yield
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except Forbidden:
        raise HTTPException(status.HTTP_403_FORBIDDEN)


@router.get("/{pk}/", response_model=schema.ChartRead)
def read_chart(pk: str, user: User = Depends(security.maybe_user)):
    with handle_project_exceptions():
        chart = project.get_chart(pk, user)
        return schema.ChartRead.from_orm(chart)


@router.post("/{pk}/render/")
def render_chart(
    pk: str,
    render_context: schema.RenderContext,
    user: User = Depends(security.maybe_user),
):
    with handle_project_exceptions():
        chart = project.get_chart(pk, user)
        return chart.get_definition(render_context)
