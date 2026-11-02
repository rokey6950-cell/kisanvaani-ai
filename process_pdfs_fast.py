import os
import json
import glob
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = r"D:\data"
KB_DIR = r"D:\kisanvaani-ai\knowledge\crops"

pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
print(f"Total PDFs found: {len(pdf_files)}")

count = 0
for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    if filename.startswith("~$"):
        continue
    try:
        reader = PdfReader(pdf_path)
        text_content = ""
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if t:
                text_content += t + "\n"
        
        crop_id = filename.lower().replace('.pdf', '').replace(' ', '_').replace('-', '_')
        record = [{
            "id": f"pdf-{crop_id}-001",
            "category": "crop_advisory_profile",
            "crop_id": crop_id,
            "crop_name": {
                "en": filename.replace('.pdf', ''),
                "hi": filename.replace('.pdf', '')
            },
            "state": "All / National",
            "season": "All Seasons",
            "topic": "Agronomic Profile & Post Harvest",
            "question": {
                "hi": f"{filename.replace('.pdf', '')} की खेती और प्रबंधन की जानकारी दें?",
                "en": f"What are the agronomic and post-harvest guidelines for {filename.replace('.pdf', '')}?"
            },
            "answer_simple": {
                "hi": f"{filename.replace('.pdf', '')} के बारे में विस्तृत दिशानिर्देश नीचे दिए गए दस्तावेजों से लिए गए हैं।",
                "en": f"Detailed guidelines for {filename.replace('.pdf', '')} are available from official profile documents."
            },
            "full_text": text_content.strip(),
            "data_type": "official_static",
            "verification_status": "verified",
            "source_file": filename
        }]
        
        out_name = f"{crop_id}.json"
        out_path = os.path.join(KB_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        count += 1
        print(f"[{count}] Processed: {filename} -> {out_name}")
    except Exception as e:
        print(f"Error {filename}: {e}")

print(f"Done! Successfully processed {count} PDFs.")
