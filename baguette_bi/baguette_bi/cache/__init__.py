from baguette_bi.cache.null import NullConnectionCache
from baguette_bi.cache.redis import RedisConnectionCache
from baguette_bi.settings import settings


def get_cache():
    if settings.cache == "none":
        return NullConnectionCache()
    if settings.cache == "redis":
        return RedisConnectionCache(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
        )
