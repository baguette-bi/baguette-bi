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

    def get(self, connection_id: str, data_request_id: str) -> Optional[pd.DataFrame]:
        with Redis(connection_pool=self.pool) as client:
            key = f"{connection_id}:{data_request_id}"
            if client.exists(key):
                data = client.get(key)
                try:
                    return pickle.loads(data)
                except pickle.UnpicklingError:
                    client.delete(key)

    def set(self, connection_id: str, data_request_id: str, df: pd.DataFrame):
        with Redis(connection_pool=self.pool) as client:
            key = f"{connection_id}:{data_request_id}"
            data = pickle.dumps(df)
            client.set(key, data, ex=settings.cache_ttl)
