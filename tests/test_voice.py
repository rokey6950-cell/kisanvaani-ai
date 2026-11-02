import io
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_voice_speak_missing_api_key_reporting():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/voice/speak",
            json={"text": "नमस्ते किसान भाई", "language": "hi"}
        )
        # Without Gnani API key, it should return 503 or clear honest error
        assert response.status_code in (200, 503)
        data = response.json()
        if response.status_code == 503:
            assert "GNANI_API_KEY" in data.get("detail", "") or "API key" in data.get("detail", "")
        else:
            # If stub returns 200 mock message, it must declare status
            assert "status" in data or "audio_url" in data

def test_voice_transcribe_missing_key_or_empty_audio():
    with TestClient(app) as client:
        # Pass >= 100 bytes so it passes the minimum length validation
        audio_content = b"fake audio content bytes " * 10
        response = client.post(
            "/api/v1/voice/transcribe",
            files={"audio": ("sample.webm", io.BytesIO(audio_content), "audio/webm")},
            data={"language": "hi"}
        )
        assert response.status_code in (200, 503)
        data = response.json()
        assert "transcript" in data
        assert "service_provider" in data
