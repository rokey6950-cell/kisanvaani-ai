import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..core.config import settings

logger = logging.getLogger("kisanvaani.knowledge")

# Multilingual & Dialect Stop Words for Indian Agricultural Queries (Hindi, Haryanvi, Punjabi, English)
BASE_HINDI_STOP_WORDS = {
    "क्या", "कैसे", "कहाँ", "कहा", "कब", "कितना", "कितनी", "कितने", "किस", "किसे", "किसने",
    "कौन", "कौनसा", "कौनसी", "और", "या", "पर", "में", "से", "को", "का", "की", "के",
    "है", "हैं", "हो", "था", "थी", "थे", "रहा", "रही", "रहे", "सकता", "सकती", "सकते",
    "चाहिए", "करें", "करनी", "बताएं", "बताओ", "बारे", "लिए", "वाला", "वाले", "वाली",
    "मुझे", "हमे", "हमें", "मेरा", "मेरी", "मेरे", "हमारा", "हमारी", "हमारे", "आप", "आपका", "आपकी",
    "कुछ", "बहुत", "ज्यादा", "कम", "अच्छा", "अच्छी", "अच्छे", "सब", "सभी", "यही", "वही",
    "k", "ki", "ke", "ka", "ko", "se", "me", "mein", "main", "par", "pe", "hai", "hain", "hoon", "hun",
    "kya", "kaise", "kaha", "kahan", "kab", "kitna", "kitni", "kitne", "kis", "kise", "kaun", "kaunsa",
    "chahiye", "kare", "karen", "karein", "karo", "karni", "batao", "bataiye", "bataana", "bataye",
    "mujhe", "hame", "hamen", "mera", "meri", "mere", "hamara", "humara", "aap", "aapka", "kuch", "bahut",
    "bhai", "bhaai", "namaskar", "namaste", "ji", "jee", "ram", "aaj", "kal", "hona",
    "gaon", "gao", "gav", "kripya", "khyaal", "today", "tomorrow"
}

HARYANVI_STOP_WORDS = {
    # Devanagari Haryanvi dialect particles
    "किकर", "कद", "किसा", "किसी", "किसे", "किते", "कितै", "क्योकर", "घणा", "घणी", "घणे",
    "सै", "सैं", "म्हारा", "म्हारी", "म्हारे", "थारा", "थारी", "थारे", "ल्याओ", "करियो",
    "बताइयो", "आच्छी", "आच्छा", "आच्छे", "लाग्या", "लागी", "लागे", "कोन्या", "कोनी", "ना",
    "तन्नै", "मन्नै", "यो", "वा", "इब", "उरे", "परै", "म्हाने", "थाने", "कै", "म्ह",
    "ताऊ", "चाचा", "बाबू", "लाडले", "कहूं", "जावै", "आवैया",

    # Romanized Haryanvi
    "kikar", "kad", "kisa", "kisi", "kise", "kite", "kitai", "kyokar", "ghana", "ghani", "ghane",
    "sai", "sain", "mhara", "mhari", "mhare", "thara", "thari", "thare", "konyo", "konya", "koni",
    "tanne", "manne", "ib", "yo", "mhane", "thane", "aacha", "aachi", "tau", "laadla"
}

PUNJABI_STOP_WORDS = {
    # Gurmukhi Punjabi particles
    "ਕਿਵੇਂ", "ਕਦੋਂ", "ਕਿੱਥੇ", "ਕੀ", "ਕਿਹੜਾ", "ਕਿਹੜੀ", "ਕਿਹੜੇ", "ਹੈ", "ਹਨ", "ਸੀ", "ਸਨ",
    "ਕਰੋ", "ਦੱਸੋ", "ਵਿੱਚ", "ਨੂੰ", "ਤੋਂ", "ਦਾ", "ਦੀ", "ਦੇ", "ਲਈ", "ਵਾਲਾ", "ਵਾਲੀ", "ਵਾਲੇ",
    "ਹੋਵੇ", "ਚਾਹੀਦਾ", "ਚਾਹੀਦੀ", "ਕਿਉਂ", "ਅਤੇ", "ਜਾਂ", "ਮੈਨੂੰ", "ਸਾਡਾ", "ਸਾਡੀ", "ਤੁਹਾਡਾ",
    "ਤੁਹਾਡੀ", "ਬਾਰੇ", "ਹੋਰ", "ਬਹੁਤ", "ਚੰਗਾ", "ਚੰਗੀ", "ਕਰੀਏ", "ਸਤਿ", "ਸ੍ਰੀ", "ਅਕਾਲ",

    # Romanized Punjabi
    "kive", "kiven", "kadon", "kithe", "kehda", "kehdi", "hove", "chahida", "chahidi",
    "dasso", "vich", "nu", "ton", "da", "di", "de", "lai", "wala", "wali", "nale",
    "tuhada", "tuhadi", "saada", "saadi", "mainu", "kariye", "paji", "paaji", "veere", "veer",
    "sat", "sri", "akaal"
}

