from pathlib import Path
from typing import Dict
from unittest.mock import MagicMock

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates_dir = Path(__file__).parent.parent.resolve() / "templates"
j2 = Jinja2Templates(directory=str(templates_dir))


def templates(request: Request):
    def render_template(name: str, context: Dict = None):
        # TODO: flashes
        ctx = {"request": request, "user": None}
        if context:
            ctx.update(context)
        return j2.TemplateResponse(name, ctx)

    return render_template
