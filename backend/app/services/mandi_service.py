from datetime import date
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("kisanvaani.mandi")

# Benchmark representative Mandi data across 7 target states based on AGMARKNET standards
# Labeled data_type="sample" as documented in verification_report.json and apicfg-mandi-001
REPRESENTATIVE_MANDI_DATA: List[Dict[str, Any]] = [
    # Punjab
    {
        "id": "mandi-wheat-khanna",
        "commodity": "Wheat",
        "commodity_hi": "गेहूं",
        "variety": "PBW 826 / HD 3086",
        "state": "Punjab",
        "district": "Ludhiana",
        "market": "Khanna Mandi",
        "min_price": 2275.0,
        "max_price": 2550.0,
        "modal_price": 2420.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 3450.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-paddy-amritsar",
        "commodity": "Basmati Rice",
        "commodity_hi": "बासमती धान",
        "variety": "Pusa 1121",
        "state": "Punjab",
        "district": "Amritsar",
        "market": "Bhagtanwala Mandi",
        "min_price": 3950.0,
        "max_price": 4500.0,
        "modal_price": 4320.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 1820.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    # Haryana
    {
        "id": "mandi-paddy-karnal",
        "commodity": "Basmati Rice",
        "commodity_hi": "बासमती धान",
        "variety": "PB 1509 / 1121",
        "state": "Haryana",
        "district": "Karnal",
        "market": "Karnal Grain Market",
        "min_price": 3850.0,
        "max_price": 4420.0,
        "modal_price": 4200.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 2650.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-wheat-hisar",
        "commodity": "Wheat",
        "commodity_hi": "गेहूं",
        "variety": "WH 1270",
        "state": "Haryana",
        "district": "Hisar",
        "market": "Hisar Mandi",
        "min_price": 2275.0,
        "max_price": 2480.0,
        "modal_price": 2390.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 1400.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-mustard-rewari",
        "commodity": "Mustard",
        "commodity_hi": "सरसों / राई",
        "variety": "RH 725",
        "state": "Haryana",
        "district": "Rewari",
        "market": "Rewari Mandi",
        "min_price": 5400.0,
        "max_price": 5850.0,
        "modal_price": 5680.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 890.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-cotton-sirsa",
        "commodity": "Cotton",
        "commodity_hi": "कपास (नरमा)",
        "variety": "Bt Cotton",
        "state": "Haryana",
        "district": "Sirsa",
        "market": "Sirsa Grain Market",
        "min_price": 6800.0,
        "max_price": 7450.0,
        "modal_price": 7180.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 650.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    # Rajasthan
    {
        "id": "mandi-mustard-ganganagar",
        "commodity": "Mustard",
        "commodity_hi": "सरसों / राई",
        "variety": "Pusa Bold",
        "state": "Rajasthan",
        "district": "Sri Ganganagar",
        "market": "Sri Ganganagar Mandi",
        "min_price": 5350.0,
        "max_price": 5950.0,
        "modal_price": 5740.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 2100.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-bajra-jaipur",
        "commodity": "Bajra",
        "commodity_hi": "बाजरा",
        "variety": "Desi / Hybrid",
        "state": "Rajasthan",
        "district": "Jaipur",
        "market": "Surajpole Krishi Upaj Mandi",
        "min_price": 2200.0,
        "max_price": 2550.0,
        "modal_price": 2410.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 720.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-gram-kota",
        "commodity": "Gram",
        "commodity_hi": "चना (काला)",
        "variety": "Desi Chana",
        "state": "Rajasthan",
        "district": "Kota",
        "market": "Bhamashah Mandi Kota",
        "min_price": 5600.0,
        "max_price": 6250.0,
        "modal_price": 6020.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 1150.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    # Uttar Pradesh
    {
        "id": "mandi-potato-agra",
        "commodity": "Potato",
        "commodity_hi": "आलू",
        "variety": "Kufri Bahar",
        "state": "Uttar Pradesh",
        "district": "Agra",
        "market": "Agra Mandi",
        "min_price": 1100.0,
        "max_price": 1550.0,
        "modal_price": 1380.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 4800.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-sugarcane-meerut",
        "commodity": "Sugarcane",
        "commodity_hi": "गन्ना",
        "variety": "Co 0238",
        "state": "Uttar Pradesh",
        "district": "Meerut",
        "market": "Meerut Mandi / Mill Gate",
        "min_price": 370.0,
        "max_price": 390.0,
        "modal_price": 380.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 6200.0,
        "arrival_date": str(date.today()),
        "data_source": "State SAP / Mandi Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    # Himachal Pradesh
    {
        "id": "mandi-apple-shimla",
        "commodity": "Apple",
        "commodity_hi": "सेब",
        "variety": "Royal Delicious",
        "state": "Himachal Pradesh",
        "district": "Shimla",
        "market": "Bhattakufer Fruit Mandi Shimla",
        "min_price": 7200.0,
        "max_price": 11500.0,
        "modal_price": 9400.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 540.0,
        "arrival_date": str(date.today()),
        "data_source": "HPMC / AGMARKNET Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    # Uttarakhand
    {
        "id": "mandi-basmati-dehradun",
        "commodity": "Basmati Rice",
        "commodity_hi": "बासमती धान / चावल",
        "variety": "Dehraduni Type-3",
        "state": "Uttarakhand",
        "district": "Dehradun",
        "market": "Niranjanpur Mandi Dehradun",
        "min_price": 4200.0,
        "max_price": 4850.0,
        "modal_price": 4550.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 320.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    # Delhi NCR
    {
        "id": "mandi-wheat-narela",
        "commodity": "Wheat",
        "commodity_hi": "गेहूं",
        "variety": "Dara / Mill Quality",
        "state": "Delhi",
        "district": "North Delhi",
        "market": "Narela Anaj Mandi",
        "min_price": 2350.0,
        "max_price": 2620.0,
        "modal_price": 2490.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 2100.0,
        "arrival_date": str(date.today()),
        "data_source": "AGMARKNET Wholesale Market Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    },
    {
        "id": "mandi-onion-azadpur",
        "commodity": "Onion",
        "commodity_hi": "प्याज",
        "variety": "Nasik Red",
        "state": "Delhi",
        "district": "North Delhi",
        "market": "Azadpur Subzi Mandi",
        "min_price": 1600.0,
        "max_price": 2400.0,
        "modal_price": 2050.0,
        "price_unit": "Rs/Quintal",
        "arrivals_tonnes": 5200.0,
        "arrival_date": str(date.today()),
        "data_source": "APMC Azadpur / AGMARKNET Standards",
        "data_type": "sample",
        "is_live": False,
        "last_updated": str(date.today())
    }
]

COMMODITIES_LIST: List[Dict[str, str]] = [
    {"crop_id": "wheat", "name_en": "Wheat", "name_hi": "गेहूं"},
    {"crop_id": "rice", "name_en": "Basmati Rice", "name_hi": "बासमती धान"},
    {"crop_id": "mustard", "name_en": "Mustard", "name_hi": "सरसों / राई"},
    {"crop_id": "cotton", "name_en": "Cotton", "name_hi": "कपास"},
    {"crop_id": "bajra", "name_en": "Bajra", "name_hi": "बाजरा"},
    {"crop_id": "gram", "name_en": "Gram / Chickpea", "name_hi": "चना"},
    {"crop_id": "potato", "name_en": "Potato", "name_hi": "आलू"},
    {"crop_id": "onion", "name_en": "Onion", "name_hi": "प्याज"},
    {"crop_id": "sugarcane", "name_en": "Sugarcane", "name_hi": "गन्ना"},
    {"crop_id": "apple", "name_en": "Apple", "name_hi": "सेब"}
]

class MandiService:
    """Service providing agricultural market prices, arrivals and transparent disclosures."""

    def get_prices(
        self,
        crop: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        mandi: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = REPRESENTATIVE_MANDI_DATA

        if state and state.strip():
            st_clean = state.strip().lower()
            results = [p for p in results if st_clean in p["state"].lower()]

        if district and district.strip():
            dt_clean = district.strip().lower()
            results = [p for p in results if dt_clean in p["district"].lower()]

        if mandi and mandi.strip():
            m_clean = mandi.strip().lower()
            results = [p for p in results if m_clean in p["market"].lower()]

        if crop and crop.strip():
            c_clean = crop.strip().lower()
            results = [
                p for p in results
                if c_clean in p["commodity"].lower() or c_clean in p["commodity_hi"].lower()
            ]

        return results

    def get_markets(self) -> Dict[str, List[Dict[str, str]]]:
        """Groups markets by state."""
        markets_by_state: Dict[str, List[Dict[str, str]]] = {}
        for item in REPRESENTATIVE_MANDI_DATA:
            st = item["state"]
            if st not in markets_by_state:
                markets_by_state[st] = []
            m_entry = {"market": item["market"], "district": item["district"]}
            if m_entry not in markets_by_state[st]:
                markets_by_state[st].append(m_entry)
        return markets_by_state

    def get_commodities(self) -> List[Dict[str, str]]:
        return COMMODITIES_LIST

mandi_service = MandiService()

