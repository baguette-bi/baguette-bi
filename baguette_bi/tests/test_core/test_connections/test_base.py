from unittest.mock import MagicMock

import pytest

from baguette_bi.core.connections.base import Connection, execute_wrapper
from baguette_bi.core.data_request import DataRequest


def test_execute_wrapper():
    mockfn = MagicMock()
    mockconn = MagicMock()
    mockreq = MagicMock()
    wrapped = execute_wrapper(mockfn)
    wrapped(mockconn, mockreq)
    assert mockconn.transform_request.call_count == 1
    assert mockfn.call_count == 1
    assert len(mockfn.call_args.args) == 2


def test_connection_dict():
    conn = Connection()
    assert conn.dict() == {"type": None, "details": {}}


def test_transform_request():
    conn = Connection()
    request = DataRequest("{{ test }}", parameters={"test": "value"})
    transformed = conn.transform_request(request)
    assert request.query == "value"
    assert transformed.query == "value"


def test_subclass_transforms_request():
    class TestConnection(Connection):
        def execute(self, request: DataRequest):
            return request.query

    req = DataRequest(query="{{ test }}", parameters={"test": "value"})
    conn = TestConnection()
    assert conn.execute(req) == "value"


def test_execute_raises_not_implemented():
    conn = Connection()
    mockreq = MagicMock()
    mockreq.query = "test"
    mockreq.parameters = {}
    with pytest.raises(NotImplementedError):
        conn.execute(mockreq)
