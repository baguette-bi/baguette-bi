from functools import wraps
from typing import Callable

from jinja2 import Template

from baguette_bi.core.data_request import DataRequest


def execute_wrapper(fn: Callable):
    @wraps(fn)
    def execute(self: "Connection", request: DataRequest):
        return fn(self, self.transform_request(request))

    return execute


class ConnectionMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.execute = execute_wrapper(cls.execute)


class Connection(metaclass=ConnectionMeta):
    type: str

    def __init__(self, **details):
        self.details = details

    def dict(self):
        return {"type": self.type, "details": self.details}

    def transform_request(self, request: DataRequest):
        request.query = Template(request.query).render(**request.parameters)
        return request

    def execute(self, request: DataRequest):
        raise NotImplementedError
