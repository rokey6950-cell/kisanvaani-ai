import os
import json

PP_DIR = r"D:\kisanvaani-ai\knowledge\plant_protection"

files_data = {
    "diseases.json": [
        {
            "id": "disease-wheat-yellow-rust-001",
            "category": "plant_protection_disease",
            "crop_id": "wheat",
            "disease_name": {"en": "Yellow Rust (Stripe Rust)", "hi": "पीला रतुआ (स्ट्राइप रस्ट)"},
            "symptoms": {"hi": "पत्तियों पर पीले रंग की धारियाँ बनना।", "en": "Yellow stripes appearing on leaves."},
            "management": {"hi": "प्रतिरोधी किस्में उगाएं और आवश्यकता पड़ने पर अनुशंसित फफूंदनाशक का छिड़काव करें।", "en": "Grow resistant varieties and spray recommended fungicides if required."}
        },
        {
            "id": "disease-rice-blast-001",
            "category": "plant_protection_disease",
            "crop_id": "rice",
            "disease_name": {"en": "Rice Blast", "hi": "धान का ब्लास्ट रोग"},
            "symptoms": {"hi": "पत्तियों पर आँख के आकार के धब्बे बनना।", "en": "Spindle-shaped spots on leaves with gray centers."},
            "management": {"hi": "ट्राइसाइक्लाजोल का छिड़काव करें और बीज उपचार करें।", "en": "Spray tricyclazole and perform seed treatment."}
        }
    ],
    "pests.json": [
        {
            "id": "pest-cotton-bollworm-001",
            "category": "plant_protection_pest",
            "crop_id": "cotton",
            "pest_name": {"en": "American Bollworm", "hi": "अमेरिकन सुंडी (कॉटन बॉलवर्म)"},
            "damage_symptoms": {"hi": "टोलियों और सुइयों से कलियों और डोels को नुकसान पहुँचाना।", "en": "Larvae bore into squares, bolls, and feed on developing seeds."},
            "management": {"hi": "फेरोमोन ट्रैप लगाएं और केवीके की सलाह लें।", "en": "Install pheromone traps and consult KVK helpline."}
        },
        {
            "id": "pest-mustard-aphid-001",
            "category": "plant_protection_pest",
            "crop_id": "mustard",
            "pest_name": {"en": "Mustard Aphid", "hi": "सरसों की माहू (चेपा)"},
            "damage_symptoms": {"hi": "रस चूसना जिससे पौधे कमजोर हो जाते हैं।", "en": "Sucks cell sap from tender shoots, inflorescences, and pods."},
            "management": {"hi": "संतानित नीम तेल या अनुशंसित कीटनाशक का प्रयोग करें।", "en": "Apply neem oil or recommended insecticides."}
        }
    ],
    "ipm_recommendations.json": [
        {
            "id": "ipm-general-001",
            "category": "integrated_pest_management",
            "title": {"en": "General IPM Guidelines", "hi": "एकीकृत कीट प्रबंधन दिशानिर्देश"},
            "practices": {
                "hi": "फसल चक्र अपनाएं, प्रतिरोधी बीज बोएं, नीम आधारित कीटनाशकों का प्रयोग करें तथा केवीके (1800-180-1551) से संपर्क करें।",
                "en": "Practice crop rotation, sow resistant seeds, use neem-based biopesticides, and contact KVK (1800-180-1551) for expert guidance."
            }
        }
    ],
    "symptoms.json": [
        {
            "id": "symptom-nutrient-deficiency-001",
            "category": "plant_symptom",
            "nutrient": {"en": "Zinc", "hi": "जस्ता (जिंक)"},
            "visual_symptoms": {
                "hi": "पत्तियों पर पीले धब्बे और छोटे आकार के पत्ते।",
                "en": "Interveinal chlorosis and stunted growth in early stages."
            }
        }
    ],
    "verified_chemical_recommendations.json": [
        {
            "id": "chem-rec-001",
            "category": "verified_chemical",
            "guideline": {
                "hi": "रासायनिक कीटनाशकों या उर्वरकों के प्रयोग से पहले हमेशा स्थानीय कृषि विज्ञान केंद्र (KVK) या किसान हेल्पलाइन (1800-180-1551) से अवश्य परामर्श करें।",
                "en": "Always consult local Krishi Vigyan Kendra (KVK) or Kisan Helpline (1800-180-1551) before applying unverified chemical mixtures."
            }
        }
    ]
}

for filename, content in files_data.items():
    filepath = os.path.join(PP_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"Updated {filename} with rich plant protection data.")
