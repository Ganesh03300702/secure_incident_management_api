def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure(client):
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401

def test_protected_endpoint_requires_token(client):
    response = client.get("/api/v1/incidents")
    assert response.status_code == 401
