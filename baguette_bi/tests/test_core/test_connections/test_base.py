from unittest.mock import MagicMock

import pytest

from baguette_bi.core.connections.base import (
    Connection,
    ConnectionMeta,
    execute_wrapper,
)
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


def test_connection_meta():
    mockcls = MagicMock()
    ConnectionMeta.__init__(mockcls, "MockCls", (), {})
    assert hasattr(mockcls, "execute")
    mockconn = MagicMock()
    mockreq = MagicMock()
    mockcls.execute(mockconn, mockreq)
    assert mockconn.transform_request.call_count == 1


def test_connection_dict():
    conn = Connection()
    assert conn.dict() == {"type": None, "details": {}}


def test_transform_request():
    conn = Connection()
    request = DataRequest("{{ test }}", parameters={"test": "value"})
    transformed = conn.transform_request(request)
    assert request.query == "value"
    assert transformed.query == "value"


def test_execute_raises_not_implemented():
    conn = Connection()
    mockreq = MagicMock()
    mockreq.query = "test"
    mockreq.parameters = {}
    with pytest.raises(NotImplementedError):
        conn.execute(mockreq)
