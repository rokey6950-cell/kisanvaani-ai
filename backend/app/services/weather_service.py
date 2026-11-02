"""
KisanVaani AI — Weather Service (Phase 7)
=========================================
Provides IMD Agromet-format weather data and farm advisory engine for all 7 pilot states.

IMPORTANT DISCLOSURE:
- India Meteorological Department (IMD) APIs require written permission for commercial use.
- All data in this service is clearly labeled data_type="sample".
- Never use this data without the "sample" label in production.
- Farmers must be directed to mausam.imd.gov.in for real forecasts.
- Source: knowledge/weather/api_configuration.json → commercial_use_status
"""

from datetime import datetime, date, timezone
from typing import Dict, List, Optional, Any


# ── Pilot-state station catalog ───────────────────────────────────────────────
# 7 states: Haryana, Punjab, UP, Rajasthan, Himachal Pradesh, Uttarakhand, Delhi NCR
# Each record matches IMD Agromet Advisory parameter format (qualitative ranges only).
# All data_type="sample" — NOT live IMD data.

WEATHER_STATIONS: Dict[str, Dict[str, Any]] = {
    # ── Haryana ──────────────────────────────────────────────────────────────
    "karnal": {
        "id": "karnal",
        "location": "Karnal",
        "district": "Karnal",
        "state": "Haryana",
        "state_code": "HR",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 24.5,
        "feels_like": 23.8,
        "humidity": 58,
        "wind_speed": 8.2,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 10,
        "visibility_km": 8.0,
        "condition": "Partly Sunny",
        "condition_hi": "हल्की धूप व अनुकूल मंद हवा",
    },
    "hisar": {
        "id": "hisar",
        "location": "Hisar",
        "district": "Hisar",
        "state": "Haryana",
        "state_code": "HR",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 27.0,
        "feels_like": 28.5,
        "humidity": 42,
        "wind_speed": 12.0,
        "wind_direction": "W",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 5,
        "visibility_km": 10.0,
        "condition": "Hot & Windy",
        "condition_hi": "गर्म व तेज हवाएं",
    },
    "ambala": {
        "id": "ambala",
        "location": "Ambala",
        "district": "Ambala",
        "state": "Haryana",
        "state_code": "HR",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 23.0,
        "feels_like": 22.5,
        "humidity": 62,
        "wind_speed": 7.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 12,
        "visibility_km": 7.0,
        "condition": "Cloudy Intervals",
        "condition_hi": "बादलों के बीच धूप",
    },
    # ── Punjab ───────────────────────────────────────────────────────────────
    "ludhiana": {
        "id": "ludhiana",
        "location": "Ludhiana",
        "district": "Ludhiana",
        "state": "Punjab",
        "state_code": "PB",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 23.0,
        "feels_like": 22.0,
        "humidity": 64,
        "wind_speed": 9.5,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 5,
        "visibility_km": 6.0,
        "condition": "Clear Sky with Morning Fog",
        "condition_hi": "साफ आसमान व सुबह हल्का कोहरा",
    },
    "amritsar": {
        "id": "amritsar",
        "location": "Amritsar",
        "district": "Amritsar",
        "state": "Punjab",
        "state_code": "PB",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 22.0,
        "feels_like": 21.5,
        "humidity": 68,
        "wind_speed": 8.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 8,
        "visibility_km": 5.5,
        "condition": "Foggy Morning",
        "condition_hi": "सुबह कोहरा, बाद में साफ",
    },
    "patiala": {
        "id": "patiala",
        "location": "Patiala",
        "district": "Patiala",
        "state": "Punjab",
        "state_code": "PB",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 24.0,
        "feels_like": 23.0,
        "humidity": 60,
        "wind_speed": 10.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 6,
        "visibility_km": 8.0,
        "condition": "Pleasant Sunny",
        "condition_hi": "सुहावनी धूप",
    },
    # ── Uttar Pradesh ────────────────────────────────────────────────────────
    "lucknow": {
        "id": "lucknow",
        "location": "Lucknow",
        "district": "Lucknow",
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 26.5,
        "feels_like": 28.0,
        "humidity": 72,
        "wind_speed": 7.5,
        "wind_direction": "E",
        "rainfall_mm_last24h": 2.0,
        "rainfall_prob": 35,
        "visibility_km": 6.0,
        "condition": "Partly Cloudy with Humidity",
        "condition_hi": "आंशिक बादल व उमस",
    },
    "agra": {
        "id": "agra",
        "location": "Agra",
        "district": "Agra",
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 28.0,
        "feels_like": 30.0,
        "humidity": 55,
        "wind_speed": 11.0,
        "wind_direction": "W",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 15,
        "visibility_km": 9.0,
        "condition": "Warm & Partly Cloudy",
        "condition_hi": "गर्म व आंशिक बादल",
    },
    "meerut": {
        "id": "meerut",
        "location": "Meerut",
        "district": "Meerut",
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 25.0,
        "feels_like": 24.5,
        "humidity": 65,
        "wind_speed": 8.5,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 20,
        "visibility_km": 7.5,
        "condition": "Hazy Sunny",
        "condition_hi": "धुंधली धूप",
    },
    # ── Rajasthan ────────────────────────────────────────────────────────────
    "jaipur": {
        "id": "jaipur",
        "location": "Jaipur",
        "district": "Jaipur",
        "state": "Rajasthan",
        "state_code": "RJ",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 30.0,
        "feels_like": 31.5,
        "humidity": 38,
        "wind_speed": 15.0,
        "wind_direction": "SW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 5,
        "visibility_km": 12.0,
        "condition": "Hot & Windy",
        "condition_hi": "गर्म व तेज हवाएं",
    },
    "jodhpur": {
        "id": "jodhpur",
        "location": "Jodhpur",
        "district": "Jodhpur",
        "state": "Rajasthan",
        "state_code": "RJ",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 33.0,
        "feels_like": 35.0,
        "humidity": 28,
        "wind_speed": 18.0,
        "wind_direction": "SW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 3,
        "visibility_km": 15.0,
        "condition": "Very Hot & Dry",
        "condition_hi": "बहुत गर्म व शुष्क",
    },
    # ── Himachal Pradesh ─────────────────────────────────────────────────────
    "shimla": {
        "id": "shimla",
        "location": "Shimla",
        "district": "Shimla",
        "state": "Himachal Pradesh",
        "state_code": "HP",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 14.0,
        "feels_like": 12.5,
        "humidity": 72,
        "wind_speed": 6.0,
        "wind_direction": "W",
        "rainfall_mm_last24h": 1.5,
        "rainfall_prob": 30,
        "visibility_km": 5.0,
        "condition": "Cool & Partly Cloudy",
        "condition_hi": "ठंडा व आंशिक बादल",
    },
    "mandi": {
        "id": "mandi",
        "location": "Mandi",
        "district": "Mandi",
        "state": "Himachal Pradesh",
        "state_code": "HP",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 18.0,
        "feels_like": 17.0,
        "humidity": 68,
        "wind_speed": 5.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.5,
        "rainfall_prob": 25,
        "visibility_km": 6.5,
        "condition": "Mild & Cloudy",
        "condition_hi": "हल्का ठंडा व बादल",
    },
    # ── Uttarakhand ──────────────────────────────────────────────────────────
    "dehradun": {
        "id": "dehradun",
        "location": "Dehradun",
        "district": "Dehradun",
        "state": "Uttarakhand",
        "state_code": "UK",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 20.0,
        "feels_like": 19.5,
        "humidity": 75,
        "wind_speed": 6.5,
        "wind_direction": "SW",
        "rainfall_mm_last24h": 3.0,
        "rainfall_prob": 40,
        "visibility_km": 5.0,
        "condition": "Overcast with Light Rain",
        "condition_hi": "बादल व हल्की बारिश",
    },
    "haridwar": {
        "id": "haridwar",
        "location": "Haridwar",
        "district": "Haridwar",
        "state": "Uttarakhand",
        "state_code": "UK",
        "imd_station_note": "IMD Agromet station — station ID must be verified from IMD docs",
        "temp": 22.0,
        "feels_like": 21.5,
        "humidity": 70,
        "wind_speed": 7.0,
        "wind_direction": "SW",
        "rainfall_mm_last24h": 1.0,
        "rainfall_prob": 30,
        "visibility_km": 6.0,
        "condition": "Partly Cloudy with Drizzle",
        "condition_hi": "आंशिक बादल व हल्की फुहार",
    },
    # ── Delhi NCR ────────────────────────────────────────────────────────────
    "delhi": {
        "id": "delhi",
        "location": "Delhi",
        "district": "New Delhi",
        "state": "Delhi NCR",
        "state_code": "DL",
        "imd_station_note": "IMD Safdarjung station — station ID must be verified from IMD docs",
        "temp": 26.0,
        "feels_like": 27.5,
        "humidity": 55,
        "wind_speed": 10.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 8,
        "visibility_km": 7.0,
        "condition": "Sunny with Haze",
        "condition_hi": "धुंध भरी धूप",
    },
    "gurgaon": {
        "id": "gurgaon",
        "location": "Gurgaon (Gurugram)",
        "district": "Gurugram",
        "state": "Delhi NCR / Haryana",
        "state_code": "HR",
        "imd_station_note": "IMD Agromet — nearest station Safdarjung/Palam",
        "temp": 25.5,
        "feels_like": 26.0,
        "humidity": 57,
        "wind_speed": 9.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 8,
        "visibility_km": 6.5,
        "condition": "Partly Sunny",
        "condition_hi": "हल्की धूप",
    },
    # ── Default fallback ─────────────────────────────────────────────────────
    "default": {
        "id": "default",
        "location": "Northern Plain Zone",
        "district": "NCR / Haryana",
        "state": "Delhi NCR / Haryana",
        "state_code": "DL",
        "imd_station_note": "Generic north-India benchmark — not a real IMD station",
        "temp": 25.0,
        "feels_like": 24.2,
        "humidity": 55,
        "wind_speed": 8.0,
        "wind_direction": "NW",
        "rainfall_mm_last24h": 0.0,
        "rainfall_prob": 5,
        "visibility_km": 8.0,
        "condition": "Pleasant Sunny",
        "condition_hi": "सुहावनी धूप व शांत हवा",
    },
}

