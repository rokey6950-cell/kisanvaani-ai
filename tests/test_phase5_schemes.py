import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_schemes_listing_and_counts():
    with TestClient(app) as client:
        res = client.get("/api/v1/schemes")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 6
        scheme_ids = [s["scheme_id"] for s in data["schemes"]]
        assert "pm-kisan" in scheme_ids
        assert "pmfby" in scheme_ids
        assert "pmksy" in scheme_ids
        assert "soil-health-card" in scheme_ids
        assert "agri-mechanization" in scheme_ids
        assert "mkisan" in scheme_ids

def test_pm_kisan_details():
    with TestClient(app) as client:
        res = client.get("/api/v1/schemes/pm-kisan")
        assert res.status_code == 200
        data = res.json()
        assert data["scheme_id"] == "pm-kisan"
        assert "6,000" in str(data["benefits"]) or "6000" in str(data["benefits"])
        assert "pmkisan.gov.in" in data["official_portal"]
        assert len(data["required_documents"]) >= 3
        assert len(data["exclusion_criteria"]) >= 3
        assert data["verification_status"] == "verified"
        assert "155261" in str(data["helpline"])

def test_pmfby_crop_insurance_details():
    with TestClient(app) as client:
        res = client.get("/api/v1/schemes/pmfby")
        assert res.status_code == 200
        data = res.json()
        assert data["scheme_id"] == "pmfby"
        assert "pmfby.gov.in" in data["official_portal"]
        assert "14447" in str(data["helpline"])
        assert "2%" in str(data["benefits"]) or "1.5%" in str(data["benefits"])

def test_schemes_category_filter():
    with TestClient(app) as client:
        res = client.get("/api/v1/schemes?category=crop_insurance")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 1
        assert data["schemes"][0]["scheme_id"] == "pmfby"

def test_schemes_search_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/schemes/search?q=सिंचाई")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] >= 1
        matched_ids = [s["scheme_id"] for s in data["schemes"]]
        assert "pmksy" in matched_ids

def test_schemes_invalid_id_404():
    with TestClient(app) as client:
        res = client.get("/api/v1/schemes/fake-non-existent-scheme")
        assert res.status_code == 404
        assert "not found" in res.json()["detail"].lower()

