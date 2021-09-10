import pickle
from typing import Optional

import pandas as pd
from redis import ConnectionPool, Redis

from baguette_bi.cache.base import ConnectionCache
from baguette_bi.settings import settings


class RedisConnectionCache(ConnectionCache):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str = None,
    ):
        self.pool = ConnectionPool(host=host, port=port, db=db, password=password)

    def get(self, data_request_id: str) -> Optional[pd.DataFrame]:
        with Redis(connection_pool=self.pool) as client:
            if client.exists(data_request_id):
                data = client.get(data_request_id)
                try:
                    return pickle.loads(data)
                except pickle.UnpicklingError:
                    client.delete(data_request_id)

    def set(self, data_request_id: str, df: pd.DataFrame):
        with Redis(connection_pool=self.pool) as client:
            data = pickle.dumps(df)
            client.set(data_request_id, data, ex=settings.cache_ttl)
