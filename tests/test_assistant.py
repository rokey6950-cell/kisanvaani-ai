import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_chat_grounded_answer():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/assistant/chat",
            json={"message": "गेहूं की बुवाई का सही समय क्या है?", "language": "hi"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] is not None
        assert "हरियाणा" in data["answer_hi"] or "बुवाई" in data["answer_hi"]
        assert len(data["sources"]) > 0
        assert data["confidence"] > 0.8
        assert data["data_type"] in ("official_static", "sample", "unverified")

def test_chat_unverified_fallback():
    with TestClient(app) as client:
        # A question with no match in the KB
        response = client.post(
            "/api/v1/assistant/chat",
            json={"message": "मंगल ग्रह पर रॉकेट कैसे बनाएं?", "language": "hi"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verification_status"] in ("unverified", "ai_generated")
        assert "सत्यापित नहीं है" in data["answer_hi"] or "KVK" in data["answer_hi"] or "किसान" in data["answer_hi"]

def test_chat_empty_message_validation():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/assistant/chat",
            json={"message": "   ", "language": "hi"}
        )
        assert response.status_code == 400

