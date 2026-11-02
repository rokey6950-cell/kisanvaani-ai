from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, computed_field

class WeatherForecastDay(BaseModel):
    day: str
    day_hi: str
    temp_max: float
    temp_min: float
    condition: str
    condition_hi: str
    rain_probability: int
    data_type: Optional[str] = "sample"

class WeatherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    location: str
    state: str
    observation_date: str
    retrieval_timestamp: str
    data_source: str
    data_type: str  # official_live | official_static | sample | unverified
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    rainfall_prob: int
    condition: str
    condition_hi: str
    spray_advisory: Dict[str, Any]
    irrigation_advisory: Dict[str, Any]
    harvest_advisory: Dict[str, Any]
    forecast: List[WeatherForecastDay]

    # Additional optional fields for enhanced agromet metadata
    district: Optional[str] = None
    state_code: Optional[str] = None
    wind_direction: Optional[str] = None
    rainfall_mm_last24h: Optional[float] = None
    visibility_km: Optional[float] = None
    imd_disclaimer: Optional[str] = None
    resolved_station: Optional[str] = None

    @computed_field
    @property
    def source(self) -> str:
        return self.data_source

    @computed_field
    @property
    def current(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "condition": self.condition,
            "condition_hi": self.condition_hi,
            "rainfall_prob": self.rainfall_prob,
        }

    @computed_field
    @property
    def farm_advisories(self) -> List[Dict[str, Any]]:
        advisories = []
        if self.spray_advisory:
            advisories.append({
                "type": "spray",
                "text": self.spray_advisory.get("message", ""),
                "text_hi": self.spray_advisory.get("message_hi", "")
            })
        if self.irrigation_advisory:
            advisories.append({
                "type": "irrigation",
                "text": self.irrigation_advisory.get("message", ""),
                "text_hi": self.irrigation_advisory.get("message_hi", "")
            })
        if self.harvest_advisory:
            advisories.append({
                "type": "harvest",
                "text": self.harvest_advisory.get("message", ""),
                "text_hi": self.harvest_advisory.get("message_hi", "")
            })
        return advisories

class WeatherStationItem(BaseModel):
    id: str
    location: str
    district: str
    state: str
    state_code: str

class WeatherLocationsResponse(BaseModel):
    total: int
    locations: List[WeatherStationItem]
    data_type: str = "sample"
    disclaimer: str

class WeatherStatusResponse(BaseModel):
    provider: str
    api_status: str
    commercial_use: str
    non_commercial_use: str
    agromet_portal: str
    weather_portal: str
    meghdoot_app: str
    data_type_in_use: str
    data_type_note: str
    credential_env_var: str
    credential_status: str
    source: str

class WeatherParameterItem(BaseModel):
    id: str
    parameter: str
    name: Dict[str, str]
    data_type: str
    verification_status: str
    notes: Optional[str] = None

class WeatherParametersResponse(BaseModel):
    total: int
    parameters: List[WeatherParameterItem]
    source: str
