import pytest
from app.core.cache import RedisCache

@pytest.fixture
async def redis_cache():
    cache = RedisCache()
    await cache.init()
    yield cache
    await cache.close()

async def test_redis_set_get(redis_cache):
    """Testa operações básicas do Redis"""
    await redis_cache.set("test_key", "test_value")
    value = await redis_cache.get("test_key")
    assert value == "test_value"

async def test_redis_expiration(redis_cache):
    """Testa expiração do cache"""
    await redis_cache.set("test_exp", "test_value", expire=1)
    value = await redis_cache.get("test_exp")
    assert value == "test_value" 