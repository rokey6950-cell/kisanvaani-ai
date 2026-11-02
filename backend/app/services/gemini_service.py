"""
KisanVaani AI — Gemini AI Fallback & Synthesis Service
======================================================
Provides:
1. Automatic AI agricultural advisory when verified local knowledge base records
   do not cover a farmer's specific question.
2. Hybrid RAG Scheme Synthesis: combines verified local government scheme facts
   with Gemini AI to produce a single, cohesive, easy-to-understand Hindi response
   for farmers without any technical meta-labels, brackets, or separate options.
3. Hybrid RAG Crop Advisory Synthesis: combines verified local crop and agronomic
   packages (HAU, PAU, ICAR, DMI) with Gemini AI for unified, natural Hindi farming advice.
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

from ..core.config import settings

logger = logging.getLogger("kisanvaani.gemini")

GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_ENDPOINT_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

AGRICULTURAL_SYSTEM_PROMPT = """आप KisanVaani AI के एक अत्यंत अनुभवी, मददगार और संवेदनशील भारतीय कृषि वैज्ञानिक सहायक हैं। 
आपका कार्य उत्तर भारत (हरियाणा, पंजाब, राजस्थान, उत्तर प्रदेश, हिमाचल, उत्तराखंड, दिल्ली NCR) के किसानों को उनकी स्थानीय परिस्थितियों के अनुकूल खेती की सही सलाह देना है।

नियम व दिशानिर्देश:
1. भाषा: सरल, आदरपूर्ण और स्वाभाविक हिंदी में जवाब दें। तकनीकी शब्दों को कोष्ठक में या सरल अर्थ के साथ समझाएं।
2. संरचना: 
   - किसान भाई को आदर से संबोधित करें (उदा. 'किसान भाई, ...')।
   - मुख्य बातें 3-4 छोटे बिंदुओं में बताएं ताकि किसान सुनकर या पढ़कर आसानी से समझ सके।
   - आवाज (TTS) के लिए वाक्य छोटे और प्रवाहपूर्ण रखें।
3. कीटनाशक व खाद सुरक्षा:
   - किसी भी केमिकल कीटनाशक या खरपतवारनाशक की मनगढ़ंत या अत्यधिक खुराक न बताएं।
   - जैविक या प्राकृतिक उपायों को प्राथमिकता दें। रासायनिक दवा के मामले में स्थानीय कृषि विज्ञान केंद्र (KVK) या राज्य कृषि विभाग से पुष्टि करने की स्पष्ट सलाह दें।
