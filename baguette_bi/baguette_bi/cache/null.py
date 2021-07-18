import pandas as pd

from baguette_bi.cache.base import ConnectionCache


class NullConnectionCache(ConnectionCache):
    def get(self, connection_id: str, data_request_id: str):
        return None

    def set(
        self, connection_id: str, data_request_id: str, df: pd.DataFrame
    ):  # pragma: no cover
        pass