# ── Station lookup aliases ────────────────────────────────────────────────────
LOCATION_ALIASES: Dict[str, str] = {
    # Haryana
    "haryana": "karnal",
    "karnal": "karnal",
    "hisar": "hisar",
    "hissar": "hisar",
    "ambala": "ambala",
    # Punjab
    "punjab": "ludhiana",
    "ludhiana": "ludhiana",
    "amritsar": "amritsar",
    "patiala": "patiala",
    # UP
    "uttar pradesh": "lucknow",
    "up": "lucknow",
    "lucknow": "lucknow",
    "agra": "agra",
    "meerut": "meerut",
    # Rajasthan
    "rajasthan": "jaipur",
    "jaipur": "jaipur",
    "jodhpur": "jodhpur",
    # Himachal Pradesh
    "himachal pradesh": "shimla",
    "himachal": "shimla",
    "shimla": "shimla",
    "mandi": "mandi",
    # Uttarakhand
    "uttarakhand": "dehradun",
    "dehradun": "dehradun",
    "haridwar": "haridwar",
    # Delhi NCR
    "delhi": "delhi",
    "new delhi": "delhi",
    "ncr": "delhi",
    "gurgaon": "gurgaon",
    "gurugram": "gurgaon",
    "noida": "delhi",
    "faridabad": "gurgaon",
}


