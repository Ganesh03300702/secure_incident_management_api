import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

@pytest.fixture
def client():
    init_db()
    return TestClient(app)

@pytest.fixture
def headers():
    return {"Authorization": "Bearer demo-cisco-project-token"}
