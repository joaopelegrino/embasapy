from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_api_key
from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisList

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    api_key: str = Depends(get_api_key)
):
    """Cria uma nova análise"""
    pass

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    api_key: str = Depends(get_api_key)
):
    """Recupera uma análise específica"""
    pass

@router.get("/", response_model=AnalysisList)
async def list_analyses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    api_key: str = Depends(get_api_key)
):
    """Lista análises paginadas"""
    pass 