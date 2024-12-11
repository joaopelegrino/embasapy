import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.core.config import settings

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def headers():
    return {"X-API-KEY": settings.API_KEY}

def test_create_analysis(client, headers):
    """Testa criação de análise via API"""
    request = {"content": "Test content"}
    response = client.post("/analysis/", json=request, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == request["content"]
    assert data["status"] == "processing"

def test_create_analysis_unauthorized(client):
    """Testa criação sem API key"""
    request = {"content": "Test content"}
    response = client.post("/analysis/", json=request)
    assert response.status_code == 403

def test_get_analysis(client, headers):
    """Testa recuperação de análise via API"""
    # Primeiro criar uma análise
    request = {"content": "Test content"}
    create_response = client.post("/analysis/", json=request, headers=headers)
    analysis_id = create_response.json()["id"]
    
    # Depois recuperar
    response = client.get(f"/analysis/{analysis_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == analysis_id

def test_list_analyses(client, headers):
    """Testa listagem de análises via API"""
    # Criar algumas análises
    for i in range(3):
        request = {"content": f"Test content {i}"}
        client.post("/analysis/", json=request, headers=headers)
    
    # Listar com paginação
    response = client.get("/analysis/?page=1&size=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] >= 3

def test_get_analysis_not_found(client, headers):
    """Testa recuperação de análise inexistente"""
    response = client.get(
        f"/analysis/{uuid4()}", 
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis not found"

def test_list_analyses_unauthorized(client):
    """Testa listagem sem autenticação"""
    response = client.get("/analysis/")
    assert response.status_code == 403

def test_create_analysis_content_too_large(client, headers):
    """Testa criação com conteúdo muito grande"""
    request = {"content": "x" * 5001}  # Conteúdo maior que 5000 caracteres
    response = client.post("/analysis/", json=request, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Content too large"

def test_root_endpoint(client):
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "EMBASA API"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"
    assert data["env"] == "test"

def test_invalid_api_key(client):
    """Testa autenticação com chave inválida"""
    headers = {"X-API-Key": "invalid_key"}
    response = client.get("/analysis/", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate API key"