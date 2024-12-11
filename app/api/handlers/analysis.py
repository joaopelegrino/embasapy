from typing import Dict, Optional
from uuid import UUID
from datetime import datetime

from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisList
from app.services.analysis import AnalysisService

class AnalysisHandler:
    """Handler para processamento de análises"""
    
    def __init__(self, service: Optional[AnalysisService] = None):
        self._service = service or AnalysisService()
    
    async def create_analysis(self, request: AnalysisRequest) -> AnalysisResponse:
        """Cria uma nova análise"""
        return await self._service.process_analysis(request)
    
    async def get_analysis(self, analysis_id: UUID) -> Optional[AnalysisResponse]:
        """Recupera uma análise específica"""
        return await self._service.get_analysis_status(analysis_id)
    
    async def list_analyses(self, page: int, size: int) -> AnalysisList:
        """Lista análises paginadas"""
        items = await self._service.list_recent_analyses(limit=size)
        return AnalysisList(
            items=items,
            total=len(items),
            page=page,
            size=size
        )
