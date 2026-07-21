import os

agenda_txt = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\scratch\extracted_agenda.txt"

if os.path.exists(agenda_txt):
    with open(agenda_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if "uis" in line.lower():
            print(f"Line {idx+1}: {line.strip()}")
else:
    print("Agenda text not found")