def resolve_station_key(location: Optional[str]) -> str:
    """Map a free-text location to a known station key, or return 'default'."""
    if not location:
        return "default"
    loc_clean = location.lower().strip()
    # Direct key match
    if loc_clean in WEATHER_STATIONS:
        return loc_clean
    # Alias match
    for alias, key in LOCATION_ALIASES.items():
        if alias in loc_clean:
            return key
    return "default"


# ── Advisory engines ─────────────────────────────────────────────────────────

def compute_spray_advisory(wind_speed: float, rainfall_prob: int, humidity: int) -> Dict[str, Any]:
    """
    IMD Agromet-inspired spray advisory.
    Thresholds: wind ≤ 10 km/h = safe, 10–15 = caution, >15 = avoid.
    Rain probability: <20% = safe, 20–40% = caution, >40% = avoid.
    """
    if wind_speed > 15 or rainfall_prob > 40:
        status = "danger"
        message = "Avoid spraying. High wind or rain risk."
        message_hi = (
            "आज छिड़काव न करें। हवा तेज है या बारिश की संभावना अधिक है। "
            "कीटनाशक बहकर जल स्रोत या अन्य फसलों को नुकसान पहुंचा सकता है।"
        )
        recommendation_hi = "अगले 2 दिन प्रतीक्षा करें। यदि जरूरी हो तो सुबह 8-10 बजे जांचें।"
    elif wind_speed > 10 or rainfall_prob > 20:
        status = "caution"
        message = "Spray with caution. Moderate wind or some rain chance."
        message_hi = (
            "सावधानी से छिड़काव करें। हवा 10-15 किमी/घंटे है या बारिश की कुछ संभावना है। "
            "सुबह 8-10 बजे, जब हवा कम हो, तब करें।"
        )
        recommendation_hi = "सुबह जल्दी या शाम को छिड़काव करें, जब हवा शांत हो।"
    else:
        status = "good"
        message = "Good spray conditions. Wind speed safe and no rain expected."
        message_hi = (
            "स्प्रे के लिए उत्तम समय। हवा 10 किमी/घंटे से कम है और बारिश नहीं होगी। "
            "सुबह 8 बजे के बाद ओस सूखने पर छिड़काव करें।"
        )
        recommendation_hi = "आज सुबह 8-11 बजे छिड़काव उचित है।"

    return {
        "status": status,
        "message": message,
        "message_hi": message_hi,
        "recommendation_hi": recommendation_hi,
        "wind_speed_kmh": wind_speed,
        "rain_probability_pct": rainfall_prob,
        "humidity_pct": humidity,
    }