4. उत्तर की लंबाई: 70 से 120 शब्दों के बीच रखें।
"""


def generate_agricultural_fallback(
    query: str,
    state: Optional[str] = None,
    crop: Optional[str] = None,
    timeout_seconds: int = 10
) -> Optional[Dict[str, Any]]:
    """
    Calls Google Gemini AI to answer agricultural questions when local knowledge has no record.
    Returns structured dict with Hindi answer, or None if unavailable.
    """
    api_key = settings.GEMINI_API_KEY.strip()
    if not api_key:
        logger.info("Gemini API key is not configured; skipping AI fallback.")
        return None

    context_details = []
    if state:
        context_details.append(f"राज्य/क्षेत्र: {state}")
    if crop:
        context_details.append(f"संबंधित फसल: {crop}")
    context_str = f" ({', '.join(context_details)})" if context_details else ""

    user_prompt = (
        f"{AGRICULTURAL_SYSTEM_PROMPT}\n\n"
        f"किसान का सवाल{context_str}: {query}\n\n"
        "कृपया उपरोक्त नियमों का पालन करते हुए सीधा और स्पष्ट उत्तर हिंदी में दें:"
    )

    url = GEMINI_ENDPOINT_TEMPLATE.format(model=GEMINI_MODEL, key=api_key)

    payload = {
        "contents": [
            {
                "parts": [{"text": user_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 350
        }
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        ans_text = parts[0]["text"].strip()
                        return {
                            "answer_hi": ans_text,
                            "answer_en": "AI-generated farming advisory based on agricultural best practices.",
                            "confidence": 0.88,
                            "intent": "ai_farming_advisory",
                            "verification_status": "ai_generated",
                            "data_type": "ai_generated_fallback",
                            "sources": [
                                {
                                    "id": "src-gemini-ai",
                                    "name": "Google Gemini AI (कृषि सहायक मॉडल)",
                                    "type": "ai_model"
                                }
                            ]
                        }
    except urllib.error.HTTPError as http_err:
        logger.warning(f"Gemini API HTTP Error {http_err.code}: {http_err.reason}")
    except Exception as exc:
        logger.warning(f"Gemini API request failed or timed out: {exc}")

    return None


def synthesize_scheme_advice(
    scheme_record: Dict[str, Any],
    query: str,
    state: Optional[str] = None,
    timeout_seconds: int = 10
) -> Optional[str]:
    """
    Combines verified local government scheme facts with Gemini AI to generate
    a single, cohesive, easy-to-understand Hindi response for farmers without
    any technical meta-labels, brackets, or separate options.
    """
    api_key = settings.GEMINI_API_KEY.strip()
    if not api_key:
        return None

    # Extract verified ground-truth fields from local database
    sch_name = scheme_record.get("title") or scheme_record.get("name")
    if isinstance(sch_name, dict):
        sch_name_hi = sch_name.get("hi") or sch_name.get("en") or "सरकारी कृषि योजना"
    else:
        sch_name_hi = str(sch_name or "सरकारी कृषि योजना")

    purpose = scheme_record.get("purpose")
    if isinstance(purpose, dict):
        purpose_text = purpose.get("hi") or purpose.get("en") or ""
    else:
        purpose_text = str(purpose or "")

    benefits = scheme_record.get("benefits")
    if isinstance(benefits, dict):
        benefits_text = benefits.get("hi") or benefits.get("en") or ""
    else:
        benefits_text = str(benefits or "")

    eligibility = str(scheme_record.get("eligibility") or "")
    exclusions = str(scheme_record.get("exclusion_criteria") or "")
    app_proc = str(scheme_record.get("application_process") or "")
    portal = str(scheme_record.get("official_portal") or "")

    helpline_info = scheme_record.get("helpline") or {}
    if isinstance(helpline_info, dict):
        h_nums = helpline_info.get("numbers", [])
        helpline_text = ", ".join(h_nums) if h_nums else ""
    elif isinstance(helpline_info, list):
        helpline_text = ", ".join([str(x) for x in helpline_info])
    else:
        helpline_text = str(helpline_info or "")

    facts = (
        f"आधिकारिक सरकारी तथ्य (Ground Truth Facts):\n"
        f"- योजना का नाम: {sch_name_hi}\n"
        f"- उद्देश्य: {purpose_text}\n"
        f"- वित्तीय लाभ: {benefits_text}\n"
        f"- आधिकारिक पोर्टल: {portal}\n"
        f"- आधिकारिक हेल्पलाइन: {helpline_text}\n"
        f"- पात्रता: {eligibility}\n"
        f"- अपात्रता: {exclusions}\n"
        f"- आवेदन प्रक्रिया: {app_proc}\n"
    )

    prompt = f"""आप KisanVaani AI के एक अत्यंत सहायक और स्पष्ट भारतीय कृषि व सरकारी योजना विशेषज्ञ हैं। 
नीचे दिए गए आधिकारिक सरकारी तथ्यों और किसान के सवाल के आधार पर केवल एक ही संपूर्ण, आदरपूर्ण, स्पष्ट और सरल ग्रामीण हिंदी में उत्तर तैयार करें।

