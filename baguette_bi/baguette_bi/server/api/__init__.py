from fastapi import APIRouter

from . import charts, folders, info

router = APIRouter()
router.include_router(charts.router, prefix="/charts")
router.include_router(info.router)
router.include_router(folders.router, prefix="/folders")
