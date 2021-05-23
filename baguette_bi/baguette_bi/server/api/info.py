from fastapi import APIRouter
from baguette_bi import __version__


router = APIRouter()


@router.get("/version/")
def version():
    return {"version": __version__}


@router.get("/health/")
def health():
    return {"status": "OK"}
