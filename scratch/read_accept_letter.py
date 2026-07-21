import os
from pypdf import PdfReader

pdf_path = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\assets\13080265.pdf"

if os.path.exists(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print("Total Pages in 13080265.pdf:", len(reader.pages))
        for idx, page in enumerate(reader.pages):
            print(f"--- Page {idx+1} ---")
            print(page.extract_text()[:2000]) # Print text of page
    except Exception as e:
        print("Error reading PDF Accepting letter:", e)
else:
    print("PDF accept letter not found")
