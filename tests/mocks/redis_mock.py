from typing import Dict, Optional

class RedisMock:
    """Mock do Redis para testes"""
    
    def __init__(self):
        self._data: Dict[str, str] = {}
    
    async def init(self):
        """Simula inicialização"""
        pass
    
    async def get(self, key: str) -> Optional[str]:
        """Simula get do Redis"""
        return self._data.get(key)
    
    async def set(self, key: str, value: str, expire: int = None):
        """Simula set do Redis"""
        self._data[key] = value
    
    async def close(self):
        """Simula fechamento da conexão"""
        self._data.clear() 