import json
from hashlib import md5
from typing import Dict, Optional

from baguette_bi.core.connections.query_builders.base import BaseQueryBuilder
from baguette_bi.core.data_request import DataRequest


class Connection:
    type: str = None
    query_builder = BaseQueryBuilder()

    def __init__(self, **details):
        self.details = details
        self.id = md5(json.dumps(self.dict(), sort_keys=True).encode()).hexdigest()

    def dict(self):
        return {"type": self.type, "details": self.details}

    def process_request(self, request: DataRequest):
        query = self.query_builder.build(
            request.query, request.parameters, request.transforms
        )
        if request.echo:
            print(query)
        return self.execute(query, request.parameters)

    def execute(self, query, parameters: Optional[Dict]):
        raise NotImplementedError
