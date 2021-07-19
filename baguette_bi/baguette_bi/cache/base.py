from abc import ABC, abstractmethod

import pandas as pd


class ConnectionCache(ABC):
    @abstractmethod
    def get(self, connection_id: str, data_request_id: str):
        raise NotImplementedError

    @abstractmethod
    def set(self, connection_id: str, data_request_id: str, df: pd.DataFrame):
        raise NotImplementedError
