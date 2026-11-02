import os
import json
import glob
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = r"D:\data"
KB_DIR = r"D:\kisanvaani-ai\knowledge\crops"

def extract_pdf_data():
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    print(f"Found {len(pdf_files)} PDF files in {DATA_DIR}")
    
    extracted_records = []
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"Processing: {filename}")
        try:
            reader = PdfReader(pdf_path)
            text_content = ""
            for i, page in enumerate(reader.pages):
                t = page.extract_text()
                if t:
                    text_content += f"\n--- Page {i+1} ---\n" + t
            
            # Create structured record
            record = {
                "id": f"pdf-{filename.lower().replace('.pdf', '').replace(' ', '-')}-001",
                "category": "crop_advisory_profile",
                "title": filename.replace('.pdf', ''),
                "source_file": filename,
                "content_preview": text_content[:1500],
                "full_text_length": len(text_content),
                "data_type": "official_static",
                "verification_status": "verified"
            }
            extracted_records.append(record)
            
            # Save individual JSON file
            out_name = filename.lower().replace('.pdf', '.json').replace(' ', '_')
            out_path = os.path.join(KB_DIR, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump([record], f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    print(f"Successfully processed and integrated {len(extracted_records)} PDFs into {KB_DIR}")

if __name__ == "__main__":
    extract_pdf_data()
