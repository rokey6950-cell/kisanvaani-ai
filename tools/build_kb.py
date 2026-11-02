#!/usr/bin/env python3
"""Generates the KisanVaani knowledge/ tree. Only facts confirmed in the 2026-11-01 verification pass are included."""
import json, os, sys

ROOT = sys.argv[1]
TODAY = "2026-11-01"
SCHEMA_VERSION = "1.0.0"
KB_VERSION = "0.1.0-pilot"


def w(rel, obj):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------------------------------------------------------------- SOURCES
def src(sid, org, stype, title, url, doctype, status, seen, scope, claims, notes, pub=None, verified=True):
    return {
        "source_id": sid, "organization": org, "source_type": stype, "title": title, "url": url,
        "document_type": doctype, "publication_date": pub,
        "last_verified": TODAY if verified else None,
        "verification_status": status,
        "evidence_level": seen,  # fetched_full | search_excerpt | report_only
        "claims_supported": claims, "geographic_scope": scope, "notes": notes,
    }

S = []
S.append(src("src-report-kisanvaani-001", "Perplexity (user-supplied research report)", "secondary_report",
    "KisanVaani AI - Deep Research Report", None, "report", "not_verified", "report_only", ["India"], [],
    "Input report. Its statements are leads, not verified facts. Several of its citations do not support the adjacent claims (see verification_report.json).", verified=False))
S.append(src("src-hau-pop-001", "CCS Haryana Agricultural University", "official_university",
    "Recommendations in Package of Practices (HAU)", "https://hau.ac.in/public/pages-pdf/1543584203.pdf", "pdf",
    "verified_university", "search_excerpt", ["Haryana"],
    ["Normal wheat sowing time for Haryana recommended as 25 Oct-15 Nov instead of 1-25 Nov"],
    "Existence and the sowing-time sentence confirmed from a search excerpt; the full PDF could not be opened. Publication date is not printed in the excerpt (the numeric file name suggests a ~2018 upload, which is NOT a verified date), so the advice may predate newer early-sowing varieties. The same excerpt mentions seed treatment for loose smut with a named fungicide; it was NOT used because registration, dose-stage and region checks were not possible."))
S.append(src("src-hp-agri-wheat-001", "Department of Agriculture, Himachal Pradesh", "official_government",
    "Wheat (Tillage & Sowing) | HP Agriculture", "https://agriculture.hp.gov.in/en/tillage-sowing-wheat/", "web_page",
    "verified_official", "fetched_full", ["Himachal Pradesh"],
    ["HP wheat land preparation", "HP timely/late sowing windows by hill zone", "HP seed rate", "HP row spacing and depth"],
    "Fetched in full. Page carries no publication date."))
S.append(src("src-datagov-current-mandi-001", "Open Government Data (OGD) Platform India", "official_government",
    "Current Daily Price of Various Commodities from Various Markets (Mandi)",
    "https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi", "web_page",
    "verified_official", "fetched_full", ["India"],
    ["Dataset generated through AGMARKNET; daily granularity; wholesale min/max/modal prices", "Catalogue page states: the API for this resource does not exist (Request API button)"],
    "CONFLICTS with the report, which presented this dataset as the API route. Catalogue dates shown: 23/05/2013 and 23/04/2025. No resource ID is displayed on the page."))
S.append(src("src-datagov-variety-mandi-001", "Open Government Data (OGD) Platform India", "official_government",
    "Variety-wise Daily Market Prices Data of Commodity", "https://www.data.gov.in/resource/variety-wise-daily-market-prices-data-commodity", "web_page",
    "verified_official", "search_excerpt", ["India"],
    ["Dataset exists; wholesale max/min/modal prices daily"],
    "Only the description excerpt was seen. The report's claim that this resource has no API was not directly re-confirmed here (the identical statement WAS confirmed for the current-price resource)."))
S.append(src("src-imd-rti-api-001", "India Meteorological Department (RTI reply, file DGM-HQ-33010/1/2025-RTI-HQ)", "official_government",
    "IMD RTI reply on API access", "https://internal.imd.gov.in/section/rti/rticases/20260112_rti_211.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["IMD provides APIs without charge for non-commercial use only"],
    "Official statement dated from an RTI of 27/08/2025 (file name suggests Jan 2026 posting). The report cited this PDF for block-level SANKALP parameters; the excerpt seen does not contain that, so that claim stays unverified."))
S.append(src("src-imd-api-doc-001", "India Meteorological Department", "official_government",
    "IMD API doc (warnings through APIs and social media)", "https://mausam.imd.gov.in/Forecast/marquee_data/API_doc.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Organisations wishing to use IMD APIs must follow IMD terms and contact the named IMD nodal officer"],
    "Contact details are in the PDF; they are deliberately not copied into this knowledge base."))
S.append(src("src-imd-api-portal-001", "India Meteorological Department", "official_government",
    "IMD API Management Platform", "https://api.imd.gov.in/public/index.php", "web_page",
    "verified_official", "fetched_full", ["India"],
    ["Portal requires account registration and login", "Home page lists city forecast, nowcast, rainfall, marine bulletins and warning services; access described as secure JWT/key based"],
    "api_reference.html was linked but could not be fetched in this pass, so individual endpoints, parameters and the report's 'Agromet Advisory API' claim are NOT verified."))
S.append(src("src-imd-agromet-001", "India Meteorological Department", "official_government",
    "IMD Agromet Advisory Services pages (district/state/national bulletins, KALP, SANKALP)", "https://mausam.imd.gov.in/responsive/agromet_adv_ser_national_past_en.php", "web_page",
    "verified_official", "search_excerpt", ["India"],
    ["IMD publishes district, state and national agromet bulletins; KALP and SANKALP platforms are listed"],
    "Existence of bulletin products confirmed. This does not prove a programmatic agromet API exists."))
S.append(src("src-pmkisan-portal-001", "Department of Agriculture and Farmers Welfare", "official_government",
    "PM-KISAN portal home page", "https://pmkisan.gov.in/", "web_page",
    "verified_official", "search_excerpt", ["India"],
    ["Helpline 155261 / 011-24300606 displayed", "eKYC mandatory for registered farmers; OTP eKYC on portal, biometric at CSC"],
    "Excerpt came from a cached copy that mentions the 16th instalment (Feb 2024); helpline must be re-checked on the live page."))
S.append(src("src-pmkisan-scheme-doc-001", "Department of Agriculture and Farmers Welfare", "official_government",
    "PM Kisan Samman Nidhi scheme document", "https://fw.pmkisan.gov.in/Documents/PMKisanSamanNidhi.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Rs 6,000 per year in three equal instalments of Rs 2,000 every four months", "Central Sector scheme with 100% GoI funding", "Exclusion categories exist"],
    "Excerpt is from the original 2018-19 scheme document; scope was later widened to all landholding families (see PIB source)."))
S.append(src("src-pmkisan-faq-001", "Department of Agriculture and Farmers Welfare", "official_government",
    "PM-KISAN FAQ", "https://fw.pmkisan.gov.in/Documents/FAQPMKISAN.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Three equal instalments of Rs 2,000 every 4 months; first instalment w.e.f. 01.12.2018"], "Excerpt only."))
S.append(src("src-pmkisan-opguide-001", "Department of Agriculture and Farmers Welfare", "official_government",
    "PM-KISAN Operational Guidelines", "https://PMkisan.gov.in/Documents/OPERATIONAL%20GUIDELINES.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Operational guidelines exist; first instalment period 01.12.2018-31.03.2019"], "Excerpt only. Read the full PDF before writing detailed eligibility."))
S.append(src("src-pib-pmkisan-001", "Press Information Bureau / DA&FW", "official_government",
    "PM-KISAN FAQ document (PIB, Nov 2021)", "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2021/nov/doc2021112361.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Documents/information needed for enrolment include name, age, gender, category and Aadhaar number", "Farmers' Corner on portal shows status; grievance via district committee"],
    "Excerpt only; Aadhaar handling must stay on the official portal."))
S.append(src("src-pib-pmkisan-2020-001", "Press Information Bureau / DA&FW", "official_government",
    "PM-KISAN press conference deck, 24 Feb 2020", "https://static.pib.gov.in/WriteReadData/userfiles/Press%20conference_24-Feb-2020.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Scheme extended to all landholding farmers by Cabinet decision dated 31.5.2019"], "Excerpt only."))
