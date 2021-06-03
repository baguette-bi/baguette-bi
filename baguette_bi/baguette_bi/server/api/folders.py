from fastapi import APIRouter, Depends, HTTPException, status

from baguette_bi.server import schema
from baguette_bi.server.project import Project, get_project

router = APIRouter()


@router.get("/", response_model=schema.FolderRead)
def read_root_folder(project: Project = Depends(get_project)):
    return schema.FolderRead.from_orm(project.root)


@router.get("/{pk}/", response_model=schema.FolderRead)
def read_folder(pk: str, project: Project = Depends(get_project)):
    folder = project.folders.get(pk)
    if folder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return schema.FolderRead.from_orm(folder)
