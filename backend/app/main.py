from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .database.connection import init_db
from .services.knowledge_retrieval import knowledge_service
from .routes import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Voice-First AI Agricultural Assistance Platform for Indian Farmers"
)

# Startup event: Initialize DB schema & preload knowledge base
@app.on_event("startup")
def startup_event():
    init_db()
    knowledge_service.load_knowledge_base()

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount versioned API routes (/api/v1)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "message": "KisanVaani AI API Server is running.",
        "tagline": "Apni Bhasha, Apni Kheti, Smart Faisle.",
        "health_check": f"{settings.API_V1_PREFIX}/health",
        "documentation": "/docs"
    }
