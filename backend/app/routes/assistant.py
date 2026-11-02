import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.models import Conversation, Message
from ..services.knowledge_retrieval import knowledge_service
from ..services import weather_service, mandi_service, gemini_service
from ..schemas.assistant import ChatRequest, ChatResponse

router = APIRouter(prefix="/assistant", tags=["AI Voice Assistant"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Core AI Question-Answering endpoint.
    Retrieves grounded records from the agricultural knowledge base,
    formats simple understandable Hindi text, attributes sources, and persists to history.
    """
    message_text = req.message.strip()
    if not message_text:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Retrieve or create Conversation in DB
    conv = None
    if req.conversation_id:
        conv = db.query(Conversation).filter(Conversation.id == req.conversation_id).first()

    if not conv:
        title_snippet = message_text[:40] + ("..." if len(message_text) > 40 else "")
        conv = Conversation(
            id=str(uuid.uuid4()),
            title=title_snippet,
            language=req.language or "hi"
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # 2. Record User Message
    user_msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conv.id,
        sender="farmer",
        text=message_text,
        intent="general"
    )
    db.add(user_msg)

    # 3. Contextual Resolution from Current Message and Conversation History
    effective_crop = req.crop
    effective_state = req.state

    all_user_text = message_text.lower()
    if conv and conv.messages:
        all_user_text += " " + " ".join([m.text for m in conv.messages if m.sender == "farmer"]).lower()

    if not effective_crop:
        if "गेहूं" in all_user_text or "wheat" in all_user_text:
            effective_crop = "wheat"
        elif "धान" in all_user_text or "चावल" in all_user_text or "rice" in all_user_text:
            effective_crop = "paddy"
        elif "सरसों" in all_user_text or "mustard" in all_user_text:
            effective_crop = "mustard"
        elif "बाजरा" in all_user_text or "bajra" in all_user_text:
            effective_crop = "bajra"

    if not effective_state:
        for st in ["haryana", "हरियाणा", "punjab", "पंजाब", "rajasthan", "राजस्थान", "himachal", "हिमाचल", "uttar pradesh", "उत्तर प्रदेश", "uttarakhand", "उत्तराखंड", "delhi", "दिल्ली"]:
            if st in all_user_text:
                effective_state = (
                    "Haryana" if st in ("haryana", "हरियाणा")
                    else "Punjab" if st in ("punjab", "पंजाब")
                    else "Rajasthan" if st in ("rajasthan", "राजस्थान")
                    else "Himachal Pradesh" if st in ("himachal", "हिमाचल")
                    else "Delhi NCR" if "delhi" in st or "दिल्ली" in st
                    else "Uttar Pradesh" if "uttar" in st or "उत्तर" in st
                    else "Uttarakhand"
                )
                break

    # 4a. Detect greeting-only or weather queries BEFORE KB search
    _WEATHER_KW = {
        "mausam", "weather", "बारिश", "बरसात", "तापमान", "बादल", "धूप", "ठंड",
        "गर्मी", "हवा", "कोहरा", "बाढ़", "ओला", "बर्फ", "सर्दी", "बरखा"
    }
    _GREETING_KW = {
        "namaskar", "namaste", "hello", "helo", "नमस्कार", "नमस्ते", "प्रणाम",
        "salam", "salaam", "sat sri akal", "jai", "ram ram"
    }
    _FILLER_STOP = {
        "k", "ki", "ke", "ka", "ko", "se", "me", "mein", "main", "par", "pe",
        "hai", "hain", "hoon", "hun", "bhai", "bhaai", "namaskar", "namaste",
        "ji", "jee", "aaj", "today", "kal", "gaon", "gao", "gav", "village",
        "khyaal", "kripya", "please", "batao", "bataiye", "the", "a", "an", "is",
        "are", "how", "what", "when", "where", "which", "for", "to", "in", "of",
        "क्या", "कैसे", "कहाँ", "कब", "और", "या", "पर", "में", "से", "को", "का",
        "की", "के", "है", "हैं", "हो", "था", "थी", "थे", "रहा", "रही", "रहे",
        "चाहिए", "करें", "बताएं", "बताओ", "वाला", "वाले", "वाली",
        "namaskar", "namaste", "ram", "jee", "ji", "hoon", "hun", "bhai", "bhaai"
    }
    _STATE_NAMES = {
        "haryana", "हरियाणा", "punjab", "पंजाब", "rajasthan", "राजस्थान",
        "himachal", "हिमाचल", "uttar", "उत्तर", "uttarakhand", "उत्तराखंड",
        "delhi", "दिल्ली"
    }

    msg_lower = message_text.lower()
    msg_tokens = [w.strip("?,.!:;\"'") for w in msg_lower.split()]

    # Is this a weather query?
    is_weather_query = any(w in _WEATHER_KW for w in msg_tokens)

    # Is this a pure greeting (all tokens are greetings/fillers/state-names/short words)?
    non_filler_tokens = [
        t for t in msg_tokens
        if t not in _FILLER_STOP and t not in _GREETING_KW and t not in _STATE_NAMES
        and len(t) > 2
    ]
    is_pure_greeting = (
        len(msg_tokens) > 0
        and len(non_filler_tokens) == 0
        and not is_weather_query
        and any(t in _GREETING_KW or t in _FILLER_STOP for t in msg_tokens)
    )

    intent = "general_advice"
    answer_hi = ""
    answer_en = ""
    sources_used: List[Dict[str, Any]] = []
    verif_status = "pending_review"
    data_type = "official_static"
    follow_ups: List[str] = []

    # Greeting-only: return a warm welcome, don't search KB
    if is_pure_greeting:
        state_mention = ""
        for st in ["haryana", "punjab", "rajasthan", "himachal", "uttar pradesh", "uttarakhand", "delhi"]:
            if st in msg_lower or st.split()[0] in msg_lower:
                state_mention = f" ({st.title()} से जुड़े)"
                break
        answer_hi = (
            f"नमस्ते किसान भाई! 🙏 KisanVaani में आपका स्वागत है।{state_mention} "
            "कृपया बताएं — आपको खेती से जुड़ी कौन सी जानकारी चाहिए? "
            "जैसे: फसल बुवाई, बीज दर, खाद, सिंचाई, मंडी भाव, या मौसम।"
        )
        answer_en = (
            f"Hello farmer! Welcome to KisanVaani.{state_mention} "
            "Please tell me — what farming information do you need? "
            "E.g.: crop sowing, seed rate, fertilizer, irrigation, mandi prices, or weather."
        )
        verif_status = "verified"
        data_type = "system_response"
        follow_ups = [
            "गेहूं की बुवाई का सही समय और बीज दर क्या है?",
            "अपने जिले का मंडी भाव कैसे देखें?",
            "आज का मौसम कैसा रहेगा?"
        ]
        intent = "greeting"

    # Weather query: return weather advisory
    elif is_weather_query:
        # Try to get live/sample weather data from weather_service
        weather_answer_hi = None
        try:
            loc = effective_state or "Haryana"
            for district in ["karnal", "hisar", "ambala", "rohtak", "panipat", "sonipat",
                             "ludhiana", "amritsar", "jaipur", "jodhpur", "lucknow", "dehradun"]:
                if district in msg_lower:
                    loc = district.title()
                    break
            wd = weather_service.get_weather_data(loc)
            if wd:
                spray_msg = wd.get("spray_advisory", {}).get("message_hi", "")
                st_name = wd.get("state", effective_state or "हरियाणा")
                loc_name = wd.get("location", loc)
                weather_answer_hi = (
                    f"किसान भाई, {loc_name} ({st_name}) का आज का मौसम:\n"
                    f"• तापमान: {wd.get('temperature')}°C | हवा में नमी: {wd.get('humidity')}%\n"
                    f"• मौसम: {wd.get('condition_hi', '')}\n"
                    f"• हवा की गति: {wd.get('wind_speed')} किमी/घंटा\n"
                    f"• बारिश की संभावना: {wd.get('rainfall_prob')}%\n\n"
                    f"कृषि सलाह: {spray_msg}\n"
                    "(सटीक जिलावार मौसम के लिए mausam.imd.gov.in देखें।)"
                )
        except Exception:
            pass

        if not weather_answer_hi:
            # Friendly fallback if weather service unavailable
            state_name = effective_state or "हरियाणा"
            weather_answer_hi = (
                f"किसान भाई, {state_name} का लाइव मौसम डेटा अभी लोड नहीं हो सका। "
                "कृपया India Meteorological Department (IMD) की वेबसाइट imd.gov.in या "
                "Kisan Suvidha ऐप पर अपने जिले का मौसम देखें। "
                "सामान्यतः इस समय मौसम गेहूं और रबी फसलों के लिए अनुकूल रहता है।"
            )
        answer_hi = weather_answer_hi
        answer_en = "Please check IMD (imd.gov.in) or Kisan Suvidha app for live weather in your district."
        verif_status = "verified"
        data_type = "sample"
        intent = "weather_query"
        follow_ups = [
            "गेहूं की बुवाई का सही समय क्या है?",
            "मेरी फसल के लिए सिंचाई की जानकारी दें।"
        ]

    # 4b. Grounded Knowledge Retrieval (only when not a greeting/weather query)
    search_results = [] if (is_pure_greeting or is_weather_query) else knowledge_service.search_knowledge(
        query=message_text,
        state=effective_state,
        crop=effective_crop
    )

    if search_results and not is_pure_greeting and not is_weather_query:
        top_match = search_results[0]
        verif_status = top_match.get("verification_status", "pending_review")
        data_type = top_match.get("data_type", "official_static")
        sources_used = top_match.get("sources", [])

        s_dict = top_match.get("answer_simple", {})
        answer_hi = s_dict.get("hi", "")
        answer_en = s_dict.get("en", "")

        intent = top_match.get("category", "farming_advice")

        follow_ups = [
            "क्या आप इस फसल की सिंचाई या खाद की मात्रा जानना चाहते हैं?",
            "क्या आपको नजदीकी मंडी भाव या मौसम की जानकारी चाहिए?"
        ]

        # Unified Scheme Synthesis: combine verified local scheme facts with Gemini AI for a single, comprehensive Hindi answer
        is_scheme_topic = (
            top_match.get("category") == "scheme"
            or "योजना" in message_text
            or "scheme" in message_text.lower()
            or "pm-kisan" in message_text.lower()
            or "pm kisan" in message_text.lower()
            or "पीएम किसान" in message_text
            or "योजना" in top_match.get("title", "")
        )

        if is_scheme_topic:
            scheme_to_use = top_match
            if top_match.get("category") != "scheme":
                # Look up rich scheme facts from national schemes if available
                for sch in knowledge_service.schemes_national:
                    s_id = (sch.get("scheme_id") or sch.get("id") or "").lower()
                    if s_id in message_text.lower() or ("kisan" in s_id and ("kisan" in message_text.lower() or "किसान" in message_text)):
                        scheme_to_use = sch
                        break
            synth_ans = gemini_service.synthesize_scheme_advice(scheme_to_use, message_text, effective_state)
            if synth_ans:
                answer_hi = synth_ans
                sources_used = top_match.get("sources", []) + [{
                    "id": "src-gemini-ai",
                    "name": "Google Gemini AI (सरल भाषा व्याख्या)",
                    "type": "ai_model"
                }]
            follow_ups = [
                "इस योजना के लिए e-KYC कैसे करें?",
                "नजदीकी सीएससी (CSC) सेंटर पर आवेदन कैसे करें?"
            ]
        elif top_match.get("category") in ("fertilizer", "fertilizer_catalog"):
            # Unified Fertilizer Advisory Synthesis: combine verified NPK/dose facts with Gemini AI
            synth_ans = gemini_service.synthesize_fertilizer_advice(top_match, message_text, effective_state)
            if synth_ans:
                answer_hi = synth_ans
                sources_used = top_match.get("sources", []) + [{
                    "id": "src-gemini-ai",
                    "name": "Google Gemini AI (सरल भाषा व्याख्या)",
                    "type": "ai_model"
                }]
            follow_ups = [
                "क्या आप जैविक खाद (जैसे गोबर खाद या वर्मीकम्पोस्ट) के बारे में जानना चाहते हैं?",
                "इस फसल में सिंचाई और पानी देने का सही समय क्या है?"
            ]
        elif top_match.get("category") == "seed_variety":
            # Unified Seed Advisory Synthesis: combine verified seed variety facts with Gemini AI
            synth_ans = gemini_service.synthesize_seed_advice(top_match, message_text, effective_state)
            if synth_ans:
                answer_hi = synth_ans
                sources_used = top_match.get("sources", []) + [{
                    "id": "src-gemini-ai",
                    "name": "Google Gemini AI (सरल भाषा व्याख्या)",
                    "type": "ai_model"
                }]
            follow_ups = [
                "इस बीज की बुवाई का सही समय और तरीका क्या है?",
                "इस किस्म के लिए खाद और उर्वरक की कितनी मात्रा चाहिए?"
            ]
        elif top_match.get("category") == "crop" or any(k in top_match.get("title", "").lower() for k in ("फसल", "खेती", "प्रबंधन", "किस्म")):
            # Unified Crop Advisory Synthesis: combine verified local crop facts with Gemini AI for single natural Hindi response
            synth_ans = gemini_service.synthesize_crop_advice(top_match, message_text, effective_state)
            if synth_ans:
                answer_hi = synth_ans
                sources_used = top_match.get("sources", []) + [{
                    "id": "src-gemini-ai",
                    "name": "Google Gemini AI (सरल भाषा व्याख्या)",
                    "type": "ai_model"
                }]
            follow_ups = [
                "इस फसल में लगने वाले प्रमुख कीट और उनकी रोकथाम बताएं।",
                "इसके लिए संतुलित खाद (NPK) की सही मात्रा क्या है?"
            ]
    elif not is_pure_greeting and not is_weather_query:
        # Automatic Shift: If not found in local Knowledge Base, try Gemini AI
        gemini_result = gemini_service.generate_agricultural_fallback(
            query=message_text,
            state=effective_state,
            crop=effective_crop
        )

        if gemini_result:
            answer_hi = gemini_result.get("answer_hi", "")
            answer_en = gemini_result.get("answer_en", "")
            verif_status = gemini_result.get("verification_status", "ai_generated")
            data_type = gemini_result.get("data_type", "ai_generated_fallback")
            sources_used = gemini_result.get("sources", [])
            intent = gemini_result.get("intent", "ai_farming_advisory")
            follow_ups = [
                "क्या आप इस विषय पर जैविक या प्राकृतिक उपाय जानना चाहते हैं?",
                "क्या आपको नजदीकी मंडी भाव या मौसम की जानकारी चाहिए?"
            ]
        else:
            # Fallback grounded response when specific record is not found and AI is unavailable
            answer_hi = (
                f"किसान भाई, आपके सवाल '{message_text}' के लिए सीधा पैकेज रिकॉर्ड फिलहाल नॉलेज बेस में सत्यापित नहीं है। "
                "गलत या बिना जांचे कीटनाशक/खाद की मात्रा बताना किसान सुरक्षा नियमों के विरुद्ध है। "
                "कृपया अपने ब्लॉक के कृषि विज्ञान केंद्र (KVK) या राज्य कृषि विभाग से संपर्क करें।"
            )
            answer_en = (
                f"Regarding your query '{message_text}', verified official guidance is not yet logged in the database. "
                "To prevent crop damage, please consult your local Krishi Vigyan Kendra (KVK) or state agriculture office."
            )
            verif_status = "unverified"
            data_type = "unverified"
            follow_ups = [
                "गेहूं की बुवाई का समय क्या है?",
                "प्रधानमंत्री किसान सम्मान निधि के क्या लाभ हैं?"
            ]

    # 4. Save Assistant Response to DB
    asst_msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conv.id,
        sender="assistant",
        text=answer_hi,
        intent=intent,
        sources_used=sources_used
    )
    db.add(asst_msg)
    db.commit()

    return ChatResponse(
        conversation_id=conv.id,
        message_id=asst_msg.id,
        answer_text=answer_hi,
        answer_hi=answer_hi,
        answer_en=answer_en,
        intent=intent,
        confidence=0.92 if search_results else (0.88 if data_type == "ai_generated_fallback" else 0.50),
        verification_status=verif_status,
        data_type=data_type,
        sources_used=sources_used,
        follow_up_questions=follow_ups,
        audio_url=None
    )

