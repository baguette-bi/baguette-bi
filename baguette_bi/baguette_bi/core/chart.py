import inspect
from typing import Dict

from baguette_bi.core import context, dataset


class ChartMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.id = f"{cls.__module__}.{name}"

    def __hash__(self) -> int:
        return hash(id(self))


class Chart(metaclass=ChartMeta):
    id = None
    rendering_engine = None

    def render(self):
        raise NotImplementedError

    def rendered_to_dict(self, obj) -> Dict:
        raise NotImplementedError

    def get_rendered(self, ctx: context.RenderContext):
        sig = inspect.signature(self.render)
        kwargs = {}
        for name, par in sig.parameters.items():
            if isinstance(par.default, dataset.DatasetMeta):
                kwargs[name] = par.default().get_data(ctx)
        return self.render(**kwargs)

    def get_definition(self, ctx: context.RenderContext):
        obj = self.get_rendered(ctx)
        return self.rendered_to_dict(obj)


class AltairChart(Chart):
    rendering_engine: str = "vega-lite"

    def rendered_to_dict(self, obj):
        return obj.to_dict()
