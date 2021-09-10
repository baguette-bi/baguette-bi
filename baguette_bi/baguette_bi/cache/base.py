from abc import ABC, abstractmethod

import pandas as pd


class ConnectionCache(ABC):
    @abstractmethod
    def get(self, data_request_id: str):
        raise NotImplementedError

    @abstractmethod
    def set(self, data_request_id: str, df: pd.DataFrame):
        raise NotImplementedError
