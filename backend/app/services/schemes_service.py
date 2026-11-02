import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("kisanvaani.schemes")

# Grounded national government schemes catalog
# Verified against official government portals (pmkisan.gov.in, pmfby.gov.in, pmksy.gov.in, agrimachinery.nic.in)
SCHEMES_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "scheme-national-pmkisan-001",
        "scheme_id": "pm-kisan",
        "category": "financial_support",
        "name": {
            "en": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "hi": "प्रधानमंत्री किसान सम्मान निधि (पीएम-किसान)"
        },
        "scope": "National (All States)",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "purpose": {
            "en": "Direct income support to landholding farmer families across the country.",
            "hi": "देश के सभी भूमिधारक किसान परिवारों को वित्तीय सहायता प्रदान करना।"
        },
        "benefits": {
            "en": "Rs 6,000 per year in three equal instalments of Rs 2,000 every four months, deposited directly into the Aadhaar-linked bank account (DBT).",
            "hi": "सालाना 6,000 रुपये की आर्थिक सहायता, 2,000-2,000 रुपये की तीन समान किस्तों में हर चार महीने पर सीधे आधार से जुड़े बैंक खाते में (डीबीटी द्वारा)।"
        },
        "eligibility": {
            "en": "All landholding farmer families who have cultivable landholding in their names. Subject to exclusion criteria.",
            "hi": "वे सभी किसान परिवार जिनके नाम पर खेती योग्य भूमि का कानूनी रिकॉर्ड है। (बशर्ते वे अपात्र श्रेणी में न आते हों)।"
        },
        "exclusion_criteria": [
            "संस्थागत भूमिधारक (Institutional landholders)",
            "संवैधानिक पदधारक (वर्तमान अथवा पूर्व)",
            "वर्तमान अथवा पूर्व मंत्री, सांसद, विधायक, नगर निगम महापौर, जिला पंचायत अध्यक्ष",
            "केंद्र व राज्य सरकार के नियमित कर्मचारी (चतुर्थ श्रेणी / ग्रुप डी को छोड़कर)",
            "10,000 रुपये या अधिक मासिक पेंशन पाने वाले सेवानिवृत्त कर्मचारी",
            "पिछले मूल्यांकन वर्ष में आयकर (Income Tax) भरने वाले व्यक्ति",
            "पेशेवर जैसे डॉक्टर, इंजीनियर, वकील, चार्टर्ड अकाउंटेंट (सीए)"
        ],
        "required_documents": [
            "आधार कार्ड (Aadhaar Card)",
            "भूमि स्वामित्व दस्तावेज / खतौनी / जमाबंदी (Land Ownership / Khatauni / Jamabandi)",
            "सक्रिय बैंक खाता पासबुक (आधार से जुड़ा व डीबीटी सक्रिय)",
            "आधार से लिंक मोबाइल नंबर (ओटीपी सत्यापन हेतु)"
        ],
        "application_process": {
            "en": "Online self-registration through 'Farmers Corner' on pmkisan.gov.in portal, or via nearest Common Service Centre (CSC). Mandatory biometric or OTP-based e-KYC required.",
            "hi": "pmkisan.gov.in पोर्टल पर 'Farmers Corner' में जाकर 'New Farmer Registration' से खुद ऑनलाइन पंजीकरण करें, या नजदीकी कॉमन सर्विस सेंटर (CSC) पर जाएं। पोर्टल पर ई-केवाईसी (e-KYC) कराना अनिवार्य है।"
        },
        "official_portal": "https://pmkisan.gov.in/",
        "helpline": {
            "toll_free": "155261",
            "landline": "011-24300606",
            "note": "आधिकारिक पीएम-किसान पोर्टल हेल्पलाइन। कॉल करके किस्त की स्थिति व ई-केवाईसी सहायता ले सकते हैं।"
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "last_verified": "2026-11-01",
        "sources": ["src-pmkisan-portal-001", "src-pmkisan-scheme-doc-001", "src-pib-pmkisan-2020-001"]
    },
    {
        "id": "scheme-national-pmfby-001",
        "scheme_id": "pmfby",
        "category": "crop_insurance",
        "name": {
            "en": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "hi": "प्रधानमंत्री फसल बीमा योजना (पीएमएफबीवाई)"
        },
        "scope": "National (Notified Areas)",
        "department": "Department of Agriculture and Farmers Welfare",
        "purpose": {
            "en": "Comprehensive financial support and risk insurance against yield loss from natural calamities, pests, and unseasonal weather.",
            "hi": "प्राकृतिक आपदाओं (सूखा, बाढ़, ओलावृष्टि, बेमौसम बारिश) और कीट-रोगों से होने वाले फसल नुकसान के विरुद्ध व्यापक बीमा सुरक्षा।"
        },
        "benefits": {
            "en": "Affordable farmer premium: Only 2% for Kharif crops, 1.5% for Rabi crops, and 5% for commercial/horticultural crops. Central & State govts pay the remaining subsidy equally.",
            "hi": "न्यूनतम प्रीमियम दर: खरीफ फसलों के लिए मात्र 2%, रबी फसलों के लिए 1.5% तथा वाणिज्यिक/बागवानी फसलों के लिए केवल 5% प्रीमियम। शेष भारी प्रीमियम केंद्र व राज्य सरकारें सब्सिडी के रूप में वहन करती हैं।"
        },
        "eligibility": {
            "en": "All farmers growing notified crops in notified areas, including sharecroppers and tenant farmers. Both loanee (KCC holders) and non-loanee farmers are eligible.",
            "hi": "अधिसूचित क्षेत्रों में अधिसूचित फसलें उगाने वाले सभी किसान (बटाईदार व पट्टेदार किसान सहित)। केसीसी (KCC) ऋणधारी और गैर-ऋणधारी दोनों किसान पात्र हैं।"
        },
        "exclusion_criteria": [
            "युद्ध, परमाणु जोखिम या दुर्भावनापूर्ण इरादे से किए गए नुकसान",
            "कटाई के 14 दिन बाद खेत में सूखने के लिए रखी फसल के अलावा अन्य कारणों से नुकसान",
            "अधिसूचित क्षेत्र व अधिसूचित फसल के बाहर के मामले"
        ],
        "required_documents": [
            "आधार कार्ड (Aadhaar Card)",
            "जमीन की फर्द / खसरा-खतौनी / पटवारी रिपोर्ट (Land Record / Jamabandi)",
            "फसल बुवाई स्व-घोषणा पत्र (Sowing Certificate)",
            "बैंक खाता पासबुक की प्रति (Bank Passbook Copy)"
        ],
        "application_process": {
            "en": "Apply through your bank branch holding the KCC loan, via nearest CSC center, or self-enroll on the national portal pmfby.gov.in before the seasonal cut-off date.",
            "hi": "जिस बैंक शाखा में आपका केसीसी खाता है वहां से, या नजदीकी सीएससी (CSC) सेंटर से, अथवा आधिकारिक पोर्टल pmfby.gov.in पर कट-ऑफ तिथि से पूर्व सीधे ऑनलाइन आवेदन करें। स्थानीय नुकसान होने पर 72 घंटे के भीतर टोल-फ्री 14447 पर सूचना देना अनिवार्य है।"
        },
        "official_portal": "https://pmfby.gov.in/",
        "helpline": {
            "toll_free": "14447",
            "whatsapp_chatbot": "7065514447",
            "note": "राष्ट्रीय फसल बीमा हेल्पलाइन 14447 (दूरसंचार विभाग व लोकसभा द्वारा पुष्ट)। नुकसान सूचना हेतु 72 घंटे के भीतर कॉल करें।"
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "last_verified": "2026-11-01",
        "sources": ["src-dot-14447-001", "src-lokSabha-krph-001"]
    },
    {
        "id": "scheme-national-pmksy-001",
        "scheme_id": "pmksy",
        "category": "irrigation",
        "name": {
            "en": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
            "hi": "प्रधानमंत्री कृषि सिंचाई योजना"
        },
        "scope": "National",
        "department": "Ministry of Agriculture & Farmers Welfare / Ministry of Jal Shakti",
        "purpose": {
            "en": "Enhance water efficiency on farms through 'Har Khet Ko Paani' and 'Per Drop More Crop' micro-irrigation systems.",
            "hi": "हर खेत को पानी और 'प्रति बूंद अधिक फसल' (Per Drop More Crop) के तहत सूक्ष्म सिंचाई (ड्रिप व स्प्रिंकलर) को बढ़ावा देना।"
        },
        "benefits": {
            "en": "Subsidies ranging from 45% to 55% for small, marginal, and other farmers on installation of Drip Irrigation and Sprinkler systems, saving 30-50% water.",
            "hi": "ड्रिप (टपक) व स्प्रिंकलर (फव्वारा) सिंचाई प्रणाली लगाने पर छोटे, सीमांत व अन्य किसानों को 45% से 55% तक सरकारी अनुदान। 30-50% पानी की बचत व 20-30% अधिक पैदावार।"
        },
        "eligibility": {
            "en": "Farmers possessing cultivable agricultural land with an assured source of water (tubewell, borewell, canal, farm pond).",
            "hi": "खेती योग्य भूमि के मालिक किसान जिनके पास पानी का कोई सुनिश्चित स्रोत (ट्यूबवेल, बोरवेल, नहर, फार्म पौंड) उपलब्ध हो।"
        },
        "exclusion_criteria": [
            "वे भूमि जहां पानी का कोई प्राथमिक स्रोत उपलब्ध न हो",
            "जिन्होंने पिछले 7 वर्षों में उसी भूमि पर इस योजना का अनुदान लिया हो"
        ],
        "required_documents": [
            "आधार कार्ड (Aadhaar Card)",
            "जमीन के मालिकाना हक का प्रमाण (जमाबंदी/खसरा)",
            "बैंक खाता विवरण",
            "खेत पर जल स्रोत प्रमाण (बिजली कनेक्शन / ट्यूबवेल रसीद)"
        ],
        "application_process": {
            "en": "Apply through State Agriculture or Horticulture Department micro-irrigation portals (e.g. Haryana Cadawa / UP Drip portal) or district horticulture officer.",
            "hi": "राज्य के उद्यान अथवा कृषि विभाग के सूक्ष्म सिंचाई पोर्टल पर ऑनलाइन आवेदन करें, अथवा जिला उद्यान अधिकारी (DHO) कार्यालय से संपर्क करें।"
        },
        "official_portal": "https://pmksy.gov.in/",
        "helpline": {
            "toll_free": "1800-180-1551",
            "note": "किसान कॉल सेंटर या जिला उद्यान अधिकारी कार्यालय से अनुदान प्रक्रिया की जानकारी लें।"
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "last_verified": "2026-11-01",
        "sources": ["src-pmksy-portal-001"]
    },
    {
        "id": "scheme-national-soil-health-card-001",
        "scheme_id": "soil-health-card",
        "category": "soil_health",
        "name": {
            "en": "Soil Health Card Scheme",
            "hi": "मृदा स्वास्थ्य कार्ड योजना"
        },
        "scope": "National",
        "department": "Department of Agriculture, Cooperation & Farmers Welfare",
        "purpose": {
            "en": "Assess soil nutrient status and provide customized fertilizer and organic manure recommendations.",
            "hi": "खेत की मिट्टी के पोषक तत्वों की जांच कर मिट्टी के स्वास्थ्य की रिपोर्ट व संतुलित खाद-उर्वरक की सिफारिश देना।"
        },
        "benefits": {
            "en": "Free printed report card showing 12 soil parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC), reducing fertilizer costs by 15-20% through targeted nutrient management.",
            "hi": "खेत की मिट्टी के 12 मापदंडों (नाइट्रोजन, फास्फोरस, पोटाश, जिंक, आयरन, कॉपर, सल्फर, बोरॉन, पीएच, जैविक कार्बन) की जांच रिपोर्ट कार्ड। खाद की बर्बादी रोककर 15-20% लागत कम होती है।"
        },
        "eligibility": {
            "en": "All agricultural landowners across all rural areas.",
            "hi": "सभी किसान भाई जिनकी कृषि भूमि है।"
        },
        "exclusion_criteria": [
            "गैर-कृषि भूमि व औद्योगिक क्षेत्र"
        ],
        "required_documents": [
            "किसान का आधार कार्ड व मोबाइल नंबर",
            "खसरा संख्या व खेत का पता"
        ],
        "application_process": {
            "en": "Soil samples are collected cyclically by state agriculture department staff and local KVKs. Farmers can also submit soil samples directly to the nearest block laboratory. Check status on soilhealth.dac.gov.in.",
            "hi": "कृषि विभाग के अधिकारी व कृषि विज्ञान केंद्र (KVK) द्वारा खेत से मिट्टी के नमूने लिए जाते हैं। किसान खुद भी अपने ब्लॉक की मिट्टी जांच प्रयोगशाला में 500 ग्राम सूखी मिट्टी का नमूना जमा कर सकते हैं। पोर्टल पर कार्ड डाउनलोड करें।"
        },
        "official_portal": "https://soilhealth.dac.gov.in/",
        "helpline": {
            "toll_free": "1800-180-1551",
            "note": "निकटतम कृषि विज्ञान केंद्र (KVK) अथवा किसान कॉल सेंटर से प्रयोगशाला का पता जानें।"
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "last_verified": "2026-11-01",
        "sources": ["src-soilhealth-portal-001"]
    },
    {
        "id": "scheme-national-agri-mechanization-001",
        "scheme_id": "agri-mechanization",
        "category": "farm_machinery",
        "name": {
            "en": "Sub-Mission on Agricultural Mechanization (SMAM)",
            "hi": "कृषि यंत्रीकरण उप-मिशन (एसएमएएम) व कृषि यंत्र अनुदान"
        },
        "scope": "National",
        "department": "Mechanization and Technology Division, MoA&FW",
        "purpose": {
            "en": "Subsidize modern farm implements, tractors, crop residue management machines, and custom hiring centers.",
            "hi": "आधुनिक कृषि यंत्रों (ट्रैक्टर, रोटावेटर, सुपर सीडर, हैप्पी सीडर, लेजर लैंड लेवलर) पर सब्सिडी और कस्टम हायरिंग सेंटर की स्थापना।"
        },
        "benefits": {
            "en": "40% to 50% subsidy on procurement of individual agricultural machinery (higher for SC/ST/women farmers) and up to 80% on establishing village Custom Hiring Centers (CHCs).",
            "hi": "व्यक्तिगत कृषि यंत्रों की खरीद पर 40% से 50% सरकारी अनुदान (महिला व अनुसूचित जाति/जनजाति किसानों हेतु अधिक)। कस्टम हायरिंग सेंटर (CHC) स्थापना हेतु 40-80% तक सहायता।"
        },
        "eligibility": {
            "en": "Individual farmers, Farmer Producer Organizations (FPOs), Cooperative societies, and rural entrepreneurs.",
            "hi": "सभी पात्र किसान, महिला किसान, स्वयं सहायता समूह (SHG), एफपीओ (FPO) व सहकारी समितियां।"
        },
        "exclusion_criteria": [
            "जिन्होंने पिछले 3 से 5 वर्षों में उसी यंत्र पर सरकारी सब्सिडी प्राप्त की हो"
        ],
        "required_documents": [
            "आधार कार्ड (Aadhaar Card)",
            "जमीन की वर्तमान जमाबंदी/खतौनी",
            "बैंक पासबुक की प्रति",
            "जाति प्रमाण पत्र (यदि लागू हो)",
            "ट्रैक्टर चालित यंत्र हेतु ट्रैक्टर की वैध आरसी (Tractor RC)"
        ],
        "application_process": {
            "en": "Apply through Direct Benefit Transfer in Agriculture Mechanization portal (agrimachinery.nic.in) or state portals (e.g. Haryana Meri Fasal Mera Byora / UP Agri DBT) when target windows open.",
            "hi": "प्रत्यक्ष लाभ अंतरण (DBT) पोर्टल agrimachinery.nic.in अथवा राज्य के कृषि यंत्र पोर्टल (जैसे हरियाणा मेरी फसल मेरा ब्यौरा / यूपी पारदर्शी किसान सेवा) पर लक्ष्य जारी होने पर ऑनलाइन आवेदन करें।"
        },
        "official_portal": "https://agrimachinery.nic.in/",
        "helpline": {
            "toll_free": "1800-180-1551",
            "note": "कृषि उप-निदेशक (DDA) या सहायक कृषि अभियंता कार्यालय से संपर्क करें।"
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "last_verified": "2026-11-01",
        "sources": ["src-agrimachinery-portal-001"]
    },
    {
        "id": "scheme-national-mkisan-001",
        "scheme_id": "mkisan",
        "category": "information_services",
        "name": {
            "en": "mKisan SMS Portal for Farmers",
            "hi": "एमकिसान पोर्टल (एसएमएस कृषि सलाह सेवा)"
        },
        "scope": "National",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "purpose": {
            "en": "Deliver targeted crop, weather, market, and package of practices advisories via free SMS in regional languages.",
            "hi": "किसानों को उनकी भाषा में मौसम, मंडी भाव, कीट चेतावनी और कृषि सलाह की मुफ्त एसएमएस सेवा प्रदान करना।"
        },
        "benefits": {
            "en": "Free personalized push SMS alerts tailored to the farmer's registered location and preferred crop. No internet required on basic feature phones.",
            "hi": "साधारण कीपैड फोन पर भी बिना इंटरनेट अपनी भाषा में मौसम की चेतावनी, कीट अलर्ट और मंडी भाव के मुफ्त एसएमएस।"
        },
        "eligibility": {
            "en": "Any farmer or rural citizen possessing a mobile number.",
            "hi": "भारत का कोई भी किसान जिसके पास मोबाइल फोन हो।"
        },
        "exclusion_criteria": [],
        "required_documents": [
            "मोबाइल नंबर व किसान का नाम",
            "राज्य, जिला व पसंदीदा फसल"
        ],
        "application_process": {
            "en": "Self-register on mkisan.gov.in, call Kisan Call Center 1800-180-1551, or SMS 'KISAAN REG <NAME>,<STATE>,<DISTRICT>,<PIN>' to 51969.",
            "hi": "mkisan.gov.in पोर्टल पर पंजीकरण करें, या किसान कॉल सेंटर 1800-180-1551 पर कॉल करके अपना नंबर व फसल दर्ज कराएं।"
        },
        "official_portal": "https://mkisan.gov.in/",
        "helpline": {
            "toll_free": "1800-180-1551",
            "note": "टोल फ्री नंबर पर कॉल करके मुफ्त एसएमएस सेवा शुरू कराएं।"
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "last_verified": "2026-11-01",
        "sources": ["src-mkisan-portal-001"]
    }
]

class SchemesService:
    """Service providing verified details on central and state agricultural schemes."""

    def get_all_schemes(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        if not category or category == "all":
            return SCHEMES_CATALOG
        return [s for s in SCHEMES_CATALOG if s.get("category") == category]

    def get_scheme_by_id(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        sid = scheme_id.strip().lower()
        for s in SCHEMES_CATALOG:
            if s.get("id").lower() == sid or s.get("scheme_id").lower() == sid:
                return s
        return None

    def search_schemes(self, query: str) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return SCHEMES_CATALOG
        matches = []
        for s in SCHEMES_CATALOG:
            s_name_en = (s.get("name") or {}).get("en", "").lower()
            s_name_hi = (s.get("name") or {}).get("hi", "").lower()
            s_id = s.get("scheme_id", "").lower()
            s_pur = str(s.get("purpose", "")).lower()
            s_ben = str(s.get("benefits", "")).lower()

            if any(term in s_name_en or term in s_name_hi or term in s_id or term in s_pur or term in s_ben for term in q.split()):
                matches.append(s)
        return matches

schemes_service = SchemesService()

