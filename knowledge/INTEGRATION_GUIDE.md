# FastAPI Integration Guide

Python 3.10+, `fastapi`, `uvicorn`, `httpx` (for live clients). Knowledge files are plain JSON, so any model or retrieval layer can sit on top.

## 1. Loading

```python
import json, pathlib
from functools import lru_cache

KB = pathlib.Path(__file__).parent / "knowledge"

def _read(rel):
    return json.loads((KB / rel).read_text(encoding="utf-8"))

@lru_cache
def kb():
    sources = {s["source_id"]: s for s in _read("sources/source_registry.json")}
    crops = [r for f in (KB / "crops").glob("*.json") if f.name != "crop_catalog.json" for r in _read(f"crops/{f.name}")]
    return {
        "sources": sources,
        "crops": crops,
        "schemes": _read("schemes/national_schemes.json") + _read("schemes/state_schemes.json"),
        "qa": _read("hindi_knowledge/farmer_questions.json"),
    }
```

## 2. Search and filters

```python
from fastapi import FastAPI, Query
app = FastAPI()

def with_sources(rec):
    out = dict(rec)
    out["sources"] = [{"id": s, "title": kb()["sources"][s]["title"], "url": kb()["sources"][s]["url"],
                       "organization": kb()["sources"][s]["organization"]} for s in rec.get("source_ids", [])]
    return out

@app.get("/crops/advice")
def crop_advice(crop: str, state: str | None = None, district: str | None = None, topic: str | None = None):
    hits = [r for r in kb()["crops"] if r["crop_id"] == crop
            and (state is None or r["state"] == state)
            and (district is None or r["district"] in (None, district))
            and (topic is None or r["topic"].lower() == topic.lower())]
    if not hits:
        return {"status": "no_verified_record", "answer_hi": "इस जानकारी के लिए मेरे पास सत्यापित रिकॉर्ड अभी नहीं है। कृपया नज़दीकी कृषि विज्ञान केंद्र से पूछें।",
                "follow_up_hi": ["आप किस राज्य और जिले में हैं?"]}
    return {"status": "ok", "records": [with_sources(r) for r in hits]}
```

**State is mandatory for numeric advice.** If the farmer has not given a state, ask for it; never fall back to another state's record.

## 3. Schemes

```python
@app.get("/schemes/{scheme_id}")
def scheme(scheme_id: str):
    s = next((x for x in kb()["schemes"] if x["scheme_id"] == scheme_id), None)
    if not s:
        return {"status": "not_found"}
    return {"status": "ok", "scheme": with_sources(s),
            "notice_hi": "आधार या बैंक की जानकारी सिर्फ आधिकारिक पोर्टल पर ही डालें।"}
```

## 4. Hindi answers for the voice flow

```python
import re

def match_intent(text_hi: str):
    # start simple: keyword rules; swap for embeddings later (the data format does not change)
    rules = {"pm-kisan": r"किसान सम्मान|पीएम.?किसान|PM.?KISAN", "pmfby": r"बीमा", "mandi-price": r"भाव|मंडी",
             "weather-rain": r"बारिश|मौसम", "pest-general": r"कीट|कीड़े"}
    for intent, pat in rules.items():
        if re.search(pat, text_hi, re.I):
            return intent
    return None

@app.post("/ask")
def ask(body: dict):
    intent = match_intent(body["text_hi"])
    q = next((x for x in kb()["qa"] if x["intent"] == intent and
              (x["filters"]["state"] in (None, body.get("state")))), None)
    if not q:
        return {"status": "no_answer", "answer_hi": "मुझे इसका सत्यापित जवाब नहीं मिला। कृपया अपने कृषि अधिकारी या नज़दीकी कृषि विज्ञान केंद्र से पूछें।"}
    return {"status": "ok", "answer_hi": q["answer_simple"]["hi"], "follow_up_hi": q["follow_up_questions"],
            "requires_live_data": q["requires_live_data"], "verification_status": q["verification_status"],
            "data_type": q["data_type"], "sources": with_sources(q)["sources"]}
```

Voice flow: Gnani Prisma STT -> `/ask` -> `answer_hi` -> Gnani Timbre TTS (`language: hi-IN`). Keep the Gnani key in `GNANI_API_KEY` on the server only. Note that Gnani also offers Prisma/Timbre v3.0; confirm model choice against the Gnani docs. Do not advertise Haryanvi.

## 5. Live clients (not ready; blocked)

```python
import os, datetime, httpx

async def mandi_price(state, district, commodity):
    cfg = _read("mandi/api_configuration.json")
    if cfg["resource_id"] is None:
        return {"status": "unavailable", "answer_hi": cfg["error_handling"]["api_down"], "reason": cfg["status_reason"]}
    key = os.environ["DATA_GOV_API_KEY"]        # never in JSON or frontend
    url = cfg["base_url_pattern"].format(resource_id=cfg["resource_id"])
    params = {"api-key": key, "format": "json", "limit": 50,
              "filters[State]": state, "filters[District]": district, "filters[Commodity]": commodity}  # verify names on first response
    async with httpx.AsyncClient(timeout=15) as c:
        rows = (await c.get(url, params=params)).json().get("records", [])
    if not rows:
        return {"status": "no_data", "answer_hi": cfg["error_handling"]["no_rows"]}
    return {"status": "ok", "data_type": "official_live", "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "attribution": cfg["attribution"], "rows": rows}
```

The weather client follows the same pattern but must wait for IMD credentials, the endpoint list from `api_reference.html`, and written permission for production use (`weather/api_configuration.json`). Return `status: "unavailable"` until then. Never synthesise a price or forecast.

## 6. Missing or unverified information

- `verification_status != "verified"`: say so to the farmer in Hindi ("यह जानकारी अभी जांच में है") or withhold numeric values; log for review.
- `display_allowed: false` (seed varieties): never show.
- Serious or uncertain crop problems: refer to a KVK, agricultural university or agriculture officer.

## 7. Example responses

Verified static answer:

```json
{"status": "ok",
 "records": [{"id": "crop-wheat-himachal-sowing-001", "state": "Himachal Pradesh", "topic": "Sowing",
   "answer_simple": {"hi": "हिमाचल प्रदेश के निचले और मध्यम पहाड़ी इलाकों में समय पर बुवाई ... 15 नवंबर तक बताई गई है।"},
   "verification_status": "verified", "data_type": "official_static", "last_verified": "2026-11-01",
   "sources": [{"id": "src-hp-agri-wheat-001", "title": "Wheat (Tillage & Sowing) | HP Agriculture",
                "url": "https://agriculture.hp.gov.in/en/tillage-sowing-wheat/", "organization": "Department of Agriculture, Himachal Pradesh"}]}]}
```

Live data unavailable:

```json
{"status": "unavailable", "answer_hi": "सरकारी भाव सेवा अभी उपलब्ध नहीं है। कृपया बाद में कोशिश करें।",
 "reason": "The data.gov.in catalogue page states the API for this resource does not exist."}
```

No verified record:

```json
{"status": "no_verified_record", "answer_hi": "इस जानकारी के लिए मेरे पास सत्यापित रिकॉर्ड अभी नहीं है। कृपया नज़दीकी कृषि विज्ञान केंद्र से पूछें।",
 "follow_up_hi": ["आप किस राज्य और जिले में हैं?"]}
```
