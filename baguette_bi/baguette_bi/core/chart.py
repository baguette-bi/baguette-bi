from abc import ABCMeta, abstractmethod
from typing import Dict

from baguette_bi.core import context


class ChartMeta(ABCMeta):
    def __init__(cls, name, bases, attrs):
        cls.id = f"{cls.__module__}.{name}"

    def __hash__(self) -> int:
        return hash(id(self))


class Chart(metaclass=ChartMeta):
    id = None
    rendering_engine = None

    @abstractmethod
    def render(self, *args, **kwargs):
        ...

    @abstractmethod
    def rendered_to_dict(self, obj) -> Dict:
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
