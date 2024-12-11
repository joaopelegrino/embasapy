import pytest
from tests.mocks.redis_mock import RedisMock
from app.core.cache import RedisCache
from app.core.config import settings

@pytest.fixture
async def redis_mock():
    cache = RedisMock()
    await cache.init()
    yield cache
    await cache.close()

@pytest.fixture
async def redis_cache(redis_mock):
    cache = RedisCache()
    cache._redis = redis_mock
    return cache

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

async def test_redis_missing_key(redis_cache):
    """Testa chave inexistente"""
    value = await redis_cache.get("missing_key")
    assert value is None 

async def test_cache_disabled(redis_cache, monkeypatch):
    """Testa operações com cache desabilitado"""
    monkeypatch.setattr(settings, "CACHE_ENABLED", False)
    redis_cache._enabled = False
    
    await redis_cache.set("test_key", "test_value")
    value = await redis_cache.get("test_key")
    assert value is None

async def test_custom_expiration(redis_cache):
    """Testa expiração customizada"""
    custom_ttl = 300
    await redis_cache.set("test_exp", "test_value", expire=custom_ttl)
    value = await redis_cache.get("test_exp")
    assert value == "test_value" 