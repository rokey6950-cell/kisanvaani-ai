from pathlib import Path
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "KisanVaani AI"
    APP_VERSION: str = "0.1.0-pilot"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # CORS Configuration
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./kisanvaani.db"

    # Agricultural Knowledge Base Directory
    # Resolves knowledge directory located in root of workspace
    KNOWLEDGE_DIR: str = str((Path(__file__).resolve().parent.parent.parent.parent / "knowledge").resolve())

    # AI Voice - Gnani API Configuration (Vachana Platform)
    GNANI_API_KEY: str = ""
    GNANI_STT_MODEL: str = "prisma-v2.5"
    GNANI_TTS_MODEL: str = "timbre-v2.5"
    GNANI_STT_ENDPOINT: str = "https://api.vachana.ai/stt/v3"
    GNANI_TTS_ENDPOINT: str = "https://api.vachana.ai/api/v1/tts/inference"

    # Optional Fallback AI Provider
    GEMINI_API_KEY: str = ""

    model_config = {
        "env_file": [
            str(Path(__file__).resolve().parent.parent.parent / ".env"),
            "backend/.env",
            ".env"
        ],
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()

