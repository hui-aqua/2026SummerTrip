import os
import re

docs_dir = r"d:\AppleICloud\iCloudDrive\2026SummerTrip\docs"
pattern = re.compile(r"\((已确认|已确定|已预订|已精确计算|已精确估算|已计算)\)")

matches = []
for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for idx, line in enumerate(lines):
                if pattern.search(line):
                    matches.append((file, idx + 1, line.strip()))

print(f"Total confirmed-like tags found: {len(matches)}")
for m in matches[:30]:
    print(f"{m[0]}:{m[1]}: {m[2]}")
