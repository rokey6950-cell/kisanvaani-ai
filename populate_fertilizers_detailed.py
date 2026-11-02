import os
import json

FERT_DIR = r"D:\kisanvaani-ai\knowledge\fertilizers"

fertilizer_catalog_data = [
    {
        "id": "fert-cat-urea-001",
        "category": "fertilizer_catalog_item",
        "fertilizer_name": {"en": "Neem Coated Urea (NCU)", "hi": "नीम लेपित यूरिया (NCU)"},
        "nutrient_composition": {"nitrogen_n": "46%", "phosphorus_p": "0%", "potassium_k": "0%"},
        "physical_properties": {
            "hi": "सफेद गोल दानेदार, पानी में पूर्णतः घुलनशील, धीमी गति से नाइट्रोजन छोड़ने वाला (Slow release)।",
            "en": "White spherical prills, water soluble, slow nitrogen release due to neem coating."
        },
        "benefits": {
            "hi": "पौधों को लगातार नाइट्रोजन मिलती है, लीचिंग व वाष्पीकरण से नुकसान कम होता है, और कीटों से सुरक्षा मिलती है।",
            "en": "Provides steady nitrogen uptake, reduces leaching/volatilization losses, and deters soil pests."
        },
        "application_guidelines": {
            "hi": "इसे बेसल डोज़ के रूप में और सिंचाई के बाद स्प्लिट डोज़ (विभाजित मात्रा) में दें। अधिक मात्रा से बचें।",
            "en": "Apply as basal dose and in split doses post-irrigation. Avoid excessive application."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-fertilizer-001"]
    },
    {
        "id": "fert-cat-dap-002",
        "category": "fertilizer_catalog_item",
        "fertilizer_name": {"en": "Di-Ammonium Phosphate (DAP)", "hi": "डाई-अमोनियम फॉस्फेट (DAP)"},
        "nutrient_composition": {"nitrogen_n": "18%", "phosphorus_p": "46% (P2O5)", "potassium_k": "0%"},
        "physical_properties": {
            "hi": "भूरे या काले रंग के दाने, जड़ विकास के लिए अत्यंत उपयोगी।",
            "en": "Dark brown/black granules, highly effective for early root development and establishment."
        },
        "benefits": {
            "hi": "मजबूत जड़ प्रणाली का विकास, फूल और बीज निर्माण में सहायता।",
            "en": "Promotes vigorous root system development, robust flowering, and grain formation."
        },
        "application_guidelines": {
            "hi": "बुवाई के समय बीज के नीचे गहराई में (Band placement) दें ताकि पौधों को सीधे पोषण मिले।",
            "en": "Apply as basal placement below seed depth at sowing time for maximum root contact."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-fertilizer-001"]
    },
    {
        "id": "fert-cat-mop-003",
        "category": "fertilizer_catalog_item",
        "fertilizer_name": {"en": "Muriate of Potash (MOP / Potassium Chloride)", "hi": "म्यूरेट ऑफ पोटाश (MOP / पोटेशियम क्लोराइड)"},
        "nutrient_composition": {"nitrogen_n": "0%", "phosphorus_p": "0%", "potassium_k": "60% (K2O)"},
        "physical_properties": {
            "hi": "लाल या गुलाबी क्रिस्टलीय चूर्ण, पानी में घुलनशील।",
            "en": "Reddish-pink crystalline powder, water soluble potassic fertilizer."
        },
        "benefits": {
            "hi": "फसल में सूखा सहन करने की क्षमता, तना मजबूत करना, और उपज की गुणवत्ता व आकार बढ़ाना।",
            "en": "Enhances drought resistance, strengthens stalks against lodging, and improves grain/fruit quality."
        },
        "application_guidelines": {
            "hi": "बुवाई के समय या कल्ले निकलते समय मिट्टी में मिलाएँ।",
            "en": "Apply during land preparation or basal dressing."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-fertilizer-001"]
    },
    {
        "id": "fert-cat-npk-004",
        "category": "fertilizer_catalog_item",
        "fertilizer_name": {"en": "NPK Complex 12:32:16", "hi": "एनपीके कॉम्प्लेक्स 12:32:16"},
        "nutrient_composition": {"nitrogen_n": "12%", "phosphorus_p": "32%", "potassium_k": "16%"},
        "physical_properties": {
            "hi": "सफेद या भूरे रंग के दाने जिनमें तीन मुख्य पोषक तत्व संतुलित रूप में होते हैं।",
            "en": "Uniform compound granules containing balanced primary macronutrients."
        },
        "benefits": {
            "hi": "एक साथ नाइट्रोजन, फास्फोरस और पोटाश की पूर्ति, शुरुआती बढ़वार और जड़ विकास के लिए उत्तम।",
            "en": "Simultaneous supply of N, P, and K for uniform early seedling growth and robust crop establishment."
        },
        "application_guidelines": {
            "hi": "बुवाई के वक्त बेसल खाद के रूप में उपयोग करें।",
            "en": "Apply basally during final land preparation."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-fertilizer-001"]
    },
    {
        "id": "fert-cat-zinc-005",
        "category": "fertilizer_catalog_item",
        "fertilizer_name": {"en": "Zinc Sulfate (21% Zn)", "hi": "जिंक सल्फेट (21% जस्ता)"},
        "nutrient_composition": {"zinc_zn": "21%", "sulfur_s": "10%"},
        "physical_properties": {
            "hi": "सफेद क्रिस्टलीय चूर्ण, पानी में घुलनशील सूक्ष्म पोषक तत्व।",
            "en": "White crystalline powder, essential micronutrient for cereal and pulse crops."
        },
        "benefits": {
            "hi": "खैरा रोग से बचाव, प्रकाश संश्लेषण (Photosynthesis) में सुधार और एंजाइम सक्रियता बढ़ाना।",
            "en": "Prevents khaira disease in rice, improves enzymatic activities and chlorophyll synthesis."
        },
        "application_guidelines": {
            "hi": "10 किलोग्राम प्रति एकड़ यूरिया या गोबर की खाद के साथ मिलाकर मिट्टी में डालें।",
            "en": "Apply 10 kg per acre mixed with soil or FYM during land preparation."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-icar-fertilizer-001"]
    }
]

fertilizer_recommendations_data = [
    {
        "id": "fert-rec-wheat-001",
        "crop_id": "wheat",
        "state": "Haryana & Punjab",
        "recommended_dose_per_acre": {
            "nitrogen_n": "50-65 kg (approx 110-140 kg Urea)",
            "phosphorus_p": "24-30 kg (approx 50-65 kg DAP)",
            "potassium_k": "15-20 kg (approx 25-30 kg MOP)"
        },
        "application_schedule": {
            "hi": "1. बुवाई के समय (बेसल): सारा फास्फोरस (DAP), सारा पोटाश (MOP) और 1/3 नाइट्रोजन (यूरिया)।\n2. पहली सिंचाई (CRI अवस्था - 20-25 DAS): 1/3 नाइट्रोजन (यूरिया)।\n3. दूसरी सिंचाई (कल्ले निकलते समय - 40-45 DAS): शेष 1/3 नाइट्रोजन (यूरिया)।",
            "en": "1. Basal at sowing: All Phosphorus, all Potassium, and 1/3rd Nitrogen.\n2. First irrigation (CRI stage, 20-25 DAS): 1/3rd Nitrogen.\n3. Second irrigation (Tillering stage, 40-45 DAS): Remaining 1/3rd Nitrogen."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {
            "guidelines": "Complete NPK split fertilizer schedule for high yielding wheat cultivation in northern plains."
        },
        "full_text": "Wheat fertilizer recommendation schedule per acre for Haryana and Punjab."
    },
    {
        "id": "fert-rec-rice-002",
        "crop_id": "rice",
        "state": "Haryana & Punjab",
        "recommended_dose_per_acre": {
            "nitrogen_n": "50-60 kg (approx 110-130 kg Urea)",
            "phosphorus_p": "20 kg (approx 45 kg DAP)",
            "potassium_k": "20 kg (approx 30 kg MOP)",
            "zinc_sulfate": "10 kg"
        },
        "application_schedule": {
            "hi": "1. रोपाई के समय बेसल डोज़ के रूप में फास्फोरस, पोटाश, जिंक और 1/3 नाइट्रोजन दें।\n2. रोपाई के 3 सप्ताह बाद पहली टॉप ड्रेसिंग (1/3 नाइट्रोजन)।\n3. रोपाई के 6 सप्ताह बाद दूसरी टॉप ड्रेसिंग (शेष 1/3 नाइट्रोजन)।",
            "en": "1. Basal at transplanting: P, K, Zinc, and 1/3rd N.\n2. 3 weeks after transplanting: 1/3rd N.\n3. 6 weeks after transplanting: Remaining 1/3rd N."
        },
        "verification_status": "verified",
        "data_type": "official_static",
        "source_ids": ["src-hau-pop-001"],
        "detailed_sections": {
            "guidelines": "Paddy NPK and Zinc fertilizer schedule."
        },
        "full_text": "Paddy fertilizer recommendation schedule per acre."
    }
]

with open(os.path.join(FERT_DIR, "fertilizer_catalog.json"), "w", encoding="utf-8") as f:
    json.dump(fertilizer_catalog_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(FERT_DIR, "fertilizer_recommendations.json"), "w", encoding="utf-8") as f:
    json.dump(fertilizer_recommendations_data, f, ensure_ascii=False, indent=2)

print("Successfully populated knowledge/fertilizers/ with detailed catalog and recommendations.")
