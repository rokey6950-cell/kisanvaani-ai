from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class MandiPriceItem(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: str
    commodity: str
    commodity_hi: str
    variety: Optional[str] = None
    state: str
    district: str
    market: str
    min_price: float
    max_price: float
    modal_price: float
    price_unit: str = "Rs/Quintal"
    arrivals_tonnes: Optional[float] = None
    arrival_date: str
    data_source: str
    data_type: str = "sample"  # official_live | official_static | sample | unverified
    is_live: bool = False
    last_updated: str

class MandiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    status: str
    message: str
    total: int
    data_source: str
    data_type: str = "sample"
    api_available: bool
    official_portal: str = "https://agmarknet.gov.in"
    disclaimer: str = "Notice: Live data.gov.in daily commodity API is unconfirmed. Benchmark sample prices shown."
    prices: List[MandiPriceItem]

class MandiMarketsResponse(BaseModel):
    total_markets: int
    states: Dict[str, List[Dict[str, str]]]

class MandiCommoditiesResponse(BaseModel):
    total: int
    commodities: List[Dict[str, str]]

