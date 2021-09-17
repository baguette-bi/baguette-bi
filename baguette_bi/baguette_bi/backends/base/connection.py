from baguette_bi.backends.base.client import Client
from baguette_bi.backends.base.query import Query
from baguette_bi.data_request import DataRequest


class Connection:
    """Base user-facing connection class."""

    type: str
    query_cls = Query

    def __init__(self, client: Client):
        self.client = client

    @property
    def id(self):
        return {"type": self.type, "client_id": self.client.id}

    def process_request(self, request: DataRequest):
        query = self.query_cls(
            client=self.client,
            base=request.query,
            parameters=request.parameters,
            transforms=request.transforms,
            echo=request.echo,
        )
        return query.execute()
