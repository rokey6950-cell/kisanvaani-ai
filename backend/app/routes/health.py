from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database.connection import get_db
from ..services.knowledge_retrieval import knowledge_service
from ..core.config import settings
from ..schemas.health import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def get_health_status(db: Session = Depends(get_db)):
    """
    Health check endpoint verifying:
    - Application status
    - Database connectivity (SQLite)
    - Agricultural knowledge base loading status
    """
    db_connected = False
    try:
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception:
        db_connected = False

    kb_status = knowledge_service.get_status()

    return HealthResponse(
        status="healthy" if (db_connected and kb_status.get("loaded", False)) else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        database_connected=db_connected,
        knowledge_base_loaded=kb_status.get("loaded", False),
        records_count=kb_status.get("total_records", 0),
        timestamp=datetime.now(timezone.utc)
    )