S.append(src("src-dot-14447-001", "Department of Telecommunications", "official_government",
    "Allocation of short code 14447 to DA&FW as PMFBY helpline", "https://dotws.cdot.in/sites/default/files/short%20code%2014447%20to%20Deptt%20of%20Agriculture%20GOI.pdf?download=1", "pdf",
    "verified_official", "search_excerpt", ["India"], ["Short code 14447 allocated to PMFBY helpline"], "Excerpt only."))
S.append(src("src-lokSabha-krph-001", "Parliament of India (Lok Sabha reply)", "official_government",
    "Parliamentary reply on Krishi Rakshak Portal and Helpline", "https://eparlib.sansad.in/bitstream/123456789/2985398/1/AU2508_gdhK8C.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Krishi Rakshak Portal and Helpline launched Jan 2024 with single toll-free number 14447"], "Excerpt only."))
S.append(src("src-udalguri-pmfby-001", "District Administration Udalguri, Assam (official circular)", "official_government",
    "Dissemination of helpline information for crop loss reporting under PMFBY", "https://udalguri.assam.gov.in/sites/default/files/public_utility/COs.pdf", "pdf",
    "verified_official", "search_excerpt", ["India"],
    ["Krishi Rakshak helpline 14447 and PMFBY WhatsApp chatbot 7065514447"],
    "A district-level official circular, not the pmfby.gov.in page the report cited. Re-check on pmfby.gov.in."))
S.append(src("src-gnani-livekit-001", "Gnani.ai (vendor documentation)", "vendor_documentation",
    "Gnani LiveKit plugin documentation", "https://docs.gnani.ai/livekit/introduction.md", "web_page",
    "verified_other", "fetched_full", ["India"],
    ["Prisma v2.5 supports ten languages; Timbre v2.5 and v3.0 exist; timbre-v2.0 retired; Prisma v3.0 adds multi-language detection and codemix",
     "Auth is via API key (env GNANI_API_KEY); no Haryanvi language code appeared in the pages fetched"],
    "The full per-language tables live on other docs pages that were not fetched. Haryanvi support is therefore UNCONFIRMED; treat as accent testing only."))
S.append(src("src-gnani-hf-001", "Gnani.ai (Hugging Face model card)", "vendor_documentation",
    "Gnani Prisma v2.5 / Timbre integration card", "https://huggingface.co/gnani-ai/gnani", "web_page",
    "verified_other", "search_excerpt", ["India"],
    ["Prisma v2.5 and Timbre support 10+ Indian languages; languages outside the supported ten are listed as unsupported"], "Excerpt only."))
S.append(src("src-greenalerts-wh1309-001", "GreenAlerts (news)", "news",
    "HAU unveils new heat-tolerant late-sown wheat variety WH 1309", "https://www.greenalerts.in/agriculture/hau-unveils-new-heat-tolerant-late-sown-wheat-variety-ready-in-125-days/", "web_page",
    "verified_other", "search_excerpt", ["Haryana"],
    ["News report: WH 1309 for late sowing, 1-20 Dec, 125 kg seed/ha"],
    "Secondary news report. Use only as a lead; confirm on hau.ac.in before showing farmers."))

# Report-cited but NOT verified
def unv(sid, org, stype, title, url, scope, notes, status="not_verified"):
    return src(sid, org, stype, title, url, "web_page", status, "report_only", scope, [], notes, verified=False)

S += [
 unv("src-icar-wheat-node2632-001", "ICAR", "official_government", "ICAR wheat recommendations (node/2632)", "https://icar.org.in/en/node/2632", ["India"], "Cited by the report; not opened."),
 unv("src-icar-landmark-001", "ICAR", "official_government", "ICAR landmark varieties", "https://icar.org.in/en/crop-science/landmark-varieties", ["India"], "Cited for HD 2967, DBW 187, HD 3226, HDCSW 18; not opened, so variety suitability is unverified."),
 unv("src-epubs-up-wheat-001", "ICAR epubs (Journal of Wheat Research)", "official_university", "Western UP wheat variety article", "https://epubs.icar.org.in/index.php/JWR/article/download/100826/39807/260742", ["Uttar Pradesh"], "Cited for UP variety lists; not opened."),
 unv("src-iiswc-001", "ICAR-IISWC", "official_government", "ICAR-IISWC new wheat varieties, Raipur block Dehradun", "https://www.icar.org.in/en/icar-iiswc-introduces-new-wheat-varieties-farmers-raipur-block-dehradun", ["Uttarakhand"], "Cited for first irrigation ~35 days after sowing; not opened. Independent web results quote CRI at 20-25 DAS, so irrigation timing is CONFLICTING and withheld."),
 unv("src-meg-wheat-001", "Meghalaya Agriculture (megagriculture.gov.in)", "official_government", "Wheat package of practices (Meghalaya)", "https://megagriculture.gov.in/public/package_of_practice_wheat.aspx", ["Meghalaya"], "Not opened. It is a Meghalaya package; its seed rate (100 kg/ha), depth (5-6 cm), spacing and urea/SSP/MOP doses are REJECTED for Northern India use.", status="not_verified"),
 unv("src-pmfby-guidelines-001", "Department of Agriculture and Farmers Welfare (PMFBY)", "official_government", "PMFBY guidelines page", "https://www.pmfby.gov.in/guidelines", ["India"], "Report's cited page; not opened in this pass."),
 unv("src-pmkisan-registration-001", "DA&FW (PM-KISAN)", "official_government", "PM-KISAN registration form page", "https://pmkisan.gov.in/RegistrationFormupdated.aspx", ["India"], "Cited for Aadhaar-authenticated registration; not opened."),
 unv("src-agri-haryana-001", "Haryana Agriculture & Farmers Welfare Department", "official_government", "Haryana Agriculture Department portal", "https://agri.haryana.gov.in/", ["Haryana"], "Starting point only; no scheme or package page verified."),
 unv("src-haryana-gov-unrelated-001", "Haryana Government portal", "official_government", "haryana.gov.in pages cited for data.gov.in API route/auth and IMD capabilities", "https://www.haryana.gov.in/departments/", ["Haryana"], "Citation audit: the report cites haryana.gov.in pages for data.gov.in API route, API-key and IMD capability claims. These are unrelated sources and were not used.", status="not_verified"),
 unv("src-agmarknet-001", "AGMARKNET (DMI, Ministry of Agriculture)", "official_government", "AGMARKNET portal", "https://agmarknet.gov.in/", ["India"], "Not opened."),
 unv("src-pmksy-001", "PMKSY", "official_government", "PMKSY portal", "https://pmksy.gov.in/", ["India"], "Not opened."),
 unv("src-soilhealth-001", "DA&FW Soil Health Card", "official_government", "Soil Health Card portal", "https://soilhealth.dac.gov.in/", ["India"], "Not opened."),
 unv("src-agrimachinery-001", "DA&FW Agricultural Mechanization", "official_government", "Agri-machinery portal", "https://agrimachinery.nic.in/", ["India"], "Not opened."),
 unv("src-mkisan-001", "mKisan", "official_government", "mKisan portal", "https://mkisan.gov.in/", ["India"], "Not opened."),
 unv("src-ppqs-cibrc-001", "PPQS / CIB&RC", "official_government", "CIB&RC registered pesticide information", "https://ppqs.gov.in/divisions/cib-rc", ["India"], "Not opened; no pesticide data used."),
 unv("src-imd-api-reference-001", "India Meteorological Department", "official_government", "IMD API reference", "https://api.imd.gov.in/public/api_reference.html", ["India"], "Fetch was refused in this pass, so endpoint names/parameters are not verified."),
]
SOURCE_IDS = {s["source_id"] for s in S}
w("sources/source_registry.json", S)

