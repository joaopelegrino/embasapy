from typing import AsyncGenerator
from fastapi import Depends

from app.core.cache import RedisCache
from app.services.analysis import AnalysisService
from app.core.config import settings

async def get_redis() -> AsyncGenerator[RedisCache, None]:
    """Dependency para obter instância do Redis"""
    if settings.APP_ENV == "test":
        from tests.mocks.redis_mock import RedisMock
        cache = RedisMock()
    else:
        cache = RedisCache()
    
    await cache.init()
    try:
        yield cache
    finally:
        await cache.close()

async def get_analysis_service(
    cache: RedisCache = Depends(get_redis)
) -> AnalysisService:
    """Dependency para obter instância do AnalysisService"""
    return AnalysisService(cache=cache) 