def compute_irrigation_advisory(
    temp: float, humidity: int, rainfall_mm: float, rainfall_prob: int
) -> Dict[str, Any]:
    """
    Simple irrigation need indicator based on temperature, humidity and rainfall.
    Not a substitute for actual soil-moisture measurement or ET0 calculations.
    """
    if rainfall_mm > 5 or rainfall_prob > 50:
        needed = False
        message_hi = (
            "हाल ही में वर्षा हुई है या होने वाली है। खेत में पर्याप्त नमी है, "
            "अभी सिंचाई की आवश्यकता नहीं। मिट्टी की नमी स्वयं जांचें।"
        )
        level = "sufficient"
    elif temp > 30 and humidity < 40:
        needed = True
        message_hi = (
            "तापमान अधिक और नमी कम है। वाष्पीकरण अधिक होगा। "
            "फसल की अवस्था अनुसार हल्की-हल्की सिंचाई करें। "
            "जड़ क्षेत्र में नमी बनाए रखें।"
        )
        level = "high_need"
    elif temp > 25 and humidity < 55 and rainfall_mm < 1:
        needed = True
        message_hi = (
            "मौसम गर्म है। यदि फसल संवेदनशील अवस्था (फूल-दाना भराई) में है तो "
            "हल्की सिंचाई की सलाह दी जाती है।"
        )
        level = "moderate_need"
    else:
        needed = False
        message_hi = (
            "वर्तमान मौसम में सिंचाई की तत्काल आवश्यकता नहीं दिखती। "
            "मिट्टी की नमी और फसल अवस्था स्वयं देखकर निर्णय लें।"
        )
        level = "low_need"

    return {
        "needed": needed,
        "level": level,
        "message_hi": message_hi,
        "disclaimer_hi": "यह सामान्य मार्गदर्शन है। वास्तविक सिंचाई निर्णय मिट्टी नमी और फसल अवस्था पर आधारित करें।",
    }


def compute_harvest_advisory(
    rainfall_prob: int, wind_speed: float, rainfall_mm: float
) -> Dict[str, Any]:
    """
    Harvest / threshing safety advisory.
    """
    if rainfall_prob > 40 or rainfall_mm > 5:
        safe = False
        message_hi = (
            "कटाई और गहाई के लिए उचित समय नहीं। बारिश की संभावना अधिक है या "
            "पिछले 24 घंटे में वर्षा हुई है। अनाज गीला हो सकता है। "
            "2-3 दिन प्रतीक्षा करें।"
        )
        level = "unsafe"
    elif rainfall_prob > 20 or wind_speed > 15:
        safe = False
        message_hi = (
            "कटाई-गहाई में सावधानी बरतें। हवा तेज है या बारिश की कुछ संभावना है। "
            "कटी हुई फसल को ढककर रखें।"
        )
        level = "caution"
    else:
        safe = True
        message_hi = (
            "मौसम सूखा और अनुकूल है। कटाई और गहाई सुरक्षित रूप से की जा सकती है। "
            "अनाज भंडारण से पहले सुखाना न भूलें।"
        )
        level = "safe"

    return {
        "safe": safe,
        "level": level,
        "message_hi": message_hi,
        "disclaimer_hi": "वास्तविक कटाई निर्णय फसल पकाव, नमी और स्थानीय परिस्थितियों पर आधारित करें।",
    }


