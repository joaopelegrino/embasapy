from typing import Optional, List
from uuid import UUID
from datetime import datetime
from hashlib import sha256
import json

from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisList
from app.core.cache import RedisCache
from app.core.config import settings

class AnalysisService:
    """Serviço para processamento de análises"""
    
    def __init__(self, cache: Optional[RedisCache] = None):
        self._analyses = {}
        self._cache = cache or RedisCache()
    
    def _generate_hash(self, content: str) -> str:
        return sha256(content.encode()).hexdigest()
    
    async def process_analysis(self, request: AnalysisRequest) -> AnalysisResponse:
        """Processa uma nova análise de forma assíncrona"""
        content_hash = self._generate_hash(request.content)
        
        # Verificar cache
        if cached := await self._cache.get(f"analysis:{content_hash}"):
            return AnalysisResponse(**json.loads(cached))
            
        # Criar nova análise
        analysis_id = str(uuid4())
        analysis = AnalysisResponse(
            id=analysis_id,
            status="processing",
            content=request.content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._analyses[analysis_id] = analysis
        await self._cache_result(content_hash, analysis)
        return analysis
    
    async def get_analysis_status(self, analysis_id: UUID) -> Optional[AnalysisResponse]:
        """Recupera o status de uma análise"""
        return self._analyses.get(str(analysis_id))
    
    async def get_cached_result(self, content_hash: str) -> Optional[AnalysisResponse]:
        """Recupera resultado do cache Redis"""
        if cached := await self._cache.get(f"analysis:{content_hash}"):
            return AnalysisResponse(**json.loads(cached))
        return None
    
    async def _cache_result(self, content_hash: str, analysis: AnalysisResponse):
        """Armazena resultado no cache Redis"""
        await self._cache.set(
            f"analysis:{content_hash}",
            json.dumps(analysis.dict()),
            expire=settings.REDIS_CACHE_TTL
        )
    
    async def list_recent_analyses(self, limit: int = 10) -> List[AnalysisResponse]:
        """Lista análises recentes"""
        analyses = list(self._analyses.values())
        analyses.sort(key=lambda x: x.created_at, reverse=True)
        return analyses[:limit]
