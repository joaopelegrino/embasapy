from typing import AsyncGenerator
from fastapi import Depends

from app.core.cache import RedisCache
from app.services.analysis import AnalysisService

async def get_redis() -> AsyncGenerator[RedisCache, None]:
    """Dependency para obter instância do Redis"""
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