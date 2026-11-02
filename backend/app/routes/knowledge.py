from typing import Optional
from fastapi import APIRouter, Query, HTTPException

from ..services.knowledge_retrieval import knowledge_service
from ..schemas.knowledge import KnowledgeStatusResponse, KnowledgeSearchResponse

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

@router.get("/status", response_model=KnowledgeStatusResponse)
def get_knowledge_base_status():
    """Returns detailed knowledge-base verification status, regions and record counts."""
    status = knowledge_service.get_status()
    return KnowledgeStatusResponse(**status)

@router.get("/search", response_model=KnowledgeSearchResponse)
def search_knowledge_base(
    q: str = Query(..., min_length=2, description="Search query in Hindi or English"),
    state: Optional[str] = Query(None, description="Filter by state (e.g. Haryana, Punjab, UP)"),
    crop: Optional[str] = Query(None, description="Filter by crop (e.g. wheat, mustard)")
):
    """Searches grounded agricultural records with source attribution and verification status."""
    results = knowledge_service.search_knowledge(query=q, state=state, crop=crop)
    return KnowledgeSearchResponse(
        query=q,
        total_matches=len(results),
        results=results
    )

@router.get("/crops")
def get_crop_catalog():
    """Returns list of prioritized crops and their state distributions."""
    return knowledge_service.get_crop_catalog()

@router.get("/crops/{crop_name}")
def get_crop_guidance(crop_name: str, state: Optional[str] = None):
    """Returns verified package of practices for a specific crop and state."""
    records = knowledge_service.get_crop_guidance(crop_name=crop_name, state=state)
    if not records and crop_name.lower() != "wheat":
        return {
            "crop": crop_name,
            "status": "pending_official_verification",
            "message": f"Official university package of practices for {crop_name} is awaiting verified state department document.",
            "records": []
        }
    return {
        "crop": crop_name,
        "state_filter": state,
        "total": len(records),
        "records": records
    }

@router.get("/seeds")
def get_seed_varieties(
    crop: Optional[str] = Query(None, description="Filter by crop (e.g. wheat, bajra)"),
    state: Optional[str] = Query(None, description="Filter by state (e.g. Haryana)")
):
    """Returns verified recommended seed varieties from agricultural university publications."""
    varieties = knowledge_service.get_seed_varieties(crop_id=crop, state=state)
    return {
        "total": len(varieties),
        "crop": crop,
        "state": state,
        "varieties": varieties
    }

@router.get("/glossary")
def get_agricultural_glossary(
    q: Optional[str] = Query(None, description="Filter glossary terms")
):
    """Returns Hindi agricultural glossary definitions."""
    terms = knowledge_service.get_glossary(query=q)
    return {
        "total": len(terms),
        "query": q,
        "terms": terms
    }

@router.get("/zones")
def get_agro_climatic_zones(
    state: Optional[str] = Query(None, description="Filter by state")
):
    """Returns agro-climatic zones covering target pilot states."""
    zones = knowledge_service.get_agro_zones(state=state)
    return {
        "total": len(zones),
        "state": state,
        "zones": zones
    }

