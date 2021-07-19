import json
from functools import wraps
from hashlib import md5
from typing import Callable

from jinja2 import Template

from baguette_bi.cache import get_cache
from baguette_bi.core.data_request import DataRequest

cache = get_cache()


def execute_wrapper(fn: Callable):
    @wraps(fn)
    def execute(self: "Connection", request: DataRequest):
        return fn(self, self.transform_request(request))

    return execute


class ConnectionMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.execute = execute_wrapper(cls.execute)


class Connection(metaclass=ConnectionMeta):
    id = None
    type: str = None

    def __init__(self, **details):
        self.details = details
        self.id = md5(json.dumps(self.dict(), sort_keys=True).encode()).hexdigest()

    def dict(self):
        return {"type": self.type, "details": self.details}

    def transform_request(self, request: DataRequest):
        request.query = Template(request.query).render(**request.parameters)
        return request

    def execute(self, request: DataRequest):
        raise NotImplementedError
