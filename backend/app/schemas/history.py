from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict

class MessageItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    sender: str
    text: str
    audio_url: Optional[str] = None
    intent: Optional[str] = None
    sources_used: Optional[Any] = None
    created_at: datetime

class ConversationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    language: str
    message_count: int
    created_at: datetime
    updated_at: datetime

class ConversationDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    language: str
    messages: List[MessageItem]
    created_at: datetime
    updated_at: datetime

