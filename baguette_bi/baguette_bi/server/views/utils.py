from typing import Dict, Optional

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse

from baguette_bi.server import models, security, settings, templating
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
