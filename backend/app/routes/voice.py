from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from ..schemas.voice import TranscriptionResponse, TTSRequest, TTSResponse, VoiceStatusResponse
from ..services.voice_service import voice_service, SUPPORTED_AUDIO_MIMES, SUPPORTED_LANGUAGES
from ..core.config import settings

router = APIRouter(prefix="/voice", tags=["AI Voice Processing"])

@router.get("/status", response_model=VoiceStatusResponse)
def get_voice_engine_status():
    """
    Returns the real-time configuration status of Gnani Prisma v2.5 STT
    and Gnani Timbre v2.5 TTS engines.
    """
    is_cfg = voice_service.is_configured()
    return VoiceStatusResponse(
        stt_provider="Gnani Prisma",
        stt_model=settings.GNANI_STT_MODEL,
        stt_configured=is_cfg,
        tts_provider="Gnani Timbre",
        tts_model=settings.GNANI_TTS_MODEL,
        tts_configured=is_cfg,
        supported_audio_formats=SUPPORTED_AUDIO_MIMES,
        supported_languages=SUPPORTED_LANGUAGES
    )

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: Optional[UploadFile] = File(None, description="Audio file from browser (named 'file')"),
    audio: Optional[UploadFile] = File(None, description="Audio file from browser (named 'audio')"),
    language: str = Form("hi", description="Language code (e.g. hi, hi-IN, haryanvi-accent)")
):
    """
    Receives voice audio from farmer, validates format and length,
    and forwards to Gnani Prisma STT (or returns honest status if API key pending).
    """
    upload = audio or file
    if not upload:
        raise HTTPException(
            status_code=400,
            detail="No audio file provided. Please send file in 'audio' or 'file' form-data field."
        )

    audio_bytes = await upload.read()
    valid, err_msg = voice_service.validate_audio(upload.content_type, len(audio_bytes))
    if not valid:
        raise HTTPException(status_code=400, detail=err_msg)

    result = await voice_service.transcribe_audio(
        audio_bytes=audio_bytes,
        content_type=upload.content_type or "audio/webm",
        language=language
    )

    return TranscriptionResponse(
        status=result.get("status", "success"),
        transcript=result.get("transcript", ""),
        language=result.get("language", "hi-IN"),
        duration_seconds=result.get("duration_seconds"),
        confidence=result.get("confidence"),
        service_provider=result.get("service_provider", "Gnani Prisma"),
        model_version=result.get("model_version", settings.GNANI_STT_MODEL),
        message=result.get("message")
    )

@router.post("/speak", response_model=TTSResponse)
async def synthesize_speech(req: TTSRequest):
    """
    Synthesizes farmer response text into Hindi speech via Gnani Timbre TTS.
    Falls back gracefully to browser SpeechSynthesis when Gnani credentials are not set.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text for speech synthesis cannot be empty.")

    result = await voice_service.synthesize_speech(
        text=req.text,
        language=req.language,
        voice_gender=req.voice_gender
    )

    return TTSResponse(
        status=result.get("status", "success"),
        audio_url=result.get("audio_url", ""),
        audio_base64=result.get("audio_base64"),
        format=result.get("format", "audio/wav"),
        duration_seconds=result.get("duration_seconds"),
        service_provider=result.get("service_provider", "Gnani Timbre"),
        model_version=result.get("model_version", settings.GNANI_TTS_MODEL),
        message=result.get("message")
    )
