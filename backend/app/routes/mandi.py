from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from ..schemas.mandi import (
    MandiResponse,
    MandiPriceItem,
    MandiMarketsResponse,
    MandiCommoditiesResponse
)
from ..services.mandi_service import mandi_service

router = APIRouter(prefix="/mandi-prices", tags=["Mandi Rates"])

@router.get("", response_model=MandiResponse)
def get_mandi_prices(
    crop: Optional[str] = Query(None, description="Filter by crop (e.g. Wheat, Mustard, Rice)"),
    state: Optional[str] = Query(None, description="Filter by state (e.g. Haryana, Punjab, UP)"),
    district: Optional[str] = Query(None, description="Filter by district"),
    mandi: Optional[str] = Query(None, description="Filter by market name")
):
    """
    Returns agricultural market prices with minimum, maximum, and modal rates.
    Mandatory Transparency: As confirmed by verification_report.json and apicfg-mandi-001,
    the live data.gov.in commodity API is unconfirmed ('API for this resource does not exist').
    Prices are benchmark sample standards based on AGMARKNET.
    """
    filtered = mandi_service.get_prices(
        crop=crop,
        state=state,
        district=district,
        mandi=mandi
    )

    return MandiResponse(
        status="success",
        message="Notice: Live data.gov.in API is unconfirmed (Request API button on portal). Showing sample AGMARKNET benchmarks.",
        total=len(filtered),
        data_source="AGMARKNET Benchmark Model (Static Sample)",
        data_type="sample",
        api_available=False,
        official_portal="https://agmarknet.gov.in",
        disclaimer="लाइव डेटा.gov.in API वर्तमान में अनुपलब्ध है। यहाँ प्रदर्शित भाव AGMARKNET बेंचमार्क मॉडल पर आधारित नमूना डेटा हैं।",
        prices=filtered
    )

@router.get("/markets", response_model=MandiMarketsResponse)
def get_mandi_markets():
    """Returns available mandis categorized by state and district."""
    markets_by_state = mandi_service.get_markets()
    total = sum(len(m_list) for m_list in markets_by_state.values())
    return MandiMarketsResponse(
        total_markets=total,
        states=markets_by_state
    )

@router.get("/commodities", response_model=MandiCommoditiesResponse)
def get_mandi_commodities():
    """Returns list of tracked agricultural commodities."""
    commodities = mandi_service.get_commodities()
    return MandiCommoditiesResponse(
        total=len(commodities),
        commodities=commodities
    )

@router.get("/status")
def get_mandi_api_status():
    """Discloses official API configuration and data.gov.in status."""
    return {
        "provider": "data.gov.in / AGMARKNET",
        "api_available": False,
        "status": "blocked_unconfirmed",
        "official_portal": "https://agmarknet.gov.in",
        "reason": "The data.gov.in catalogue page for the current daily mandi price resource states 'The API for this resource does not exist' and offers a Request API button. No working resource ID has been confirmed or tested.",
        "data_label": "sample",
        "compliance": "Never generate fake live prices. Display clear limitation notices."
    }
