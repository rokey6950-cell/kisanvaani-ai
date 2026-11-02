import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_mandi_prices_returns_sample_flag_and_disclaimer():
    with TestClient(app) as client:
        res = client.get("/api/v1/mandi-prices")
        assert res.status_code == 200
        data = res.json()
        assert data["data_type"] == "sample"
        assert data["api_available"] is False
        assert data["official_portal"] == "https://agmarknet.gov.in"
        assert "unconfirmed" in data["message"].lower() or "अनुपलब्ध" in data.get("disclaimer", "")
        assert len(data["prices"]) >= 5

def test_mandi_prices_state_filtering():
    with TestClient(app) as client:
        # Punjab mandis (Khanna, Amritsar)
        res_punjab = client.get("/api/v1/mandi-prices?state=Punjab")
        assert res_punjab.status_code == 200
        data_punjab = res_punjab.json()
        assert data_punjab["total"] >= 2
        for p in data_punjab["prices"]:
            assert p["state"] == "Punjab"

        # Haryana mandis (Karnal, Hisar, etc.)
        res_haryana = client.get("/api/v1/mandi-prices?state=Haryana")
        assert res_haryana.status_code == 200
        data_haryana = res_haryana.json()
        assert data_haryana["total"] >= 3
        for p in data_haryana["prices"]:
            assert p["state"] == "Haryana"

def test_mandi_prices_crop_filtering():
    with TestClient(app) as client:
        res_wheat = client.get("/api/v1/mandi-prices?crop=Wheat")
        assert res_wheat.status_code == 200
        data_wheat = res_wheat.json()
        assert data_wheat["total"] >= 2
        for p in data_wheat["prices"]:
            assert "wheat" in p["commodity"].lower() or "गेहूं" in p["commodity_hi"]

def test_mandi_markets_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/mandi-prices/markets")
        assert res.status_code == 200
        data = res.json()
        assert data["total_markets"] >= 8
        assert "Punjab" in data["states"] or "Haryana" in data["states"]

def test_mandi_commodities_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/mandi-prices/commodities")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] >= 6
        crop_ids = [c["crop_id"] for c in data["commodities"]]
        assert "wheat" in crop_ids
        assert "mustard" in crop_ids

def test_mandi_status_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/mandi-prices/status")
        assert res.status_code == 200
        data = res.json()
        assert data["api_available"] is False
        assert data["status"] == "blocked_unconfirmed"
        assert "fake live prices" in data["compliance"].lower()

