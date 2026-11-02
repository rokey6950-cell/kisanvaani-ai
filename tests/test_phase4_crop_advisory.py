import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_crop_advisory_districts():
    with TestClient(app) as client:
        # Haryana districts
        res_haryana = client.get("/api/v1/crop-advisory/districts?state=Haryana")
        assert res_haryana.status_code == 200
        data_haryana = res_haryana.json()
        assert data_haryana["total"] >= 5
        assert "Karnal" in data_haryana["districts"] or "करनाल" in data_haryana["districts"]

        # Punjab districts
        res_punjab = client.get("/api/v1/crop-advisory/districts?state=Punjab")
        assert res_punjab.status_code == 200
        data_punjab = res_punjab.json()
        assert "Ludhiana" in data_punjab["districts"] or "लुधियाना" in data_punjab["districts"]

def test_crop_advisory_topics():
    with TestClient(app) as client:
        res = client.get("/api/v1/crop-advisory/topics")
        assert res.status_code == 200
        topics = res.json()["topics"]
        assert len(topics) >= 5
        topic_ids = [t["id"] for t in topics]
        assert "sowing" in topic_ids
        assert "pest_disease" in topic_ids
        assert "irrigation" in topic_ids

def test_wheat_haryana_sowing_recommendation():
    with TestClient(app) as client:
        res = client.post(
            "/api/v1/crop-advisory/recommendation",
            json={
                "crop": "गेहूं",
                "state": "हरियाणा",
                "district": "करनाल",
                "season": "रबी",
                "topic": "sowing"
            }
        )
        assert res.status_code == 200
        data = res.json()
        assert "25 अक्टूबर" in data["advisory_hi"] or "15 नवंबर" in data["advisory_hi"]
        assert data["verification_status"] == "verified"
        assert len(data["sources"]) > 0
        assert data["kvk_referral"]["toll_free"] == "1800-180-1551"

def test_crop_seed_varieties_recommendation():
    with TestClient(app) as client:
        res = client.post(
            "/api/v1/crop-advisory/recommendation",
            json={
                "crop": "गेहूं",
                "state": "हरियाणा",
                "topic": "seed_varieties"
            }
        )
        assert res.status_code == 200
        data = res.json()
        assert "WH 1309" in data["advisory_hi"] or "HD" in data["advisory_hi"]
        assert data["safety_disclaimer"] is not None

def test_crop_ipm_pest_safety_guidance():
    with TestClient(app) as client:
        res = client.post(
            "/api/v1/crop-advisory/recommendation",
            json={
                "crop": "सरसों",
                "state": "राजस्थान",
                "topic": "pest_disease"
            }
        )
        assert res.status_code == 200
        data = res.json()
        # Must enforce farmer safety rule against guessing pesticide doses
        assert "बिना पहचान" in data["advisory_hi"] or "KVK" in data["advisory_hi"] or "जैविक" in data["advisory_hi"]
        assert "सुरक्षा" in data["safety_disclaimer"]
        assert data["kvk_referral"]["toll_free"] == "1800-180-1551"

def test_crop_advisory_empty_crop_validation():
    with TestClient(app) as client:
        res = client.post(
            "/api/v1/crop-advisory/recommendation",
            json={"crop": "   "}
        )
        assert res.status_code == 400

