import os

agenda_txt = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\scratch\extracted_agenda.txt"

if os.path.exists(agenda_txt):
    with open(agenda_txt, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    
    print("searching in text...")
    for word in ["norway", "sola", "cheng", "yang", "hui", "qian"]:
        if word in text:
            print(f"Matched '{word}'!")
        else:
            print(f"'{word}' not found.")
else:
    print("Agenda text not found")
