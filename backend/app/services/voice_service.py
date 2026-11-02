import base64
import logging
from typing import Dict, Any, Optional, Tuple
import httpx

from ..core.config import settings

logger = logging.getLogger("kisanvaani.voice")

SUPPORTED_AUDIO_MIMES = [
    "audio/webm",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "audio/mp4",
    "audio/mpeg",
    "audio/aac",
    "video/webm",
]

SUPPORTED_LANGUAGES = [
    {"code": "hi", "name": "Hindi", "gnani_code": "hi-IN"},
    {"code": "hi-haryanvi", "name": "Hindi (Haryanvi Accent)", "gnani_code": "hi-IN"},
    {"code": "en", "name": "English (Indian)", "gnani_code": "en-IN"},
]

class VoiceService:
    """
    Manages speech-to-text (Gnani Prisma v2.5) and text-to-speech (Gnani Timbre v2.5).
    Enforces honest limitation reporting: when API keys are not supplied,
    it returns clear status messages rather than pretending an external call succeeded.
    """

    def __init__(self):
        self.stt_endpoint = settings.GNANI_STT_ENDPOINT
        self.tts_endpoint = settings.GNANI_TTS_ENDPOINT
        self.stt_model = settings.GNANI_STT_MODEL
        self.tts_model = settings.GNANI_TTS_MODEL

    @property
    def api_key(self) -> str:
        return settings.GNANI_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def validate_audio(self, content_type: Optional[str], size_bytes: int) -> Tuple[bool, Optional[str]]:
        """Validates that uploaded audio meets MIME and size constraints."""
        if not content_type:
            return False, "Audio content-type is missing."
        
        # Check against supported mime types
        is_supported = any(content_type.startswith(mime) for mime in SUPPORTED_AUDIO_MIMES)
        if not is_supported:
            return False, f"Unsupported audio format '{content_type}'. Must be audio/webm, audio/wav, or audio/ogg."

        if size_bytes < 100:
            return False, "Audio recording is too short or empty (less than 100 bytes)."

        if size_bytes > 15 * 1024 * 1024:
            return False, "Audio file exceeds maximum size limit of 15MB."

        return True, None

    def estimate_duration_seconds(self, size_bytes: int, content_type: Optional[str]) -> float:
        """Estimates duration in seconds based on typical bitrates."""
        # For 16kHz mono 16-bit PCM WAV: 32,000 bytes/sec
        # For Opus WebM: ~3,000 to 4,000 bytes/sec
        if content_type and "webm" in content_type:
            rate = 3500.0
        elif content_type and "wav" in content_type:
            rate = 32000.0
        else:
            rate = 4000.0
        est = round(size_bytes / rate, 1)
        return max(0.5, min(est, 60.0))

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        content_type: str,
        language: str = "hi"
    ) -> Dict[str, Any]:
        """
        Sends recorded audio to Gnani Prisma v2.5 STT endpoint.
        Returns recognized Hindi transcript or explicit status.
        """
        duration = self.estimate_duration_seconds(len(audio_bytes), content_type)
        lang_code = "hi-IN" if "hi" in language.lower() else "en-IN"

        # Check if Gnani API Key is configured
        if not self.is_configured():
            logger.info("Gnani API key not configured. Returning pending_configuration state.")
            return {
                "status": "pending_configuration",
                "transcript": "",
                "language": lang_code,
                "duration_seconds": duration,
                "confidence": 0.0,
                "service_provider": f"Gnani Prisma ({self.stt_model} - Pending API Key)",
                "model_version": self.stt_model,
                "message": (
                    "Gnani Prisma API Key is not set in backend .env. "
                    "Voice upload and format validation succeeded."
                )
            }

        headers = {
            "X-API-Key-ID": self.api_key.strip(),
            "Accept": "application/json",
        }

        ext = "wav" if "wav" in content_type else "webm" if "webm" in content_type else "ogg"
        files = {
            "audio_file": (f"recording.{ext}", audio_bytes, content_type),
        }
        data = {
            "language_code": lang_code,
            "language": lang_code,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(self.stt_endpoint, headers=headers, files=files, data=data)

                if res.status_code == 200:
                    res_json = res.json()
                    transcript = (
                        res_json.get("transcript")
                        or res_json.get("text")
                        or res_json.get("asr_output", "")
                    )
                    confidence = float(res_json.get("confidence", 0.95))
                    return {
                        "status": "success",
                        "transcript": transcript,
                        "language": lang_code,
                        "duration_seconds": duration,
                        "confidence": confidence,
                        "service_provider": "Gnani Prisma",
                        "model_version": self.stt_model,
                        "message": "Transcription completed successfully."
                    }
                elif res.status_code in (401, 403):
                    logger.warning(f"Gnani authentication failed: HTTP {res.status_code}")
                    return {
                        "status": "error",
                        "transcript": "",
                        "language": lang_code,
                        "duration_seconds": duration,
                        "confidence": 0.0,
                        "service_provider": "Gnani Prisma",
                        "model_version": self.stt_model,
                        "message": f"Gnani Prisma authentication failed (HTTP {res.status_code}). Please verify GNANI_API_KEY in backend .env."
                    }
                else:
                    logger.warning(f"Gnani Prisma STT returned HTTP {res.status_code}. Attempting Gemini fallback...")
                    fallback_txt = await self._transcribe_with_gemini(audio_bytes, content_type, language)
                    if fallback_txt:
                        return {
                            "status": "success",
                            "transcript": fallback_txt,
                            "language": lang_code,
                            "duration_seconds": duration,
                            "confidence": 0.90,
                            "service_provider": "Gemini Audio (Fallback)",
                            "model_version": "gemini-3.5-flash-lite",
                            "message": "Transcription completed successfully via fallback engine."
                        }

                    err_msg = ""
                    try:
                        err_json = res.json()
                        err_msg = (
                            err_json.get("error", {}).get("message")
                            or err_json.get("message")
                            or ""
                        )
                    except Exception:
                        pass
                    detail_str = f": {err_msg}" if err_msg else ""
                    return {
                        "status": "error",
                        "transcript": "",
                        "language": lang_code,
                        "duration_seconds": duration,
                        "confidence": 0.0,
                        "service_provider": "Gnani Prisma",
                        "model_version": self.stt_model,
                        "message": f"Gnani Prisma STT (HTTP {res.status_code}){detail_str}"
                    }
        except httpx.TimeoutException:
            logger.warning("Gnani Prisma STT timed out. Attempting Gemini audio fallback...")
            fallback_txt = await self._transcribe_with_gemini(audio_bytes, content_type, language)
            if fallback_txt:
                return {
                    "status": "success",
                    "transcript": fallback_txt,
                    "language": lang_code,
                    "duration_seconds": duration,
                    "confidence": 0.90,
                    "service_provider": "Gemini Audio (Fallback)",
                    "model_version": "gemini-3.5-flash-lite",
                    "message": "Transcription completed successfully via fallback engine."
                }
            return {
                "status": "error",
                "transcript": "",
                "language": lang_code,
                "duration_seconds": duration,
                "confidence": 0.0,
                "service_provider": "Gnani Prisma",
                "model_version": self.stt_model,
                "message": "Voice recognition timed out. Please retry."
            }
        except Exception as e:
            logger.error(f"Gnani Prisma STT exception: {e}")
            fallback_txt = await self._transcribe_with_gemini(audio_bytes, content_type, language)
            if fallback_txt:
                return {
                    "status": "success",
                    "transcript": fallback_txt,
                    "language": lang_code,
                    "duration_seconds": duration,
                    "confidence": 0.90,
                    "service_provider": "Gemini Audio (Fallback)",
                    "model_version": "gemini-3.5-flash-lite",
                    "message": "Transcription completed successfully via fallback engine."
                }
            return {
                "status": "error",
                "transcript": "",
                "language": lang_code,
                "duration_seconds": duration,
                "confidence": 0.0,
                "service_provider": "Gnani Prisma",
                "model_version": self.stt_model,
                "message": f"Voice service error: {str(e)}"
            }

    async def _transcribe_with_gemini(
        self,
        audio_bytes: bytes,
        content_type: str,
        language: str = "hi"
    ) -> Optional[str]:
        """
        Fallback audio transcriber using Gemini 3.5 Flash Lite
        Activated automatically if Gnani Prisma encounters 504 Gateway Timeout or server errors.
        """
        api_key = settings.GEMINI_API_KEY.strip()
        if not api_key:
            return None

        try:
            b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            mime = "audio/wav" if "wav" in content_type else "audio/webm"
            lang_prompt = "in pure Devanagari Hindi" if "hi" in language else "in Indian English"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"

            payload = {
                "contents": [{
                    "parts": [
                        {"inline_data": {"mime_type": mime, "data": b64_audio}},
                        {"text": f"Listen to this audio and transcribe the spoken words verbatim {lang_prompt}. Output ONLY the transcribed words. Do not add any punctuation, preamble, quotes, notes, or explanation. If silence or inaudible, output nothing."}
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 200
                }
            }

            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    candidates = resp.json().get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            txt = parts[0]["text"].strip()
                            if txt:
                                logger.info(f"Successfully transcribed audio via Gemini fallback: {txt[:50]}")
                                return txt
        except Exception as ex:
            logger.warning(f"Gemini audio transcription fallback encountered error: {ex}")
        return None

    async def synthesize_speech(
        self,
        text: str,
        language: str = "hi",
        voice_gender: str = "female"
    ) -> Dict[str, Any]:
        """
        Synthesizes Hindi agricultural advice text into spoken speech via Gnani Timbre v2.5.
        Returns base64-encoded audio or transparent fallback notification.
        """
        text_clean = text.strip()
        if not text_clean:
            return {
                "status": "error",
                "audio_url": "",
                "audio_base64": None,
                "format": "audio/wav",
                "duration_seconds": 0.0,
                "service_provider": "Gnani Timbre",
                "model_version": self.tts_model,
                "message": "Text for speech synthesis cannot be empty."
            }

        est_duration = max(1.0, round(len(text_clean.split()) * 0.35, 1))

        if not self.is_configured():
            logger.info("Gnani API key not configured for TTS. Client will use browser Web Speech API.")
            return {
                "status": "fallback",
                "audio_url": "",
                "audio_base64": None,
                "format": "audio/wav",
                "duration_seconds": est_duration,
                "service_provider": f"Gnani Timbre ({self.tts_model} - Client WebSpeech Fallback)",
                "model_version": self.tts_model,
                "message": (
                    "GNANI_API_KEY is not configured in backend .env. "
                    "Browser Web Speech API is being used for Hindi audio output."
                )
            }

        headers = {
            "X-API-Key-ID": self.api_key,
            "token": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, audio/wav, audio/mpeg"
        }
        voice_name = "Deepak" if voice_gender == "male" else "Nalini"
        payload = {
            "text": text_clean,
            "language": "hi-IN" if "hi" in language.lower() else "en-IN",
            "model": self.tts_model,
            "voice": voice_name,
            "speed": 1,
            "audio_config": {
                "encoding": "linear_pcm",
                "container": "wav",
                "num_channels": 1,
                "sample_rate": 24000
            }
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(self.tts_endpoint, headers=headers, json=payload)
                if res.status_code == 200:
                    content_type = res.headers.get("content-type", "")
                    if "audio" in content_type:
                        audio_b64 = base64.b64encode(res.content).decode("utf-8")
                        return {
                            "status": "success",
                            "audio_url": "",
                            "audio_base64": audio_b64,
                            "format": "audio/wav",
                            "duration_seconds": est_duration,
                            "service_provider": "Gnani Timbre",
                            "model_version": self.tts_model,
                            "message": "Audio synthesized successfully."
                        }
                    else:
                        res_json = res.json()
                        audio_b64 = res_json.get("audio_content") or res_json.get("audio_base64")
                        audio_url = res_json.get("audio_url", "")
                        return {
                            "status": "success",
                            "audio_url": audio_url,
                            "audio_base64": audio_b64,
                            "format": "audio/wav",
                            "duration_seconds": est_duration,
                            "service_provider": "Gnani Timbre",
                            "model_version": self.tts_model,
                            "message": "Audio synthesized successfully."
                        }
                elif res.status_code in (401, 403):
                    return {
                        "status": "fallback",
                        "audio_url": "",
                        "audio_base64": None,
                        "format": "audio/wav",
                        "duration_seconds": est_duration,
                        "service_provider": "Gnani Timbre",
                        "model_version": self.tts_model,
                        "message": f"Gnani Timbre authentication failed (HTTP {res.status_code}). Using browser speech fallback."
                    }
                else:
                    return {
                        "status": "fallback",
                        "audio_url": "",
                        "audio_base64": None,
                        "format": "audio/wav",
                        "duration_seconds": est_duration,
                        "service_provider": "Gnani Timbre",
                        "model_version": self.tts_model,
                        "message": f"Gnani Timbre HTTP {res.status_code}. Using browser speech fallback."
                    }
        except Exception as e:
            logger.error(f"Gnani Timbre TTS exception: {e}")
            return {
                "status": "fallback",
                "audio_url": "",
                "audio_base64": None,
                "format": "audio/wav",
                "duration_seconds": est_duration,
                "service_provider": "Gnani Timbre",
                "model_version": self.tts_model,
                "message": f"Gnani Timbre request error ({str(e)}). Using browser speech fallback."
            }

voice_service = VoiceService()

