import json
from hashlib import md5
from typing import Protocol

import pandas as pd

from .context import RenderContext
from .data_request import DataRequest
from .secret import SecretDict


class Connectable(Protocol):
    type: str
    params: SecretDict

    def store(self, identifier: str, df: pd.DataFrame):
        """Store a dataframe"""

    def retrieve(self, identifier: str):
        """Store a dataframe"""

    def execute(self, data_request: DataRequest) -> pd.DataFrame:
        """Execute a query against this connection"""

    def unstore(self, identifier: str):
        """Delete stored data."""


class Dataset:
    def __init__(
        self,
        name: str,
        query: str,
        connection: Connectable,
        storage_connection: Connectable = None,
        refresh_interval: int = None,
    ):
        self.id = md5(
            json.dumps({"query": query, "connection": connection.dict()}).encode(
                "UTF-8"
            )
        ).hexdigest()
        self.name = name
        self.query = query
        self.connection = connection
        self.storage_connection = storage_connection
        self.refresh_interval = refresh_interval

    def get_data(self, render_context: RenderContext):
        request = DataRequest(query=self.query)
        return self.connection.execute(request)

    def __hash__(self) -> int:
        return hash(id(self))
