from baguette_bi.server import schema
from baguette_bi.server.project import project
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/", response_model=schema.FolderRead)
def read_root_folder():
    return schema.FolderRead.from_orm(project.root)


@router.get("/{pk}/", response_model=schema.FolderRead)
def read_folder(pk: str):
    folder = project.folders.get(pk)
    if folder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return schema.FolderRead.from_orm(folder)
