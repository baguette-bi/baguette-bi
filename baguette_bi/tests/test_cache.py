import pandas as pd
import pytest

from baguette_bi.cache.null import NullConnectionCache
from baguette_bi.cache.redis import RedisConnectionCache


def test_null_get():
    assert NullConnectionCache().get("", "") is None


@pytest.fixture(scope="module")
def redis_cache(redis):
    return RedisConnectionCache()


def test_redis_set(redis_cache: RedisConnectionCache):
    df = pd.DataFrame(data={"a": [1, 2, 3], "b": [2, 3, 4]})
    redis_cache.set("test", "test", df)

    assert redis_cache.get("test", "test").equals(df)