def generate_forecast(station: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    5-day benchmark forecast generated from station base data.
    All data_type="sample" — NOT real IMD forecast.
    """
    base_temp = station["temp"]
    base_rain_prob = station["rainfall_prob"]

    schedule = [
        {"offset": 0, "day_en": "Today", "day_hi": "आज", "temp_adj": 0, "rain_adj": 0, "cond_en": station["condition"], "cond_hi": station["condition_hi"]},
        {"offset": 1, "day_en": "Tomorrow", "day_hi": "कल", "temp_adj": +1, "rain_adj": -2, "cond_en": "Sunny", "cond_hi": "खुली धूप"},
        {"offset": 2, "day_en": "Day 3", "day_hi": "परसों", "temp_adj": -1, "rain_adj": +5, "cond_en": "Partly Cloudy", "cond_hi": "आंशिक बादल"},
        {"offset": 3, "day_en": "Day 4", "day_hi": "चौथा दिन", "temp_adj": -2, "rain_adj": 0, "cond_en": "Clear", "cond_hi": "साफ"},
        {"offset": 4, "day_en": "Day 5", "day_hi": "पांचवां दिन", "temp_adj": +1, "rain_adj": +3, "cond_en": "Mostly Sunny", "cond_hi": "अधिकतर धूप"},
    ]

    forecast = []
    for s in schedule:
        rain_prob = max(0, min(100, base_rain_prob + s["rain_adj"]))
        temp_max = round(base_temp + s["temp_adj"] + 2, 1)
        temp_min = round(base_temp + s["temp_adj"] - 10, 1)
        forecast.append({
            "day": s["day_en"],
            "day_hi": s["day_hi"],
            "temp_max": temp_max,
            "temp_min": temp_min,
            "condition": s["cond_en"],
            "condition_hi": s["cond_hi"],
            "rain_probability": rain_prob,
            "data_type": "sample",
        })

    return forecast


# ── Public API ────────────────────────────────────────────────────────────────

def get_weather_data(location: Optional[str] = None) -> Dict[str, Any]:
    """
    Return full weather + advisory payload for a given location.
    All data labeled data_type='sample'.
    """
    key = resolve_station_key(location)
    station = WEATHER_STATIONS[key]

    spray = compute_spray_advisory(
        station["wind_speed"], station["rainfall_prob"], station["humidity"]
    )
    irrigation = compute_irrigation_advisory(
        station["temp"], station["humidity"],
        station["rainfall_mm_last24h"], station["rainfall_prob"]
    )
    harvest = compute_harvest_advisory(
        station["rainfall_prob"], station["wind_speed"], station["rainfall_mm_last24h"]
    )
    forecast = generate_forecast(station)

    return {
        "location": station["location"],
        "district": station["district"],
        "state": station["state"],
        "state_code": station["state_code"],
        "observation_date": str(date.today()),
        "retrieval_timestamp": datetime.now(timezone.utc).isoformat(),
        "data_source": "IMD Agromet Advisory Parameters (Benchmark Sample — Non-Commercial Model)",
        "data_type": "sample",
        "imd_disclaimer": (
            "IMD API का व्यावसायिक उपयोग लिखित अनुमति से। "
            "यह डेटा बेंचमार्क नमूना है, वास्तविक IMD डेटा नहीं।"
        ),
        "temperature": station["temp"],
        "feels_like": station["feels_like"],
        "humidity": station["humidity"],
        "wind_speed": station["wind_speed"],
        "wind_direction": station["wind_direction"],
        "rainfall_mm_last24h": station["rainfall_mm_last24h"],
        "rainfall_prob": station["rainfall_prob"],
        "visibility_km": station["visibility_km"],
        "condition": station["condition"],
        "condition_hi": station["condition_hi"],
        "spray_advisory": spray,
        "irrigation_advisory": irrigation,
        "harvest_advisory": harvest,
        "forecast": forecast,
        "resolved_station": key,
    }


def list_locations() -> List[Dict[str, Any]]:
    """Return the catalog of supported pilot-state stations (excluding 'default')."""
    result = []
    for key, station in WEATHER_STATIONS.items():
        if key == "default":
            continue
        result.append({
            "id": station["id"],
            "location": station["location"],
            "district": station["district"],
            "state": station["state"],
            "state_code": station["state_code"],
        })
    return result


def get_imd_status() -> Dict[str, Any]:
    """Return IMD API status disclosure."""
    return {
        "provider": "India Meteorological Department (IMD)",
        "api_status": "pending_official_agreement",
        "commercial_use": "NOT APPROVED — written permission required from IMD nodal officer",
        "non_commercial_use": "Allowed for research and non-commercial purposes per IMD terms",
        "agromet_portal": "https://agromet.imd.gov.in",
        "weather_portal": "https://mausam.imd.gov.in",
        "meghdoot_app": "https://play.google.com/store/apps/details?id=com.imd.meghdoot",
        "data_type_in_use": "sample",
        "data_type_note": (
            "All weather data served by KisanVaani AI is benchmark sample data. "
            "It is NOT live IMD data. Direct farmers to mausam.imd.gov.in for real forecasts."
        ),
        "credential_env_var": "IMD_API_CREDENTIAL",
        "credential_status": "not_configured",
        "source": "knowledge/weather/api_configuration.json",
    }

