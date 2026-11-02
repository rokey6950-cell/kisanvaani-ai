from fastapi import APIRouter

from .health import router as health_router
from .knowledge import router as knowledge_router
from .assistant import router as assistant_router
from .schemes import router as schemes_router
from .mandi import router as mandi_router
from .weather import router as weather_router
from .history import router as history_router
from .voice import router as voice_router
from .crop_advisory import router as crop_advisory_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(knowledge_router)
api_router.include_router(assistant_router)
api_router.include_router(schemes_router)
api_router.include_router(mandi_router)
api_router.include_router(weather_router)
api_router.include_router(history_router)
api_router.include_router(voice_router)
api_router.include_router(crop_advisory_router)

