import os
import json
import glob
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = r"D:\data"
KB_DIR = r"D:\kisanvaani-ai\knowledge\crops"

pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
print(f"Total PDFs found for deep extraction: {len(pdf_files)}")

count = 0
for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    if filename.startswith("~$"):
        continue
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
        sections = {}
        current_section = "general"
        sections[current_section] = []
        
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if not t:
                continue
            full_text += f"\n--- Page {i+1} ---\n" + t
            lines = t.split("\n")
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                # Detect potential section headings (short lines in all caps or ending with colon)
                if len(line_str) < 60 and (line_str.isupper() or line_str.endswith(":") or "Introduction" in line_str or "Cultivation" in line_str or "Varieties" in line_str or "Pest" in line_str or "Disease" in line_str or "Harvest" in line_str or "Storage" in line_str or "Market" in line_str):
                    current_section = line_str[:50]
                    if current_section not in sections:
                        sections[current_section] = []
                else:
                    sections[current_section].append(line_str)
        
        # Summarize sections for structured details
        structured_sections = {}
        for sec, lines_list in sections.items():
            if lines_list:
                structured_sections[sec] = " ".join(lines_list[:150]) # keep up to 150 lines per section
                
        crop_id = filename.lower().replace('.pdf', '').replace(' ', '_').replace('-', '_')
        crop_title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        record = [{
            "id": f"pdf-detailed-{crop_id}-001",
            "category": "comprehensive_crop_profile",
            "crop_id": crop_id,
            "crop_name": {
                "en": crop_title,
                "hi": crop_title
            },
            "state": "All / National Benchmark",
            "season": "All Seasons",
            "topic": "Complete Agronomic, Varieties, Pest Management & Post Harvest Profile",
            "question": {
                "hi": f"{crop_title} की खेती, उन्नत किस्में, कीट प्रबंधन और भंडारण की पूरी जानकारी दें?",
                "en": f"Provide comprehensive details on cultivation, improved varieties, pest management, and post-harvest storage for {crop_title}?"
            },
            "answer_simple": {
                "hi": f"{crop_title} के संबंध में आधिकारिक दिशानिर्देश और तकनीकी प्रोफाइल नीचे दिए गए दस्तावेजों से संकलित हैं।",
                "en": f"Comprehensive guidelines and technical profiles regarding {crop_title} are compiled below from official documentation."
            },
            "detailed_sections": structured_sections,
            "full_text": full_text.strip(),
            "data_type": "official_static",
            "verification_status": "verified",
            "source_file": filename
        }]
        
        out_name = f"{crop_id}.json"
        out_path = os.path.join(KB_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        count += 1
        print(f"[{count}] Enhanced: {filename} -> {out_name} (Length: {len(full_text)} chars, Sections: {len(sections)})")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print(f"Successfully enriched {count} JSON files with detailed extraction.")
