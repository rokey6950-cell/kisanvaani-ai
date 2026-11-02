"""
Tests for Phase 8 — End-to-End System Integration & Production Handover
Validates complete cross-system user journeys, schema consistency, and safety guardrails across all 8 phases.
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

def test_system_health_and_subsystems():
    """Verify backend, SQLite database, and Knowledge Base subsystems are healthy and loaded."""
    with TestClient(app) as client:
        res = client.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["database_connected"] is True
        assert data["knowledge_base_loaded"] is True
        assert data["records_count"] >= 100

def test_full_assistant_grounded_conversation_flow():
    """Verify conversational Q&A grounding, context maintenance, and safety guardrails."""
    with TestClient(app) as client:
        # Step 1: Ask about wheat sowing time
        res1 = client.post("/api/v1/assistant/chat", json={
            "message": "गेहूं की बुवाई का सही समय क्या है?",
            "language": "hi"
        })
        assert res1.status_code == 200
        data1 = res1.json()
        assert data1["confidence"] > 0
        assert data1["verification_status"] in ["verified", "pending_review"]
        assert len(data1["sources"]) > 0
        conv_id = data1.get("conversation_id")
        assert conv_id is not None

        # Step 2: Follow-up question referencing the previous crop context
        res2 = client.post("/api/v1/assistant/chat", json={
            "message": "इसमें सिंचाई कब करनी चाहिए?",
            "language": "hi",
            "conversation_id": conv_id
        })
        assert res2.status_code == 200
        data2 = res2.json()
        assert data2["confidence"] > 0
        assert "CRI" in data2["answer"] or "सिंचाई" in data2["answer"] or "दिन" in data2["answer"]

def test_crop_to_mandi_to_weather_cross_journey():
    """Verify cross-module consistency for a farmer exploring wheat farming in Karnal, Haryana."""
    with TestClient(app) as client:
        # 1. Sowing recommendation via POST /crop-advisory/recommendation
        rec_res = client.post("/api/v1/crop-advisory/recommendation", json={
            "crop": "wheat",
            "state": "Haryana",
            "topic": "sowing"
        })
        assert rec_res.status_code == 200
        rec_data = rec_res.json()
        assert "wheat" in rec_data["crop"].lower() or "गेहूं" in rec_data["crop"]
        assert rec_data["kvk_referral"]["toll_free"] == "1800-180-1551"

        # 2. Mandi price benchmark check
        mandi_res = client.get("/api/v1/mandi-prices?crop=wheat&state=Haryana")
        assert mandi_res.status_code == 200
        mandi_data = mandi_res.json()
        assert mandi_data["data_type"] == "sample"
        assert len(mandi_data["prices"]) > 0
        assert mandi_data["prices"][0]["commodity"].lower() == "wheat"

        # 3. Weather check for Karnal
        weather_res = client.get("/api/v1/weather?location=Karnal")
        assert weather_res.status_code == 200
        weather_data = weather_res.json()
        assert weather_data["data_type"] == "sample"
        assert weather_data["location"] == "Karnal"
        assert len(weather_data["forecast"]) == 5
        assert weather_data["spray_advisory"]["status"] in ["good", "caution", "danger"]

def test_voice_subsystem_readiness_and_contracts():
    """Verify Voice STT and TTS API contract compliance and graceful handling of missing credentials."""
    with TestClient(app) as client:
        status_res = client.get("/api/v1/voice/status")
        assert status_res.status_code == 200
        status_data = status_res.json()
        assert "Gnani" in status_data["stt_provider"]
        assert "Gnani" in status_data["tts_provider"]
        assert len(status_data["supported_languages"]) > 0

        # Speak endpoint contract
        speak_res = client.post("/api/v1/voice/speak", json={
            "text": "किसान भाइयों को नमस्कार",
            "language": "hi"
        })
        assert speak_res.status_code == 200
        speak_data = speak_res.json()
        assert "status" in speak_data

def test_schemes_navigation_and_helpline_integrity():
    """Verify schemes catalog integrity, official links, and national helplines."""
    with TestClient(app) as client:
        # Search for PM-KISAN
        search_res = client.get("/api/v1/schemes/search?q=kisan")
        assert search_res.status_code == 200
        data = search_res.json()
        assert "schemes" in data
        schemes = data["schemes"]
        assert len(schemes) > 0
        pm_kisan = next((s for s in schemes if s["scheme_id"] == "pm-kisan"), None)
        assert pm_kisan is not None
        assert "155261" in str(pm_kisan["helpline"])
        assert "pmkisan.gov.in" in pm_kisan["official_portal"]

def test_conversation_history_crud_lifecycle():
    """Verify full conversation persistence, retrieval, and deletion flow."""
    with TestClient(app) as client:
        # 1. Ask a question to create a conversation
        chat_res = client.post("/api/v1/assistant/chat", json={
            "message": "मिट्टी की जांच कैसे करें?",
            "language": "hi"
        })
        assert chat_res.status_code == 200
        conv_id = chat_res.json()["conversation_id"]

        # 2. Retrieve history list
        hist_res = client.get("/api/v1/history")
        assert hist_res.status_code == 200
        conversations = hist_res.json()
        assert any(c["id"] == conv_id for c in conversations)

        # 3. Retrieve single conversation details
        detail_res = client.get(f"/api/v1/history/{conv_id}")
        assert detail_res.status_code == 200
        detail_data = detail_res.json()
        assert detail_data["id"] == conv_id
        assert len(detail_data["messages"]) >= 2

        # 4. Delete the conversation
        del_res = client.delete(f"/api/v1/history/{conv_id}")
        assert del_res.status_code == 200

        # 5. Verify deleted
        detail_after_res = client.get(f"/api/v1/history/{conv_id}")
        assert detail_after_res.status_code == 404
