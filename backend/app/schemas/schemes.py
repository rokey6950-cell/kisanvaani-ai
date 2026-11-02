from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


class SchemeItem(BaseModel):
    """
    Flexible scheme schema that accepts whatever the knowledge base JSON contains.
    Fields like purpose, benefits, eligibility and helpline can be strings, dicts,
    lists or null depending on how deep the KB record was populated.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: str
    scheme_id: str
    # name, purpose, benefits, etc. are typed as Any because the KB stores them as
    # both plain strings (one-language stubs) and {"hi": …, "en": …} dicts
    name: Any
    scope: Optional[str] = None
    department: Optional[str] = None
    purpose: Optional[Any] = None
    benefits: Optional[Any] = None
    eligibility: Optional[Any] = None
    exclusion_criteria: Optional[Any] = None
    application_process: Optional[Any] = None
    required_documents: Optional[Any] = None
    application_deadline: Optional[str] = None
    official_portal: Optional[str] = None
    helpline: Optional[Any] = None
    official_notification_url: Optional[str] = None
    verification_status: str = "pending_review"
    data_type: str = "official_static"
    last_verified: Optional[str] = None
    sources: List[Any] = []


class SchemesListResponse(BaseModel):
    total: int
    schemes: List[SchemeItem]

