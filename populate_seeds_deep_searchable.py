import os
import json

SEEDS_DIR = r"D:\kisanvaani-ai\knowledge\seeds"

seed_varieties_detailed = [
    {
        "id": "seedvar-wheat-hd2967-001",
        "crop_id": "wheat",
        "variety": "HD 2967",
        "state": "Haryana, Punjab, Uttar Pradesh, Rajasthan",
        "zone": "North Western Plain Zone (NWPZ)",
        "sowing_condition": "Timely sown, irrigated conditions",
        "irrigation_status": "Irrigated (5-6 critical irrigations)",
        "display_allowed": True,
        "yield_potential": {"hi": "50-55 क्विंटल प्रति हेक्टेयर", "en": "50-55 quintals per hectare"},
        "maturity_period": {"hi": "140-145 दिन", "en": "140-145 days"},
        "resistance": {"hi": "पीला और भूरा रतुआ के प्रति सहनशील", "en": "Tolerant to yellow and brown rusts"},
        "features": {
            "hi": "यह उत्तर भारत में सबसे लोकप्रिय किस्मों में से एक है। इसका तना मजबूत होता है जिससे फसल गिरती नहीं है। इसकी चपाती की गुणवत्ता उत्कृष्ट है।",
            "en": "One of the most popular wheat varieties in northern India. Possesses strong stems preventing lodging and has excellent chapati-making qualities."
        },
        "detailed_sections": {
            "agronomic_traits": "High tillering capacity, dark green foliage, medium height, resistant to lodging under normal irrigation.",
            "fertilizer_response": "Responds very well to balanced NPK application (120:60:40 kg NPK/ha)."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "full_text": "Detailed agronomic profile of HD 2967 wheat variety covering yield, duration, resistance, and fertilizer response."
    },
    {
        "id": "seedvar-wheat-dbw187-001",
        "crop_id": "wheat",
        "variety": "DBW 187 (Karan Vandana)",
        "state": "Haryana, Punjab, Western UP, Bihar",
        "zone": "North Western & North Eastern Plain Zones",
        "sowing_condition": "Timely sown, high fertility irrigated conditions",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "55-60 क्विंटल प्रति हेक्टेयर (अधिकतम 75 क्विंटल)", "en": "55-60 q/ha (max up to 75 q/ha)"},
        "maturity_period": {"hi": "120-125 दिन", "en": "120-125 days"},
        "resistance": {"hi": "पीला और भूरा रतुआ (Yellow & Brown Rust) के प्रति उच्च प्रतिरोधक", "en": "Highly resistant to yellow and brown rusts"},
        "features": {
            "hi": "आईआईडब्ल्यूबीआर (IIWBR Karnal) द्वारा विकसित यह बायोफोर्टिफाइड किस्म उच्च प्रोटीन (लगभग 12%) और आयरन से भरपूर है।",
            "en": "Developed by IIWBR Karnal, this biofortified variety has high protein (~12%) and iron content, with exceptional resistance to rust diseases."
        },
        "detailed_sections": {
            "agronomic_traits": "Semi-dwarf plant type, erect leaves, bold amber grains, high sink capacity.",
            "disease_resistance": "Immune to stripe rust under normal field conditions."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "full_text": "DBW 187 Karan Vandana biofortified wheat variety comprehensive profile."
    },
    {
        "id": "seedvar-wheat-hd3086-001",
        "crop_id": "wheat",
        "variety": "HD 3086 (Pusa Gautami)",
        "state": "Haryana, Punjab, Delhi, Western UP",
        "zone": "North Western Plain Zone (NWPZ)",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "50-55 क्विंटल प्रति हेक्टेयर", "en": "50-55 q/ha"},
        "maturity_period": {"hi": "142 दिन", "en": "142 days"},
        "resistance": {"hi": "टर्मिनल हीट टॉलरेंट (गर्मी सहन करने की क्षमता) और रतुआ रोधी", "en": "Terminal heat tolerance and rust resistant"},
        "features": {
            "hi": "यह किस्म तापमान में अचानक वृद्धि (टर्मिनल हीट) को सहन करने में सक्षम है, जिससे दाने सिकुड़ते नहीं हैं।",
            "en": "Equipped with strong terminal heat tolerance, ensuring grain filling is not affected by sudden temperature spikes in spring."
        },
        "detailed_sections": {
            "climate_adaptability": "Performs exceptionally well under late October to mid-November sowing windows in NWPZ."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "full_text": "HD 3086 Pusa Gautami wheat variety comprehensive agronomic traits."
    },
    {
        "id": "seedvar-wheat-wh1105-001",
        "crop_id": "wheat",
        "variety": "WH 1105",
        "state": "Haryana, Punjab",
        "zone": "North Western Plain Zone (NWPZ)",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "52-58 क्विंटल प्रति हेक्टेयर", "en": "52-58 q/ha"},
        "maturity_period": {"hi": "143 दिन", "en": "143 days"},
        "resistance": {"hi": "पीला रतुआ और सिंचित अवस्था के अनुकूल", "en": "Stripe rust resistant and tailored for high fertility irrigated soils"},
        "features": {
            "hi": "चौधरी चरण सिंह हरियाणा कृषि विश्वविद्यालय (HAU Hissar) द्वारा विकसित अत्यधिक उत्पादक किस्म।",
            "en": "High-yielding variety released by CCS HAU Hissar with bold grains and excellent baking quality."
        },
        "detailed_sections": {
            "fertility_management": "Requires adequate NPK fertilizer split across CRI, tillering and heading stages."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "full_text": "WH 1105 wheat variety detailed cultivation profile."
    }
]

seed_recommendations_detailed = [
    {
        "id": "seedrec-wheat-comprehensive-001",
        "crop_id": "wheat",
        "state": "Haryana & North India",
        "crop_record_id": "crop-wheat-haryana-sowing-001",
        "seed_rate": {
            "timely_sowing": "40 kg per acre (100 kg/ha)",
            "late_sowing": "50 kg per acre (125 kg/ha)"
        },
        "seed_depth": "4 to 5 cm in moist soil zone",
        "row_spacing": "20 cm to 22.5 cm between rows",
        "seed_treatment_protocol": {
            "hi": "फफूंद जनित रोगों से बचाव के लिए कार्बेन्डाजिम 50% WP (2 ग्राम प्रति किलो बीज) या ट्राइकोडर्मा (4 ग्राम प्रति किलो बीज) से उपचारित करें। दीमक प्रभावित क्षेत्रों में क्लोरपाइरीफोस से उपचार करें।",
            "en": "Treat seeds with Carbendazim 50% WP @ 2g per kg or Trichoderma @ 4g per kg to protect against seed-borne and soil-borne fungal pathogens."
        },
        "critical_stages_irrigation": {
            "hi": "1. सीआरआई अवस्था (बुवाई के 20-25 दिन बाद) - सबसे महत्वपूर्ण\n2. कल्ले निकलते समय (40-45 दिन)\n3. गाँठ बनते समय (60-65 दिन)\n4. बालियाँ निकलते समय (80-85 दिन)\n5. दाना भरते समय (100-105 दिन)",
            "en": "1. CRI stage (20-25 DAS) - Most critical\n2. Tillering (40-45 DAS)\n3. Jointing (60-65 DAS)\n4. Heading (80-85 DAS)\n5. Grain filling (100-105 DAS)"
        },
        "applies_only_to": "Haryana, Punjab, and North-Western Plain Zone",
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {
            "complete_guidelines": "Exhaustive seed rate, treatment, depth, spacing, and irrigation schedules for wheat."
        },
        "full_text": "Comprehensive seed rate, treatment, depth, spacing and irrigation schedule for wheat cultivation."
    }
]

with open(os.path.join(SEEDS_DIR, "seed_varieties.json"), "w", encoding="utf-8") as f:
    json.dump(seed_varieties_detailed, f, ensure_ascii=False, indent=2)

with open(os.path.join(SEEDS_DIR, "seed_recommendations.json"), "w", encoding="utf-8") as f:
    json.dump(seed_recommendations_detailed, f, ensure_ascii=False, indent=2)

print("Successfully updated knowledge/seeds/ files with highly detailed prexipility-searchable data.")
