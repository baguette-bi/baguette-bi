from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from baguette_bi.server import api, static, views
from baguette_bi.settings import settings

static_dir = Path(static.__file__).parent.resolve() / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.include_router(api.router, prefix="/api")
app.include_router(views.router)
