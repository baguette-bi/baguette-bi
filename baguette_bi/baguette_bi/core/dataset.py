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
    main_registry = {}

    def __init__(cls, name, bases, attrs):
        cls.__parameters_model__ = pydantic.dataclasses.dataclass(
            cls.Parameters
        ).__pydantic_model__
        cls.id = f"{cls.__module__}:{name}"
        if cls.__module__ == "__main__":
            cls.main_registry[cls.id] = cls
        super().__init__(name, bases, attrs)

    def __hash__(self):
        return hash(id(self))

    @property
    def name(cls):
        return alt.NamedData(cls.id)

    def _repr_html_(self):
        """For Jupyter"""
        return self.connection.execute(
            DataRequest(query=self.query, transforms=[alt.SampleTransform(sample=10)])
        ).to_html()


class Dataset(metaclass=DatasetMeta):

    connection: Connectable
    query: Any = None
    echo: bool = False

    class Parameters:
        pass

    def get_data(
        self, render_context, transforms: Optional[List] = None
    ) -> pd.DataFrame:
        parameters = self.__parameters_model__.parse_obj(render_context.parameters)
        request = DataRequest(
            query=self.query,
            parameters=parameters.dict(),
            transforms=transforms,
            echo=self.echo,
        )
        cached = cache.get(self.connection.id, request.id)
        if cached is not None:
            return cached
        df = self.transform(self.connection.execute(request))
        cache.set(self.connection.id, request.id, df)
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
