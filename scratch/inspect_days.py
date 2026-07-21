import os
import re

docs_dir = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\docs"
days_dir = os.path.join(docs_dir, "days")

for i in range(1, 14):
    day_file = os.path.join(days_dir, f"Day{i:02d}.md")
    if os.path.exists(day_file):
        with open(day_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"=== Day {i:02d} ===")
        # Get title
        title = content.split('\n')[0]
        print(title)
        # Get summary
        summary_match = re.search(r"## Summary\s*\n(.*?)(?=\n##|$)", content, re.DOTALL)
        if summary_match:
            print("Summary:", summary_match.group(1).strip())
        # Get Hotel address
        hotel_match = re.search(r"Address:\s*(.*?)(?=\n|$)", content)
        if hotel_match:
            print("Hotel Address:", hotel_match.group(1).strip())
        # Get Meals
        meals_match = re.search(r"## Meals\s*\n(.*?)(?=\n##|$)", content, re.DOTALL)
        if meals_match:
            print("Meals:\n", meals_match.group(1).strip())
        print()