नियम:
1. उत्तर में कोई भी तकनीकी कोष्ठक या लेबल (जैसे 'लोकल डेटा', 'Gemini व्याख्या', 'विकल्प 1', 'विकल्प 2', '(सत्यापित)') बिल्कुल न लिखें।
2. उत्तर को एक ही स्वाभाविक, साफ और सुंदर संदेश के रूप में लिखें, जिसमें 4-5 मुख्य बिंदु हों:
   • योजना का लाभ (स्पष्ट और सटीक राशि/सहयोग)
   • कौन पात्र है (और कौन अपात्र है)
   • जरूरी कागजात (उदा. आधार कार्ड बैंक से लिंक, जमीन की खतौनी/फर्द, बैंक पासबुक, मोबाइल नंबर)
   • आवेदन व e-KYC की आसान प्रक्रिया (CSC सेंटर या आधिकारिक पोर्टल)
   • आधिकारिक वेबसाइट और हेल्पलाइन नंबर
3. आधिकारिक पोर्टल ({portal}) और हेल्पलाइन ({helpline_text}) में कोई बदलाव न करें।
4. भाषा बहुत ही सरल, शुद्ध और आदरपूर्ण हिंदी होनी चाहिए ताकि किसान भाई पढ़कर या सुनकर आसानी से समझ सकें।

किसान का सवाल: {query}
{facts}

कृपया उपरोक्त नियमों का पालन करते हुए सीधा, प्राकृतिक और पूर्ण उत्तर हिंदी में दें:"""

    url = GEMINI_ENDPOINT_TEMPLATE.format(model=GEMINI_MODEL, key=api_key)

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 450
        }
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        ans = parts[0]["text"].strip()
                        if ans:
                            return ans
    except Exception as e:
        logger.warning(f"Scheme synthesis with Gemini failed: {e}")

    return None


def synthesize_crop_advice(
    crop_record: Dict[str, Any],
    query: str,
    state: Optional[str] = None,
    timeout_seconds: int = 10
) -> Optional[str]:
    """
    Combines verified local agricultural knowledge (HAU Hisar, PAU, ICAR, DMI package of practices)
    with Gemini AI to produce a single, cohesive, easy-to-understand Hindi response
    without any technical meta-labels, brackets, or split options.
    Enforces pesticide safety guardrails (organic/IPM first, KVK referral for chemical sprays).
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None

    crop_title = crop_record.get("title") or ""
    crop_name = crop_record.get("crop_name")
    if isinstance(crop_name, dict):
        crop_display = crop_name.get("hi") or crop_name.get("en") or crop_title
    elif isinstance(crop_name, str):
        crop_display = crop_name
    else:
        crop_display = crop_title or "फसल"

    topic = crop_record.get("topic") or "उन्नत खेती व प्रबंधन"

    ans_simple = crop_record.get("answer_simple")
    if isinstance(ans_simple, dict):
        ans_simple_text = ans_simple.get("hi") or ans_simple.get("en") or ""
    elif isinstance(ans_simple, str):
        ans_simple_text = ans_simple
    else:
        ans_simple_text = ""

    detailed = crop_record.get("answer_detailed") or crop_record.get("detailed_sections") or {}
    detailed_facts = []
    if isinstance(detailed, dict):
        for k, v in detailed.items():
            clean_k = k.replace("_", " ").strip()
            if clean_k and clean_k[0].isdigit():
                parts = clean_k.split(" ", 1)
                if len(parts) > 1:
                    clean_k = parts[1]
            if isinstance(v, str) and v.strip():
                detailed_facts.append(f"- {clean_k}: {v.strip()[:250]}")
    elif isinstance(detailed, str) and detailed.strip():
        detailed_facts.append(f"- विस्तृत जानकारी: {detailed.strip()[:600]}")

    facts_str = "\n".join(detailed_facts[:6])

    prompt = f"""आप KisanVaani AI के एक अत्यंत अनुभवी, मददगार और व्यावहारिक भारतीय कृषि विशेषज्ञ (ICAR / KVK कृषि वैज्ञानिक) हैं।
नीचे दिए गए आधिकारिक व सत्यापित कृषि तथ्यों और किसान के सवाल के आधार पर केवल एक ही संपूर्ण, आदरपूर्ण, स्पष्ट और सरल ग्रामीण हिंदी में उत्तर तैयार करें।

नियम:
1. उत्तर में कोई भी तकनीकी कोष्ठक या लेबल (जैसे 'लोकल डेटा', 'Gemini व्याख्या', 'विकल्प 1', 'विकल्प 2', '(सत्यापित)') बिल्कुल न लिखें।
2. उत्तर को एक ही स्वाभाविक, साफ और सुंदर संदेश के रूप में लिखें, जिसमें 4-5 मुख्य बिंदु हों:
   • उपयुक्त जलवायु, मिट्टी की तैयारी एवं बुवाई का सही समय
   • प्रमाणित उन्नत किस्में और बीज उपचार
   • सिंचाई के प्रमुख चरण और संतुलित खाद/उर्वरक प्रबंधन
   • कीट व रोग नियंत्रण (एकीकृत कीट प्रबंधन - IPM और जैविक उपायों को प्राथमिकता दें)
   • किसान सुरक्षा निर्देश (रासायनिक कीटनाशक छिड़कने से पहले हमेशा नजदीकी कृषि विज्ञान केंद्र - KVK या कृषि अधिकारी से सलाह लेने का निर्देश दें)
3. रासायनिक दवाओं या कीटनाशकों की मनगढ़ंत मात्रा कभी न बताएं।
4. भाषा बहुत ही सरल, शुद्ध और आदरपूर्ण हिंदी होनी चाहिए ताकि किसान भाई पढ़कर या आवाज में सुनकर आसानी से समझ सकें।

किसान का सवाल: {query}
राज्य/क्षेत्र: {state or 'उत्तर भारत'}
फसल: {crop_display} ({topic})
स्थानीय सत्यापित आधार तथ्य:
{ans_simple_text}
{facts_str}

कृपया उपरोक्त नियमों का पालन करते हुए सीधा, प्राकृतिक और पूर्ण उत्तर हिंदी में दें:"""

    url = GEMINI_ENDPOINT_TEMPLATE.format(model=GEMINI_MODEL, key=api_key)

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 500
        }
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        ans = parts[0]["text"].strip()
                        if ans:
                            return ans
    except Exception as e:
        logger.warning(f"Crop advisory synthesis with Gemini failed: {e}")

    return None


