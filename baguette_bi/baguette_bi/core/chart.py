from abc import ABC, abstractmethod
from typing import Dict

from baguette_bi.core import context


class Chart(ABC):
    id = None
    rendering_engine = None

    def __init_subclass__(cls):
        cls.id = f"{cls.__module__}:{cls.__name__}"

    @abstractmethod
    def render(self, *args, **kwargs):  # pragma: no cover
        ...

    @abstractmethod
    def rendered_to_dict(self, obj) -> Dict:  # pragma: no cover
        ...

    def get_rendered(self, ctx: context.RenderContext):
        return ctx.execute(self.render)

    def get_definition(self, ctx: context.RenderContext):
        obj = self.get_rendered(ctx)
        return self.rendered_to_dict(obj)


class AltairChart(Chart):
    rendering_engine: str = "vega-lite"

    def rendered_to_dict(self, obj):
        return obj.to_dict()
