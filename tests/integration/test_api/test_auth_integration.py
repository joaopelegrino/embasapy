import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def api_client():
    return TestClient(app)

def test_protected_endpoint_with_valid_key(api_client, test_headers):
    """Teste de integração com API Key válida"""
    response = api_client.get("/api/v1/", headers=test_headers)
    assert response.status_code == 200

def test_protected_endpoint_without_key(api_client):
    """Teste de integração sem API Key"""
    response = api_client.get("/api/v1/")
    assert response.status_code == 403
    assert "Could not validate API key" in response.json()["detail"]

@pytest.mark.parametrize("invalid_header", [
    {"X-API-Key": "invalid_key"},
    {"X-API-Key": ""},
    {"X-API-Key": " "},
    {},
])
def test_protected_endpoint_with_invalid_key(api_client, invalid_header):
    """Teste de integração com diferentes API Keys inválidas"""
    response = api_client.get("/api/v1/", headers=invalid_header)
    assert response.status_code == 403
    assert "Could not validate API key" in response.json()["detail"]

def test_unprotected_endpoint(api_client):
    """Teste de integração em endpoint não protegido"""
    response = api_client.get("/health")
    assert response.status_code == 200 