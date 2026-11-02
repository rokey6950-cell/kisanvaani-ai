import os
import json

SEEDS_DIR = r"D:\kisanvaani-ai\knowledge\seeds"

seed_varieties_data = [
    {
        "id": "seedvar-wheat-dbw187-001",
        "crop_id": "wheat",
        "variety": "DBW 187 (Karan Vandana)",
        "state": "Haryana, Punjab, UP",
        "zone": "North Western Plain Zone (NWPZ)",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "55-60 क्विंटल प्रति हेक्टेयर", "en": "55-60 quintals per hectare"},
        "features": {
            "hi": "पीला रतुआ (Yellow Rust) के प्रति सहनशील, चपाती की उत्कृष्ट गुणवत्ता और उच्च प्रोटीन युक्त।",
            "en": "Resistant to yellow rust, excellent chapati quality, high protein content."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "detailed_sections": {
            "variety_overview": "DBW 187 is a high yielding wheat variety recommended for NWPZ under timely sown irrigated conditions.",
            "resistance": "Highly resistant against yellow and brown rusts."
        },
        "full_text": "DBW 187 Karan Vandana wheat variety characteristics, yield, and disease resistance."
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
        "yield_potential": {"hi": "50-55 क्विंटल प्रति हेक्टेयर", "en": "50-55 quintals per hectare"},
        "features": {
            "hi": "गर्मी सहन करने की क्षमता (Heat tolerance), समय पर बुवाई के लिए उत्तम।",
            "en": "Heat tolerant variety, excellent for timely sowing in northern plains."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "detailed_sections": {
            "variety_overview": "HD 3086 Pusa Gautami is adapted to timely sown irrigated conditions with strong lodging resistance.",
            "resistance": "Good tolerance to terminal heat stress."
        },
        "full_text": "HD 3086 wheat variety agronomic traits and yield performance."
    },
    {
        "id": "seedvar-rice-pr126-001",
        "crop_id": "rice",
        "variety": "PR 126",
        "state": "Punjab, Haryana",
        "zone": "North Western Zone",
        "sowing_condition": "Puddled transplanted / Direct seeded",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "30-32 क्विंटल प्रति एकड़", "en": "30-32 quintals per acre"},
        "features": {
            "hi": "कम अवधि में पकने वाली (लगभग 90-95 दिन), पानी की कम खपत।",
            "en": "Short duration variety (90-95 days), saves water and allows timely wheat sowing."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-pau-rice-001"],
        "detailed_sections": {
            "variety_overview": "PR 126 is an early maturing paddy variety developed by PAU Ludhiana.",
            "resistance": "Resistant to lodging and tolerant to major bacterial blight strains."
        },
        "full_text": "PR 126 paddy variety maturity duration, yield and water saving benefits."
    }
]

seed_recommendations_data = [
    {
        "id": "seedrec-wheat-haryana-001",
        "crop_id": "wheat",
        "state": "Haryana",
        "crop_record_id": "crop-wheat-haryana-sowing-001",
        "seed_rate": {
            "timely_sowing": "40 kg per acre (100 kg/ha)",
            "late_sowing": "50 kg per acre (125 kg/ha)"
        },
        "seed_treatment": {
            "hi": "बुवाई से पहले बीज को कार्बेन्डाजिम (2 ग्राम प्रति किलो बीज) या ट्राइकोडर्मा से उपचारित अवश्य करें।",
            "en": "Treat seeds with Carbendazim @ 2g per kg of seed or Trichoderma before sowing."
        },
        "sowing_depth": "4-5 cm in moisture zone",
        "row_spacing": "20-22.5 cm",
        "applies_only_to": "Haryana and Punjab region",
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {
            "guidelines": "Complete seed rate, depth, spacing and seed treatment protocol for wheat in Haryana."
        },
        "full_text": "Wheat seed rate, spacing, depth and treatment protocols for Haryana."
    },
    {
        "id": "seedrec-paddy-haryana-001",
        "crop_id": "rice",
        "state": "Haryana",
        "crop_record_id": "crop-paddy-seed-001",
        "seed_rate": {
            "basmati": "8-10 kg per acre",
            "non_basmati": "10-12 kg per acre"
        },
        "seed_treatment": {
            "hi": "नमक के घोल (10%) से छंटाई के बाद कार्बेन्डाजिम और स्ट्रेप्टोसाइक्लिन से उपचारित करें।",
            "en": "Soak seeds in 10% saltwater solution to discard chaff, then treat with carbendazim and streptocycline."
        },
        "applies_only_to": "Haryana",
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {
            "guidelines": "Paddy nursery seed rate and chemical treatment guidelines."
        },
        "full_text": "Paddy nursery sowing seed rate and treatment guidelines for Haryana."
    }
]

with open(os.path.join(SEEDS_DIR, "seed_varieties.json"), "w", encoding="utf-8") as f:
    json.dump(seed_varieties_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(SEEDS_DIR, "seed_recommendations.json"), "w", encoding="utf-8") as f:
    json.dump(seed_recommendations_data, f, ensure_ascii=False, indent=2)

print("Successfully updated knowledge/seeds/ files with detailed seed varieties and recommendations.")
