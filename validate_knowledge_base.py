#!/usr/bin/env python3
"""Validate the KisanVaani knowledge base. Standard library only.

Usage: python3 validate_knowledge_base.py [path/to/knowledge]
Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""
import json, os, re, sys, datetime

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge")
TODAY = datetime.date.today()

DATA_TYPES = {"official_live", "official_static", "sample", "unverified"}
VERIF = {"verified", "pending_review", "rejected", "expired"}
SRC_STATUS = {"verified_official", "verified_university", "verified_other", "broken_link", "inaccessible", "not_verified", "conflicting_sources"}
CROP_KEYS = {"id", "category", "crop_id", "crop_name", "state", "district", "agro_climatic_zone", "season", "topic", "question",
             "answer_simple", "answer_detailed", "recommendation", "conditions", "source_ids", "verification_status",
             "data_type", "publication_date", "last_verified", "review_required"}
SRC_KEYS = {"source_id", "organization", "source_type", "title", "url", "document_type", "publication_date", "last_verified",
            "verification_status", "claims_supported", "geographic_scope", "notes"}
SCHEME_KEYS = {"id", "scheme_id", "name", "scope", "department", "purpose", "benefits", "eligibility", "exclusion_criteria",
               "application_process", "required_documents", "application_deadline", "official_portal", "helpline",
               "official_notification_url", "source_ids", "verification_status", "last_verified", "data_type"}
QA_KEYS = {"id", "question", "answer_simple", "answer_detailed", "follow_up_questions", "filters", "source_ids",
           "verification_status", "data_type"}
STATES = {"Haryana", "Punjab", "Uttar Pradesh", "Rajasthan", "Himachal Pradesh", "Uttarakhand", "Delhi NCR"}
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL = re.compile(r"^https?://[^\s]+$")
DOSE = re.compile(r"\b\d+(\.\d+)?\s*(ml|g|gm|kg|l|litre|liter)\s*(/|per)\s*(ha|hectare|acre|l|litre|liter|kg|seed)\b", re.I)
PESTICIDE_WORDS = re.compile(r"\b(raxil|tebuconazole|propiconazole|chlorpyrifos|imidacloprid|mancozeb|carbendazim|glyphosate|2,4-d|fungicide|insecticide|herbicide|pesticide dose)\b", re.I)

errors, warnings = [], []
E = lambda m: errors.append(m)
W = lambda m: warnings.append(m)


def load(rel):
    p = os.path.join(ROOT, rel)
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception as ex:  # noqa
        E(f"{rel}: cannot parse JSON ({ex})")
        return None


# 1. parse all files
files = []
for dp, _, fns in os.walk(ROOT):
    for fn in fns:
        if fn.endswith(".json"):
            files.append(os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, "/"))
files.sort()
data = {f: load(f) for f in files}
for f in ("manifest.json", "sources/source_registry.json"):
    if f not in data:
        E(f"missing required file {f}")

# required structure files
REQUIRED = """geography/states.json geography/districts.json geography/agro_climatic_zones.json crops/crop_catalog.json crops/wheat.json
crops/mustard.json crops/rice.json crops/potato.json crops/maize.json crops/bajra.json crops/sugarcane.json crops/cotton.json crops/gram.json
crops/barley.json crops/apple.json crops/vegetables.json soil/soil_types.json soil/soil_testing.json soil/soil_health_card.json
seeds/seed_varieties.json seeds/seed_recommendations.json fertilizers/fertilizer_catalog.json fertilizers/fertilizer_recommendations.json
plant_protection/pests.json plant_protection/diseases.json plant_protection/symptoms.json plant_protection/ipm_recommendations.json
plant_protection/verified_chemical_recommendations.json schemes/national_schemes.json schemes/state_schemes.json schemes/scheme_documents.json
mandi/mandi_catalog.json mandi/commodity_mapping.json mandi/api_configuration.json weather/weather_parameters.json
weather/agromet_advisory_mapping.json weather/api_configuration.json hindi_knowledge/farmer_questions.json hindi_knowledge/simple_answers.json
hindi_knowledge/agricultural_glossary.json sources/source_registry.json sources/source_claim_mapping.json sources/verification_report.json""".split()
for r in REQUIRED:
    if r not in data:
        E(f"missing required file {r}")

# 2. source registry
registry = data.get("sources/source_registry.json") or []
src_ids = {}
for s in registry:
    sid = s.get("source_id")
    if not sid:
        E("source_registry: record without source_id"); continue
    if sid in src_ids:
        E(f"source_registry: duplicate source_id {sid}")
    src_ids[sid] = s
    miss = SRC_KEYS - set(s)
    if miss:
        E(f"{sid}: missing keys {sorted(miss)}")
    if s.get("verification_status") not in SRC_STATUS:
        E(f"{sid}: invalid verification_status {s.get('verification_status')}")
    if s.get("url") is not None and not URL.match(s["url"]):
        E(f"{sid}: malformed url")
    for k in ("publication_date", "last_verified"):
        if s.get(k) and not ISO.match(s[k]):
            E(f"{sid}: {k} not ISO")
    if s.get("verification_status", "").startswith("verified"):
        if s.get("evidence_level") == "report_only":
            E(f"{sid}: marked verified but evidence_level is report_only")
        if not s.get("last_verified") or not s.get("url"):
            E(f"{sid}: verified source needs url and last_verified")

# 3. generic record checks
ids_seen = {}
LIST_FILES_WITH_RECORDS = [f for f in data if isinstance(data[f], list) and f not in ("sources/source_registry.json",)]
for f in LIST_FILES_WITH_RECORDS:
    for i, r in enumerate(data[f]):
        if not isinstance(r, dict):
            E(f"{f}[{i}]: record is not an object"); continue
        rid = r.get("id")
        if not rid:
            E(f"{f}[{i}]: missing id"); continue
        if rid in ids_seen:
            E(f"{f}: duplicate id {rid} (also in {ids_seen[rid]})")
        ids_seen[rid] = f
        if "data_type" in r and r["data_type"] not in DATA_TYPES:
            E(f"{rid}: invalid data_type {r['data_type']}")
        if "verification_status" in r and r["verification_status"] not in VERIF:
            E(f"{rid}: invalid verification_status {r['verification_status']}")
        if f.startswith("sources/source_claim"):
            for s in r.get("source_ids", []):
                if s not in src_ids:
                    E(f"{rid}: unknown source id {s}")
            continue
        sids = r.get("source_ids")
        if sids is not None:
            for s in sids:
                if s not in src_ids:
                    E(f"{rid}: source id {s} not in registry")
            if r.get("verification_status") == "verified" and not sids:
                E(f"{rid}: verified record has no sources")
            if r.get("verification_status") == "verified":
                if not any(src_ids.get(s, {}).get("verification_status", "").startswith("verified") for s in sids):
                    E(f"{rid}: marked verified but none of its sources is verified")
        elif f.startswith(("crops/", "schemes/", "hindi_knowledge/q", "seeds/", "fertilizers/", "plant_protection/")):
            E(f"{rid}: factual record without source_ids")
        for k in ("last_verified", "publication_date", "start_date", "application_deadline"):
            v = r.get(k)
            if v and not (isinstance(v, str) and ISO.match(v)):
                E(f"{rid}: {k}='{v}' is not YYYY-MM-DD")

# 4. schema checks per category
for r in data.get("crops/wheat.json", []):
    miss = CROP_KEYS - set(r)
    if miss:
        E(f"{r.get('id')}: crop record missing {sorted(miss)}")
    st = r.get("state")
    if st is None:
        E(f"{r.get('id')}: crop recommendation has no state (would be treated as universal)")
    elif st not in STATES:
        E(f"{r.get('id')}: unknown state {st}")
    for s in r.get("source_ids", []):
        scope = src_ids.get(s, {}).get("geographic_scope", [])
        if st and scope and "India" not in scope and st not in scope:
            E(f"{r['id']}: state {st} not covered by source {s} scope {scope}")
    rec = r.get("recommendation", {})
    if any(rec.get(k) for k in ("seed_rate", "fertilizer", "irrigation")) and not r.get("source_ids"):
        E(f"{r['id']}: quantitative recommendation without source")
for s in data.get("schemes/national_schemes.json", []):
    miss = SCHEME_KEYS - set(s)
    if miss:
        E(f"{s.get('id')}: scheme missing {sorted(miss)}")
    d = s.get("application_deadline")
    if d:
        if s.get("verification_status") != "verified":
            E(f"{s['id']}: deadline present on unverified scheme")
        elif ISO.match(d) and datetime.date.fromisoformat(d) < TODAY:
            E(f"{s['id']}: application deadline {d} has passed")
    blob = json.dumps(s, ensure_ascii=False)
    if re.search(r"\b\d{12}\b", blob):
        E(f"{s['id']}: possible Aadhaar-like number stored")
for q in data.get("hindi_knowledge/farmer_questions.json", []):
    miss = QA_KEYS - set(q)
    if miss:
        E(f"{q.get('id')}: Q&A missing {sorted(miss)}")
    ans = (q.get("answer_simple") or {}).get("hi") or ""
    if not ans:
        E(f"{q['id']}: empty simple Hindi answer")
    if len(re.split(r"[।.?!]", ans)) - 1 > 6:
        W(f"{q['id']}: simple answer is long for speech")
    if q.get("requires_live_data") and q.get("data_type") == "official_live":
        E(f"{q['id']}: live template labelled official_live")

# 5. safety checks
chem = data.get("plant_protection/verified_chemical_recommendations.json", [])
for r in chem:
    need = ("crop_id", "pest", "state", "registered_use_reference", "dose", "application_stage", "pre_harvest_interval_days", "source_ids")
    miss = [k for k in need if r.get(k) in (None, "", [])]
    if miss:
        E(f"{r.get('id')}: chemical record missing {miss}")
    if r.get("verification_status") != "verified":
        E(f"{r.get('id')}: chemical record must be verified")
for f, d in data.items():
    if f.startswith("sources/"):
        continue
    text = json.dumps(d, ensure_ascii=False)
    # pesticide mentions outside the chemical file
    if f != "plant_protection/verified_chemical_recommendations.json" and PESTICIDE_WORDS.search(text):
        W(f"{f}: mentions pesticide terms; confirm no unsupported advice")
    if f.startswith(("hindi_knowledge", "crops")) and DOSE.search(text):
        for r in (d if isinstance(d, list) else [d]):
            t = json.dumps(r, ensure_ascii=False)
            if DOSE.search(t) and re.search(r"(फफूंद|कीटनाशक|दवा|spray|pesticide|fungicide|insecticide|herbicide)", t, re.I):
                E(f"{r.get('id')}: dose-like value near a pesticide term")
    if re.search(r"haryanvi", text, re.I) and re.search(r"(supports?|supported)\s+haryanvi|haryanvi\s+(is\s+)?supported", text, re.I):
        E(f"{f}: makes a Haryanvi support claim")
for f in ("mandi/api_configuration.json", "weather/api_configuration.json"):
    c = data.get(f) or {}
    blob = json.dumps(c)
    if re.search(r"api[_-]?key\"\s*:\s*\"[A-Za-z0-9]{16,}", blob, re.I):
        E(f"{f}: looks like an embedded credential")
    if c.get("data_type") in ("official_live",) and not c.get("verification_status") == "verified":
        E(f"{f}: config marked official_live but unverified")
m = data.get("mandi/api_configuration.json") or {}
if m.get("resource_id") not in (None,) and m.get("status", "").startswith("blocked"):
    E("mandi config: resource_id set while status is blocked")
w = data.get("weather/api_configuration.json") or {}
if "NOT APPROVED" not in (w.get("commercial_use_status") or "") and "approved" in (w.get("commercial_use_status") or "").lower():
    E("weather config: commercial use claimed approved without evidence")
for f in ("mandi", "weather"):
    for fn, d in data.items():
        if fn.startswith(f + "/") and isinstance(d, list):
            for r in d:
                if r.get("data_type") == "sample" and r.get("data_status") == "live":
                    E(f"{r.get('id')}: sample record labelled live")
# seeds & fertilizers must be state-scoped
for r in data.get("seeds/seed_recommendations.json", []):
    if not r.get("state"):
        E(f"{r['id']}: seed recommendation without state (universal)")
for r in data.get("seeds/seed_varieties.json", []):
    if r.get("display_allowed") and r.get("verification_status") != "verified":
        E(f"{r['id']}: variety displayable but not verified")
for r in data.get("fertilizers/fertilizer_recommendations.json", []):
    if not r.get("state") or not r.get("source_ids"):
        E(f"{r.get('id')}: fertilizer recommendation needs state and sources")

# 6. URL fabrication check: every URL in non-source files must appear in the registry
reg_urls = {s["url"].rstrip("/").lower() for s in registry if s.get("url")}
url_re = re.compile(r"https?://[^\s\"'),]+")
for f, d in data.items():
    if f.startswith("sources/"):
        continue
    for u in set(url_re.findall(json.dumps(d, ensure_ascii=False))):
        if u.rstrip("/").lower() not in reg_urls and not any(u.lower().startswith(x) for x in ("https://pmkisan.gov.in", "https://pmfby.gov.in", "https://pmksy.gov.in", "https://soilhealth.dac.gov.in", "https://agrimachinery.nic.in", "https://mkisan.gov.in", "https://api.data.gov.in/resource/{resource_id}", "https://api.imd.gov.in")):
            W(f"{f}: URL not in source registry: {u}")

# 7. manifest counts
man = data.get("manifest.json") or {}
for f, n in (man.get("record_counts") or {}).items():
    d = data.get(f)
    actual = len(d) if isinstance(d, list) else 1
    if actual != n:
        E(f"manifest count mismatch for {f}: manifest {n}, actual {actual}")
for f in files:
    if f != "manifest.json" and f not in (man.get("record_counts") or {}):
        E(f"manifest missing {f}")

# report
print(f"Files checked : {len(files)}")
print(f"Records       : {len(ids_seen)} (+ {len(registry)} source records)")
print(f"Warnings      : {len(warnings)}")
for x in warnings:
    print("  WARN", x)
print(f"Errors        : {len(errors)}")
for x in errors:
    print("  ERROR", x)
print("RESULT:", "PASS" if not errors else "FAIL")
sys.exit(1 if errors else 0)
