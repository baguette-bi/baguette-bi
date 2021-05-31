import inspect
from hashlib import md5
from typing import Dict

from baguette_bi.core import context, dataset, utils
from baguette_bi.core.permissions import Permissions


class ChartMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.id = md5(f"{cls.__module__}.{name}".encode("UTF-8")).hexdigest()
        if cls.name is None and not cls.__module__.startswith("baguette_bi.core."):
            cls.name = utils.class_to_name(name)
        if cls.folder is not None:
            cls.folder.charts.append(cls)

    def __hash__(self) -> int:
        return hash(id(self))


class Chart(metaclass=ChartMeta):
    id = None
    name = None
    folder = None
    rendering_engine = None

    permissions = Permissions.inherit

    def render(self):
        raise NotImplementedError

    def rendered_to_dict(self, obj) -> Dict:
        raise NotImplementedError

    def get_rendered(self, ctx: context.RenderContext):
        sig = inspect.signature(self.render)
        kwargs = {}
        for name, par in sig.parameters.items():
            if isinstance(par.default, dataset.Dataset):
                kwargs[name] = par.default.get_data(ctx)
            elif name in ctx.parameters:
                kwargs[name] = ctx.parameters[name].value
            else:
                raise ValueError(f"Parameter {name} not found")
        return self.render(**kwargs)

    @property
    def parent(self):
        """For permissions"""
        return self.folder

    def get_definition(self, ctx: context.RenderContext):
        obj = self.get_rendered(ctx)
        return self.rendered_to_dict(obj)


class AltairChart(Chart):
    rendering_engine: str = "vega-lite"

    def rendered_to_dict(self, obj):
        return obj.to_dict()
