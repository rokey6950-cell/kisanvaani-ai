from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    app_name: str
    version: str
    environment: str
    database_connected: bool
    knowledge_base_loaded: bool
    records_count: int
    timestamp: datetime

