from typing import Any, Dict, List, Optional, Protocol

import altair as alt
import pandas as pd
import pydantic

from baguette_bi.cache import get_cache
from baguette_bi.core.data_request import DataRequest

cache = get_cache()


class Connectable(Protocol):
    type: str
    details: Dict

    def execute(self, data_request: DataRequest) -> pd.DataFrame:
        ...


class DatasetMeta(type):
    registry: Dict[str, "DatasetMeta"] = {}

    def __init__(cls, name, bases, attrs):
        cls.__parameters_model__ = pydantic.dataclasses.dataclass(
            cls.Parameters
        ).__pydantic_model__
        cls.id = f"{cls.__module__}.{name}"
        cls.transform = classmethod(cls.transform)
        cls.registry[cls.id] = cls
        super().__init__(name, bases, attrs)

    def __hash__(self):
        return hash(id(self))

    @property
    def name(self):
        return alt.NamedData(self.id)

    def request(
        self, parameters: Optional[Dict] = None, transforms: Optional[List] = None
    ) -> DataRequest:
        parameters = (
            self.__parameters_model__.parse_obj(parameters).dict()
            if parameters is not None
            else {}
        )
        return DataRequest(
            dataset=self,
            parameters=parameters,
            transforms=transforms,
            echo=self.echo,
        )

    def get_data(
        self, parameters: Optional[Dict] = None, transforms: Optional[List] = None
    ) -> pd.DataFrame:
        return self.transform(
            self.request(parameters, transforms).execute(),
        )

    def _repr_html_(self):
        """For Jupyter"""
        return (
            self.request(transforms=[alt.SampleTransform(sample=10)])
            .execute()
            .to_html()
        )


class Dataset(metaclass=DatasetMeta):

    connection: Connectable
    query: Any = None
    echo: bool = False

    class Parameters:
        pass

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
