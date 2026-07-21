import os
import re

docs_dir = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\docs"
pattern = re.compile(r"\s*\((已确认|已确定|已精确计算|已精确估算|已计算)\)")

modified_count = 0
for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = pattern.sub("", content)
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Cleaned confirmed tags in {file}")
                modified_count += 1

print(f"Total files updated: {modified_count}")
