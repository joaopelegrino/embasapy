import pytest
from uuid import UUID

from app.api.handlers.analysis import AnalysisHandler
from app.api.schemas.analysis import AnalysisRequest

@pytest.fixture
def handler():
    return AnalysisHandler()

async def test_create_analysis(handler):
    request = AnalysisRequest(content="Test content")
    response = await handler.create_analysis(request)
    assert response is not None
    assert response.id is not None
    assert response.status == "pending"

async def test_get_analysis(handler):
    # Primeiro criar uma análise
    request = AnalysisRequest(content="Test content")
    created = await handler.create_analysis(request)
    
    # Depois recuperar
    response = await handler.get_analysis(created.id)
    assert response is not None
    assert response.id == created.id
    assert response.content == request.content

async def test_list_analyses(handler):
    # Criar algumas análises
    for i in range(3):
        request = AnalysisRequest(content=f"Test content {i}")
        await handler.create_analysis(request)
    
    # Listar com paginação
    response = await handler.list_analyses(page=1, size=2)
    assert response.total >= 3
    assert len(response.items) == 2
    assert response.page == 1
    assert response.size == 2

async def test_get_analysis_not_found(handler):
    response = await handler.get_analysis(UUID('00000000-0000-0000-0000-000000000000'))
    assert response is None
