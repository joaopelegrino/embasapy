from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    content: str = Field(..., description="Conteúdo para análise")
    context: Optional[str] = Field(None, description="Contexto adicional")
    options: Optional[dict] = Field(default_factory=dict, description="Opções de análise")

class AnalysisResponse(BaseModel):
    id: str = Field(..., description="ID único da análise")
    status: str = Field(..., description="Status da análise")
    result: Optional[dict] = Field(None, description="Resultado da análise")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AnalysisList(BaseModel):
    items: List[AnalysisResponse]
    total: int
    page: int
    size: int 