import io
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_voice_status_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/v1/voice/status")
        assert response.status_code == 200
        data = response.json()
        assert data["stt_provider"] == "Gnani Prisma"
        assert data["stt_model"] == "prisma-v2.5"
        assert data["tts_provider"] == "Gnani Timbre"
        assert data["tts_model"] == "timbre-v2.5"
        assert len(data["supported_audio_formats"]) > 0
        assert len(data["supported_languages"]) >= 2

def test_voice_transcribe_validation():
    with TestClient(app) as client:
        # 1. Invalid audio MIME type rejection
        bad_file = io.BytesIO(b"not an audio file at all" * 10)
        res_bad = client.post(
            "/api/v1/voice/transcribe",
            files={"audio": ("document.pdf", bad_file, "application/pdf")},
            data={"language": "hi"}
        )
        assert res_bad.status_code == 400
        assert "Unsupported audio format" in res_bad.json()["detail"]

        # 2. Too short audio rejection (< 100 bytes)
        tiny_audio = io.BytesIO(b"short")
        res_tiny = client.post(
            "/api/v1/voice/transcribe",
            files={"audio": ("click.wav", tiny_audio, "audio/wav")},
            data={"language": "hi"}
        )
        assert res_tiny.status_code == 400
        assert "too short or empty" in res_tiny.json()["detail"]

        # 3. Valid WebM audio with 'audio' field
        valid_audio = io.BytesIO(b"RIFF" + b"\x00" * 300)
        res_valid = client.post(
            "/api/v1/voice/transcribe",
            files={"audio": ("voice.webm", valid_audio, "audio/webm")},
            data={"language": "hi"}
        )
        assert res_valid.status_code == 200
        data_valid = res_valid.json()
        assert data_valid["status"] in ("success", "pending_configuration", "error")
        assert data_valid["model_version"] == "prisma-v2.5"

        # 4. Valid WAV audio with 'file' field (alternative parameter name)
        valid_wav = io.BytesIO(b"RIFF" + b"\x00" * 300)
        res_wav = client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("recording.wav", valid_wav, "audio/wav")},
            data={"language": "hi"}
        )
        assert res_wav.status_code == 200
        data_wav = res_wav.json()
        assert data_wav["status"] in ("success", "pending_configuration", "error")

def test_voice_speak_validation():
    with TestClient(app) as client:
        # 1. Empty text rejection
        res_empty = client.post(
            "/api/v1/voice/speak",
            json={"text": "   ", "language": "hi"}
        )
        assert res_empty.status_code == 400
        assert "cannot be empty" in res_empty.json()["detail"]

        # 2. Valid Hindi synthesis request
        res_valid = client.post(
            "/api/v1/voice/speak",
            json={"text": "किसान भाई, गेहूं की बुवाई 25 अक्टूबर से 15 नवंबर के बीच करें।", "language": "hi"}
        )
        assert res_valid.status_code == 200
        data_tts = res_valid.json()
        assert data_tts["status"] in ("success", "fallback")
        assert data_tts["model_version"] == "timbre-v2.5"
        assert data_tts["format"] == "audio/wav"

def test_end_to_end_voice_and_knowledge_pipeline():
    with TestClient(app) as client:
        # Step 1: Transcribe simulated voice recording
        audio_bytes = io.BytesIO(b"simulated audio packet content" * 15)
        trans_res = client.post(
            "/api/v1/voice/transcribe",
            files={"audio": ("farmer_question.webm", audio_bytes, "audio/webm")},
            data={"language": "hi"}
        )
        assert trans_res.status_code == 200

        # Step 2: Query AI Assistant with agricultural question
        query_text = "गेहूं की बुवाई का सही समय क्या है?"
        chat_res = client.post(
            "/api/v1/assistant/chat",
            json={"message": query_text, "language": "hi"}
        )
        assert chat_res.status_code == 200
        chat_data = chat_res.json()
        assert chat_data["conversation_id"] is not None
        answer_text = chat_data["answer"]
        assert len(answer_text) > 20
        assert len(chat_data["sources"]) > 0

        # Step 3: Synthesize AI Answer into Speech
        tts_res = client.post(
            "/api/v1/voice/speak",
            json={"text": answer_text, "language": "hi"}
        )
        assert tts_res.status_code == 200
        tts_data = tts_res.json()
        assert tts_data["model_version"] == "timbre-v2.5"

        # Step 4: Verify Conversation was persisted to history
        hist_res = client.get(f"/api/v1/history/{chat_data['conversation_id']}")
        assert hist_res.status_code == 200
        hist_data = hist_res.json()
        assert len(hist_data["messages"]) >= 2
        assert hist_data["messages"][0]["text"] == query_text
        assert hist_data["messages"][1]["text"] == chat_data["answer_hi"]

