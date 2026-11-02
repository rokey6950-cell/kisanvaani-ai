from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException

from ..schemas.crop_advisory import CropAdvisoryRequest, CropAdvisoryResponse
from ..services.crop_advisory_service import crop_advisory_service

router = APIRouter(prefix="/crop-advisory", tags=["Smart Crop Advisory"])

@router.get("/districts")
def get_districts(state: str = Query(..., description="Target State (e.g. Haryana, Punjab, UP)")):
    """Returns official districts list for a state."""
    districts = crop_advisory_service.get_districts_for_state(state)
    return {
        "state": state,
        "total": len(districts),
        "districts": districts
    }

@router.get("/topics")
def get_advisory_topics():
    """Returns all supported agricultural advisory topics."""
    topics = crop_advisory_service.get_topics()
    return {
        "total": len(topics),
        "topics": topics
    }

@router.post("/recommendation", response_model=CropAdvisoryResponse)
def get_crop_recommendation(req: CropAdvisoryRequest):
    """
    Returns grounded, university-verified agricultural advisory.
    Strictly prevents inventing unverified chemical doses or pesticide mixes.
    """
    if not req.crop.strip():
        raise HTTPException(status_code=400, detail="Crop name is required.")

    result = crop_advisory_service.generate_advisory(
        crop=req.crop,
        state=req.state,
        district=req.district,
        season=req.season,
        topic=req.topic
    )
    return CropAdvisoryResponse(**result)

