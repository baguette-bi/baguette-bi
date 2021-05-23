from pathlib import Path

from baguette_bi.server import api, views
from baguette_bi.settings import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

static_dir = Path(__file__).parent.resolve() / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.include_router(api.router, prefix="/api")
app.include_router(views.router)
