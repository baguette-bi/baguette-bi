from unittest.mock import MagicMock

import pytest

from baguette_bi.core.dataset import Dataset


@pytest.fixture
def ds():
    class TestDataset(Dataset):
        connection = MagicMock()

    return TestDataset


def test_hash(ds):
    assert hash(ds) == hash(id(ds))


def test_id(ds):
    assert ds.id == "tests.test_core.test_dataset.TestDataset"


def test_get_data(ds):
    ctx = MagicMock()
    ds().get_data(ctx)
    assert ds.connection.execute.call_count == 1
