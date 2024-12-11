import pytest
from uuid import uuid4

from app.services.analysis import AnalysisService
from app.api.schemas.analysis import AnalysisRequest
from app.core.cache import RedisCache
from tests.mocks.redis_mock import RedisMock

@pytest.fixture
async def service_with_mock_cache():
    service = AnalysisService(cache=RedisMock())
    await service._cache.init()
    yield service
    await service._cache.close()

async def test_analysis_cache_integration(service_with_mock_cache):
    """Testa integração entre análise e cache Redis"""
    request = AnalysisRequest(content="Cache integration test")
    first_response = await service_with_mock_cache.process_analysis(request)
    
    content_hash = service_with_mock_cache._generate_hash(request.content)
    cached = await service_with_mock_cache.get_cached_result(content_hash)
    
    assert cached is not None
    assert cached.id == first_response.id

async def test_cache_persistence(service_with_mock_cache):
    """Testa persistência do cache entre instâncias"""
    # Criar análise na primeira instância
    request = AnalysisRequest(content="Persistence test")
    first_response = await service_with_mock_cache.process_analysis(request)
    
    # Criar nova instância do serviço
    new_service = AnalysisService()
    await new_service._cache.init()
    
    # Tentar recuperar do cache
    content_hash = new_service._generate_hash(request.content)
    cached = await new_service.get_cached_result(content_hash)
    
    assert cached is not None
    assert cached.id == first_response.id
    await new_service._cache.close() 