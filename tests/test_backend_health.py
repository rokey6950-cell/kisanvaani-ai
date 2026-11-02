import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.knowledge_retrieval import knowledge_service

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "KisanVaani AI" in data["message"]
    assert "health_check" in data

def test_health_endpoint():
    # Ensure knowledge is loaded
    knowledge_service.load_knowledge_base()

    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert data["knowledge_base_loaded"] is True
    assert data["records_count"] > 0
    assert "timestamp" in data

