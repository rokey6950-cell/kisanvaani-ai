import logging
from typing import Dict, Any, List, Optional

from .knowledge_retrieval import knowledge_service

logger = logging.getLogger("kisanvaani.crop_advisory")

STATE_DISTRICTS: Dict[str, List[str]] = {
    "हरियाणा": ["करनाल", "हिसार", "अंबाला", "सिरसा", "रोहतक", "कुरुक्षेत्र", "फतेहाबाद", "जींद", "पानीपत", "सोनीपत", "यमुनानगर"],
    "Haryana": ["Karnal", "Hisar", "Ambala", "Sirsa", "Rohtak", "Kurukshetra", "Fatehabad", "Jind", "Panipat", "Sonipat", "Yamunanagar"],
    "पंजाब": ["लुधियाना", "पटियाला", "अमृतसर", "बठिंडा", "जालंधर", "गुरदासपुर", "संगरूर", "फिरोजपुर"],
    "Punjab": ["Ludhiana", "Patiala", "Amritsar", "Bathinda", "Jalandhar", "Gurdaspur", "Sangrur", "Firozpur"],
    "उत्तर प्रदेश": ["लखनऊ", "आगरा", "मेरठ", "वाराणसी", "कानपुर", "गोरखपुर", "मुरादाबाद", "सहारनपुर", "अलीगढ़", "बरेली"],
    "Uttar Pradesh": ["Lucknow", "Agra", "Meerut", "Varanasi", "Kanpur", "Gorakhpur", "Moradabad", "Saharanpur", "Aligarh", "Bareilly"],
    "राजस्थान": ["जयपुर", "जोधपुर", "श्रीगंगानगर", "कोटा", "बीकानेर", "अलवर", "भरतपुर", "सीकर"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Sri Ganganagar", "Kota", "Bikaner", "Alwar", "Bharatpur", "Sikar"],
    "हिमाचल प्रदेश": ["शिमला", "कांगड़ा", "मंडी", "सोलन", "हमीरपुर", "ऊना", "कुल्लू"],
    "Himachal Pradesh": ["Shimla", "Kangra", "Mandi", "Solan", "Hamirpur", "Una", "Kullu"],
    "उत्तराखंड": ["देहरादून", "हरिद्वार", "ऊधम सिंह नगर", "नैनीताल", "पौड़ी गढ़वाल"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Udham Singh Nagar", "Nainital", "Pauri Garhwal"],
    "दिल्ली NCR": ["नई दिल्ली", "उत्तर दिल्ली", "दक्षिण दिल्ली", "गाजियाबाद", "नोएडा", "गुरुग्राम", "फरीदाबाद"],
    "Delhi NCR": ["New Delhi", "North Delhi", "South Delhi", "Ghaziabad", "Noida", "Gurugram", "Faridabad"]
}

ADVISORY_TOPICS = [
    {"id": "sowing", "name_hi": "बुवाई का समय", "name_en": "Sowing Time"},
    {"id": "seed_varieties", "name_hi": "प्रमाणित बीज किस्में", "name_en": "Seed Varieties"},
    {"id": "soil_management", "name_hi": "खेत की तैयारी व मिट्टी प्रबंधन", "name_en": "Soil & Land Preparation"},
    {"id": "irrigation", "name_hi": "सिंचाई प्रबंधन", "name_en": "Irrigation Management"},
    {"id": "fertilizer", "name_hi": "उर्वरक व खाद प्रबंधन", "name_en": "Fertilizer Management"},
    {"id": "pest_disease", "name_hi": "कीट व रोग (IPM)", "name_en": "Pest & Disease IPM"},
    {"id": "harvesting", "name_hi": "कटाई व भंडारण", "name_en": "Harvesting & Storage"},
]

NATIONAL_KVK_REFERRAL = {
    "helpline_name": "Kisan Call Center (किसान कॉल सेंटर)",
    "toll_free": "1800-180-1551",
    "hours": "सुबह 6:00 से रात 10:00 बजे (सातों दिन)",
    "advice": "सटीक मिट्टी परीक्षण, कीटनाशक मात्रा अथवा स्थानीय कीट प्रकोप के लिए अपने जिले के कृषि विज्ञान केंद्र (KVK) या किसान कॉल सेंटर 1800-180-1551 पर संपर्क करें।"
}

class CropAdvisoryService:
    """
    Service generating grounded agricultural guidance.
    Enforces strict safety guardrails: never invents fertilizer doses or pesticide recipes.
    """

    def get_districts_for_state(self, state: Optional[str]) -> List[str]:
        if not state:
            return []
        for s_key, dists in STATE_DISTRICTS.items():
            if s_key.lower() == state.strip().lower():
                return dists
        return []

    def get_topics(self) -> List[Dict[str, str]]:
        return ADVISORY_TOPICS

    def generate_advisory(
        self,
        crop: str,
        state: Optional[str] = None,
        district: Optional[str] = None,
        season: Optional[str] = None,
        topic: Optional[str] = "sowing"
    ) -> Dict[str, Any]:
        crop_clean = crop.strip()
        state_clean = state.strip() if state else None
        district_clean = district.strip() if district else None
        topic_clean = (topic or "sowing").lower()

        # Is it wheat?
        is_wheat = any(w in crop_clean.lower() for w in ["wheat", "गेहूं", "गेंहू"])

        # Topic 1: Sowing
        if "sow" in topic_clean or "बुवाई" in topic_clean:
            if is_wheat:
                if state_clean and any(h in state_clean.lower() for h in ["haryana", "हरियाणा"]):
                    return {
                        "crop": "गेहूं (Wheat)",
                        "state": state_clean,
                        "district": district_clean,
                        "season": season or "रबी",
                        "topic": "बुवाई का समय",
                        "title": "हरियाणा में गेहूं की सामान्य बुवाई का समय",
                        "advisory_hi": (
                            "चौधरी चरण सिंह हरियाणा कृषि विश्वविद्यालय (HAU), हिसार के पैकेज अनुसार "
                            "हरियाणा में गेहूं की सामान्य बुवाई का उपयुक्त समय 25 अक्टूबर से 15 नवंबर है। "
                            "यदि आप देर से बुवाई कर रहे हैं, तो देर से बोई जाने वाली विशेष किस्में (जैसे WH 1309) चुननी चाहिए। "
                            "सटीक बीज दर व कतार दूरी के लिए स्थानीय कृषि विभाग या KVK से मार्गदर्शन लें।"
                        ),
                        "advisory_en": "HAU Hisar recommends 25 October to 15 November as normal wheat sowing window for Haryana.",
                        "verified_guidance": {
                            "recommended_window": "25 अक्टूबर से 15 नवंबर",
                            "late_sowing_window": "दिसंबर प्रथम पखवाड़ा (देर से बुवाई हेतु किस्में)",
                            "source_authority": "CCS Haryana Agricultural University"
                        },
                        "safety_disclaimer": "अनुशंसा सामान्य मार्गदर्शन हेतु है। मौसम व मिट्टी की नमी अनुसार बुवाई करें।",
                        "kvk_referral": NATIONAL_KVK_REFERRAL,
                        "verification_status": "verified",
                        "data_type": "official_static",
                        "sources": ["src-hau-pop-001"]
                    }
                elif state_clean and any(hp in state_clean.lower() for hp in ["himachal", "हिमाचल"]):
                    return {
                        "crop": "गेहूं (Wheat)",
                        "state": state_clean,
                        "district": district_clean,
                        "season": season or "रबी",
                        "topic": "बुवाई का समय",
                        "title": "हिमाचल प्रदेश में गेहूं की बुवाई",
                        "advisory_hi": (
                            "हिमाचल प्रदेश के सिंचित व असिंचित क्षेत्रों के अनुसार बुवाई समय बदलता है। "
                            "खेत की 2-3 बार गहरी जुताई कर पाटा लगाएं। बीज दर 100 किग्रा प्रति हेक्टेयर (सामान्य परिस्थितियों में) "
                            "और कतार दूरी 20-22.5 सेमी रखें। अपने जिले की सटीक मौसम स्थिति के लिए स्थानीय KVK से पुष्टि करें।"
                        ),
                        "advisory_en": "Himachal Pradesh wheat sowing and field preparation guidance.",
                        "verified_guidance": {
                            "row_spacing": "20-22.5 सेमी",
                            "seed_depth": "4-5 सेमी",
                            "source_authority": "ICAR-IISWC / State Agriculture Guidelines"
                        },
                        "safety_disclaimer": "पहाड़ी ढलानों व वर्षा आधारित क्षेत्रों में नमी संरक्षण का विशेष ध्यान रखें।",
                        "kvk_referral": NATIONAL_KVK_REFERRAL,
                        "verification_status": "pending_review",
                        "data_type": "official_static",
                        "sources": ["src-iiswc-001"]
                    }
                else:
                    return {
                        "crop": "गेहूं (Wheat)",
                        "state": state_clean or "सामान्य",
                        "district": district_clean,
                        "season": season or "रबी",
                        "topic": "बुवाई का समय",
                        "title": "गेहूं बुवाई दिशानिर्देश",
                        "advisory_hi": (
                            "उत्तर भारत के मैदानी भागों में गेहूं की सामान्य बुवाई नवंबर के पहले पखवाड़े में की जाती है। "
                            "किस्म और सिंचाई सुविधा अनुसार समय में अंतर आ सकता है। "
                            "सटीक तारीख के लिए अपने राज्य कृषि विश्वविद्यालय के पैकेज ऑफ प्रैक्टिसेज का पालन करें।"
                        ),
                        "advisory_en": "Normal wheat sowing in Northern plains is conducted during first fortnight of November.",
                        "verified_guidance": {
                            "season": "रबी (Rabi)",
                            "ideal_temperature": "बुवाई के समय 20-22°C तापमान अनुकूल रहता है।"
                        },
                        "safety_disclaimer": "मौसम व मिट्टी की स्थिति देखकर ही बुवाई प्रारंभ करें।",
                        "kvk_referral": NATIONAL_KVK_REFERRAL,
                        "verification_status": "pending_review",
                        "data_type": "official_static",
                        "sources": ["src-hau-pop-001"]
                    }

        # Topic 2: Seed Varieties
        if "seed" in topic_clean or "किस्म" in topic_clean or "variety" in topic_clean:
            varieties = knowledge_service.get_seed_varieties(crop_id="wheat" if is_wheat else None, state=state_clean)
            var_names = [v.get("variety") for v in varieties]
            var_text = ", ".join(var_names) if var_names else "WH 1309, HD 2967, DBW 187, HD 3226, PBW 826"
            return {
                "crop": crop_clean,
                "state": state_clean or "उत्तरी क्षेत्र",
                "district": district_clean,
                "season": season or "रबी",
                "topic": "प्रमाणित बीज किस्में",
                "title": f"{crop_clean} की अनुशंसित किस्में",
                "advisory_hi": (
                    f"कृषि अनुसंधान संस्थानों द्वारा अनुशंसित प्रमुख प्रमाणित किस्में हैं: {var_text}। "
                    "देर से बुवाई के लिए विशेष किस्में (जैसे WH 1309) उपयुक्त हैं। "
                    "हमेशा राज्य बीज निगम या प्रमाणित केंद्र से ही टैग लगा बीज खरीदें।"
                ),
                "advisory_en": f"Recommended certified varieties include: {var_text}.",
                "verified_guidance": {
                    "certified_varieties": var_names,
                    "seed_source": "राज्य बीज प्रमाणन एजेंसी अथवा NSC"
                },
                "safety_disclaimer": "निजी बिना लेबल वाले बीजों से बचें। बीज का अंकुरण परीक्षण अवश्य करें।",
                "kvk_referral": NATIONAL_KVK_REFERRAL,
                "verification_status": "verified" if varieties else "pending_review",
                "data_type": "official_static",
                "sources": ["src-hau-pop-001"]
            }

        # Topic 3: Irrigation
        if "irrig" in topic_clean or "सिंचाई" in topic_clean or "पानी" in topic_clean:
            return {
                "crop": crop_clean,
                "state": state_clean or "सामान्य",
                "district": district_clean,
                "season": season or "रबी",
                "topic": "सिंचाई प्रबंधन",
                "title": f"{crop_clean} में सिंचाई प्रबंधन",
                "advisory_hi": (
                    "गेहूं में पहली सिंचाई ताज मूल (CRI - Crown Root Initiation) अवस्था पर बुवाई के लगभग 20-25 दिन बाद की जाती है। "
                    "हल्की मिट्टी में पहली सिंचाई समय पर करना अत्यंत आवश्यक है। "
                    "धान की फसल में लगातार पानी भरने की बजाय वैकल्पिक गीला व सूखा (AWD) पद्धति पानी की बचत करती है। "
                    "सटीक सिंचाई चक्र के लिए खेत की नमी व मिट्टी के प्रकार अनुसार निर्णय लें।"
                ),
                "advisory_en": "Critical irrigation stages: CRI stage in wheat (21 days after sowing).",
                "verified_guidance": {
                    "critical_stages": "CRI अवस्था (21 दिन), कल्ले फूटते समय, गाभा अवस्था, दाना भरते समय"
                },
                "safety_disclaimer": "अत्यधिक जलभराव से जड़ें सड़ सकती हैं। खेत में जलनिकासी की उचित व्यवस्था रखें।",
                "kvk_referral": NATIONAL_KVK_REFERRAL,
                "verification_status": "pending_review",
                "data_type": "official_static",
                "sources": ["src-iiswc-001"]
            }

        # Topic 4: Pest & Disease IPM
        if "pest" in topic_clean or "रोग" in topic_clean or "कीट" in topic_clean or "ipm" in topic_clean:
            return {
                "crop": crop_clean,
                "state": state_clean or "सामान्य",
                "district": district_clean,
                "season": season,
                "topic": "कीट व रोग (IPM)",
                "title": f"{crop_clean} में एकीकृत कीट प्रबंधन (IPM)",
                "advisory_hi": (
                    "किसान सुरक्षा नियम: बिना पहचान किए किसी भी कीटनाशक का अंधाधुंध छिड़काव न करें। "
                    "कीट-रोग प्रबंधन के लिए पहले लक्षण देखें:\n"
                    "1. पीला रतुआ (गेहूं): पत्तियों पर पीले पाउडर जैसी धारियां दिखाई दें तो तुरंत कृषि विशेषज्ञ को दिखाएं।\n"
                    "2. माहू/चेपा (सरसों): फूल आने के समय तने व कलियों पर काले/हरे कीट दिखें तो नीम आधारित घोल या जैविक नियंत्रण अपनाएं।\n"
                    "3. मित्र कीटों (जैसे लेडीबर्ड बीटल) का संरक्षण करें।\n"
                    "रासायनिक कीटनाशक की सही मात्रा अपने जिले के कृषि विज्ञान केंद्र (KVK) से पर्ची बनवाकर ही लें।"
                ),
                "advisory_en": "Integrated Pest Management (IPM) guidelines. Identify pest before application.",
                "verified_guidance": {
                    "ipm_steps": "नियमित खेत निरीक्षण, मित्र कीट संरक्षण, जैविक नियंत्रण, रासायनिक छिड़काव केवल अंतिम विकल्प"
                },
                "safety_disclaimer": "किसान सुरक्षा: बिना सरकारी पर्ची/अनुशंसा के किसी भी कीटनाशक कॉकटेल का प्रयोग न करें।",
                "kvk_referral": NATIONAL_KVK_REFERRAL,
                "verification_status": "verified",
                "data_type": "official_static",
                "sources": ["src-report-kisanvaani-001"]
            }

        # Fallback General Crop Advisory
        return {
            "crop": crop_clean,
            "state": state_clean or "सामान्य",
            "district": district_clean,
            "season": season,
            "topic": topic_clean,
            "title": f"{crop_clean} कृषि प्रबंधन सलाह",
            "advisory_hi": (
                f"किसान भाई, {crop_clean} की सफल खेती के लिए प्रमाणित बीज, उचित बुवाई समय और संतुलित खाद-पानी आवश्यक है। "
                "मिट्टी की जांच (Soil Health Card) के आधार पर ही पोषक तत्व दें। "
                "मौसम की मार से बचाव के लिए फसल बीमा योजना (PMFBY) का लाभ लें। "
                "विस्तृत कृषि कार्ययोजना हेतु अपने निकटतम कृषि विज्ञान केंद्र से संपर्क करें।"
            ),
            "advisory_en": f"Comprehensive management guidance for {crop_clean}.",
            "verified_guidance": {
                "crop": crop_clean,
                "recommended_action": "मृदा स्वास्थ्य कार्ड अनुसार पोषक तत्व प्रबंधन"
            },
            "safety_disclaimer": "सटीक मात्रा व दवा के नाम हेतु स्थानीय कृषि अधिकारी से मार्गदर्शन लें।",
            "kvk_referral": NATIONAL_KVK_REFERRAL,
            "verification_status": "pending_review",
            "data_type": "official_static",
            "sources": ["src-hau-pop-001"]
        }

crop_advisory_service = CropAdvisoryService()

