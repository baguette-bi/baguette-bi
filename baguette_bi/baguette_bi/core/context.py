from typing import Any, Dict


class RenderContext:
    def __init__(self, parameters: Dict[str, Any] = None):
        self.parameters = parameters if parameters is not None else {}
