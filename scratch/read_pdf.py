import os
from pypdf import PdfReader # Let's try standard pypdf first

pdf_path = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\assets\German Bundestag\SYS-20260611-214020-Buchungsbestaetigung.pdf"

if os.path.exists(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print("Total Pages:", len(reader.pages))
        for idx, page in enumerate(reader.pages):
            print(f"--- Page {idx+1} ---")
            print(page.extract_text()[:1000]) # Print first 1000 chars of each page
    except Exception as e:
        print("Error reading PDF:", e)
else:
    print("PDF not found")