ENGLISH_STOP_WORDS = {
    # Pronouns, Articles & Prepositions
    "the", "a", "an", "is", "are", "am", "was", "were", "be", "been", "being",
    "how", "what", "when", "where", "which", "who", "whom", "whose", "why",
    "for", "to", "in", "of", "on", "at", "by", "with", "from", "into", "during", "before", "after",
    "and", "or", "but", "not", "so", "if", "as",
    "this", "that", "these", "those", "my", "our", "your", "his", "her", "their", "its",

    # Conversational & Query fillers
    "can", "could", "should", "would", "will", "shall", "may", "might", "must",
    "tell", "give", "need", "want", "please", "kindly", "help", "guide", "suggest",
    "about", "regarding", "best", "good", "ideal", "right", "proper", "normal",
    "method", "process", "technique", "practice", "system", "time", "timing", "date",
    "detail", "details", "info", "information", "guidance", "solution", "advice",
    "today", "tomorrow", "village", "farmer", "agriculture", "farming"
}

ALL_STOP_WORDS = BASE_HINDI_STOP_WORDS | HARYANVI_STOP_WORDS | PUNJABI_STOP_WORDS | ENGLISH_STOP_WORDS
HINDI_STOP_WORDS = ALL_STOP_WORDS

# Bilingual crop name synonyms mapping Hindi, romanized, and English terms to canonical crop catalog keys
CROP_SYNONYMS: Dict[str, List[str]] = {
    # Vegetables & Fruits
    "टमाटर": ["tomato"],
    "tamatar": ["tomato"],
    "tomato": ["tomato"],
    "अंगूर": ["grapes", "grape"],
    "angoor": ["grapes", "grape"],
    "angur": ["grapes", "grape"],
    "grapes": ["grapes", "grape"],
    "grape": ["grapes", "grape"],
    "मिर्च": ["chilli", "chili"],
    "mirch": ["chilli", "chili"],
    "chilli": ["chilli", "chili"],
    "chili": ["chilli", "chili"],
    "आलू": ["potato"],
    "aalu": ["potato"],
    "aloo": ["potato"],
    "potato": ["potato"],
    "प्याज": ["onion", "onions"],
    "pyaj": ["onion", "onions"],
    "pyaaz": ["onion", "onions"],
    "onion": ["onion", "onions"],
    "onions": ["onion", "onions"],
    "केला": ["banana"],
    "kela": ["banana"],
    "banana": ["banana"],
    "संतरा": ["mandarin", "orange"],
    "किन्नू": ["mandarin"],
    "mandarin": ["mandarin"],
    "orange": ["mandarin"],
    "सेब": ["apple"],
    "seb": ["apple"],
    "apple": ["apple"],

    # Commercial & Fiber
    "कपास": ["cotton"],
    "kapas": ["cotton"],
    "cotton": ["cotton"],
    "गन्ना": ["sugarcane"],
    "ganna": ["sugarcane"],
    "sugarcane": ["sugarcane"],

    # Pulses
    "चना": ["bengal_gram", "gram"],
    "chana": ["bengal_gram", "gram"],
    "gram": ["bengal_gram", "gram"],
    "मूंग": ["green_gram"],
    "moong": ["green_gram"],
    "mung": ["green_gram"],
    "उड़द": ["blackgram", "black_gram"],
    "urad": ["blackgram", "black_gram"],
    "अरहर": ["arhar", "tur"],
    "तुअर": ["arhar", "tur"],
    "तुवर": ["arhar", "tur"],
    "tur": ["arhar", "tur"],
    "सोयाबीन": ["soybean"],
    "soybean": ["soybean"],

    # Oilseeds
    "सरसों": ["mustard", "rapeseed"],
    "sarson": ["mustard", "rapeseed"],
    "राई": ["mustard", "rapeseed"],
    "rai": ["mustard", "rapeseed"],
    "mustard": ["mustard", "rapeseed"],
    "मूंगफली": ["groundnut"],
    "mungfali": ["groundnut"],
    "groundnut": ["groundnut"],

    # Cereals & Millets
    "गेहूं": ["wheat"],
    "gehu": ["wheat"],
    "gehun": ["wheat"],
    "wheat": ["wheat"],
    "धान": ["paddy", "rice"],
    "चावल": ["rice", "paddy"],
    "rice": ["rice", "paddy"],
    "paddy": ["paddy", "rice"],
    "मक्का": ["maize"],
    "makka": ["maize"],
    "maize": ["maize"],
    "बाजरा": ["bajra"],
    "bajra": ["bajra"],
    "जौ": ["barley"],
    "jau": ["barley"],
    "barley": ["barley"],
    "रागी": ["finger_millet"],
    "कंगनी": ["foxtail_millet"],
    "कोदो": ["kodo_millet"],
    "सांवा": ["barnyard_millet"],
    "कुटकी": ["little_millet"],
    "चीना": ["broomcorn_millet"],
    "मकरा": ["browntop_millet"],
}