# ---------------------------------------------------------------- GEOGRAPHY
states = [
 ("haryana", "Haryana", "हरियाणा", "state", "plains"),
 ("punjab", "Punjab", "पंजाब", "state", "plains"),
 ("uttar_pradesh", "Uttar Pradesh", "उत्तर प्रदेश", "state", "plains_with_hills"),
 ("rajasthan", "Rajasthan", "राजस्थान", "state", "plains_arid"),
 ("himachal_pradesh", "Himachal Pradesh", "हिमाचल प्रदेश", "state", "hill"),
 ("uttarakhand", "Uttarakhand", "उत्तराखंड", "state", "hill_and_plains"),
 ("delhi_ncr", "Delhi NCR", "दिल्ली एनसीआर", "region", "peri_urban"),
]
w("geography/states.json", [{
  "id": f"geo-state-{k}", "state_id": k, "name": {"en": en, "hi": hi}, "kind": kind, "terrain_class": terr,
  "lgd_code": None, "pilot_priority": 1 if k == "haryana" else None,
  "notes": ("Delhi NCR is a region: NCT of Delhi plus NCR districts of Haryana, UP and Rajasthan. District membership must come from an official NCR list; not yet added." if k == "delhi_ncr" else None),
  "source_ids": ["src-report-kisanvaani-001"], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": None, "review_required": True} for k, en, hi, kind, terr in states])
w("geography/districts.json", [])
zones = [("nwpz", "North Western Plains Zone"), ("nepz", "North Eastern Plains Zone"), ("central", "Central Zone"), ("nhz", "Northern Hill Zone")]
w("geography/agro_climatic_zones.json", [{
  "id": f"zone-wheat-{k}", "zone_id": k, "name": {"en": n, "hi": None}, "scheme": "ICAR wheat mega-zones as named in the report",
  "states": None, "source_ids": ["src-report-kisanvaani-001"], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": None, "review_required": True,
  "notes": "Zone names come from the report's reading of ICAR material (not opened). State-to-zone mapping is not asserted."} for k, n in zones])

# ---------------------------------------------------------------- CROPS
def crop(rid, crop_id, en, hi, state, season, topic, q_hi, q_en, simple_hi, simple_en, det_hi, det_en, rec, cond, sids, vs, pub=None, review=False, notes=None, zone=None):
    return {
        "id": rid, "category": "crop_advisory", "crop_id": crop_id, "crop_name": {"en": en, "hi": hi},
        "state": state, "district": None, "agro_climatic_zone": zone, "season": season, "topic": topic,
        "question": {"hi": q_hi, "en": q_en}, "answer_simple": {"hi": simple_hi, "en": simple_en},
        "answer_detailed": {"hi": det_hi, "en": det_en},
        "recommendation": {"sowing_window": None, "seed_rate": None, "seed_depth": None, "row_spacing": None,
                           "irrigation": None, "fertilizer": None, "soil_requirement": None, "land_preparation": None, **rec},
        "conditions": {"irrigation_status": None, "sowing_type": None, "soil_type": None, **cond},
        "source_ids": sids, "verification_status": vs, "data_type": "official_static",
        "publication_date": pub, "last_verified": TODAY, "review_required": review, "notes": notes}

WHEAT = []
WHEAT.append(crop("crop-wheat-haryana-sowing-001", "wheat", "Wheat", "गेहूं", "Haryana", "Rabi", "Sowing",
  "हरियाणा में गेहूं की बुवाई कब करें?", "When should wheat be sown in Haryana?",
  "हरियाणा के लिए चौधरी चरण सिंह हरियाणा कृषि विश्वविद्यालय ने गेहूं की सामान्य बुवाई का समय 25 अक्टूबर से 15 नवंबर बताया है। किस्म और खेत की स्थिति के अनुसार सलाह बदल सकती है। अपने जिले की ताज़ा सलाह के लिए नज़दीकी कृषि विज्ञान केंद्र से पूछें।",
  "CCS Haryana Agricultural University recommends 25 October to 15 November as the normal wheat sowing period for Haryana. Advice can change with variety and field condition. Check with your nearest KVK for current district advice.",
  "विश्वविद्यालय की पुरानी सिफारिश में सामान्य बुवाई का समय 1 से 25 नवंबर की जगह 25 अक्टूबर से 15 नवंबर करने को कहा गया है। देर से बुवाई की किस्म, बीज दर और खाद अलग हो सकती है, इसलिए यहां उनका कोई आंकड़ा नहीं दिया गया है।",
  "The HAU package recommends moving the normal sowing window to 25 Oct-15 Nov instead of 1-25 Nov. Variety, seed rate and fertiliser differ for late sowing, so none are given here.",
  {"sowing_window": "25 October - 15 November (normal sowing)"}, {"sowing_type": "normal/timely"},
  ["src-hau-pop-001"], "pending_review", review=True,
  notes="Full PDF not opened and its date is unknown; may predate early-sowing (October) varieties. Re-confirm against the current HAU package of practices.", zone=None))
hp_srcs = ["src-hp-agri-wheat-001"]
WHEAT.append(crop("crop-wheat-himachal-landprep-001", "wheat", "Wheat", "गेहूं", "Himachal Pradesh", "Rabi", "Land preparation",
  "हिमाचल में गेहूं के लिए खेत कैसे तैयार करें?", "How should land be prepared for wheat in Himachal Pradesh?",
  "हिमाचल कृषि विभाग के अनुसार गेहूं के लिए अच्छे जल निकास वाली मध्यम दोमट ज़मीन सबसे उपयुक्त है। गहरी जुताई के बाद देसी हल से एक-दो जुताई करें और ढेले तोड़ दें। धान के बाद गेहूं लेना हो तो एक जुताई और करें।",
  "HP Agriculture says medium loamy, well-drained land is best. After deep ploughing give 1-2 ploughings with the local plough and break clods; add one more ploughing after paddy.",
  "यह सलाह हिमाचल प्रदेश कृषि विभाग के पन्ने से है। दूसरे राज्यों के लिए इसे अपने आप लागू न करें।",
  "This is from the HP Department of Agriculture page and should not be applied to other states automatically.",
  {"land_preparation": "Deep ploughing, then 1-2 ploughings with local plough; break clods; one extra ploughing if following paddy", "soil_requirement": "Medium loamy land with good drainage"},
  {"soil_type": "medium loamy, well drained"}, hp_srcs, "verified"))
WHEAT.append(crop("crop-wheat-himachal-sowing-001", "wheat", "Wheat", "गेहूं", "Himachal Pradesh", "Rabi", "Sowing",
  "हिमाचल में गेहूं की बुवाई कब करें?", "When should wheat be sown in Himachal Pradesh?",
  "हिमाचल प्रदेश के निचले और मध्यम पहाड़ी इलाकों में समय पर बुवाई अक्टूबर के आखिरी सप्ताह से 15 नवंबर तक बताई गई है। ऊँचे पहाड़ी इलाकों में यह 1 से 15 अक्टूबर है। देर से बुवाई पर उत्पादन काफी घट जाता है।",
  "In HP, timely sowing in lower and intermediate hill areas is the last week of October to 15 November; in high mountain areas 1-15 October. Late sowing sharply reduces yield.",
  "देर से बुवाई: निचले और मध्यम पहाड़ी इलाकों में सिंचित खेत में दिसंबर के अंत तक, बारानी में बारिश देखकर दिसंबर के अंत तक। ऊँचे इलाकों में सिंचित में 1 अक्टूबर तक और बारानी में 15 अक्टूबर तक।",
  "Late sowing: lower/intermediate hills by end December (irrigated), rainfall-dependent but by end December (unirrigated); high mountain areas till 1 Oct (irrigated) and 15 Oct (unirrigated).",
  {"sowing_window": {
     "timely": {"lower_hill": "last week of October - 15 November", "intermediate_hill": "last week of October - 15 November", "high_mountain": "1 - 15 October"},
     "late": {"lower_and_intermediate_hill_irrigated": "by end of December", "lower_and_intermediate_hill_unirrigated": "rain-dependent, by end of December",
              "high_mountain_irrigated": "till 1 October", "high_mountain_unirrigated": "till 15 October"}}},
  {"sowing_type": "timely and late"}, hp_srcs, "verified"))
WHEAT.append(crop("crop-wheat-himachal-seedrate-001", "wheat", "Wheat", "गेहूं", "Himachal Pradesh", "Rabi", "Seed rate",
  "हिमाचल में गेहूं का बीज कितना डालें?", "What seed rate for wheat in Himachal Pradesh?",
  "हिमाचल कृषि विभाग के अनुसार समय पर बुवाई के लिए 100 किलो प्रति हेक्टेयर बीज काफी है। बारानी इलाकों में 20 दिसंबर के बाद बुवाई के लिए 150 किलो प्रति हेक्टेयर बीज बताया गया है।",
  "HP Agriculture: 100 kg/ha is sufficient for timely sowing; 150 kg/ha for rainfed areas sown after 20 December.",
  "यह आंकड़ा केवल हिमाचल प्रदेश के लिए है। हरियाणा, पंजाब या उत्तर प्रदेश में इसे अपने आप लागू न करें।",
  "This figure is for Himachal Pradesh only; do not apply automatically to Haryana, Punjab or UP.",
  {"seed_rate": {"timely_sowing": "100 kg/ha", "rainfed_after_20_december": "150 kg/ha"}},
  {"sowing_type": "timely; rainfed late"}, hp_srcs, "verified"))
WHEAT.append(crop("crop-wheat-himachal-spacing-001", "wheat", "Wheat", "गेहूं", "Himachal Pradesh", "Rabi", "Row spacing and depth",
  "हिमाचल में गेहूं की कतार की दूरी और गहराई कितनी रखें?", "What row spacing and depth for wheat in Himachal Pradesh?",
  "हिमाचल कृषि विभाग कतार में बुवाई की सलाह देता है, जिसमें कतार से कतार 22 सेंटीमीटर रखें। बीज 5 सेंटीमीटर से ज्यादा गहरा न डालें। छिटकवां विधि में निराई कठिन होती है और उपज घटती है।",
  "HP Agriculture recommends line sowing with 22 cm row spacing and seed no deeper than 5 cm. Broadcasting makes weeding difficult and lowers yield.",
  "यह सलाह हिमाचल प्रदेश के लिए है।", "Advice is for Himachal Pradesh.",
  {"row_spacing": "22 cm", "seed_depth": "not more than 5 cm"}, {"sowing_type": "line sowing"}, hp_srcs, "verified"))
w("crops/wheat.json", WHEAT)

CATALOG = [
 ("wheat", "Wheat", "गेहूं", "Rabi", ["Haryana", "Punjab", "Uttar Pradesh", "Rajasthan", "Himachal Pradesh", "Uttarakhand"], 1),
 ("mustard", "Mustard", "सरसों", "Rabi", ["Haryana", "Rajasthan", "Uttar Pradesh"], 2),
 ("rice", "Rice / Paddy", "धान", "Kharif", ["Punjab", "Haryana", "Uttar Pradesh"], 3),
 ("potato", "Potato", "आलू", "Rabi", ["Uttar Pradesh", "Punjab", "Haryana", "Himachal Pradesh"], 4),
 ("maize", "Maize", "मक्का", "Kharif", ["Rajasthan", "Haryana", "Punjab", "Uttar Pradesh", "Himachal Pradesh"], 5),
 ("bajra", "Bajra (Pearl millet)", "बाजरा", "Kharif", ["Rajasthan", "Haryana"], 6),
 ("sugarcane", "Sugarcane", "गन्ना", "Annual", ["Uttar Pradesh", "Haryana", "Uttarakhand"], 7),
 ("cotton", "Cotton", "कपास", "Kharif", ["Punjab", "Haryana", "Rajasthan"], 8),
 ("gram", "Gram / Chickpea", "चना", "Rabi", ["Rajasthan", "Haryana", "Uttar Pradesh"], 9),
 ("barley", "Barley", "जौ", "Rabi", ["Rajasthan", "Haryana", "Uttar Pradesh"], 10),
 ("apple", "Apple", "सेब", "Perennial", ["Himachal Pradesh", "Uttarakhand"], 11),
 ("vegetables", "Vegetables (tomato, onion, cauliflower, cabbage, peas)", "सब्जियां", "Various", ["Delhi NCR", "Punjab", "Himachal Pradesh", "Uttarakhand"], 12),
]
w("crops/crop_catalog.json", [{
  "id": f"catalog-{cid}", "crop_id": cid, "name": {"en": en, "hi": hi}, "season_hint": season,
  "priority_rank": rank, "states_listed_in_report": states_, "has_verified_records": cid == "wheat",
  "source_ids": ["src-report-kisanvaani-001"], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": None, "review_required": True,
  "notes": "State list and season come from the report's priority table only; do not infer that every district grows the crop. Season hint is a convenience label, not a verified recommendation."}
  for cid, en, hi, season, states_, rank in CATALOG])
for f in ["mustard", "rice", "potato", "maize", "bajra", "sugarcane", "cotton", "gram", "barley", "apple", "vegetables"]:
    w(f"crops/{f}.json", [])

# ---------------------------------------------------------------- SOIL / SEEDS / FERTILIZERS
w("soil/soil_types.json", [])
w("soil/soil_testing.json", [])
w("soil/soil_health_card.json", [])
w("seeds/seed_varieties.json", [
 {"id": f"seedvar-wheat-{v.lower().replace(' ', '')}-001", "crop_id": "wheat", "variety": v, "state": None, "zone": None,
  "sowing_condition": None, "irrigation_status": None, "display_allowed": False,
  "source_ids": ["src-report-kisanvaani-001", sid], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": None, "review_required": True,
  "notes": "Named in the report (" + note + "). Region and sowing-condition suitability were NOT verified; do not recommend to farmers yet."}
 for v, sid, note in [("HD 2967", "src-icar-landmark-001", "ICAR landmark varieties"), ("DBW 187", "src-icar-landmark-001", "ICAR landmark varieties"),
                      ("HD 3226", "src-icar-landmark-001", "ICAR landmark varieties"), ("HDCSW 18", "src-icar-landmark-001", "ICAR landmark varieties")]
] + [
 {"id": "seedvar-wheat-wh1309-001", "crop_id": "wheat", "variety": "WH 1309", "state": "Haryana", "zone": None,
  "sowing_condition": "late sowing (reported 1-20 December)", "irrigation_status": None, "display_allowed": False,
  "source_ids": ["src-greenalerts-wh1309-001"], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": TODAY, "review_required": True,
  "notes": "News report only (125 kg seed/ha, ~125 days). Confirm on hau.ac.in before use."}])
w("seeds/seed_recommendations.json", [{
  "id": "seedrec-wheat-himachal-001", "crop_id": "wheat", "state": "Himachal Pradesh", "crop_record_id": "crop-wheat-himachal-seedrate-001",
  "seed_rate": {"timely_sowing": "100 kg/ha", "rainfed_after_20_december": "150 kg/ha"}, "applies_only_to": "Himachal Pradesh",
  "source_ids": hp_srcs, "verification_status": "verified", "data_type": "official_static", "last_verified": TODAY, "review_required": False}])
w("fertilizers/fertilizer_catalog.json", [])
w("fertilizers/fertilizer_recommendations.json", [])

# ---------------------------------------------------------------- PLANT PROTECTION
for f in ["pests", "diseases", "symptoms", "ipm_recommendations", "verified_chemical_recommendations"]:
    w(f"plant_protection/{f}.json", [])

# ---------------------------------------------------------------- SCHEMES
def scheme(**kw):
    base = {"application_deadline": None, "required_documents": None, "official_notification_url": None, "state": None}
    base.update(kw)
    return base

SCHEMES = [
 scheme(id="scheme-national-pmkisan-001", scheme_id="pm-kisan", name={"en": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", "hi": "प्रधानमंत्री किसान सम्मान निधि (पीएम-किसान)"},
   scope="national", department="Department of Agriculture and Farmers Welfare, Government of India",
   purpose="Income support to landholding farmer families",
   benefits="Rs 6,000 per year in three equal instalments of Rs 2,000 every four months, paid to the beneficiary's bank account",
   start_date="2018-12-01",
   eligibility="Landholding farmer families; scope was extended from small/marginal farmers to all landholding families by a Cabinet decision dated 31 May 2019. Detailed rules: see operational guidelines.",
   exclusion_criteria="Certain categories are excluded (for example institutional landholders). Full list must be read from the official guidelines; not reproduced here.",
   application_process="Self-registration on the official portal's Farmers Corner, or through a Common Service Centre. eKYC is stated as mandatory (OTP on portal, biometric at CSC).",
   official_portal="https://pmkisan.gov.in/",
   helpline={"numbers": ["155261", "011-24300606"], "note": "Seen on official portal home page (cached copy). Re-check on the live page before display."},
   official_notification_url="https://PMkisan.gov.in/Documents/OPERATIONAL%20GUIDELINES.pdf",
   sensitive_data_policy="Do not collect Aadhaar or bank details in KisanVaani; direct farmers to the official portal or CSC.",
   source_ids=["src-pmkisan-portal-001", "src-pmkisan-scheme-doc-001", "src-pmkisan-faq-001", "src-pmkisan-opguide-001", "src-pib-pmkisan-2020-001", "src-pib-pmkisan-001"],
   verification_status="pending_review", data_type="official_static", last_verified=TODAY, review_required=True,
   notes="Benefit amount, instalment structure and start date confirmed in official documents (excerpts). Detailed eligibility and exclusions not yet transcribed. The report's 'family = husband, wife and minor children' was not re-confirmed. A toll-free 1800-115-526 appears only on non-official sites and is excluded."),
 scheme(id="scheme-national-pmfby-001", scheme_id="pmfby", name={"en": "Pradhan Mantri Fasal Bima Yojana (PMFBY)", "hi": "प्रधानमंत्री फसल बीमा योजना (पीएमएफबीवाई)"},
   scope="national", department="Department of Agriculture and Farmers Welfare, Government of India",
   purpose="Crop insurance against yield loss", benefits=None, eligibility=None, exclusion_criteria=None,
   application_process=None, official_portal="https://pmfby.gov.in/",
   helpline={"numbers": ["14447"], "whatsapp_chatbot": "7065514447", "note": "14447 is confirmed by DoT and a Lok Sabha reply; the WhatsApp number comes from an official district circular."},
   source_ids=["src-dot-14447-001", "src-lokSabha-krph-001", "src-udalguri-pmfby-001", "src-pmfby-guidelines-001"],
   verification_status="pending_review", data_type="official_static", last_verified=TODAY, review_required=True,
   notes="Premium rates, cut-off dates, sum insured and the crop-loss reporting window vary by state/season/notification and were not verified from pmfby.gov.in. Never state them from memory."),
]
for sid, en, hi, portal, ssrc, use in [
  ("pmksy", "PM Krishi Sinchayee Yojana (PMKSY)", "प्रधानमंत्री कृषि सिंचाई योजना", "https://pmksy.gov.in/", "src-pmksy-001", "irrigation coverage and water-use efficiency; state implementation varies"),
  ("soil-health-card", "Soil Health Card scheme", "मृदा स्वास्थ्य कार्ड योजना", "https://soilhealth.dac.gov.in/", "src-soilhealth-001", "soil-testing workflow and nutrient recommendations"),
  ("agri-mechanization", "Agricultural Mechanization schemes", "कृषि यंत्रीकरण योजनाएं", "https://agrimachinery.nic.in/", "src-agrimachinery-001", "machinery subsidies and custom hiring centres"),
  ("mkisan", "mKisan", "एमकिसान", "https://mkisan.gov.in/", "src-mkisan-001", "mobile advisory dissemination")]:
    SCHEMES.append(scheme(id=f"scheme-national-{sid}-001", scheme_id=sid, name={"en": en, "hi": hi}, scope="national",
      department="Department of Agriculture and Farmers Welfare, Government of India", purpose=None, benefits=None, eligibility=None,
      exclusion_criteria=None, application_process=None, official_portal=portal, helpline=None,
      source_ids=[ssrc, "src-report-kisanvaani-001"], verification_status="pending_review", data_type="unverified",
      last_verified=None, review_required=True,
      notes=f"Stub. Report suggests use for: {use}. Portal not opened in this pass; no benefit or eligibility facts recorded."))
w("schemes/national_schemes.json", SCHEMES)
w("schemes/state_schemes.json", [])
w("schemes/scheme_documents.json", [
 {"id": f"schemedoc-{i}", "scheme_id": "pm-kisan", "title": t, "url": u, "source_ids": [s_], "language": "en",
  "verification_status": "verified", "data_type": "official_static", "last_verified": TODAY, "review_required": False}
 for i, (t, u, s_) in enumerate([
   ("PM-KISAN Operational Guidelines", "https://PMkisan.gov.in/Documents/OPERATIONAL%20GUIDELINES.pdf", "src-pmkisan-opguide-001"),
   ("PM-KISAN FAQ", "https://fw.pmkisan.gov.in/Documents/FAQPMKISAN.pdf", "src-pmkisan-faq-001"),
   ("PM Kisan Samman Nidhi scheme document", "https://fw.pmkisan.gov.in/Documents/PMKisanSamanNidhi.pdf", "src-pmkisan-scheme-doc-001")], 1)])

# ---------------------------------------------------------------- MANDI
w("mandi/mandi_catalog.json", [])
w("mandi/commodity_mapping.json", [{
  "id": f"commodity-{cid}", "crop_id": cid, "name": {"en": en, "hi": hi}, "agmarknet_commodity_name": None,
  "source_ids": ["src-report-kisanvaani-001"], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": None, "review_required": True,
  "notes": "AGMARKNET's exact commodity/variety spellings must be read from real API rows before matching."}
  for cid, en, hi, _, _, _ in CATALOG[:11]])
w("mandi/api_configuration.json", {
  "id": "apicfg-mandi-001", "provider": "data.gov.in / AGMARKNET",
  "status": "blocked_unconfirmed",
  "status_reason": "The data.gov.in catalogue page for the current daily mandi price resource states 'The API for this resource does not exist' and offers a Request API button. No working resource ID has been confirmed or tested.",
  "base_url_pattern": "https://api.data.gov.in/resource/{resource_id}",
  "base_url_status": "from report and third-party wrappers; not confirmed against official OGD API docs",
  "resource_id": None,
  "resource_id_note": "Do not invent. A third-party 2021 library lists IDs, but the mapping to the mandi dataset was ambiguous and untested. Obtain the ID from the official data.gov.in resource page after the API is enabled.",
  "api_key_env_var": "DATA_GOV_API_KEY", "api_key_policy": "Server-side environment variable only; never in JSON, frontend code or logs.",
  "supported_query_params": None, "supported_query_params_note": "Report mentions api-key, format, offset/limit and filters[field]; confirm from official docs and a live test.",
  "response_field_mapping": {"state": "State", "district": "District", "market": "Market", "commodity": "Commodity", "variety": "Variety",
                             "grade": "Grade", "arrival_date": "Arrival_Date", "min_price": "Min_Price", "max_price": "Max_Price", "modal_price": "Modal_Price"},
  "response_field_mapping_status": "unverified - field names are presumed; verify on first successful response (price units are typically Rs per quintal but must be confirmed)",
  "pagination": "offset/limit (unverified)", "cache_ttl_minutes": 30, "cache_note": "Report suggests 15-30 minutes; keep <= 30.",
  "freshness_rule": "Reject rows whose arrival_date is older than 3 days when the farmer asks for 'today'; tell the farmer the date shown.",
  "error_handling": {"no_rows": "इस मंडी के लिए आज का सत्यापित भाव उपलब्ध नहीं है।", "api_down": "सरकारी भाव सेवा अभी उपलब्ध नहीं है। कृपया बाद में कोशिश करें।", "never_synthesize_price": True},
  "attribution": "स्रोत: AGMARKNET / data.gov.in; show retrieval timestamp; follow the dataset's Open Government Data licence terms.",
  "fallback_options": ["Request API access for the resource on data.gov.in", "Check AGMARKNET's own services", "Evaluate e-NAM later (not verified)"],
  "source_ids": ["src-datagov-current-mandi-001", "src-datagov-variety-mandi-001", "src-agmarknet-001"],
  "verification_status": "pending_review", "data_type": "unverified", "last_verified": TODAY, "review_required": True})

# ---------------------------------------------------------------- WEATHER
w("weather/weather_parameters.json", [{
  "id": f"wparam-{k}", "parameter": k, "name": {"en": en, "hi": hi}, "unit": None,
  "source_ids": ["src-report-kisanvaani-001"], "verification_status": "pending_review", "data_type": "unverified",
  "last_verified": None, "review_required": True,
  "notes": "Parameter named in the report (Mausam SANKALP block-level list); IMD field names and units not yet verified."}
  for k, en, hi in [("rainfall", "Rainfall", "बारिश"), ("temperature_max", "Maximum temperature", "अधिकतम तापमान"),
                    ("temperature_min", "Minimum temperature", "न्यूनतम तापमान"), ("humidity_max", "Maximum relative humidity", "अधिकतम आर्द्रता"),
                    ("humidity_min", "Minimum relative humidity", "न्यूनतम आर्द्रता"), ("wind_speed", "Wind speed", "हवा की गति")]])
w("weather/agromet_advisory_mapping.json", [])
w("weather/api_configuration.json", {
  "id": "apicfg-weather-001", "provider": "India Meteorological Department (IMD)",
  "status": "needs_credentials_and_permission",
  "platform_url": "https://api.imd.gov.in/public/index.php", "documented_base_url": None,
  "base_url_note": "Platform confirmed; api_reference.html could not be fetched, so the endpoint base URL and paths are unverified.",
  "endpoints": {"city_forecast": None, "location_forecast": None, "rainfall_forecast": None, "current_weather": None,
                "nowcast_district": None, "nowcast_station": None, "agromet_advisory": None},
  "endpoints_note": "Report lists these capability names; confirm each from IMD's API reference after registering. The 'Agromet Advisory API' is unverified.",
  "authentication": "Account registration and login on the IMD API platform; key/JWT based (per platform home page).",
  "credential_env_var": "IMD_API_CREDENTIAL", "credential_policy": "Server-side only; exact variable semantics depend on IMD's auth flow.",
  "district_station_mapping": None, "district_station_mapping_note": "IMD district/station IDs must be taken from IMD docs; not invented.",
  "forecast_fields": None, "advisory_fields": None,
  "cache_ttl_minutes": 60, "cache_note": "Suggested default; tune after reading IMD update frequency.",
  "commercial_use_status": "NOT APPROVED. IMD states (RTI reply) that APIs are free for non-commercial use only; organisations must follow IMD terms and contact the IMD nodal officer named in the IMD API doc. Get written permission before any public/commercial launch.",
  "source_timestamp_required": True,
  "error_handling": {"api_down": "मौसम की सरकारी जानकारी अभी उपलब्ध नहीं है। आप IMD का मौसम या मेघदूत ऐप देख सकते हैं।", "never_synthesize_forecast": True},
  "fallback_options": ["IMD agromet district bulletins (public web pages) with attribution, pending terms review"],
  "source_ids": ["src-imd-rti-api-001", "src-imd-api-doc-001", "src-imd-api-portal-001", "src-imd-agromet-001", "src-imd-api-reference-001"],
  "verification_status": "pending_review", "data_type": "unverified", "last_verified": TODAY, "review_required": True})

# ---------------------------------------------------------------- HINDI Q&A
def qa(i, q_hi, q_en, s_hi, s_en, d_hi, follow, crop_f, state_f, sids, vs, kind="static", dt="official_static", route=None):
    return {"id": f"qa-{i}", "intent": route or i, "question": {"hi": q_hi, "en": q_en},
            "answer_simple": {"hi": s_hi, "en": s_en}, "answer_detailed": {"hi": d_hi, "en": None},
            "follow_up_questions": follow, "filters": {"crop": crop_f, "state": state_f},
            "answer_kind": kind, "requires_live_data": kind == "live_template",
            "linked_record_ids": [], "source_ids": sids, "verification_status": vs, "data_type": dt,
            "last_verified": TODAY, "review_required": vs != "verified"}

QAS = []
q = qa("wheat-sowing-haryana", "गेहूं की बुवाई कब करनी चाहिए?", "When should wheat be sown?",
  WHEAT[0]["answer_simple"]["hi"], WHEAT[0]["answer_simple"]["en"], WHEAT[0]["answer_detailed"]["hi"],
  ["आप किस राज्य और जिले में हैं?", "बुवाई समय पर करनी है या देर से?"], "wheat", "Haryana", ["src-hau-pop-001"], "pending_review")
q["linked_record_ids"] = ["crop-wheat-haryana-sowing-001"]; QAS.append(q)
q = qa("wheat-sowing-himachal", "हिमाचल में गेहूं की बुवाई कब करें?", "When to sow wheat in Himachal?",
  WHEAT[2]["answer_simple"]["hi"], WHEAT[2]["answer_simple"]["en"], WHEAT[2]["answer_detailed"]["hi"],
  ["आपका खेत निचले, मध्यम या ऊँचे पहाड़ी इलाके में है?", "सिंचित है या बारानी?"], "wheat", "Himachal Pradesh", hp_srcs, "verified")
q["linked_record_ids"] = ["crop-wheat-himachal-sowing-001"]; QAS.append(q)
q = qa("wheat-seed-himachal", "गेहूं का बीज कितना डालें?", "How much wheat seed to use?",
  WHEAT[3]["answer_simple"]["hi"], WHEAT[3]["answer_simple"]["en"], WHEAT[3]["answer_detailed"]["hi"],
  ["आप किस राज्य में हैं?"], "wheat", "Himachal Pradesh", hp_srcs, "verified")
q["linked_record_ids"] = ["crop-wheat-himachal-seedrate-001"]; q["notes"] = "Only answer from this record if the farmer's state is Himachal Pradesh; otherwise ask the state and say no verified figure is stored yet."
QAS.append(q)
QAS.append(qa("wheat-first-irrigation", "गेहूं में पहली सिंचाई कब करें?", "When to give the first irrigation to wheat?",
  "पहली सिंचाई का सही समय राज्य, किस्म और बुवाई की तारीख पर निर्भर करता है। अभी मेरे पास इसकी सत्यापित जानकारी नहीं है, इसलिए मैं दिन नहीं बताऊंगा। कृपया अपने राज्य कृषि विश्वविद्यालय या नज़दीकी कृषि विज्ञान केंद्र से पूछें।",
  "The right time depends on state, variety and sowing date. I do not have verified information yet, so I will not give a number of days. Please ask your state agricultural university or nearest KVK.",
  None, ["आप किस राज्य और जिले में हैं?", "गेहूं कब बोया था?", "कौन सी किस्म है?"], "wheat", None, ["src-iiswc-001"], "pending_review", dt="unverified",
  route="wheat-irrigation"))
QAS[-1]["notes"] = "Conflicting figures exist (about 35 days in a report-cited ICAR-IISWC item vs CRI 20-25 DAS on other sites). Withheld until a state package is verified."
QAS.append(qa("mustard-yellow-leaves", "सरसों में पीले पत्ते क्यों आ रहे हैं?", "Why are mustard leaves turning yellow?",
  "पीले पत्तों के कई कारण हो सकते हैं, इसलिए बिना जानकारी के सही कारण बताना ठीक नहीं होगा। कृपया बताइए कि फसल कितने दिन की है, कौन से पत्ते पीले हैं और आप किस जिले में हैं। पक्की पहचान के लिए नज़दीकी कृषि विज्ञान केंद्र या कृषि अधिकारी को खेत दिखाएं।",
  "Yellow leaves can have several causes, so I should not name one without details. Tell me crop age, which leaves are yellow and your district. For a firm diagnosis show the field to your KVK or agriculture officer.",
  None, ["फसल कितने दिन की है?", "ऊपर के पत्ते पीले हैं या नीचे के?", "पत्तों पर धब्बे या कीड़े दिखते हैं?", "आप किस जिले में हैं?"], "mustard", None, [], "pending_review", dt="unverified", route="mustard-yellow-leaves"))
QAS.append(qa("paddy-water", "धान की फसल में पानी कितना देना चाहिए?", "How much water should paddy get?",
  "पानी की मात्रा राज्य, किस्म और फसल की अवस्था पर निर्भर करती है। अभी मेरे पास इसकी सत्यापित जानकारी नहीं है। अपने राज्य की कृषि विश्वविद्यालय की सलाह देखें या नज़दीकी कृषि विज्ञान केंद्र से पूछें।",
  "Water need depends on state, variety and crop stage. I do not have verified information yet. Check your state university's advice or ask your KVK.",
  None, ["आप किस राज्य और जिले में हैं?", "धान की कौन सी किस्म है?", "रोपाई कब की थी?"], "rice", None, [], "pending_review", dt="unverified", route="paddy-water"))
QAS.append(qa("pest-general", "मेरी फसल में कीट लग गए हैं, क्या करूं?", "My crop has pests, what should I do?",
  "पहले यह पहचानना ज़रूरी है कि कौन सा कीट है और कौन सी फसल है। कृपया फसल का नाम, जिला और कीट या नुकसान का लक्षण बताइए। दवा की मात्रा या नाम मैं तभी बताऊंगा जब वह सरकारी स्रोत से सत्यापित हो; तब तक नज़दीकी कृषि विज्ञान केंद्र या कृषि अधिकारी से सलाह लें।",
  "First the pest and crop must be identified. Tell me the crop, district and the damage you see. I will only name a pesticide or dose if it is verified from an official source; until then consult your KVK or agriculture officer.",
  None, ["कौन सी फसल है?", "आप किस जिले में हैं?", "कीट कैसा दिखता है और पौधे के किस हिस्से पर है?"], None, None, ["src-report-kisanvaani-001"], "pending_review", dt="unverified", route="pest-general"))
QAS.append(qa("mandi-price", "आज मेरी मंडी में सरसों का भाव क्या है?", "What is today's mustard price in my mandi?",
  "भाव मैं सीधे सरकारी स्रोत से लाऊंगा, अनुमान से नहीं बताऊंगा। कृपया अपना राज्य, जिला और मंडी का नाम बताइए। अगर आज का सत्यापित भाव उपलब्ध नहीं हुआ तो मैं यही बताऊंगा।",
  "I will fetch the price from the official source, not estimate it. Tell me your state, district and mandi. If today's verified price is unavailable I will say so.",
  None, ["आप किस राज्य में हैं?", "कौन से जिले और मंडी का भाव चाहिए?"], "mustard", None, ["src-datagov-current-mandi-001"], "pending_review", kind="live_template", dt="official_static", route="mandi-price"))
QAS[-1]["notes"] = "Template only. Live price integration is blocked until a working data.gov.in resource API is confirmed."
QAS.append(qa("pm-kisan-benefit", "PM-KISAN योजना का लाभ कैसे मिलेगा?", "How do I get the PM-KISAN benefit?",
  "पात्र भूमिधारक किसान परिवार को साल में 6,000 रुपये मिलते हैं, तीन किस्तों में, हर चार महीने पर 2,000 रुपये, सीधे बैंक खाते में। पंजीकरण आधिकारिक पोर्टल pmkisan.gov.in पर या कॉमन सर्विस सेंटर पर होता है, और ई-केवाईसी ज़रूरी है। आधार या बैंक की जानकारी सिर्फ आधिकारिक पोर्टल पर ही डालें। मदद के लिए हेल्पलाइन 155261 या 011-24300606 पर संपर्क करें।",
  "Eligible landholding farmer families get Rs 6,000 a year in three instalments of Rs 2,000 every four months into the bank account. Register on pmkisan.gov.in or at a CSC; eKYC is required. Share Aadhaar or bank details only on the official portal. Helpline: 155261 or 011-24300606.",
  "कुछ श्रेणियां योजना से बाहर हैं। पात्रता की पूरी सूची के लिए आधिकारिक दिशानिर्देश देखें।",
  ["आपके पास खेती की अपनी ज़मीन है?", "क्या आप पहले से पंजीकृत हैं?"], None, None,
  ["src-pmkisan-portal-001", "src-pmkisan-scheme-doc-001", "src-pib-pmkisan-2020-001"], "pending_review", route="pm-kisan"))
QAS[-1]["linked_record_ids"] = ["scheme-national-pmkisan-001"]
QAS.append(qa("pmfby-insurance", "मेरी फसल का बीमा कैसे करवाएं?", "How do I insure my crop?",
  "फसल बीमा प्रधानमंत्री फसल बीमा योजना के तहत होता है। इसकी जानकारी आधिकारिक पोर्टल pmfby.gov.in, अपने बैंक या कॉमन सर्विस सेंटर से लें। फसल के नुकसान की सूचना या शिकायत के लिए हेल्पलाइन 14447 है। बीमा की आखिरी तारीख राज्य और मौसम के हिसाब से अलग होती है, इसलिए अपने जिले की सूचना ज़रूर देखें।",
  "Crop insurance is under PMFBY. Get details from pmfby.gov.in, your bank or a CSC. For crop-loss reports or complaints call 14447. Cut-off dates vary by state and season, so check your district notice.",
  None, ["आप किस राज्य और जिले में हैं?", "कौन सी फसल और कौन सा मौसम (रबी/खरीफ)?"], None, None,
  ["src-dot-14447-001", "src-lokSabha-krph-001", "src-udalguri-pmfby-001"], "pending_review", route="pmfby"))
QAS[-1]["linked_record_ids"] = ["scheme-national-pmfby-001"]
QAS[-1]["notes"] = "Enrolment channels (bank/CSC/portal) are standard but were only confirmed on non-official sites; verify on pmfby.gov.in."
QAS.append(qa("weather-rain", "अगले कुछ दिनों में बारिश होने की संभावना है क्या?", "Is rain likely in the next few days?",
  "इसके लिए मैं भारतीय मौसम विभाग का ताज़ा पूर्वानुमान देखूंगा, अनुमान नहीं लगाऊंगा। कृपया अपना राज्य और जिला बताइए। अभी यह सेवा जुड़ना बाकी है, इसलिए तब तक IMD का मौसम या मेघदूत ऐप देख सकते हैं।",
  "I will check the latest IMD forecast rather than guess. Tell me your state and district. This service is not connected yet, so meanwhile use the IMD Mausam or Meghdoot app.",
  None, ["आप किस राज्य और जिले में हैं?"], None, None, ["src-imd-api-portal-001", "src-imd-agromet-001"], "pending_review", kind="live_template", dt="official_static", route="weather-rain"))
QAS[-1]["notes"] = "Template only. IMD access needs credentials and written permission for production use."
w("hindi_knowledge/farmer_questions.json", QAS)
w("hindi_knowledge/simple_answers.json", [{
  "id": f"simple-{x['id']}", "question_id": x["id"], "answer_simple": x["answer_simple"], "source_ids": x["source_ids"],
  "verification_status": x["verification_status"], "data_type": x["data_type"], "requires_live_data": x["requires_live_data"],
  "last_verified": x["last_verified"], "review_required": x["review_required"]} for x in QAS])
GL = [("sowing", "बुवाई", "Sowing"), ("irrigation", "सिंचाई", "Irrigation"), ("mandi", "मंडी", "Wholesale market"),
      ("modal_price", "मॉडल भाव", "Modal price (most common traded price)"), ("seed_rate", "बीज दर", "Seed rate"),
      ("rabi", "रबी", "Rabi (winter-sown season)"), ("kharif", "खरीफ", "Kharif (monsoon-sown season)"),
      ("kvk", "कृषि विज्ञान केंद्र (केवीके)", "Krishi Vigyan Kendra (district farm science centre)"),
      ("soil_test", "मिट्टी की जांच", "Soil test"), ("fertilizer", "खाद / उर्वरक", "Fertiliser")]
w("hindi_knowledge/agricultural_glossary.json", [{
  "id": f"gloss-{k}", "term": {"hi": hi, "en": en}, "kind": "glossary", "source_ids": [], "verification_status": "pending_review",
  "data_type": "unverified", "last_verified": None, "review_required": True,
  "notes": "Plain-language vocabulary for the voice assistant; no agronomic claim."} for k, hi, en in GL])

# ---------------------------------------------------------------- CLAIM MAPPING
CL = [
 ("claim-001", "Haryana normal wheat sowing window is 25 Oct-15 Nov (HAU)", ["src-hau-pop-001"], "supported_search_excerpt", "Full PDF unopened; date unknown"),
 ("claim-002", "HP wheat sowing windows by hill zone, seed rate, spacing and depth", ["src-hp-agri-wheat-001"], "supported_fetched", None),
 ("claim-003", "Current daily mandi price dataset has no API on data.gov.in", ["src-datagov-current-mandi-001"], "supported_fetched", "Contradicts the report's API-route claim"),
 ("claim-004", "data.gov.in resource API route is api.data.gov.in/resource/<id> with api-key", [], "unresolved", "Report cited unrelated haryana.gov.in page; official OGD docs not yet read"),
 ("claim-005", "A working mandi resource ID exists", [], "unresolved", "None confirmed"),
 ("claim-006", "IMD APIs are free for non-commercial use only", ["src-imd-rti-api-001"], "supported_search_excerpt", None),
 ("claim-007", "IMD requires contacting its nodal officer to use APIs under IMD terms", ["src-imd-api-doc-001"], "supported_search_excerpt", None),
 ("claim-008", "IMD API platform needs registration/login", ["src-imd-api-portal-001"], "supported_fetched", None),
 ("claim-009", "IMD has a dedicated Agromet Advisory API", ["src-imd-api-reference-001"], "unresolved", "api_reference.html not fetchable in this pass; bulletins confirmed, API not"),
 ("claim-010", "Mausam SANKALP block-level parameters (rain, Tmax/Tmin, RH, wind)", ["src-imd-rti-api-001"], "unresolved", "Cited PDF excerpt does not show this"),
 ("claim-011", "PM-KISAN Rs 6,000/yr in 3 instalments, operational 1 Dec 2018", ["src-pmkisan-scheme-doc-001", "src-pmkisan-faq-001"], "supported_search_excerpt", None),
 ("claim-012", "PM-KISAN extended to all landholding farmers (31 May 2019)", ["src-pib-pmkisan-2020-001"], "supported_search_excerpt", None),
 ("claim-013", "PM-KISAN helpline 155261 / 011-24300606", ["src-pmkisan-portal-001"], "supported_search_excerpt", "Cached page; recheck live"),
 ("claim-014", "PM-KISAN family = husband, wife and minor children", [], "unresolved", "Not re-confirmed"),
 ("claim-015", "PMFBY helpline 14447", ["src-dot-14447-001", "src-lokSabha-krph-001"], "supported_search_excerpt", None),
 ("claim-016", "PMFBY WhatsApp chatbot 7065514447", ["src-udalguri-pmfby-001"], "supported_search_excerpt", "District circular; recheck on pmfby.gov.in"),
 ("claim-017", "Meghalaya wheat package values apply to Northern India", ["src-meg-wheat-001"], "rejected", "Different state; values excluded"),
 ("claim-018", "Wheat first irrigation ~35 days after sowing (ICAR-IISWC)", ["src-iiswc-001"], "unresolved", "Conflicts with CRI 20-25 DAS on other sites; withheld"),
 ("claim-019", "Wheat variety suitability (HD 2967, DBW 187, HD 3226, HDCSW 18, UP lists)", ["src-icar-landmark-001", "src-epubs-up-wheat-001"], "unresolved", "Source pages not opened"),
 ("claim-020", "Gnani supports Haryanvi", ["src-gnani-livekit-001"], "not_supported", "No Haryanvi code found in pages fetched; treat as accent testing"),
 ("claim-021", "Gnani Prisma/Timbre v2.5 support ten Indian languages", ["src-gnani-livekit-001", "src-gnani-hf-001"], "supported", "Newer v3.0 models also exist"),
 ("claim-022", "WH 1309 late-sown variety (1-20 Dec, 125 kg/ha)", ["src-greenalerts-wh1309-001"], "supported_secondary_only", "News report only"),
]
w("sources/source_claim_mapping.json", [{"id": c[0], "claim": c[1], "source_ids": c[2], "status": c[3], "note": c[4]} for c in CL])

# ---------------------------------------------------------------- VERIFICATION REPORT
verified = [s for s in S if s["verification_status"].startswith("verified")]
notver = [s for s in S if s["verification_status"] == "not_verified"]
w("sources/verification_report.json", {
  "id": "verification-report-001", "generated": TODAY, "method": "Web search and page fetches on 2026-11-01. Evidence levels: fetched_full, search_excerpt, report_only.",
  "totals": {"sources_registered": len(S), "verified": len(verified), "verified_fetched_full": len([s for s in verified if s["evidence_level"] == "fetched_full"]),
             "verified_search_excerpt_only": len([s for s in verified if s["evidence_level"] == "search_excerpt"]),
             "not_verified": len(notver), "broken_links": 0, "inaccessible": 1, "conflicting_sources": 1,
             "claims_total": len(CL), "claims_unresolved": len([c for c in CL if c[3] == "unresolved"]),
             "claims_rejected_or_unsupported": len([c for c in CL if c[3] in ("rejected", "not_supported")])},
  "inaccessible": ["https://api.imd.gov.in/public/api_reference.html (fetch refused; endpoint list unverified)"],
  "conflicting_sources": ["Report says current mandi dataset is the API route; data.gov.in page says its API does not exist."],
  "key_findings": [
    "Mandi: no working data.gov.in API/resource ID confirmed. Live mandi answers stay templates until one is tested.",
    "IMD: free for non-commercial use only; written permission needed for production/commercial use. Endpoint details unverified.",
    "Haryanvi: no Gnani confirmation found. Keep as accent testing only. Gnani Prisma/Timbre v3.0 now exist alongside the v2.5 in the project's stack.",
    "The HAU sowing window is confirmed only from a search excerpt of an undated, possibly older package.",
    "Only Himachal Pradesh wheat guidance was fully read from an official page. Haryana, Punjab, UP, Rajasthan and Uttarakhand have no fully verified crop packages yet.",
    "The report's Meghalaya package values were excluded.",
    "The report cites unrelated haryana.gov.in pages for data.gov.in and IMD claims; they were not used."],
  "unverified_claims": [c[0] + ": " + c[1] for c in CL if c[3] == "unresolved"],
  "missing_official_documents": [
    "Current HAU wheat package of practices (full PDF, dated)", "PAU, UP (CSAUK/SVPUAT), Rajasthan (SKRAU/MPUAT), Uttarakhand (GBPUAT) crop packages",
    "Haryana, Punjab, UP, Rajasthan, Uttarakhand state scheme notifications", "PMFBY notification/guidelines from pmfby.gov.in",
    "PM-KISAN full operational guidelines text", "CIB&RC registered pesticide uses and label claims", "LGD district list for all seven regions",
    "IMD API reference and terms", "Official data.gov.in OGD API documentation", "Gnani per-language support tables"],
  "empty_files_and_reasons": {
    "geography/districts.json": "Needs official LGD district list", "crops/*(except wheat, catalog)": "No state-university source verified",
    "soil/*": "No source opened", "fertilizers/*": "Only a rejected Meghalaya package seen; no Northern India doses verified",
    "plant_protection/*": "No registered-use, dose, stage and PHI evidence; chemical advice intentionally empty",
    "schemes/state_schemes.json": "No state scheme page verified", "mandi/mandi_catalog.json": "Needs live API rows",
    "weather/agromet_advisory_mapping.json": "Needs IMD advisory fields"},
  "limitations": [
    "Most 'verified' entries rest on search excerpts, not full documents.", "No API call to data.gov.in or IMD was made (no keys).",
    "Dates of many documents are unknown.", "Hindi answers were written by Claude from verified facts and need native-speaker review."]})

# ---------------------------------------------------------------- MANIFEST
def count(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        d = json.load(f)
    return len(d) if isinstance(d, list) else 1

files = []
for dp, _, fns in os.walk(ROOT):
    for fn in fns:
        if fn.endswith(".json") and fn != "manifest.json":
            files.append(os.path.relpath(os.path.join(dp, fn), ROOT))
files.sort()
w("manifest.json", {
  "kb_name": "KisanVaani AI knowledge base", "kb_version": KB_VERSION, "schema_version": SCHEMA_VERSION, "generated": TODAY,
  "last_verification_date": TODAY,
  "target_regions": [s[1] for s in states],
  "pilot": "Haryana wheat (only partly verified); Himachal Pradesh wheat fully read",
  "languages": {"primary": "hi", "secondary": "en", "haryanvi": "accent testing only; unconfirmed Gnani support"},
  "categories": ["geography", "crops", "soil", "seeds", "fertilizers", "plant_protection", "schemes", "mandi", "weather", "hindi_knowledge", "sources"],
  "record_counts": {f: count(f) for f in files},
  "status_note": "Pilot-scale, accuracy-first. Many files are intentionally empty; see sources/verification_report.json."})
print("built", len(files) + 1, "json files")
