import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_history_flow():
    with TestClient(app) as client:
        # 1. Send chat message to create conversation
        chat_res = client.post(
            "/api/v1/assistant/chat",
            json={"message": "धान की फसल के बारे में जानकारी दें", "language": "hi"}
        )
        assert chat_res.status_code == 200
        conv_id = chat_res.json()["conversation_id"]

        # 2. Get history list
        hist_res = client.get("/api/v1/history")
        assert hist_res.status_code == 200
        conversations = hist_res.json()
        assert any(c["id"] == conv_id for c in conversations)

        # 3. Get single conversation details
        detail_res = client.get(f"/api/v1/history/{conv_id}")
        assert detail_res.status_code == 200
        messages = detail_res.json()["messages"]
        assert len(messages) >= 2  # user and assistant messages

        # 4. Delete single conversation
        del_res = client.delete(f"/api/v1/history/{conv_id}")
        assert del_res.status_code == 200
        assert del_res.json()["status"] == "success"

        # 5. Confirm it's gone
        get_deleted = client.get(f"/api/v1/history/{conv_id}")
        assert get_deleted.status_code == 404
