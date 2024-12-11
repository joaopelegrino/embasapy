import pytest
from uuid import uuid4

from app.services.analysis import AnalysisService
from app.api.schemas.analysis import AnalysisRequest

@pytest.fixture
def service():
    return AnalysisService()

async def test_process_analysis(service):
    request = AnalysisRequest(content="Test content")
    response = await service.process_analysis(request)
    assert response is not None
    assert response.id is not None
    assert response.status == "processing"

async def test_get_analysis_status(service):
    # Criar análise primeiro
    request = AnalysisRequest(content="Test content")
    created = await service.process_analysis(request)
    
    # Verificar status
    status = await service.get_analysis_status(created.id)
    assert status is not None
    assert status.id == created.id
    assert status.status in ["processing", "completed"]

async def test_get_cached_result(service):
    # Processar primeira análise
    request = AnalysisRequest(content="Test content")
    first = await service.process_analysis(request)
    
    # Tentar recuperar do cache
    cached = await service.get_cached_result("test_content_hash")
    assert cached is not None
    assert cached.content == request.content

async def test_list_recent_analyses(service):
    # Criar múltiplas análises
    for i in range(3):
        request = AnalysisRequest(content=f"Test content {i}")
        await service.process_analysis(request)
    
    # Listar recentes
    recent = await service.list_recent_analyses(limit=2)
    assert len(recent) == 2
