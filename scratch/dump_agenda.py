import os
from pypdf import PdfReader

pdf_path = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\assets\ICMCF2026-Preliminary-Programme_06-29.pdf"
out_txt = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\scratch\extracted_agenda.txt"

if os.path.exists(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        with open(out_txt, 'w', encoding='utf-8') as f:
            for idx, page in enumerate(reader.pages):
                f.write(f"================ PAGE {idx+1} ================\n")
                f.write(page.extract_text() or "")
                f.write("\n\n")
        print(f"Extracted all PDF text to {out_txt} successfully!")
    except Exception as e:
        print("Error reading PDF:", e)
else:
    print("PDF not found")
