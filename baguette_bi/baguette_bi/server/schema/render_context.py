from typing import Any, Dict

from baguette_bi.server.schema.base import Base


class RenderContext(Base):
    parameters: Dict[str, Any] = {}
