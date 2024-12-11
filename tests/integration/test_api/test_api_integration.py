import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def api_client():
    return TestClient(app)

def test_health_check_integration(api_client):
    """Teste de integração do health check"""
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint_integration(api_client, test_headers):
    """Teste de integração do endpoint raiz"""
    response = api_client.get("/api/v1/", headers=test_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "EMBASA API v0.1.0"}

def test_cors_headers_integration(api_client):
    """Teste de integração das configurações CORS"""
    response = api_client.options("/api/v1/", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
    })
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers 