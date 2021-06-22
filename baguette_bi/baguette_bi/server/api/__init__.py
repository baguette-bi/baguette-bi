from fastapi import APIRouter

from baguette_bi.server.api import charts, info

router = APIRouter()
router.include_router(charts.router, prefix="/charts")
router.include_router(info.router)
