from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisList
from app.api.handlers.analysis import AnalysisHandler
from app.services.analysis import AnalysisService
from app.api.deps import get_analysis_service

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service)
):
    """Cria uma nova análise"""
    handler = AnalysisHandler(service=service)
    return await handler.create_analysis(request)

@router.get("/{analysis_id}", response_model=Optional[AnalysisResponse])
async def get_analysis(
    analysis_id: UUID,
    service: AnalysisService = Depends(get_analysis_service)
):
    """Recupera uma análise específica"""
    handler = AnalysisHandler(service=service)
    if result := await handler.get_analysis(analysis_id):
        return result
    raise HTTPException(status_code=404, detail="Analysis not found")

@router.get("/", response_model=AnalysisList)
async def list_analyses(
    page: int = 1,
    size: int = 10,
    service: AnalysisService = Depends(get_analysis_service)
):
    """Lista análises paginadas"""
    handler = AnalysisHandler(service=service)
    return await handler.list_analyses(page=page, size=size) 