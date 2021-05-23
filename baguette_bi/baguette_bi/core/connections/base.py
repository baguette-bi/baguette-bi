from functools import wraps
from typing import Callable

from jinja2 import Template

from baguette_bi.core.data_request import DataRequest
from baguette_bi.core.dataset import Dataset
from baguette_bi.core.secret import SecretDict


def execute_wrapper(fn: Callable):
    @wraps(fn)
    def execute(self: "Connection", request: DataRequest):
        return fn(self, self.transform_request(request))

    return execute


class ConnectionMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.execute = execute_wrapper(cls.execute)


class Connection(metaclass=ConnectionMeta):
    type: str = None

    def __init__(self, **details):
        self.details = SecretDict(details)

    def dict(self):
        return {"type": self.type, "details": self.details.dict()}

    def transform_request(self, request: DataRequest):
        request.query = Template(request.query).render(**request.parameters)
        return request

    def execute(self, request: DataRequest):
        raise NotImplementedError

    def dataset(
        self,
        name: str,
        query: str,
        storage_connection: "Connection" = None,
        refresh_interval: int = None,
    ):
        return Dataset(
            name=name,
            query=query,
            connection=self,
            storage_connection=storage_connection,
            refresh_interval=refresh_interval,
        )
