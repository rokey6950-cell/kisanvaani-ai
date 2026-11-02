from typing import Optional, Dict, Any
from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    status: str = "success"  # success | error | pending_configuration
    transcript: str
    language: str = "hi-IN"
    duration_seconds: Optional[float] = None
    confidence: Optional[float] = None
    service_provider: str = "Gnani Prisma"
    model_version: str = "prisma-v2.5"
    message: Optional[str] = None

class TTSRequest(BaseModel):
    text: str
    language: str = "hi"
    voice_gender: str = "female"
    audio_format: str = "wav"

class TTSResponse(BaseModel):
    status: str = "success"  # success | fallback | error
    audio_url: Optional[str] = ""
    audio_base64: Optional[str] = None
    format: str = "audio/wav"
    duration_seconds: Optional[float] = None
    service_provider: str = "Gnani Timbre"
    model_version: str = "timbre-v2.5"
    message: Optional[str] = None

class VoiceStatusResponse(BaseModel):
    stt_provider: str
    stt_model: str
    stt_configured: bool
    tts_provider: str
    tts_model: str
    tts_configured: bool
    supported_audio_formats: list[str]
    supported_languages: list[Dict[str, str]]

