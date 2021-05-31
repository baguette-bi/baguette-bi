from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from baguette_bi.server import api, settings, startup, static, views
from baguette_bi.server.views.exc import WebException

static_dir = Path(static.__file__).parent.resolve()

startup.run()

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="strict",
    max_age=settings.session_max_age,
)

app.include_router(api.router, prefix="/api")
app.include_router(views.router)


@app.exception_handler(WebException)
def handle_web_exception(request: Request, exc: WebException):
    return RedirectResponse(request.url_for("get_login"))
