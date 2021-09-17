from typing import Any, Dict, List, Optional

import pandas as pd

from baguette_bi.cache import get_cache
from baguette_bi.mixins import IDMixin

cache = get_cache()


class DataTransform:
    pass


class DataRequest(IDMixin):
    def __init__(
        self,
        *,
        dataset,
        parameters: Optional[Dict[str, Any]] = None,
        transforms: Optional[List] = None,
        echo: bool = False,
    ):
        self.dataset = dataset
        self.parameters = parameters if parameters is not None else {}
        self.transforms = transforms if transforms is not None else []
        self.echo = echo

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"DataRequest({self.id})"

    def __repr__(self):
        return str(self)

    @property
    def query(self):
        return self.dataset.query

    def details(self):
        return {
            "dataset_id": self.dataset.id,
            "connection_id": self.dataset.connection.id,
            "parameters": self.parameters,
            "transforms": [t.to_dict() for t in self.transforms],
        }

    def execute(self) -> pd.DataFrame:
        cached = cache.get(self.id)
        if cached is not None:
            return cached
        df = self.dataset.connection.process_request(self)
        cache.set(self.id, df)
        return df
