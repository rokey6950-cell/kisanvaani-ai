from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query

from ..services.schemes_service import schemes_service
from ..schemas.schemes import SchemesListResponse, SchemeItem

router = APIRouter(prefix="/schemes", tags=["Government Schemes"])

@router.get("", response_model=SchemesListResponse)
def list_government_schemes(
    category: Optional[str] = Query(None, description="Filter by category (financial_support, crop_insurance, irrigation, etc.)"),
    q: Optional[str] = Query(None, description="Search keyword in Hindi or English")
):
    """
    Lists all verified government agricultural schemes.
    Includes PM-KISAN, PMFBY, PMKSY, Soil Health Card, SMAM, and mKisan.
    """
    if q and q.strip():
        schemes = schemes_service.search_schemes(q.strip())
    else:
        schemes = schemes_service.get_all_schemes(category=category)

    return SchemesListResponse(
        total=len(schemes),
        schemes=schemes
    )

@router.get("/search", response_model=SchemesListResponse)
def search_schemes(
    q: str = Query(..., min_length=2, description="Search keyword")
):
    """Searches schemes by scheme name, benefits, or purpose."""
    schemes = schemes_service.search_schemes(q)
    return SchemesListResponse(
        total=len(schemes),
        schemes=schemes
    )

@router.get("/{scheme_id}", response_model=SchemeItem)
def get_scheme_details(scheme_id: str):
    """
    Retrieves verified details, benefits, eligibility, required documents,
    official portals, and helpline contacts for a specific scheme.
    """
    scheme = schemes_service.get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=404,
            detail=f"Scheme with ID '{scheme_id}' not found in the verified knowledge base."
        )
    return scheme
