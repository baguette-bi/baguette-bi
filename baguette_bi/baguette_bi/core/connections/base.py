import json
from functools import wraps
from hashlib import md5
from typing import Callable

import altair as alt
from jinja2 import Template

from baguette_bi.cache import get_cache
from baguette_bi.core.connections.transforms.base import BaseTransformMixin
from baguette_bi.core.data_request import DataRequest

cache = get_cache()


def execute_wrapper(fn: Callable):
    @wraps(fn)
    def execute(self: "Connection", request: DataRequest):
        return fn(self, self.prepare_request(request))

    return execute


class Connection(BaseTransformMixin):
    type: str = None

    def __init__(self, **details):
        self.details = details
        self.id = md5(json.dumps(self.dict(), sort_keys=True).encode()).hexdigest()

    def __init_subclass__(cls):
        cls.execute = execute_wrapper(cls.execute)

    def dict(self):
        return {"type": self.type, "details": self.details}

    def prepare_request(self, request: DataRequest):
        query = Template(request.query).render(**request.parameters)
        for transform in request.transforms:
            if isinstance(transform, alt.AggregateTransform):
                query = self.transform_aggregate(query, transform)
            elif isinstance(transform, alt.SampleTransform):
                query = self.transform_sample(query, transform)
            else:
                raise ValueError(
                    f"Transform {transform.__class__.__name__} is not supported yet"
                )
        return DataRequest(query=query, parameters=request.parameters)

    def execute(self, query):
        raise NotImplementedError
