import inspect
from hashlib import md5
from typing import Dict, Optional

from .context import RenderContext
from .dataset import Dataset
from .parameters import Parameter
from .utils import class_to_name


class ChartMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.id = md5(f"{cls.__module__}.{name}".encode("UTF-8")).hexdigest()
        if cls.name is None and not cls.__module__.startswith("baguette_bi.core."):
            cls.name = class_to_name(name)
        if cls.folder is not None:
            cls.folder.charts.append(cls)

    def __hash__(self) -> int:
        return hash(id(self))


class Chart(metaclass=ChartMeta):
    id = None
    name = None
    folder = None
    parameters: Optional[Dict[str, Parameter]] = None
    chart_cls = None
    rendering_engine: str = None

    def render(self) -> chart_cls:
        raise NotImplementedError

    def rendered_to_dict(self, obj) -> Dict:
        raise NotImplementedError

    def get_definition(self, ctx: RenderContext):
        sig = inspect.signature(self.render)
        kwargs = {}
        for name, par in sig.parameters.items():
            if isinstance(par.default, Dataset):
                kwargs[name] = par.default.get_data(ctx)
            elif name in ctx.parameters:
                kwargs[name] = ctx.parameters[name].value
            else:
                raise ValueError(f"Parameter {name} not found")
        obj = self.render(**kwargs)
        return self.rendered_to_dict(obj)


class AltairChart(Chart):
    rendering_engine: str = "vega-lite"

    def rendered_to_dict(self, obj):
        return obj.to_dict()
