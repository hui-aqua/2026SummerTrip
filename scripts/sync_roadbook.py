import os
import re
import json
import urllib.request
import hashlib
import subprocess

# Paths
workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_dir = os.path.join(workspace, "docs")
days_dir = os.path.join(docs_dir, "days")
packing_file = os.path.join(docs_dir, "11_Packing_List.md")

SYNC_URL = 'https://kvdb.io/hui_noora_roadbook_2026/roadbook_state'

def get_clean_hash(label):
    # Match the clean hash generation in JS/compile_roadbook.py
    label_clean = re.sub(r'<.*?>', '', label) # strip HTML
    label_clean = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '', label_clean) # alphanumeric & Chinese
    return "chk-" + hashlib.md5(label_clean.encode('utf-8')).hexdigest()[:10]

def pull_and_sync():
    print("Fetching sync state from cloud...")
    try:
        req = urllib.request.Request(SYNC_URL)
        with urllib.request.urlopen(req) as res:
            cloud_state = json.loads(res.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching state from cloud: {e}")
        return False
        
    checklists = cloud_state.get("checklists", {})
    custom_items = cloud_state.get("customItems", [])
    
    print(f"Found {len(checklists)} checked states and {len(custom_items)} custom items.")
    
    # 1. Update standard markdown files
    def sync_file_checkboxes(filepath):
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        modified = False
        new_lines = []
        
        for line in lines:
            # Match checklist items: - [ ] Some Label
            match = re.match(r"^(\s*-\s*\[)([ x])(\]\s*)(.*?)$", line)
            if match:
                prefix = match.group(1)
                current_val = match.group(2)
                suffix = match.group(3)
                label = match.group(4).strip()
                
                # Check stable hash
                chk_id = get_clean_hash(label)
                if chk_id in checklists:
                    expected_val = 'x' if checklists[chk_id] else ' '
                    if current_val != expected_val:
                        line = f"{prefix}{expected_val}{suffix}{label}\n"
                        modified = True
            new_lines.append(line)
            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Updated checkboxes in: {os.path.basename(filepath)}")

    # Sync all docs and daily plans
    for f_name in os.listdir(docs_dir):
        if f_name.endswith(".md"):
            sync_file_checkboxes(os.path.join(docs_dir, f_name))
            
    for f_name in os.listdir(days_dir):
        if f_name.endswith(".md"):
            sync_file_checkboxes(os.path.join(days_dir, f_name))

    # 2. Specially update docs/11_Packing_List.md to append/refresh custom items
    if os.path.exists(packing_file):
        with open(packing_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Strip out any existing ## 自定义行李 section at the bottom
        if "## 自定义行李" in content:
            parts = content.split("## 自定义行李")
            content = parts[0].strip() + "\n"
            
        if custom_items:
            custom_md = "\n## 自定义行李 (Custom Items)\n\n"
            for item in custom_items:
                val = 'x' if item.get("checked") else ' '
                custom_md += f"- [{val}] {item.get('name')}\n"
            content = content.strip() + "\n" + custom_md
            
        with open(packing_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Synchronized custom items to 11_Packing_List.md!")

    # 3. Re-run compilation scripts
    print("Re-compiling roadbook artifacts...")
    subprocess.run(['python', 'scripts/compile_roadbook.py'], cwd=workspace)
    subprocess.run(['python', 'scripts/compile_consolidated_md.py'], cwd=workspace)
    
    # 4. Push updates to GitHub
    print("Pushing updates to GitHub...")
    subprocess.run(['git', 'add', '.'], cwd=workspace)
    subprocess.run(['git', 'commit', '-m', 'Synchronize checklist and custom packing list state from cloud'], cwd=workspace)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=workspace)
    print("Synchronization and GitHub Pages deployment complete!")
    return True

if __name__ == "__main__":
    pull_and_sync()
