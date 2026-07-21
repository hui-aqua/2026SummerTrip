import os
from pypdf import PdfReader

pdf_path = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\assets\ICMCF2026-Preliminary-Programme_06-29.pdf"

if os.path.exists(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print("Total Pages in Agenda:", len(reader.pages))
        
        # Let's search for keywords like "Yang", "Qian", "oral", "poster", "presentation", "chair"
        found = False
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if "yang" in text.lower():
                found = True
                print(f"=== Keyword 'yang' found on Page {idx+1} ===")
                # Print lines containing the keyword
                lines = text.split('\n')
                for line in lines:
                    if "yang" in line.lower():
                        print("LINE:", line)
            if "qian" in text.lower():
                print(f"=== Keyword 'qian' found on Page {idx+1} ===")
                lines = text.split('\n')
                for line in lines:
                    if "qian" in line.lower():
                        print("LINE:", line)
                        
        # Also print the first 2 pages to understand the overall schedule/agenda structure
        print("\n=== PAGE 1 SUMMARY ===")
        print(reader.pages[0].extract_text()[:1500])
        print("\n=== PAGE 2 SUMMARY ===")
        print(reader.pages[1].extract_text()[:1500])
        
    except Exception as e:
        print("Error reading PDF:", e)
else:
    print("PDF not found")
