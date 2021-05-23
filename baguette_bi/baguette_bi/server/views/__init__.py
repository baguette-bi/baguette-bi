from typing import Callable

from baguette_bi.server.project import project
from fastapi import APIRouter, Depends, HTTPException, status

from .utils import templates

router = APIRouter()


@router.get("/")
def index(render: Callable = Depends(templates)):
    return render(
        "tree.html.j2", dict(charts=project.root.charts, folders=project.root.children)
    )


@router.get("/folders/{pk}/")
def folder_page(pk: str, render: Callable = Depends(templates)):
    folder = project.folders.get(pk)
    if folder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return render("tree.html.j2", dict(charts=folder.charts, folders=folder.children))


@router.get("/charts/{pk}/")
def chart_page(pk: str, render: Callable = Depends(templates)):
    chart = project.charts.get(pk)
    if chart is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return render("chart.html.j2", dict(chart=chart))
