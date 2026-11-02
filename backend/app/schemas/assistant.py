from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, computed_field


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    language: str = "hi"
    state: Optional[str] = None
    district: Optional[str] = None
    crop: Optional[str] = None


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    conversation_id: str
    message_id: str
    answer_text: str
    answer_hi: str
    answer_en: Optional[str] = None
    intent: str
    confidence: float
    verification_status: str  # verified | pending_review | unverified
    data_type: str            # official_static | official_live | sample | unverified
    sources_used: List[Dict[str, Any]] = []
    follow_up_questions: List[str] = []
    audio_url: Optional[str] = None

    @computed_field
    @property
    def answer(self) -> str:
        """Alias consumed by frontend api.js → data.answer"""
        return self.answer_hi or self.answer_text

    @computed_field
    @property
    def sources(self) -> List[str]:
        """Flat list of source names for frontend display"""
        names = []
        for s in self.sources_used:
            if isinstance(s, dict):
                name = s.get("name") or s.get("source_id") or s.get("id")
                if name:
                    names.append(str(name))
            elif isinstance(s, str):
                names.append(s)
        return names

