from pathlib import Path
from typing import Dict, Optional

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates

from baguette_bi.server import models, security, settings, templates

templates_dir = Path(templates.__file__).parent.resolve()
j2 = Jinja2Templates(directory=str(templates_dir))


def templates(
    request: Request, user: Optional[models.User] = Depends(security.maybe_user)
):
    def render_template(name: str, context: Dict = None):
        # TODO: flashes
        ctx = {
            "request": request,
            "user": user,
            "icon": settings.icon,
            "title": settings.title,
        }
        if context:
            ctx.update(context)
        return j2.TemplateResponse(name, ctx)

    return render_template
