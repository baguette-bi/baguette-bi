from typing import Dict

from .parameters import Parameter


class RenderContext:
    def __init__(self, parameters: Dict[str, Parameter]):
        self.parameters = parameters
