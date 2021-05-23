from unittest.mock import MagicMock

import pytest
from baguette_bi.core.dataset import Dataset


@pytest.fixture
def conn():
    conn = MagicMock()
    conn.dict.return_value = {}
    return conn


@pytest.fixture
def ds(conn):
    return Dataset("test", "test", conn)


def test_hash(ds):
    assert hash(ds) == hash(id(ds))


def test_id(ds):
    assert ds.id == "4e184628fa31f63a83f29ac224758a5b"


def test_get_data(ds):
    ctx = MagicMock()
    ds.get_data(ctx)
    assert ds.connection.execute.call_count == 1
