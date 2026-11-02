import os
import json

SEEDS_DIR = r"D:\kisanvaani-ai\knowledge\seeds"

seed_varieties_data = [
    {
        "id": "seedvar-wheat-hd2967-001",
        "crop_id": "wheat",
        "variety": "HD 2967",
        "state": "Haryana, Punjab, UP",
        "zone": "North Western Plain Zone",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "50-55 क्विंटल प्रति हेक्टेयर", "en": "50-55 q/ha"},
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "detailed_sections": {"overview": "Popular wheat variety in NWPZ."},
        "full_text": "HD 2967 wheat variety."
    },
    {
        "id": "seedvar-wheat-dbw187-001",
        "crop_id": "wheat",
        "variety": "DBW 187 (Karan Vandana)",
        "state": "Haryana, Punjab, UP",
        "zone": "North Western Plain Zone (NWPZ)",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "55-60 क्विंटल प्रति हेक्टेयर", "en": "55-60 q/ha"},
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "detailed_sections": {"overview": "Resistant to yellow rust, high protein."},
        "full_text": "DBW 187 Karan Vandana wheat variety."
    },
    {
        "id": "seedvar-wheat-hd3086-001",
        "crop_id": "wheat",
        "variety": "HD 3086 (Pusa Gautami)",
        "state": "Haryana, Punjab, Delhi",
        "zone": "North Western Plain Zone",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "50-55 क्विंटल प्रति हेक्टेयर", "en": "50-55 q/ha"},
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-landmark-001"],
        "detailed_sections": {"overview": "Heat tolerant variety."},
        "full_text": "HD 3086 wheat variety."
    },
    {
        "id": "seedvar-wheat-wh1105-001",
        "crop_id": "wheat",
        "variety": "WH 1105",
        "state": "Haryana",
        "zone": "North Western Plain Zone",
        "sowing_condition": "Timely sown, irrigated",
        "irrigation_status": "Irrigated",
        "display_allowed": True,
        "yield_potential": {"hi": "52-58 क्विंटल प्रति हेक्टेयर", "en": "52-58 q/ha"},
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {"overview": "HAU recommended high yielding wheat variety."},
        "full_text": "WH 1105 wheat variety."
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
            "hi": "कार्बेन्डाजिम से बीज उपचार।",
            "en": "Carbendazim seed treatment."
        },
        "applies_only_to": "Haryana",
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {"guidelines": "Wheat seed rate and treatment."},
        "full_text": "Wheat seed rate for Haryana."
    }
]

with open(os.path.join(SEEDS_DIR, "seed_varieties.json"), "w", encoding="utf-8") as f:
    json.dump(seed_varieties_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(SEEDS_DIR, "seed_recommendations.json"), "w", encoding="utf-8") as f:
    json.dump(seed_recommendations_data, f, ensure_ascii=False, indent=2)

print("Updated seed_varieties.json with 4+ wheat varieties.")
