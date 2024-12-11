from typing import Optional
import aioredis
from app.core.config import settings

class RedisCache:
    """Gerenciador de cache Redis"""
    
    def __init__(self):
        self._redis = None
    
    async def init(self):
        """Inicializa conexão com Redis"""
        if not self._redis:
            self._redis = await aioredis.create_redis_pool(
                settings.REDIS_URL,
                minsize=5,
                maxsize=10
            )
    
    async def get(self, key: str) -> Optional[str]:
        """Recupera valor do cache"""
        await self.init()
        return await self._redis.get(key)
    
    async def set(self, key: str, value: str, expire: int = 3600):
        """Armazena valor no cache"""
        await self.init()
        await self._redis.set(key, value, expire=expire)
    
    async def close(self):
        """Fecha conexão com Redis"""
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed() 