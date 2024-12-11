from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient, test_headers):
    response = client.get("/api/v1/", headers=test_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "EMBASA API v0.1.0"}

def test_root_endpoint_without_api_key(client: TestClient):
    response = client.get("/api/v1/")
    assert response.status_code == 403
    assert "Could not validate API key" in response.json()["detail"] 