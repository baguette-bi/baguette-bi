from pathlib import Path
from typing import Dict

from fastapi import Request
from fastapi.templating import Jinja2Templates

from baguette_bi.server import templates

templates_dir = Path(templates.__file__).parent.resolve()
j2 = Jinja2Templates(directory=str(templates_dir))


def templates(request: Request):
    def render_template(name: str, context: Dict = None):
        # TODO: flashes
        ctx = {"request": request, "user": None}
        if context:
            ctx.update(context)
        return j2.TemplateResponse(name, ctx)

    return render_template
