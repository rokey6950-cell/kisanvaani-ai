from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class CropAdvisoryRequest(BaseModel):
    crop: str
    state: Optional[str] = None
    district: Optional[str] = None
    season: Optional[str] = None
    topic: Optional[str] = "general"

class CropAdvisoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop: str
    state: Optional[str] = None
    district: Optional[str] = None
    season: Optional[str] = None
    topic: str
    title: str
    advisory_hi: str
    advisory_en: Optional[str] = None
    verified_guidance: Optional[Dict[str, Any]] = None
    safety_disclaimer: str
    kvk_referral: Dict[str, str]
    verification_status: str  # verified | pending_review | unverified
    data_type: str            # official_static | sample | unverified
    sources: List[Any] = []

