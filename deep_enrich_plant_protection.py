import os
import json

PP_DIR = r"D:\kisanvaani-ai\knowledge\plant_protection"

detailed_data = {
    "diseases.json": [
        {
            "id": "disease-wheat-yellow-rust-001",
            "category": "plant_protection_disease",
            "crop_id": "wheat",
            "disease_name": {"en": "Yellow Rust (Stripe Rust)", "hi": "पीला रतुआ (स्ट्राइप रस्ट)"},
            "pathogen": {"en": "Puccinia striiformis", "hi": "पुकिसिनिया स्ट्राइफॉर्मिस"},
            "favorable_conditions": {"hi": "कम तापमान (10-15°C) और उच्च आर्द्रता या बारिश।", "en": "Low temperature (10-15°C) and high relative humidity or winter rains."},
            "symptoms": {
                "hi": "पत्तियों की ऊपरी सतह पर पीले रंग की धारियाँ (धब्बे) कतार में बनना, जिन पर पीले चूर्ण (बीजाणु) पाए जाते हैं। अत्यधिक संक्रमण से पत्तियाँ सूख जाती हैं और दाने सिकुड़ जाते हैं।",
                "en": "Bright yellow pustules forming stripes along the leaf veins. Severe infection leads to premature leaf drying and shriveled grains."
            },
            "management": {
                "hi": "प्रतिरोधी किस्में (जैसे HD 3086, DBW 187) उगाएं। लक्षण दिखते ही प्रोपコナज़ोल (Propiconazole 25 EC) 200 मिली प्रति एकड़ 200 लीटर पानी में मिलाकर छिड़काव करें।",
                "en": "Grow resistant varieties. Spray Propiconazole 25 EC @ 200 ml in 200 liters of water per acre at the appearance of initial symptoms."
            }
        },
        {
            "id": "disease-rice-blast-001",
            "category": "plant_protection_disease",
            "crop_id": "rice",
            "disease_name": {"en": "Rice Blast", "hi": "धान का ब्लास्ट (पाइरिकुलरिया) रोग"},
            "pathogen": {"en": "Pyricularia oryzae", "hi": "पाइरिकुलरिया ओरिजी"},
            "favorable_conditions": {"hi": "बादल छाए रहना, अधिक आर्द्रता, और रात का तापमान कम होना।", "en": "Overcast skies, high relative humidity, intermittent drizzle, and cooler night temperatures."},
            "symptoms": {
                "hi": "पत्तियों पर आँख के आकार (spindle-shaped) के धब्बे जिनके बीच का हिस्सा भूरा-सफेद होता है। गर्दन पर संक्रमण होने पर बाली टूट जाती है जिसे 'नेक ब्लास्ट' कहते हैं।",
                "en": "Spindle-shaped lesions on leaves with gray centers and brown margins. Node/neck infection causes the panicle to break off (neck blast)."
            },
            "management": {
                "hi": "बीज उपचार कार्बेन्डाजिम से करें। लक्षण दिखते ही ट्राइसाइक्लाजोल (Tricyclazole 75% WP) 0.6 ग्राम प्रति लीटर पानी में घोलकर छिड़काव करें।",
                "en": "Treat seeds with carbendazim. Spray Tricyclazole 75% WP @ 0.6g per liter of water at first sign of infection."
            }
        },
        {
            "id": "disease-cotton-root-rot-001",
            "category": "plant_protection_disease",
            "crop_id": "cotton",
            "disease_name": {"en": "Cotton Root Rot", "hi": "कपास का जड़ गलन (रूट रॉट) रोग"},
            "pathogen": {"en": "Rhizoctonia bataticola", "hi": "राइजोक्टोनिया बटाटिकोला"},
            "favorable_conditions": {"hi": "उच्च तापमान (30-35°C) और मिट्टी में नमी की कमी के बाद अचानक सिंचाई।", "en": "High soil temperature (30-35°C) and alternating dry and wet soil conditions."},
            "symptoms": {
                "hi": "पौधे अचानक मुरझा जाते हैं और पत्तियाँ पीली पड़कर गिर जाती हैं। जड़ें सड़ जाती हैं और छाल आसानी से उतर जाती है।",
                "en": "Sudden wilting of plants, yellowing and shedding of leaves. Roots become dark and bark shreds easily."
            },
            "management": {
                "hi": "गहरी जुताई करें, फसल चक्र अपनाएं और ट्राइकोडर्मा (Trichoderma viride) का गोबर की खाद के साथ प्रयोग करें।",
                "en": "Deep summer ploughing, crop rotation with legumes, and soil application of Trichoderma mixed with FYM."
            }
        }
    ],
    "pests.json": [
        {
            "id": "pest-cotton-bollworm-001",
            "category": "plant_protection_pest",
            "crop_id": "cotton",
            "pest_name": {"en": "American Bollworm", "hi": "अमेरिकन सुंडी (हेलिकोवर्पा आर्मिगेरा)"},
            "damage_symptoms": {
                "hi": "लारवा फूलों की कलियों (squares), फूलों और डोels (bolls) में छेद करके अंदर खाता है। सुंडी का सिर अंदर और शरीर बाहर रहता है।",
                "en": "Larvae bore circular holes into squares, flowers, and bolls, feeding with head inside and body outside."
            },
            "management": {
                "hi": "खेत में फेरोमोन ट्रैप (Pheromone traps) 5-6 प्रति एकड़ लगाएं। पक्षियों के बैठने के लिए 'T' आकार की टंकियाँ लगाएं। आवश्यकता पर KVK की सलाह से कीटनाशक छिड़कें।",
                "en": "Install 5-6 pheromone traps per acre for mass trapping. Erect bird perches ('T' shaped) and consult KVK before chemical application."
            }
        },
        {
            "id": "pest-mustard-aphid-001",
            "category": "plant_protection_pest",
            "crop_id": "mustard",
            "pest_name": {"en": "Mustard Aphid", "hi": "सरसों की माहू / चेपा (लिपिस इरीसिमी)"},
            "damage_symptoms": {
                "hi": "नैनिफ और वयस्क पौधे के कोमल अंगों, फूलों और फलियों से रस चूसते हैं। चिपचिपा पदार्थ (honeydew) छोड़ते हैं जिससे फंगस लग जाती है और पौधा बौना रह जाता है।",
                "en": "Nymphs and adults suck cell sap from tender shoots, inflorescences, and developing pods, secreting honeydew leading to sooty mold."
            },
            "management": {
                "hi": "अक्टूबर के प्रथम सप्ताह में बुवाई पूरी करें। माहू के शुरुआती प्रकोप पर नीम का तेल (Neem oil 0.5%) या इमिडाक्लोप्रिड का छिड़काव करें।",
                "en": "Complete sowing by early October. Spray neem oil (0.5%) or recommended systemic insecticides at early infestation."
            }
        },
        {
            "id": "pest-rice-stem-borer-001",
            "category": "plant_protection_pest",
            "crop_id": "rice",
            "pest_name": {"en": "Yellow Stem Borer", "hi": "धान का पीला तना छेदक"},
            "damage_symptoms": {
                "hi": "सुंडी तने के अंदर घुसकर खाती है जिससे मुख्य गोभ सूख जाती है (Deadheart)। बाद में बालियां सफेद और दाने खाली रह जाते हैं (White ear)।",
                "en": "Larvae bore into stems causing drying of central shoot (deadheart) in vegetative stage and white earheads at reproductive stage."
            },
            "management": {
                "hi": "रोपाई के समय प्रकाश प्रपंच (Light traps) का प्रयोग करें। कार्टाप हाइड्रोक्लोराइड (Cartap hydrochloride 4G) 10 किलो प्रति एकड़ जमीन में दें।",
                "en": "Use light traps. Apply Cartap hydrochloride 4G @ 10 kg per acre in soil at root zone."
            }
        }
    ],
    "ipm_recommendations.json": [
        {
            "id": "ipm-comprehensive-001",
            "category": "integrated_pest_management",
            "title": {"en": "Comprehensive Integrated Pest Management (IPM) Framework", "hi": "व्यापक एकीकृत कीट प्रबंधन (IPM) रूपरेखा"},
            "core_principles": {
                "hi": "एकीकृत कीट प्रबंधन (IPM) पर्यावरण अनुकूल दृष्टिकोण है जो कीटों को आर्थिक क्षति स्तर (ETL) से नीचे रखने के लिए सांस्कृतिक, यांत्रिक, जैविक और विवेकपूर्ण रासायनिक नियंत्रण का संयोजन करता है।",
                "en": "IPM is an ecosystem-based strategy focusing on long-term prevention of pests through a combination of cultural, mechanical, biological, and judicious chemical methods."
            },
            "cultural_practices": {
                "hi": "गहरी ग्रीष्मकालीन जुताई, फसल चक्र अपनाना, रोगमुक्त एवं प्रमाणित बीजों का चयन, और संतुलित उर्वरक (विशेषकर नत्रजन का सीमित प्रयोग) करना।",
                "en": "Deep summer ploughing to expose pupae, crop rotation with non-host crops, selection of certified disease-resistant seeds, and balanced nitrogen fertilization."
            },
            "mechanical_controls": {
                "hi": "हाथ से कीटों व अंडों को एकत्र कर नष्ट करना, पीले रंग के चिपचिपे ट्रैप (Yellow sticky traps) और फेरोमोन ट्रैप का प्रयोग करना।",
                "en": "Handpicking and destruction of egg masses, setting up yellow sticky traps (10-15/acre) and sex pheromone traps for pest monitoring."
            },
            "biological_control": {
                "hi": "मित्र कीटों (जैसे लेडीबर्ड बीटल, क्राइसोपा) का संरक्षण करना और ट्राइकोग्रामा (Trichogramma) जैसे परजीवियों का उपयोग करना।",
                "en": "Conservation of natural predators (ladybird beetles, spiders) and release of bio-agents like Trichogramma egg parasitoids."
            },
            "safety_helpline": {
                "hi": "रासायनिक कीटनाशकों के अंधाधुंध प्रयोग से बचें। किसी भी जटिल रोग या कीट की पहचान और सटीक नियंत्रण के लिए अपने नजदीकी कृषि विज्ञान केंद्र (KVK) या किसान कॉल सेंटर टोल-फ्री नंबर 1800-180-1551 पर संपर्क करें।",
                "en": "Avoid indiscriminate chemical use. For accurate pest identification and precise recommendations, consult your nearest Krishi Vigyan Kendra (KVK) or Kisan Helpline 1800-180-1551."
            }
        }
    ],
    "symptoms.json": [
        {
            "id": "symptom-zinc-deficiency-001",
            "category": "plant_symptom",
            "nutrient": {"en": "Zinc Deficiency", "hi": "जिंक (जस्ता) की कमी के लक्षण"},
            "visual_symptoms": {
                "hi": "धान में पत्ती के मध्य शिराओं के बीच पीले-सफेद धब्बे (Khaira disease), पौधों की बढ़वार रुकना, और छोटी पत्तियां। मक्का व गेहूं में पत्तियों पर हल्के पीले या सफेद रंग के चौड़े धब्बे बनना।",
                "en": "Interveinal chlorosis in lower leaves (Khaira disease in rice), stunted internodes, and smaller leaf size in cereals."
            },
            "correction": {
                "hi": "जिंक सल्फेट (Zinc Sulfate 21%) 10 किलोग्राम प्रति एकड़ यूरिया या गोबर की खाद के साथ मिलाकर मिट्टी में दें या 0.5% घोल का छिड़काव करें।",
                "en": "Apply Zinc Sulfate (21%) @ 10 kg per acre mixed with soil/FYM or spray 0.5% zinc sulfate solution with lime."
            }
        },
        {
            "id": "symptom-nitrogen-deficiency-001",
            "category": "plant_symptom",
            "nutrient": {"en": "Nitrogen Deficiency", "hi": "नत्रजन (नाइट्रोजन) की कमी के लक्षण"},
            "visual_symptoms": {
                "hi": "पुरानी पत्तियां पीली पड़ जाती हैं (Chlorosis), पौधे का विकास धीमा होता है और तना कमजोर हो जाता है।",
                "en": "General yellowing of older leaves starting from the tip, stunted plant growth, and thin, spindly stems."
            },
            "correction": {
                "hi": "अनुशंसित यूरिया की मात्रा को विभाजित करके (split doses) सिंचाई के साथ दें।",
                "en": "Apply recommended nitrogen fertilizer in split doses followed by light irrigation."
            }
        }
    ],
    "verified_chemical_recommendations.json": [
        {
            "id": "chem-guidelines-001",
            "category": "verified_chemical_safety",
            "title": {"en": "Safe Pesticide Handling and KVK Advisory Protocol", "hi": "सुरक्षित कीटनाशक उपयोग एवं KVK परामर्श प्रोटोकॉल"},
            "guidelines": [
                {
                    "rule_1": {
                        "hi": "कीटनाशक खरीदते समय हमेशा पक्का बिल लें और सीलबंद पैकेट पर CIB&RC (Central Insecticides Board) पंजीकरण संख्या की जाँच करें।",
                        "en": "Always obtain a valid cash memo and check CIB&RC registration number on sealed pesticide containers."
                    }
                },
                {
                    "rule_2": {
                        "hi": "छिड़काव के समय मुंह पर मास्क, हाथों में दस्ताने और पूरी बांह के कपड़े पहनें। हवा की विपरीत दिशा में छिड़काव न करें।",
                        "en": "Wear protective gear (mask, gloves, full sleeves) during spraying. Never spray against wind direction."
                    }
                },
                {
                    "rule_3": {
                        "hi": "अज्ञात या अप्रमाणित रसायनों के मिश्रण का प्रयोग कदापि न करें। किसी भी कीट या रोग के लक्षण दिखने पर स्थानीय कृषि विज्ञान केंद्र (KVK) या टोल-फ्री किसान हेल्पलाइन (1800-180-1551) से अवश्य मार्गदर्शन लें।",
                        "en": "Never use unverified chemical mixtures. For any pest or disease symptom, always seek guidance from local Krishi Vigyan Kendra (KVK) or toll-free Kisan Helpline 1800-180-1551."
                    }
                }
            ]
        }
    ]
}

for filename, content in detailed_data.items():
    filepath = os.path.join(PP_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"Deeply enriched plant protection file: {filename}")

print("All plant protection files updated with detailed comprehensive information successfully!")
