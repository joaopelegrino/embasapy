from typing import Optional, List
from uuid import UUID
from datetime import datetime
from hashlib import sha256

from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisList

class AnalysisService:
    """Serviço para processamento de análises"""
    
    def __init__(self):
        self._analyses = {}
        self._cache = {}
    
    def _generate_hash(self, content: str) -> str:
        return sha256(content.encode()).hexdigest()
    
    async def process_analysis(self, request: AnalysisRequest) -> AnalysisResponse:
        """Processa uma nova análise de forma assíncrona"""
        content_hash = self._generate_hash(request.content)
        
        # Verificar cache
        if cached := self._cache.get(content_hash):
            return cached
            
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
        self._cache[content_hash] = analysis
        return analysis
    
    async def get_analysis_status(self, analysis_id: UUID) -> Optional[AnalysisResponse]:
        """Recupera o status de uma análise"""
        return self._analyses.get(str(analysis_id))
    
    async def get_cached_result(self, content_hash: str) -> Optional[AnalysisResponse]:
        """Recupera resultado do cache se disponível"""
        return self._cache.get(content_hash)
    
    async def list_recent_analyses(self, limit: int = 10) -> List[AnalysisResponse]:
        """Lista análises recentes"""
        analyses = list(self._analyses.values())
        analyses.sort(key=lambda x: x.created_at, reverse=True)
        return analyses[:limit]
