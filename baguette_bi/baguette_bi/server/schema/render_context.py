from typing import Any, Dict

from baguette_bi.schema.base import Base


class RenderContext(Base):
    parameters: Dict[str, Any] = {}
