import json
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import APIRouter, Query

from ..schemas.weather import (
    WeatherResponse,
    WeatherLocationsResponse,
    WeatherStationItem,
    WeatherStatusResponse,
    WeatherParametersResponse,
    WeatherParameterItem,
)
from ..services import weather_service

router = APIRouter(prefix="/weather", tags=["Weather & Agromet Advisory"])

@router.get("/status", response_model=WeatherStatusResponse)
def get_weather_status():
    """
    Returns API status, commercial usage restrictions, and source attribution for IMD weather data.
    Clearly discloses that live IMD APIs require written permission, and current data is benchmark sample data.
    """
    return weather_service.get_imd_status()

@router.get("/locations", response_model=WeatherLocationsResponse)
def get_weather_locations():
    """
    Returns list of supported pilot agro-meteorological stations across 7 states.
    """
    locs = weather_service.list_locations()
    items = [WeatherStationItem(**loc) for loc in locs]
    return WeatherLocationsResponse(
        total=len(items),
        locations=items,
        data_type="sample",
        disclaimer="Supported IMD agromet sample stations. Official IDs pending IMD API agreement."
    )

@router.get("/parameters", response_model=WeatherParametersResponse)
def get_weather_parameters():
    """
    Returns IMD Agromet advisory parameters catalog from knowledge base.
    """
    kb_path = Path(__file__).resolve().parent.parent.parent.parent / "knowledge" / "weather" / "weather_parameters.json"
    params = []
    if kb_path.exists():
        try:
            with open(kb_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    params.append(
                        WeatherParameterItem(
                            id=item.get("id", ""),
                            parameter=item.get("parameter", ""),
                            name=item.get("name", {}),
                            data_type=item.get("data_type", "unverified"),
                            verification_status=item.get("verification_status", "pending_review"),
                            notes=item.get("notes")
                        )
                    )
        except Exception:
            pass

    return WeatherParametersResponse(
        total=len(params),
        parameters=params,
        source="knowledge/weather/weather_parameters.json"
    )

@router.get("/advisory")
def get_farm_advisory_only(
    location: Optional[str] = Query(None, description="District or city name")
) -> Dict[str, Any]:
    """
    Dedicated endpoint returning strictly farm advisories (spray, irrigation, harvest).
    """
    full_data = weather_service.get_weather_data(location)
    return {
        "location": full_data["location"],
        "state": full_data["state"],
        "observation_date": full_data["observation_date"],
        "data_type": full_data["data_type"],
        "spray_advisory": full_data["spray_advisory"],
        "irrigation_advisory": full_data["irrigation_advisory"],
        "harvest_advisory": full_data["harvest_advisory"],
        "disclaimer_hi": full_data["imd_disclaimer"]
    }

@router.get("", response_model=WeatherResponse)
def get_weather_advisory(
    location: Optional[str] = Query(None, description="District or city name (e.g. Karnal, Ludhiana, Jaipur)")
):
    """
    Returns weather data and agrometeorological advisory.
    Notice: Based on IMD Agromet Advisory format standards.
    Clearly indicates data_type='sample' pending commercial/official IMD API agreement.
    """
    data = weather_service.get_weather_data(location)
    return WeatherResponse(**data)
