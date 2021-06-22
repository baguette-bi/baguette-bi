from typing import Any, Dict, Protocol

import pandas as pd
import pydantic

from baguette_bi.core.data_request import DataRequest


class Connectable(Protocol):
    type: str
    details: Dict

    def execute(self, data_request: DataRequest) -> pd.DataFrame:
        ...


class DatasetMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.__parameters_model__ = pydantic.dataclasses.dataclass(
            cls.Parameters
        ).__pydantic_model__
        cls.id = f"{cls.__module__}.{name}"
        super().__init__(name, bases, attrs)

    def __hash__(self):
        return hash(id(self))


class Dataset(metaclass=DatasetMeta):

    connection: Connectable
    query: Any = None

    class Parameters:
        pass

    def get_data(self, render_context) -> pd.DataFrame:
        parameters = self.__parameters_model__.parse_obj(render_context.parameters)
        request = DataRequest(query=self.query, parameters=parameters.dict())
        df = self.connection.execute(request)
        return self.transform(df)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
