import json
from hashlib import md5
from typing import Dict, Optional

import altair as alt
from jinja2 import Template

from baguette_bi.cache import get_cache
from baguette_bi.core.connections.transforms.base import BaseTransformMixin
from baguette_bi.core.data_request import DataRequest

cache = get_cache()


class Connection(BaseTransformMixin):
    type: str = None

    def __init__(self, **details):
        self.details = details
        self.id = md5(json.dumps(self.dict(), sort_keys=True).encode()).hexdigest()

    def dict(self):
        return {"type": self.type, "details": self.details}

    def prepare_query(self, request: DataRequest):
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
        if request.echo:
            print(query)
        return query, request.parameters

    def process_request(self, request: DataRequest):
        return self.execute(*self.prepare_query(request))

    def execute(self, query, parameters: Optional[Dict]):
        raise NotImplementedError
