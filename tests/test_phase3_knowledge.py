import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_seeds_endpoint():
    with TestClient(app) as client:
        # 1. All seeds
        res = client.get("/api/v1/knowledge/seeds")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] >= 4
        varieties = [v["variety"] for v in data["varieties"]]
        assert any("WH" in v or "HD" in v for v in varieties)

        # 2. Filtered by wheat
        res_wheat = client.get("/api/v1/knowledge/seeds?crop=wheat")
        assert res_wheat.status_code == 200
        data_wheat = res_wheat.json()
        assert data_wheat["total"] >= 4
        for v in data_wheat["varieties"]:
            assert v["crop_id"].lower() == "wheat"

def test_glossary_endpoint():
    with TestClient(app) as client:
        # 1. All terms
        res = client.get("/api/v1/knowledge/glossary")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] >= 8

        # 2. Filtered term
        res_filtered = client.get("/api/v1/knowledge/glossary?q=बुवाई")
        assert res_filtered.status_code == 200
        terms = res_filtered.json()["terms"]
        assert len(terms) >= 1
        assert "बुवाई" in terms[0]["term"]["hi"]

def test_agro_zones_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/knowledge/zones")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] >= 3

def test_multiturn_crop_context_resolution():
    with TestClient(app) as client:
        # Turn 1: Farmer mentions wheat
        turn1 = client.post(
            "/api/v1/assistant/chat",
            json={"message": "गेहूं की बुवाई कब करें?", "language": "hi"}
        )
        assert turn1.status_code == 200
        conv_id = turn1.json()["conversation_id"]

        # Turn 2: Follow-up question using anaphoric reference ("इसके लिए कौन से बीज अच्छे हैं?")
        turn2 = client.post(
            "/api/v1/assistant/chat",
            json={
                "message": "इसके लिए कौन से बीज अच्छे हैं?",
                "conversation_id": conv_id,
                "language": "hi"
            }
        )
        assert turn2.status_code == 200
        turn2_data = turn2.json()
        assert turn2_data["conversation_id"] == conv_id
        # Engine should match on seed varieties or wheat crop guidance
        ans = turn2_data["answer_hi"]
        assert len(ans) > 20
        assert turn2_data["confidence"] >= 0.8
        assert len(turn2_data["sources"]) > 0

def test_scheme_query_in_chat():
    with TestClient(app) as client:
        res = client.post(
            "/api/v1/assistant/chat",
            json={"message": "PM-KISAN योजना की जानकारी और लाभ बताएं", "language": "hi"}
        )
        assert res.status_code == 200
        data = res.json()
        assert "योजना" in data["answer_hi"] or "किसान" in data["answer_hi"]
        assert len(data["sources"]) > 0

