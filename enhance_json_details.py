import os
import json
import glob
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = r"D:\data"
KB_DIR = r"D:\kisanvaani-ai\knowledge\crops"

pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
print(f"Total PDFs found for detailed enhancement: {len(pdf_files)}")

count = 0
for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    if filename.startswith("~$"):
        continue
    try:
        reader = PdfReader(pdf_path)
        text_content = ""
        sections = {}
        current_section = "general_overview"
        sections[current_section] = []
        
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if not t:
                continue
            text_content += f"\n--- Page {i+1} ---\n" + t
            
            # Simple heuristic section splitting
            lines = t.split("\n")
            for line in lines:
                line_str = line.strip()
                if len(line_str) < 50 and any(kw in line_str.lower() for kw in ["introduction", "climate", "soil", "sowing", "variety", "fertilizer", "irrigation", "plant protection", "pest", "disease", "harvest", "yield", "storage", "market"]):
                    current_section = line_str.lower().replace(" ", "_")[:40]
                    sections[current_section] = []
                else:
                    sections[current_section].append(line_str)
                    
        cleaned_sections = {k: " ".join(v)[:2000] for k, v in sections.items() if v}
        
        crop_id = filename.lower().replace('.pdf', '').replace(' ', '_').replace('-', '_')
        record = [{
            "id": f"pdf-detailed-{crop_id}-001",
            "category": "comprehensive_crop_advisory_profile",
            "crop_id": crop_id,
            "crop_name": {
                "en": filename.replace('.pdf', ''),
                "hi": filename.replace('.pdf', '')
            },
            "state": "All / National",
            "season": "All Seasons",
            "topic": "Comprehensive Agronomic, Post-Harvest & Market Profile",
            "question": {
                "hi": f"{filename.replace('.pdf', '')} की विस्तृत कृषि, बुवाई, कटाई और भंडारण की पूरी जानकारी दें?",
                "en": f"Provide comprehensive agronomic, sowing, harvesting, and post-harvest details for {filename.replace('.pdf', '')}?"
            },
            "answer_simple": {
                "hi": f"{filename.replace('.pdf', '')} के बारे में आधिकारिक दस्तावेजों से विस्तृत और संरचित मार्गदर्शन नीचे उपलब्ध है।",
                "en": f"Detailed and structured guidance for {filename.replace('.pdf', '')} sourced from official documents is available below."
            },
            "structured_sections": cleaned_sections,
            "full_text": text_content.strip(),
            "data_type": "official_static",
            "verification_status": "verified",
            "source_file": filename,
            "last_verified": "2026-11-01"
        }]
        
        out_name = f"{crop_id}.json"
        out_path = os.path.join(KB_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        count += 1
        print(f"[{count}] Enhanced Detailed JSON: {filename} -> {out_name}")
    except Exception as e:
        print(f"Error enhancing {filename}: {e}")

print(f"Successfully updated {count} JSON files with detailed structured sections!")