def synthesize_seed_advice(
    seed_record: Dict[str, Any],
    query: str,
    state: Optional[str] = None,
    timeout_seconds: int = 10
) -> Optional[str]:
    """
    Combines verified local seed variety data (HAU, PAU, ICAR recommendations)
    with Gemini AI to produce a single, natural Hindi advisory —
    no meta-labels, no brackets, with KVK referral for local confirmation.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None

    raw = seed_record.get("_raw_rec") or seed_record
    variety = raw.get("variety") or seed_record.get("title") or "उन्नत किस्म"
    crop_id = raw.get("crop_id") or seed_record.get("crop_id") or ""
    sowing_cond = raw.get("sowing_condition") or ""
    irrig_status = raw.get("irrigation_status") or ""
    yield_pot = raw.get("yield_potential") or ""
    maturity = raw.get("maturity_period") or ""
    resistance = raw.get("resistance") or ""
    features = raw.get("features") or ""
    rec_state = raw.get("state") or seed_record.get("state") or state or "उत्तर भारत"
    zone = raw.get("zone") or ""

    detailed = raw.get("detailed_sections") or seed_record.get("detailed_sections") or {}
    detail_lines = []
    if isinstance(detailed, dict):
        for k, v in list(detailed.items())[:4]:
            clean_k = k.replace("_", " ").strip()
            if isinstance(v, str) and v.strip():
                detail_lines.append(f"- {clean_k}: {v.strip()[:200]}")
    detail_str = "\n".join(detail_lines)

    prompt = f"""आप KisanVaani AI के एक अत्यंत अनुभवी भारतीय बीज विशेषज्ञ (ICAR / SAU प्रमाणित) हैं।
