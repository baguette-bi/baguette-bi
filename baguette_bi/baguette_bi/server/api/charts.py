from baguette_bi.core.chart import Chart
from baguette_bi.server import schema
from baguette_bi.server.project import project
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/{pk}/", response_model=schema.ChartRead)
def read_chart(pk: str):
    chart = project.charts.get(pk)
    if chart is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return schema.ChartRead.from_orm(chart)


@router.post("/{pk}/render/")
def render_chart(pk: str, render_context: schema.RenderContext):
    chart_cls = project.charts.get(pk)
    if chart_cls is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    chart: Chart = chart_cls()
    return chart.get_definition(render_context)
