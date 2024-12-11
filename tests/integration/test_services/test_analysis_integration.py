import pytest
from uuid import uuid4

from app.services.analysis import AnalysisService
from app.api.schemas.analysis import AnalysisRequest
from app.api.handlers.analysis import AnalysisHandler
from app.config import settings

@pytest.fixture
async def service():
    return AnalysisService()

@pytest.fixture
async def handler():
    return AnalysisHandler()

async def test_service_handler_integration(service, handler):
    """Testa integração entre service e handler"""
    # Criar análise via handler
    request = AnalysisRequest(content="Integration test")
    handler_response = await handler.create_analysis(request)
    
    # Verificar no service
    service_response = await service.get_analysis_status(handler_response.id)
    assert service_response is not None
    assert service_response.content == request.content

async def test_cache_integration(service):
    """Testa integração com cache"""
    # Primeira requisição
    request = AnalysisRequest(content="Cache test")
    first_response = await service.process_analysis(request)
    
    # Segunda requisição (deve vir do cache)
    content_hash = service._generate_hash(request.content)
    cached_response = await service.get_cached_result(content_hash)
    
    assert cached_response is not None
    assert cached_response.id == first_response.id
    assert cached_response.content == request.content

async def test_list_integration(service):
    """Testa integração da listagem"""
    # Criar várias análises
    analyses = []
    for i in range(5):
        request = AnalysisRequest(content=f"List test {i}")
        response = await service.process_analysis(request)
        analyses.append(response)
    
    # Verificar listagem
    recent = await service.list_recent_analyses(limit=3)
    assert len(recent) == 3
    assert recent[0].created_at >= recent[1].created_at >= recent[2].created_at

async def test_cache_disabled(service_with_mock_cache, monkeypatch):
    """Testa processamento com cache desabilitado"""
    monkeypatch.setattr(settings, "CACHE_ENABLED", False)
    
    request = AnalysisRequest(content="No cache test")
    response = await service_with_mock_cache.process_analysis(request)
    
    content_hash = service_with_mock_cache._generate_hash(request.content)
    cached = await service_with_mock_cache.get_cached_result(content_hash)
    assert cached is None
