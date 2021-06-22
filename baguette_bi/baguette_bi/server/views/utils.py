import json
from typing import Dict, Optional

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse

from baguette_bi.server import models, security, settings, static, templating
from baguette_bi.server.project import Project, get_project


def template_context(
    request: Request,
    user: Optional[models.User] = Depends(security.maybe_user),
    project: Project = Depends(get_project),
) -> Dict:
    return {
        "request": request,
        "user": user,
        "icon": settings.icon,
        "title": settings.title,
        "url_for": request.url_for,
        "project": project,
    }


def templates(ctx: Dict = Depends(template_context)):
    def render(name: str, **context) -> HTMLResponse:
        ctx.update(context)
        return HTMLResponse(templating.inner.get_template(name).render(ctx))

    return render


fallback_locale = "en-US.json"


def get_format_locale(filename: str, folder: str = "format"):
    basepath = static.path / "locales" / folder
    if not (path := basepath / filename).is_file():
        path = basepath / fallback_locale
    return json.loads(path.read_text())


def get_time_format_locale(filename: str):
    return get_format_locale(filename, folder="time-format")


def get_locale_definition():
    basename = settings.locale.split(".")[0].replace("_", "-")
    filename = f"{basename}.json"
    return {
        "formatLocale": get_format_locale(filename),
        "timeFormatLocale": get_time_format_locale(filename),
    }
