import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_list_schemes():
    with TestClient(app) as client:
        response = client.get("/api/v1/schemes")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 5
        assert len(data["schemes"]) >= 5
        first_scheme = data["schemes"][0]
        assert "scheme_id" in first_scheme
        assert "name" in first_scheme
        assert first_scheme["data_type"] in ("official_static", "sample", "unverified")

def test_get_scheme_by_id():
    with TestClient(app) as client:
        response = client.get("/api/v1/schemes/pm-kisan")
        assert response.status_code == 200
        data = response.json()
        assert data["scheme_id"] == "pm-kisan"
        assert "sources" in data

def test_get_invalid_scheme():
    with TestClient(app) as client:
        response = client.get("/api/v1/schemes/non-existent-scheme")
        assert response.status_code == 404