class KnowledgeBaseService:
    """
    Robust loader and search engine for the KisanVaani Agricultural Knowledge Base.
    Preserves raw JSON structure, source attribution, and verification status.
    """

    def __init__(self, knowledge_dir: Optional[str] = None):
        self.knowledge_dir = Path(knowledge_dir or settings.KNOWLEDGE_DIR).resolve()
        self.manifest: Dict[str, Any] = {}
        self.sources: Dict[str, Dict[str, Any]] = {}
        self.claims: List[Dict[str, Any]] = []
        self.crop_catalog: List[Dict[str, Any]] = []
        self.crops_data: Dict[str, List[Dict[str, Any]]] = {}
        self.schemes_national: List[Dict[str, Any]] = []
        self.scheme_documents: List[Dict[str, Any]] = []
        self.farmer_questions: List[Dict[str, Any]] = []
        self.simple_answers: List[Dict[str, Any]] = []
        self.glossary: List[Dict[str, Any]] = []
        self.states: List[Dict[str, Any]] = []
        self.agro_zones: List[Dict[str, Any]] = []
        self.seed_varieties: List[Dict[str, Any]] = []
        self.seed_recommendations: List[Dict[str, Any]] = []
        self.fertilizer_catalog: List[Dict[str, Any]] = []
        self.fertilizer_recommendations: List[Dict[str, Any]] = []
        self.commodity_mapping: List[Dict[str, Any]] = []
        self.weather_parameters: List[Dict[str, Any]] = []
        self.mandi_config: Dict[str, Any] = {}
        self.weather_config: Dict[str, Any] = {}

        # Raw file lookup table
        self.raw_files: Dict[str, Any] = {}
        self.loaded: bool = False
        self.load_errors: List[str] = []

    def load_knowledge_base(self) -> bool:
        """Loads and validates all JSON files in the knowledge directory."""
        if not self.knowledge_dir.exists():
            error_msg = f"Knowledge directory does not exist: {self.knowledge_dir}"
            logger.error(error_msg)
            self.load_errors.append(error_msg)
            self.loaded = False
            return False

        logger.info(f"Loading knowledge base from {self.knowledge_dir}...")
        self.load_errors.clear()

        # 1. Load manifest.json
        manifest_path = self.knowledge_dir / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    self.manifest = json.load(f)
            except Exception as e:
                self.load_errors.append(f"Failed to load manifest.json: {e}")
        else:
            self.load_errors.append("manifest.json not found")

        # 2. Iterate and load all JSON files recursively
        for json_file in self.knowledge_dir.rglob("*.json"):
            rel_path = json_file.relative_to(self.knowledge_dir).as_posix()
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.raw_files[rel_path] = data
            except Exception as e:
                self.load_errors.append(f"Error loading {rel_path}: {e}")

        # 3. Populate specific indexed collections
        # Sources
        raw_sources = self.raw_files.get("sources/source_registry.json", [])
        if isinstance(raw_sources, list):
            for s in raw_sources:
                sid = s.get("source_id")
                if sid:
                    self.sources[sid] = s

        self.claims = self.raw_files.get("sources/source_claim_mapping.json", [])

        # Crops
        self.crop_catalog = self.raw_files.get("crops/crop_catalog.json", [])
        for rel_path, data in self.raw_files.items():
            if rel_path.startswith("crops/") and rel_path != "crops/crop_catalog.json" and isinstance(data, list):
                crop_name = Path(rel_path).stem
                self.crops_data[crop_name] = data

        # Schemes
        self.schemes_national = self.raw_files.get("schemes/national_schemes.json", [])
        self.scheme_documents = self.raw_files.get("schemes/scheme_documents.json", [])

        # Hindi Knowledge
        self.farmer_questions = self.raw_files.get("hindi_knowledge/farmer_questions.json", [])
        self.simple_answers = self.raw_files.get("hindi_knowledge/simple_answers.json", [])
        self.glossary = self.raw_files.get("hindi_knowledge/agricultural_glossary.json", [])

        # Geography
        self.states = self.raw_files.get("geography/states.json", [])
        self.agro_zones = self.raw_files.get("geography/agro_climatic_zones.json", [])

        # Seeds
        self.seed_varieties = self.raw_files.get("seeds/seed_varieties.json", [])
        self.seed_recommendations = self.raw_files.get("seeds/seed_recommendations.json", [])

        # Fertilizers
        self.fertilizer_catalog = self.raw_files.get("fertilizers/fertilizer_catalog.json", [])
        self.fertilizer_recommendations = self.raw_files.get("fertilizers/fertilizer_recommendations.json", [])

        # Mandi & Weather
        self.commodity_mapping = self.raw_files.get("mandi/commodity_mapping.json", [])
        self.mandi_config = self.raw_files.get("mandi/api_configuration.json", {})
        self.weather_parameters = self.raw_files.get("weather/weather_parameters.json", [])
        self.weather_config = self.raw_files.get("weather/api_configuration.json", {})

        self.loaded = len(self.raw_files) > 0 and len(self.load_errors) == 0
        logger.info(
            f"Knowledge base loaded successfully. Files: {len(self.raw_files)}, "
            f"Sources: {len(self.sources)}, National Schemes: {len(self.schemes_national)}, "
            f"Q&As: {len(self.farmer_questions)}, "
            f"Fertilizer Catalog: {len(self.fertilizer_catalog)}, "
            f"Fertilizer Recs: {len(self.fertilizer_recommendations)}"
        )
        return self.loaded

    def get_status(self) -> Dict[str, Any]:
        """Returns comprehensive status and record counts of the knowledge base."""
        total_records = 0
        verified_count = 0
        pending_count = 0

        for rel, data in self.raw_files.items():
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        total_records += 1
                        st = item.get("verification_status", "")
                        if st == "verified":
                            verified_count += 1
                        elif st in ("pending_review", "unverified"):
                            pending_count += 1
            elif isinstance(data, dict) and rel != "manifest.json":
                total_records += 1
                st = data.get("verification_status", "")
                if st == "verified":
                    verified_count += 1
                elif st in ("pending_review", "unverified"):
                    pending_count += 1

        return {
            "loaded": self.loaded,
            "manifest_version": self.manifest.get("kb_version", "unknown"),
            "target_regions": self.manifest.get("target_regions", []),
            "total_files": len(self.raw_files),
            "total_records": total_records,
            "source_records": len(self.sources),
            "verified_records": verified_count,
            "pending_records": pending_count,
            "categories": self.manifest.get("categories", []),
            "status_note": self.manifest.get("status_note", ""),
            "load_errors": self.load_errors
        }

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        return self.sources.get(source_id)

    def get_sources_for_record(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        sids = record.get("source_ids", [])
        matched = [self.sources[sid] for sid in sids if sid in self.sources]
        if not matched and record.get("source_file"):
            matched = [{
                "id": "src-dmi-official-profile",
                "name": f"कृषि एवं किसान कल्याण मंत्रालय (DMI भारत सरकार) - {record.get('source_file')}",
                "type": "official_manual"
            }]
        elif not matched:
            matched = [{
                "id": "src-gov-agriculture-knowledge",
                "name": "राष्ट्रीय कृषि ज्ञान प्रणाली (ICAR / DMI भारत सरकार)",
                "type": "official_static"
            }]
        return matched

    def get_all_schemes(self) -> List[Dict[str, Any]]:
        result = []
        for scheme in self.schemes_national:
            item = dict(scheme)
            item["sources"] = self.get_sources_for_record(scheme)
            result.append(item)
        return result

    def get_scheme_by_id(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        for scheme in self.schemes_national:
            if scheme.get("id") == scheme_id or scheme.get("scheme_id") == scheme_id:
                item = dict(scheme)
                item["sources"] = self.get_sources_for_record(scheme)
                return item
        return None

    def get_crop_catalog(self) -> List[Dict[str, Any]]:
        return self.crop_catalog

    def get_crop_guidance(self, crop_name: str = "wheat", state: Optional[str] = None) -> List[Dict[str, Any]]:
        records = self.crops_data.get(crop_name.lower(), [])
        if state:
            return [r for r in records if r.get("state") == state]
        return records

    def search_knowledge(
        self,
        query: str,
        state: Optional[str] = None,
        crop: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Grounded search over farmer questions, crop packages, and schemes.
        Ranked by matching keywords and strict regional scoping.
        """
        q_lower = query.lower()
        results = []

        # Clean and filter query words
        raw_words = [w.strip("?,.!:;\"'") for w in q_lower.split()]
        words = [w for w in raw_words if len(w) > 2 and w not in HINDI_STOP_WORDS]

        # Guard: if no meaningful words remain after filtering, there is nothing to match
        if not words:
            logger.info("search_knowledge: all query words were stop words; returning empty results.")
            return []

        # Detect explicitly mentioned state in query to avoid cross-state mismatch
        query_state = state
        if not query_state:
            for st_name in ["haryana", "हरियाणा", "punjab", "पंजाब", "rajasthan", "राजस्थान", "himachal", "हिमाचल", "uttar pradesh", "उत्तर प्रदेश", "uttarakhand", "उत्तराखंड"]:
                if st_name in q_lower:
                    query_state = "Haryana" if st_name in ("haryana", "हरियाणा") else "Punjab" if st_name in ("punjab", "पंजाब") else "Rajasthan" if st_name in ("rajasthan", "राजस्थान") else "Himachal Pradesh" if st_name in ("himachal", "हिमाचल") else "Uttar Pradesh" if "uttar" in st_name or "उत्तर" in st_name else "Uttarakhand"
                    break

        # Detect crop mentioned in query using bilingual synonyms
        detected_crop_aliases: List[str] = []
        for syn, aliases in CROP_SYNONYMS.items():
            if syn in q_lower:
                detected_crop_aliases.extend(aliases)

        # 1. Search in farmer_questions
        for item in self.farmer_questions:
            score = 0.0
            q_text = (item.get("question") or {}).get("hi", "").lower()
            ans_hi = (item.get("answer_simple") or {}).get("hi", "").lower()
            topic = item.get("topic", "").lower()

            for w in words:
                if w in q_text:
                    score += 3.0
                if w in ans_hi:
                    score += 1.5
                if w in topic:
                    score += 2.0

            if crop and crop.lower() in (item.get("crop_id") or "").lower():
                score += 2.5
            if state and state.lower() in (item.get("state") or "").lower():
                score += 2.0

            if score >= 3.0:
                results.append({
                    "id": item.get("id"),
                    "category": "qa",
                    "title": (item.get("question") or {}).get("hi", ""),
                    "answer_simple": item.get("answer_simple", {}),
                    "answer_detailed": item.get("answer_detailed"),
                    "state": item.get("state"),
                    "verification_status": item.get("verification_status", "pending_review"),
                    "data_type": item.get("data_type", "unverified"),
                    "sources": self.get_sources_for_record(item),
                    "relevance_score": score
                })

        # 2. Search in crops_data (crop packages, profiles & manuals)
        for cname, records in self.crops_data.items():
            cname_l = cname.lower()
            for rec in records:
                score = 0.0
                topic = (rec.get("topic") or "").lower()
                ans_s = (rec.get("answer_simple") or {}).get("hi", "").lower()
                r_state = rec.get("state")
                rec_crop_id = (rec.get("crop_id") or "").lower()

                target_st = query_state or state
                if target_st and r_state and target_st.lower() not in r_state.lower() and r_state.lower() not in target_st.lower() and "all" not in r_state.lower():
                    continue

                # Direct crop synonym match (e.g. टमाटर -> tomato, grapes -> grapes)
                for alias in detected_crop_aliases:
                    if alias in cname_l or alias in rec_crop_id:
                        score += 5.0
                        break

                for w in words:
                    if w in cname_l or w in rec_crop_id:
                        score += 4.0
                    if w in topic:
                        score += 3.0
                    if w in ans_s:
                        score += 1.5

                if crop and (crop.lower() in cname_l or crop.lower() in rec_crop_id):
                    score += 3.5

                if score >= 3.0:
                    cname_display = rec.get("crop_name")
                    if isinstance(cname_display, dict):
                        cname_display = cname_display.get("hi") or cname_display.get("en") or cname
                    elif not cname_display:
                        cname_display = cname.title()

                    results.append({
                        "id": rec.get("id"),
                        "category": "crop",
                        "title": f"{cname_display}: {rec.get('topic') or 'कृषि एवं प्रबंधन प्रोफाइल'}",
                        "answer_simple": rec.get("answer_simple", {}),
                        "answer_detailed": rec.get("answer_detailed") or rec.get("detailed_sections"),
                        "state": r_state,
                        "verification_status": rec.get("verification_status", "verified"),
                        "data_type": rec.get("data_type", "official_static"),
                        "sources": self.get_sources_for_record(rec),
                        "relevance_score": score
                    })

        # 3. Search in seed varieties
        seed_keywords = {"किस्म", "किस्में", "वैरायटी", "बीज", "seed", "variety", "varieties"}
        has_seed_query = any(w in seed_keywords for w in words)
        for var in self.seed_varieties:
            score = 0.0
            v_name = var.get("variety", "").lower()
            v_crop = var.get("crop_id", "").lower()
            v_state = var.get("state")
            v_cond = (var.get("sowing_condition") or "").lower()

            if state and v_state and state.lower() != v_state.lower():
                continue

            for w in words:
                if w in v_name:
                    score += 5.0
                if w in v_cond:
                    score += 2.0

            if (crop and crop.lower() in v_crop) or has_seed_query:
                score += 3.0

            if score >= 4.0:
                cond_text = f" ({var.get('sowing_condition')})" if var.get("sowing_condition") else ""
                state_text = f" राज्य: {var.get('state')}" if var.get("state") else ""
                ans_text_hi = f"अनुशंसित किस्म: {var.get('variety')}{cond_text}।{state_text}। कृपया अपने स्थानीय कृषि विज्ञान केंद्र से अपने जिले के लिए नवीनतम सिफारिश की पुष्टि करें।"
                results.append({
                    "id": var.get("id"),
                    "category": "seed_variety",
                    "title": f"बीज किस्म: {var.get('variety')} ({var.get('crop_id')})",
                    "variety": var.get("variety"),
                    "crop_id": var.get("crop_id"),
                    "sowing_condition": var.get("sowing_condition"),
                    "irrigation_status": var.get("irrigation_status"),
                    "yield_potential": var.get("yield_potential"),
                    "maturity_period": var.get("maturity_period"),
                    "resistance": var.get("resistance"),
                    "features": var.get("features"),
                    "detailed_sections": var.get("detailed_sections"),
                    "answer_simple": {"hi": ans_text_hi, "en": f"Recommended variety: {var.get('variety')}{cond_text}."},
                    "answer_detailed": var.get("notes") or var.get("detailed_sections"),
                    "state": v_state,
                    "verification_status": var.get("verification_status", "pending_review"),
                    "data_type": var.get("data_type", "official_static"),
                    "sources": self.get_sources_for_record(var),
                    "relevance_score": score,
                    "_raw_rec": var
                })

        # 4. Search in fertilizer recommendations (crop-specific NPK/micronutrient advice)
        fert_keywords = {
            "खाद", "उर्वरक", "यूरिया", "डीएपी", "dap", "npk", "नाइट्रोजन", "फास्फोरस", "पोटाश",
            "fertilizer", "manure", "खाद्य", "पोषण", "जिंक", "zinc", "sulfur", "सल्फर",
            "khad", "urvarak", "urea", "nutrition", "dose", "मात्रा", "soil", "मिट्टी"
        }
        has_fert_query = any(w in fert_keywords for w in words)
        for frec in self.fertilizer_recommendations:
            score = 0.0
            f_crop_id = (frec.get("crop_id") or "").lower()
            f_crop_name_dict = frec.get("crop_name") or {}
            f_crop_name_hi = (f_crop_name_dict.get("hi") if isinstance(f_crop_name_dict, dict) else str(f_crop_name_dict)).lower()
            f_crop_name_en = (f_crop_name_dict.get("en") if isinstance(f_crop_name_dict, dict) else "").lower()
            f_state = frec.get("state", "")
            f_category = (frec.get("category") or "").lower()

            # State filter — allow "All" or matching records
            if state and f_state and "all" not in f_state.lower() and state.lower() not in f_state.lower():
                continue

            # Crop match via synonym detection
            for alias in detected_crop_aliases:
                if alias in f_crop_id or alias in f_crop_name_en.lower():
                    score += 5.0
                    break

            # Direct keyword match in crop name
            for w in words:
                if w in f_crop_id or w in f_crop_name_en or w in f_crop_name_hi:
                    score += 4.0
                if w in f_category:
                    score += 1.5

            # Explicit crop param match
            if crop and crop.lower() in f_crop_id:
                score += 4.0

            # Fertilizer query bonus
            if has_fert_query:
                score += 2.0

            if score >= 4.0:
                dose = frec.get("recommended_dose_per_acre") or {}
                n_dose = dose.get("nitrogen_n", "")
                p_dose = dose.get("phosphorus_p", "")
                k_dose = dose.get("phosphorus_k") or dose.get("potassium_k", "")
                micro = dose.get("micronutrients", "")
                safety = frec.get("safety_and_guidelines") or {}
                safety_hi = (safety.get("hi") if isinstance(safety, dict) else str(safety or ""))
                display_name = f_crop_name_hi or f_crop_id or "फसल"
                ans_hi = (
                    f"{display_name} के लिए अनुशंसित उर्वरक मात्रा (प्रति एकड़): "
                    f"नाइट्रोजन - {n_dose}; फास्फोरस - {p_dose}; पोटाश - {k_dose}; "
                    f"सूक्ष्म पोषक तत्व - {micro}। "
                    f"{safety_hi} "
                    f"सटीक मात्रा के लिए अपना Soil Health Card देखें और KVK हेल्पलाइन 1800-180-1551 से संपर्क करें।"
                )
                results.append({
                    "id": frec.get("id"),
                    "category": "fertilizer",
                    "title": f"उर्वरक सलाह: {display_name}",
                    "answer_simple": {"hi": ans_hi, "en": f"Fertilizer recommendation for {f_crop_name_en or f_crop_id}."},
                    "answer_detailed": frec.get("detailed_sections") or frec.get("application_schedule"),
                    "state": f_state,
                    "verification_status": frec.get("verification_status", "verified"),
                    "data_type": frec.get("data_type", "official_static"),
                    "sources": self.get_sources_for_record(frec),
                    "relevance_score": score,
                    "_raw_rec": frec  # kept for synthesizer access
                })

        # 5. Search in fertilizer catalog (general fertilizer info — urea, DAP, NPK etc.)
        for fcat in self.fertilizer_catalog:
            score = 0.0
            fname_dict = fcat.get("fertilizer_name") or {}
            fname_hi = (fname_dict.get("hi") if isinstance(fname_dict, dict) else str(fname_dict)).lower()
            fname_en = (fname_dict.get("en") if isinstance(fname_dict, dict) else "").lower()
            f_cat_type = (fcat.get("category") or "").lower()

            for w in words:
                if w in fname_hi or w in fname_en:
                    score += 5.0
                if w in f_cat_type:
                    score += 1.5

            if has_fert_query:
                score += 1.5

            if score >= 4.0:
                benefits_dict = fcat.get("benefits") or {}
                benefits_hi = (benefits_dict.get("hi") if isinstance(benefits_dict, dict) else str(benefits_dict or ""))
                apply_dict = fcat.get("application_guidelines") or {}
                apply_hi = (apply_dict.get("hi") if isinstance(apply_dict, dict) else str(apply_dict or ""))
                nutrient = fcat.get("nutrient_composition") or {}
                n_pct = nutrient.get("nitrogen_n", "")
                p_pct = nutrient.get("phosphorus_p", "")
                k_pct = nutrient.get("potassium_k", "")
                display = (fname_dict.get("hi") if isinstance(fname_dict, dict) else fname_hi) or "उर्वरक"
                ans_hi = (
                    f"{display}: नाइट्रोजन {n_pct}, फास्फोरस {p_pct}, पोटाश {k_pct}। "
                    f"लाभ: {benefits_hi[:200]}। प्रयोग विधि: {apply_hi[:200]}। "
                    f"रासायनिक उर्वरक के प्रयोग से पहले KVK या कृषि विभाग से सलाह अवश्य लें।"
                )
                results.append({
                    "id": fcat.get("id"),
                    "category": "fertilizer_catalog",
                    "title": f"उर्वरक जानकारी: {display}",
                    "answer_simple": {"hi": ans_hi, "en": f"Fertilizer: {fname_en}."},
                    "answer_detailed": fcat.get("detailed_sections"),
                    "state": "All",
                    "verification_status": fcat.get("verification_status", "verified"),
                    "data_type": fcat.get("data_type", "official_static"),
                    "sources": self.get_sources_for_record(fcat),
                    "relevance_score": score,
                    "_raw_rec": fcat
                })

        # 6. Search in schemes
        for sch in self.schemes_national:
            score = 0.0
            s_name_dict = sch.get("name") if isinstance(sch.get("name"), dict) else {}
            s_name_hi = (s_name_dict.get("hi") or (sch.get("name") if isinstance(sch.get("name"), str) else "")).lower()
            s_name_en = (s_name_dict.get("en") or "").lower()
            s_id = (sch.get("scheme_id") or sch.get("id") or "").lower()

            for w in words:
                if w in s_name_hi or w in s_name_en or w in s_id:
                    score += 4.0

            if score >= 3.0:
                pur = sch.get("purpose")
                pur_text = (pur.get("hi") if isinstance(pur, dict) else pur) or "सरकारी कृषि योजना"
                ben = sch.get("benefits")
                ben_text = (ben.get("hi") if isinstance(ben, dict) else ben) or ""
                ans_text = f"योजना: {s_name_hi or s_id}। उद्देश्य: {pur_text}। लाभ: {ben_text}। अधिक जानकारी व आवेदन के लिए आधिकारिक पोर्टल {sch.get('official_portal', '')} पर जाएं।"
                results.append({
                    "id": sch.get("id"),
                    "category": "scheme",
                    "title": s_name_hi or s_id,
                    "answer_simple": {"hi": ans_text, "en": str(sch.get("purpose"))},
                    "answer_detailed": str(sch.get("benefits")),
                    "state": "National",
                    "verification_status": sch.get("verification_status", "verified"),
                    "data_type": sch.get("data_type", "official_static"),
                    "sources": self.get_sources_for_record(sch),
                    "relevance_score": score
                })

        # Sort descending by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results

    def get_seed_varieties(self, crop_id: Optional[str] = None, state: Optional[str] = None) -> List[Dict[str, Any]]:
        varieties = []
        for var in self.seed_varieties:
            if crop_id and var.get("crop_id", "").lower() != crop_id.lower():
                continue
            if state and var.get("state") and var.get("state").lower() != state.lower():
                continue
            item = dict(var)
            item["sources"] = self.get_sources_for_record(var)
            varieties.append(item)
        return varieties

    def get_glossary(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        if not query:
            return self.glossary
        q_l = query.lower()
        res = []
        for term in self.glossary:
            t_hi = (term.get("term") or {}).get("hi", "").lower()
            t_en = (term.get("term") or {}).get("en", "").lower()
            if q_l in t_hi or q_l in t_en:
                res.append(term)
        return res

    def get_agro_zones(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        if not state:
            return self.agro_zones
        return [z for z in self.agro_zones if state in z.get("states", [])]

knowledge_service = KnowledgeBaseService()

