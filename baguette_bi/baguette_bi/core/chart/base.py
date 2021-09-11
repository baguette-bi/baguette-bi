from abc import ABC, abstractmethod
from typing import Dict

from baguette_bi.core.context import RenderContext


class Chart(ABC):
    id = None
    rendering_engine = None

    def __init_subclass__(cls):
        cls.id = f"{cls.__module__}.{cls.__name__}"

    @abstractmethod
    def render(self, *args, **kwargs):  # pragma: no cover
        ...

    @abstractmethod
    def rendered_to_dict(self, obj) -> Dict:  # pragma: no cover
        ...

    def get_definition(self, ctx: RenderContext):
        obj = ctx.execute(self.render)
        return self.rendered_to_dict(obj)
