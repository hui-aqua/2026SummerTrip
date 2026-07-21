import os
import sys

# Add current directory to path to allow import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from complete_trip_todos import clean_day_plan, update_manifest, DAYS_DATA

if __name__ == "__main__":
    print("Running roadbook enrichment via complete_trip_todos wrapper...")
    for day_key, data in DAYS_DATA.items():
        clean_day_plan(day_key, data)
    update_manifest()
    
    # Run compiler scripts
    print("\nRunning compilation scripts...")
    os.system("python scripts/compile_roadbook.py")
    os.system("python scripts/compile_consolidated_md.py")
    print("Enrichment wrapper run complete!")
