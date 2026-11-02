from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

class KnowledgeStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    loaded: bool
    manifest_version: str
    target_regions: List[str]
    total_files: int
    total_records: int
    source_records: int
    verified_records: int
    pending_records: int
    categories: List[str]
    status_note: str

class SourceItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    source_id: Optional[str] = None
    organization: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    verification_status: Optional[str] = None
    evidence_level: Optional[str] = None
    claims_supported: List[str] = []

class KnowledgeSearchResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    category: str
    title: str
    answer_simple: Any
    answer_detailed: Optional[Any] = None
    state: Optional[str] = None
    verification_status: str
    data_type: str
    sources: List[Any] = []
    relevance_score: float = 0.0

class KnowledgeSearchResponse(BaseModel):
    query: str
    total_matches: int
    results: List[KnowledgeSearchResult]

class SeedVarietyItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    crop_id: str
    variety: str
    state: Optional[str] = None
    zone: Optional[str] = None
    sowing_condition: Optional[str] = None
    irrigation_status: Optional[str] = None
    verification_status: str
    data_type: str
    sources: List[Any] = []

class GlossaryItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    term: Dict[str, str]
    kind: Optional[str] = None
    definition: Optional[Dict[str, str]] = None
    verification_status: str
    data_type: str

class AgroZoneItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    zone_id: str
    name: Dict[str, str]
    states: List[str] = []
    verification_status: str
    data_type: str