नीचे दिए गए आधिकारिक व सत्यापित बीज किस्म के तथ्यों और किसान के सवाल के आधार पर केवल एक ही संपूर्ण, आदरपूर्ण और सरल ग्रामीण हिंदी में उत्तर तैयार करें।

नियम:
1. उत्तर में कोई भी तकनीकी कोष्ठक या लेबल (जैसे 'लोकल डेटा', 'AI व्याख्या', 'विकल्प') बिल्कुल न लिखें।
2. उत्तर को एक ही स्वाभाविक संदेश के रूप में लिखें, जिसमें 4-5 मुख्य बिंदु हों:
   • किस्म का नाम और किस क्षेत्र/राज्य के लिए अनुशंसित है
   • उपयुक्त बुवाई का समय और सिंचाई की स्थिति
   • उपज क्षमता और पकने की अवधि
   • रोग-प्रतिरोधकता और विशेष गुण (यदि उपलब्ध)
   • किसान सुरक्षा निर्देश: अपने जिले की नवीनतम सिफारिश के लिए नजदीकी KVK या कृषि विभाग से अवश्य पुष्टि करें
3. भाषा बहुत ही सरल, शुद्ध और आदरपूर्ण हिंदी होनी चाहिए।

किसान का सवाल: {query}
राज्य/क्षेत्र: {rec_state}
किस्म का नाम: {variety}
फसल: {crop_id}
बुवाई की स्थिति: {sowing_cond}
सिंचाई: {irrig_status}
उपज क्षमता: {yield_pot}
पकने की अवधि: {maturity}
रोग-प्रतिरोधकता: {resistance}
विशेष गुण: {features}
कृषि-जलवायु क्षेत्र: {zone}
{detail_str}

