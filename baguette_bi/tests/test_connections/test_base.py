from unittest.mock import MagicMock

import pytest

from baguette_bi.connections.base import Connection
from baguette_bi.data_request import DataRequest


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
