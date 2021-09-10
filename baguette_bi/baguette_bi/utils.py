from pprint import pformat
from typing import Dict, List, Optional


class Empty:
    """When there's no value in NamespaceDict"""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Empty({self.name})"

    def __repr__(self):
        return str(self)


class NamespaceDict:
    """Helper object to access dict keys as attributes. Recursively loads an object
    into nested NamespaceDicts. Lists stay lists.
    """

    def __init__(self, d: Optional[Dict] = None, **kwargs):
        if d is None:
            d = {}
        d.update(kwargs)
        for k, v in d.items():
            if isinstance(v, dict):
                setattr(self, k, NamespaceDict(v))
            elif isinstance(v, list) and all(isinstance(i, dict) for i in v):
                setattr(self, k, [NamespaceDict(i) for i in v])
            else:
                setattr(self, k, v)

    def to_dict(self):
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, NamespaceDict):
                d[k] = v.to_dict()
            elif isinstance(v, list) and all(isinstance(i, NamespaceDict) for i in v):
                d[k] = [i.to_dict() for i in v]
            elif v != Empty:
                d[k] = v
        return d

    def copy(self):
        return NamespaceDict(self.to_dict())

    def __getitem__(self, k):
        return getattr(self, k)

    def __setitem__(self, k, v):
        if isinstance(v, dict):
            setattr(self, k, NamespaceDict(v))
        elif isinstance(v, list) and all(isinstance(i, dict) for i in v):
            setattr(self, k, [NamespaceDict(i) for i in v])
        elif v != Empty:
            setattr(k, v)

    def __getattr__(self, name: str):
        return Empty

    def __iter__(self):
        return iter(self.to_dict())

    def __contains__(self, item):
        return hasattr(self, item)

    def items(self):
        return self.to_dict().items()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return str(self)


types = ["concat", "vconcat", "hconcat", "layer", "repeat", "facet"]
multiview_charts = types[:4]


class Chart(NamespaceDict):
    @property
    def type(self):
        for t in types:
            if self.t != Empty:
                return t
        return "chart"

    @property
    def items(self):
        if self.type in multiview_charts:
            return self[self.type]

    @items.setter
    def items(self, vals: List):
        if self.items is None:
            raise TypeError("Chart is not compound")
        self[self.type] = vals
