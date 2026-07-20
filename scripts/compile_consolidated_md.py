import os

# Paths
workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_dir = os.path.join(workspace, "docs")
days_dir = os.path.join(docs_dir, "days")
consolidated_file = os.path.join(workspace, "Family_Roadbook_V4.0_CN.md")

# Order of files to concatenate
FILES_ORDER = [
    os.path.join(docs_dir, "00_Cover.md"),
    os.path.join(docs_dir, "01_Version_History.md"),
    os.path.join(docs_dir, "02_TOC.md"),
    os.path.join(docs_dir, "03_Trip_Overview.md"),
    os.path.join(docs_dir, "04_Family.md"),
    os.path.join(docs_dir, "05_Vehicle.md"),
    os.path.join(docs_dir, "06_Ferries.md"),
    os.path.join(docs_dir, "07_Hotels.md"),
    # Daily plans
]

# Append Day01.md to Day13.md to the order list
for i in range(1, 14):
    day_file = os.path.join(days_dir, f"Day{i:02d}.md")
    if os.path.exists(day_file):
        FILES_ORDER.append(day_file)

# Append remaining docs
REMAINING_FILES = [
    os.path.join(docs_dir, "08_Berlin.md"),
    os.path.join(docs_dir, "09_Driving_Rules_DE.md"),
    os.path.join(docs_dir, "10_Driving_Rules_DK.md"),
    os.path.join(docs_dir, "11_Packing_List.md"),
    os.path.join(docs_dir, "12_Emergency.md"),
    os.path.join(docs_dir, "13_Journal.md"),
    os.path.join(docs_dir, "14_Budget.md"),
    os.path.join(docs_dir, "15_Appendix.md"),
]
FILES_ORDER.extend(REMAINING_FILES)

def concatenate_markdown():
    print("Concatenating modular markdown files into consolidated master...")
    master_content = []
    
    for filepath in FILES_ORDER:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            filename = os.path.basename(filepath)
            master_content.append(f"<!-- START OF {filename} -->\n")
            master_content.append(content)
            master_content.append(f"\n<!-- END OF {filename} -->\n\n---\n\n")
        else:
            print(f"Warning: File not found: {filepath}")
            
    # Combine and write
    full_text = "".join(master_content)
    # Remove the final separator
    if full_text.endswith("\n\n---\n\n"):
        full_text = full_text[:-9]
        
    with open(consolidated_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
        
    print(f"Consolidated roadbook written to {consolidated_file}!")

if __name__ == "__main__":
    concatenate_markdown()