कृपया उपरोक्त नियमों का पालन करते हुए सीधा, प्राकृतिक और पूर्ण उत्तर हिंदी में दें:"""

    url = GEMINI_ENDPOINT_TEMPLATE.format(model=GEMINI_MODEL, key=api_key)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 450}
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        ans = parts[0]["text"].strip()
                        if ans:
                            return ans
    except Exception as e:
        logger.warning(f"Seed advice synthesis with Gemini failed: {e}")

    return None


def synthesize_fertilizer_advice(
    fert_record: Dict[str, Any],
    query: str,
    state: Optional[str] = None,
    timeout_seconds: int = 10
) -> Optional[str]:
    """
    Combines verified local fertilizer recommendation data (ICAR/SAU/Soil Health Card)
    with Gemini AI for a single, natural Hindi advisory.
    Always enforces Soil Health Card + KVK helpline (1800-180-1551) safety guardrail.
    Never fabricates chemical doses.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None

    raw_rec = fert_record.get("_raw_rec") or fert_record
    category = raw_rec.get("category") or ""

    # Determine if this is a crop-specific recommendation or a catalog item
    is_crop_rec = "recommendation" in category.lower()

    if is_crop_rec:
        crop_name_dict = raw_rec.get("crop_name") or {}
        crop_display = (crop_name_dict.get("hi") if isinstance(crop_name_dict, dict) else str(crop_name_dict)) or raw_rec.get("crop_id", "फसल")
        dose = raw_rec.get("recommended_dose_per_acre") or {}
        n_dose = dose.get("nitrogen_n", "")
        p_dose = dose.get("phosphorus_p", "")
        k_dose = dose.get("phosphorus_k") or dose.get("potassium_k", "")
        micro = dose.get("micronutrients", "")
        schedule_dict = raw_rec.get("application_schedule") or {}
        schedule_hi = (schedule_dict.get("hi") if isinstance(schedule_dict, dict) else str(schedule_dict or ""))[:400]
        safety_dict = raw_rec.get("safety_and_guidelines") or {}
        safety_hi = (safety_dict.get("hi") if isinstance(safety_dict, dict) else str(safety_dict or ""))[:300]
        facts = (
            f"फसल: {crop_display}\n"
            f"अनुशंसित मात्रा (प्रति एकड़):\n"
            f"  - नाइट्रोजन (N): {n_dose}\n"
            f"  - फास्फोरस (P): {p_dose}\n"
            f"  - पोटाश (K): {k_dose}\n"
            f"  - सूक्ष्म पोषक तत्व: {micro}\n"
            f"प्रयोग अनुसूची:\n{schedule_hi}\n"
            f"सुरक्षा दिशानिर्देश: {safety_hi}"
        )
        subject = f"{crop_display} के लिए उर्वरक एवं पोषण प्रबंधन"
    else:
        fname_dict = raw_rec.get("fertilizer_name") or {}
        fname_hi = (fname_dict.get("hi") if isinstance(fname_dict, dict) else str(fname_dict)) or "उर्वरक"
        nutrient = raw_rec.get("nutrient_composition") or {}
        benefits_dict = raw_rec.get("benefits") or {}
        benefits_hi = (benefits_dict.get("hi") if isinstance(benefits_dict, dict) else str(benefits_dict or ""))[:300]
        apply_dict = raw_rec.get("application_guidelines") or {}
        apply_hi = (apply_dict.get("hi") if isinstance(apply_dict, dict) else str(apply_dict or ""))[:300]
        facts = (
            f"उर्वरक: {fname_hi}\n"
            f"पोषक तत्व: N={nutrient.get('nitrogen_n','')}, P={nutrient.get('phosphorus_p','')}, K={nutrient.get('potassium_k','')}\n"
            f"लाभ: {benefits_hi}\n"
            f"प्रयोग विधि: {apply_hi}"
        )
        subject = f"{fname_hi} उर्वरक की जानकारी"

    prompt = f"""आप KisanVaani AI के एक अत्यंत अनुभवी भारतीय कृषि पोषण विशेषज्ञ (ICAR / Soil Health Card सलाहकार) हैं।
नीचे दिए गए आधिकारिक व सत्यापित उर्वरक तथ्यों और किसान के सवाल के आधार पर केवल एक ही संपूर्ण, आदरपूर्ण और सरल ग्रामीण हिंदी में उत्तर तैयार करें।

नियम:
1. उत्तर में कोई भी तकनीकी कोष्ठक या लेबल (जैसे 'लोकल डेटा', 'AI व्याख्या') बिल्कुल न लिखें।
2. उत्तर को एक ही स्वाभाविक संदेश के रूप में 4-5 बिंदुओं में लिखें:
   • बुवाई/रोपाई के समय बेसल डोज़ (N, P, K की मात्रा)
   • पौध बढ़वार और फूल/फल भराव पर टॉप-ड्रेसिंग कार्यक्रम
   • सूक्ष्म पोषक तत्व (जिंक, सल्फर, बोरान) की आवश्यकता
   • महत्वपूर्ण: **Soil Health Card** के अनुसार मात्रा निर्धारित करें
   • किसान सुरक्षा: रासायनिक उर्वरक के प्रयोग में दस्ताने पहनें और किसी भी संशय में KVK हेल्पलाइन **1800-180-1551** पर कॉल करें
3. रासायनिक उर्वरकों की मनगढ़ंत मात्रा कभी न बताएं — सदा verified facts के अनुसार बोलें।
4. भाषा बहुत ही सरल, शुद्ध और आदरपूर्ण हिंदी होनी चाहिए।

किसान का सवाल: {query}
राज्य/क्षेत्र: {state or 'उत्तर भारत'}
विषय: {subject}
सत्यापित तथ्य:
{facts}

कृपया उपरोक्त नियमों का पालन करते हुए सीधा, प्राकृतिक और पूर्ण उत्तर हिंदी में दें:"""

    url = GEMINI_ENDPOINT_TEMPLATE.format(model=GEMINI_MODEL, key=api_key)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 480}
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        ans = parts[0]["text"].strip()
                        if ans:
                            return ans
    except Exception as e:
        logger.warning(f"Fertilizer advice synthesis with Gemini failed: {e}")

    return None
