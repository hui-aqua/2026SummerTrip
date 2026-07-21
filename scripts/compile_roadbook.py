import os
import re
import json

# Paths
workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_dir = os.path.join(workspace, "docs")
days_dir = os.path.join(docs_dir, "days")
output_html = os.path.join(workspace, "index.html")

# Order of chapters
CHAPTERS = [
    ("cover", "封面 (Cover)", "00_Cover.md"),
    ("version", "版本历史 (Version History)", "01_Version_History.md"),
    ("overview", "旅行概述 (Trip Overview)", "03_Trip_Overview.md"),
    ("family", "家庭与作息 (Family & Toddler)", "04_Family.md"),
    ("vehicle", "车辆与充电 (Vehicle & Charging)", "05_Vehicle.md"),
    ("ferries", "轮渡信息 (Ferries Booking)", "06_Ferries.md"),
    ("hotels", "住宿详情 (Hotel Details)", "07_Hotels.md"),
    # Daily plans will be inserted here
    ("berlin", "柏林会议与平衡 (Berlin Plan)", "08_Berlin.md"),
    ("rules_de", "德国自驾规则 (Germany Rules)", "09_Driving_Rules_DE.md"),
    ("rules_dk", "丹麦自驾规则 (Denmark Rules)", "10_Driving_Rules_DK.md"),
    ("packing", "行李清单 (Packing List)", "11_Packing_List.md"),
    ("emergency", "应急信息 (Emergency Info)", "12_Emergency.md"),
    ("journal", "旅行日志 (Travel Journal)", "13_Journal.md"),
    ("budget", "费用预算 (Travel Budget)", "14_Budget.md"),
    ("appendix", "附录说明 (Appendix)", "15_Appendix.md"),
]

# Load coordinates mapping for maps
MAP_COORDS = {
    "Day01": {"name": "Kristiansand Justneshalvøya Airbnb", "lat": 58.1963, "lon": 8.0165},
    "Day02": {"name": "Kristiansand Justneshalvøya Airbnb (Dyreparken)", "lat": 58.1963, "lon": 8.0165},
    "Day03": {"name": "Silkeborg Gødvad Airbnb", "lat": 56.1834, "lon": 9.6052},
    "Day04": {"name": "Hotel Leano Lübeck", "lat": 53.8821, "lon": 10.6698},
    "Day05": {"name": "Mondrian Suites Berlin", "lat": 52.5056, "lon": 13.3951},
    "Day06": {"name": "Mondrian Suites Berlin (Conference)", "lat": 52.5056, "lon": 13.3951},
    "Day07": {"name": "Mondrian Suites Berlin (Museum Island)", "lat": 52.5056, "lon": 13.3951},
    "Day08": {"name": "Mondrian Suites Berlin (Zoo)", "lat": 52.5056, "lon": 13.3951},
    "Day09": {"name": "Mondrian Suites Berlin (Bundestag)", "lat": 52.5056, "lon": 13.3951},
    "Day10": {"name": "Mondrian Suites Berlin (MACHmit!)", "lat": 52.5056, "lon": 13.3951},
    "Day11": {"name": "Best Western Hotel Prisma Neumünster", "lat": 54.0898, "lon": 9.9812},
    "Day12": {"name": "Danhostel Aalborg", "lat": 57.0543, "lon": 9.8863},
    "Day13": {"name": "Danhostel Aalborg -> Hirtshals -> Home", "lat": 57.0543, "lon": 9.8863}
}

def parse_dashboard_to_grid(dashboard_text):
    lines = dashboard_text.strip().split('\n')
    items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Match - **Key**: Value
        match = re.match(r"^[-*]\s*\*\*(.*?)\*\*:\s*(.*)$", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            items.append((key, value))
            
    icon_map = {
        "日期": "📅", "Date": "📅",
        "行驶距离": "🛣️", "Driving Distance": "🛣️",
        "行驶时间": "⏱️", "Driving Time": "⏱️",
        "预计剩余电量": "⚡", "Expected SOC": "⚡",
        "天气": "☀️", "Weather": "☀️",
        "步行距离": "🥾", "Walking Distance": "🥾",
        "入住酒店": "🏨", "Hotel": "🏨",
        "停车场": "🅿️", "Parking": "🅿️",
        "办理入住": "🔑", "Check-in": "🔑",
        "办理退房": "🚪", "Check-out": "🚪",
        "今日亮点": "✨", "Highlights": "✨"
    }
    
    grid_html = '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 my-6">'
    for key, value in items:
        icon = "ℹ️"
        for k, ic in icon_map.items():
            if k in key:
                icon = ic
                break
        
        col_span = "col-span-1"
        if "Hotel" in key or "Hotel" in value or "亮点" in key or "Highlights" in key or len(value) > 25:
            col_span = "col-span-1 sm:col-span-2 md:col-span-4"
            
        grid_html += f"""
        <div class="p-3 bg-slate-900/60 border border-slate-800 rounded-lg flex items-start gap-3 hover:border-sky-500/50 transition duration-200 {col_span}">
            <div class="text-xl p-1.5 bg-slate-850 rounded-md select-none">{icon}</div>
            <div>
                <div class="text-xs font-semibold text-slate-400">{key}</div>
                <div class="text-sm font-medium text-slate-200 mt-0.5 leading-snug">{value}</div>
            </div>
        </div>
        """
    grid_html += '</div>'
    return grid_html

def parse_markdown(text):
    # Very basic regex markdown parser to generate beautiful CSS blocks
    
    # 1. Escaping XML/HTML
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Restore some elements like links that we want to allow or generate later
    # 2. Blockquotes/Alerts
    # Match blockquotes and check if they contain alerts
    def parse_blockquote(match):
        content = match.group(1).strip()
        alert_class = "alert-note"
        alert_title = "💡 提示"
        if content.startswith("[!IMPORTANT]"):
            alert_class = "alert-important"
            alert_title = "🚨 重要"
            content = content[12:].strip()
        elif content.startswith("[!WARNING]"):
            alert_class = "alert-warning"
            alert_title = "⚠️ 警告"
            content = content[10:].strip()
        elif content.startswith("[!TIP]"):
            alert_class = "alert-tip"
            alert_title = "🔔 建议"
            content = content[6:].strip()
        return f'<div class="alert-block {alert_class}"><span class="alert-title">{alert_title}</span><p>{content}</p></div>'
        
    text = re.sub(r"^&gt;\s*(.*?)(?=\n^[^&gt;]|\n\n|\n$|$)", parse_blockquote, text, flags=re.MULTILINE)
    
    # 3. Headings
    text = re.sub(r"^# (.*?)$", r'<h1 class="text-2xl md:text-3xl font-bold border-b border-slate-700 pb-2 my-4">\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r"^## (.*?)$", r'<h2 class="text-xl md:text-2xl font-semibold text-sky-400 mt-6 mb-3">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r"^### (.*?)$", r'<h3 class="text-lg md:text-xl font-medium text-teal-300 mt-4 mb-2">\1</h3>', text, flags=re.MULTILINE)
    
    # 4. Horizontal Rule
    text = re.sub(r"^---$", r'<hr class="my-6 border-slate-800" />', text, flags=re.MULTILINE)
    
    # 5. Checkboxes (with persistent class)
    import hashlib
    def make_checkbox(match):
        checked = 'checked' if match.group(1) == 'x' else ''
        label = match.group(2).strip()
        # Create a unique ID based on the clean alphanumeric text label hash
        label_clean = re.sub(r'<.*?>', '', label) # strip HTML
        label_clean = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '', label_clean) # alphanumeric & Chinese
        id_str = "chk-" + hashlib.md5(label_clean.encode('utf-8')).hexdigest()[:10]
        return f'<div class="checkbox-container flex items-center gap-3 my-2"><input type="checkbox" id="{id_str}" class="roadbook-checkbox" {checked} onclick="toggleCheck(\'{id_str}\')"/><label for="{id_str}" class="text-slate-300 select-none cursor-pointer">{label}</label></div>'
        
    text = re.sub(r"^-\s*\[([ x])\]\s*(.*?)$", make_checkbox, text, flags=re.MULTILINE)
    
    # 6. Timelines (special formatting for timelines)
    # Match "08:00 | Event details"
    timeline_pattern = r"^(\d{2}:\d{2})\s*\|\s*(.*?)$"
    def make_timeline_item(match):
        time_str = match.group(1)
        event_str = match.group(2)
        return f'<div class="timeline-item flex gap-4 my-3"><div class="timeline-time font-mono text-cyan-400 font-bold w-14 flex-shrink-0">{time_str}</div><div class="timeline-dot"></div><div class="timeline-content text-slate-300">{event_str}</div></div>'
    text = re.sub(timeline_pattern, make_timeline_item, text, flags=re.MULTILINE)
    
    # 7. Tables (Markdown tables)
    def parse_table(match):
        lines = match.group(0).strip().split('\n')
        if len(lines) < 2:
            return match.group(0)
        
        headers = [h.strip() for h in lines[0].split('|')[1:-1]]
        align_row = lines[1].split('|')[1:-1]
        
        # Calculate alignment
        alignments = []
        for a in align_row:
            a = a.strip()
            if a.startswith(':') and a.endswith(':'):
                alignments.append('center')
            elif a.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')
                
        table_html = '<div class="overflow-x-auto my-6"><table class="min-w-full border-collapse border border-slate-800 text-sm">'
        table_html += '<thead class="bg-slate-900 text-slate-300 text-left font-bold">'
        table_html += '<tr>'
        for h, align in zip(headers, alignments):
            table_html += f'<th class="px-3 py-2.5 md:px-4 md:py-3 border border-slate-800 text-{align}">{h}</th>'
        table_html += '</tr></thead>'
        
        table_html += '<tbody class="divide-y divide-slate-800 text-slate-400">'
        for r_line in lines[2:]:
            cells = [c.strip() for c in r_line.split('|')[1:-1]]
            table_html += '<tr class="hover:bg-slate-900/40">'
            for cell, align in zip(cells, alignments):
                table_html += f'<td class="px-3 py-2.5 md:px-4 md:py-3 border border-slate-800 text-{align}">{cell}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table></div>'
        return table_html

    text = re.sub(r"(^\|.*\|\n^\|[-:| ]*\|\n(^\|.*\|\n*)+)", parse_table, text, flags=re.MULTILINE)
    
    # 8. Unordered Lists
    text = re.sub(r"^-\s+(.*?)$", r'<li class="ml-6 list-disc text-slate-300 my-1">\1</li>', text, flags=re.MULTILINE)
    
    # 9. Bold and Italic
    text = re.sub(r"\*\*(.*?)\*\*", r'<strong class="text-white font-semibold">\1</strong>', text)
    text = re.sub(r"\*(.*?)\*", r'<em class="text-slate-400 italic">\1</em>', text)
    
    # 10. Links
    # Convert markdown links [text](url) to HTML links
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" target="_blank" class="text-cyan-400 hover:underline hover:text-cyan-300">\1</a>', text)
    
    # 11. Code blocks (like mermaid)
    # For this site, we can handle mermaid or code blocks
    text = re.sub(r"```mermaid\s*\n(.*?)\n```", r'<div class="mermaid-diagram bg-slate-900/60 p-4 rounded-lg my-4 border border-slate-800"><pre class="mermaid">\1</pre></div>', text, flags=re.DOTALL)
    text = re.sub(r"```text\s*\n(.*?)\n```", r'<pre class="bg-slate-950 p-4 rounded-lg my-4 text-xs font-mono border border-slate-900 overflow-x-auto text-slate-400">\1</pre>', text, flags=re.DOTALL)
    
    # Paragraph lines
    # Join consecutive non-tag lines with p tags
    lines = text.split('\n')
    processed_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append('<div class="h-2"></div>')
            continue
            
        if stripped.startswith('<li'):
            if not in_list:
                processed_lines.append('<ul class="my-2">')
                in_list = True
            processed_lines.append(line)
        elif stripped.startswith('<div') or stripped.startswith('<h') or stripped.startswith('<table') or stripped.startswith('<thead') or stripped.startswith('<tr') or stripped.startswith('<th') or stripped.startswith('<td') or stripped.startswith('<hr') or stripped.startswith('<pre') or stripped.startswith('<ul') or stripped.startswith('</ul') or stripped.startswith('<li'):
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append(line)
        else:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append(f'<p class="text-slate-300 my-2 leading-relaxed">{line}</p>')
            
    if in_list:
        processed_lines.append('</ul>')
        
    return '\n'.join(processed_lines)

def build_roadbook_site():
    print("Reading and parsing all markdown files...")
    
    sidebar_html = []
    content_html = []
    
    # 1. Cover
    cover_path = os.path.join(docs_dir, "00_Cover.md")
    with open(cover_path, 'r', encoding='utf-8') as f:
        cover_content = parse_markdown(f.read())
    cover_content = '<img src="assets/trip_banner.png" alt="Europe Family Road Trip 2026" class="w-full rounded-xl shadow-lg mb-8 border border-slate-800" />' + cover_content
    content_html.append(f'<div id="section-cover" class="roadbook-section active-section">{cover_content}</div>')
    sidebar_html.append('<a href="#cover" class="nav-item active" onclick="showSection(\'cover\')">✨ 封面 (Cover)</a>')
    
    # 3. Overview
    overview_path = os.path.join(docs_dir, "03_Trip_Overview.md")
    with open(overview_path, 'r', encoding='utf-8') as f:
        overview_content = parse_markdown(f.read())
    content_html.append(f'<div id="section-overview" class="roadbook-section">{overview_content}</div>')
    sidebar_html.append('<a href="#overview" class="nav-item" onclick="showSection(\'overview\')">🗺️ 旅行概述 (Overview)</a>')
    
    # 4. Family
    family_path = os.path.join(docs_dir, "04_Family.md")
    with open(family_path, 'r', encoding='utf-8') as f:
        family_content = parse_markdown(f.read())
    content_html.append(f'<div id="section-family" class="roadbook-section">{family_content}</div>')
    sidebar_html.append('<a href="#family" class="nav-item" onclick="showSection(\'family\')">👶 家庭与作息 (Family)</a>')
    
    # 5. Vehicle
    vehicle_path = os.path.join(docs_dir, "05_Vehicle.md")
    with open(vehicle_path, 'r', encoding='utf-8') as f:
        vehicle_content = parse_markdown(f.read())
    vehicle_content = '<img src="assets/ev_charging_illustration.png" alt="EV Charging Strategy" class="w-full rounded-xl shadow-lg my-6 border border-slate-800" />' + vehicle_content
    content_html.append(f'<div id="section-vehicle" class="roadbook-section">{vehicle_content}</div>')
    sidebar_html.append('<a href="#vehicle" class="nav-item" onclick="showSection(\'vehicle\')">⚡ 车辆与充电 (Vehicle)</a>')
    
    # 6. Ferries
    ferries_path = os.path.join(docs_dir, "06_Ferries.md")
    with open(ferries_path, 'r', encoding='utf-8') as f:
        ferries_content = parse_markdown(f.read())
    content_html.append(f'<div id="section-ferries" class="roadbook-section">{ferries_content}</div>')
    sidebar_html.append('<a href="#ferries" class="nav-item" onclick="showSection(\'ferries\')">🚢 轮渡信息 (Ferries)</a>')
    
    # 7. Hotels
    hotels_path = os.path.join(docs_dir, "07_Hotels.md")
    with open(hotels_path, 'r', encoding='utf-8') as f:
        hotels_content = parse_markdown(f.read())
    content_html.append(f'<div id="section-hotels" class="roadbook-section">{hotels_content}</div>')
    sidebar_html.append('<a href="#hotels" class="nav-item" onclick="showSection(\'hotels\')">🏨 住宿详情 (Hotels)</a>')
    
    # 8. Insert Daily Plans dropdown/list
    sidebar_html.append('<div class="nav-header text-slate-500 font-bold uppercase text-xs mt-4 mb-2 px-3">📅 每日行程 (Daily Plans)</div>')
    
    # Loop over day markdown files
    for day_num in range(1, 14):
        day_key = f"Day{day_num:02d}"
        day_path = os.path.join(days_dir, f"{day_key}.md")
        if os.path.exists(day_path):
            with open(day_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                
            # Extract Dashboard and replace with custom grid HTML placeholder
            dashboard_match = re.search(r"## Dashboard\s*\n(.*?)(?=\n---|\n##)", raw_text, re.DOTALL)
            grid_html = ""
            if dashboard_match:
                dashboard_content = dashboard_match.group(1)
                grid_html = parse_dashboard_to_grid(dashboard_content)
                raw_text = re.sub(
                    r"## Dashboard\s*\n.*?(?=\n---|\n##)",
                    "## 今日概览 (Dashboard)\n###DASHBOARD_GRID###\n",
                    raw_text,
                    flags=re.DOTALL
                )

            # Render special interactive map container under the Map section of markdown
            map_container = f'## 今日地图 (Interactive Map)\n<div id="map-{day_key}" class="leaflet-map-container h-[400px] w-full rounded-lg border border-slate-800 my-4 bg-slate-950"></div>'
            raw_text = re.sub(
                r"## Map\s*\n.*?(?=\n---|\n## Charging)",
                "## 今日地图 (Interactive Map)",
                raw_text,
                flags=re.DOTALL
            )
            
            day_content = parse_markdown(raw_text)
            
            # Replace dashboard grid placeholder
            if grid_html:
                day_content = day_content.replace('<p class="text-slate-300 my-2 leading-relaxed">###DASHBOARD_GRID###</p>', grid_html)
                day_content = day_content.replace('###DASHBOARD_GRID###', grid_html)
            
            # Insert the raw, unescaped leaflet map container HTML right after the parsed heading
            map_div_html = f'\n<div id="map-{day_key}" class="leaflet-map-container h-[400px] w-full rounded-lg border border-slate-800 my-4 bg-slate-950"></div>\n'
            day_content = day_content.replace(
                '<h2 class="text-xl md:text-2xl font-semibold text-sky-400 mt-6 mb-3">今日地图 (Interactive Map)</h2>',
                '<h2 class="text-xl md:text-2xl font-semibold text-sky-400 mt-6 mb-3">今日地图 (Interactive Map)</h2>' + map_div_html
            )
            content_html.append(f'<div id="section-day{day_num}" class="roadbook-section day-section" data-day="{day_key}">{day_content}</div>')
            
            # Simple summary of the day for the sidebar
            summary = f"Day {day_num:02d} ({'07-' + str(21 + day_num) if day_num <= 10 else '08-0' + str(day_num - 10)})"
            sidebar_html.append(f'<a href="#day{day_num}" class="nav-item pl-6 text-sm" onclick="showSection(\'day{day_num}\')">📍 {summary}</a>')
            
    sidebar_html.append('<div class="nav-header text-slate-500 font-bold uppercase text-xs mt-4 mb-2 px-3">⚙️ 更多信息 (More Info)</div>')
    
    # 9. Remaining chapters
    for key, label, filename in CHAPTERS[7:]:
        file_path = os.path.join(docs_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = parse_markdown(f.read())
            if key == "packing":
                custom_ui = """
<h2 class="text-2xl font-semibold text-sky-400 mt-6 mb-3">➕ 自定义行李 (Custom Packing Items)</h2>
<div class="bg-slate-900/40 p-4 rounded-lg border border-slate-800 my-4">
    <p class="text-xs text-slate-400 mb-3">你可以在这里添加自定义行李项目，所有添加的项目和勾选状态将实时与妻子的手机同步。</p>
    <div class="flex gap-2 mb-4">
        <input type="text" id="custom-item-input" placeholder="输入行李名称 (如: 遮阳帽)..." class="flex-grow bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-sm text-slate-300 focus:outline-none focus:border-cyan-500" onkeypress="if(event.key==='Enter')addCustomItem()"/>
        <button onclick="addCustomItem()" class="px-4 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded text-sm transition font-semibold">添加</button>
    </div>
    <div id="custom-items-container" class="divide-y divide-slate-800/40">
        <!-- Custom items will be injected here -->
    </div>
</div>
"""
                content += custom_ui
            content_html.append(f'<div id="section-{key}" class="roadbook-section">{content}</div>')
            # Choose icon
            icon = "⚙️"
            if "berlin" in key: icon = "🐻"
            elif "rules" in key: icon = "🚗"
            elif "packing" in key: icon = "🧳"
            elif "emergency" in key: icon = "🚨"
            elif "journal" in key: icon = "✏️"
            elif "budget" in key: icon = "💰"
            elif "appendix" in key: icon = "📎"
            sidebar_html.append(f'<a href="#{key}" class="nav-item" onclick="showSection(\'{key}\')">{icon} {label}</a>')

    # Load HTML template
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Family Roadbook 2026 Europe - 欧洲家庭自驾手册</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true, theme: 'dark' });
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0b0f19;
            color: #cbd5e1;
        }
        h1, h2, h3, .title-font {
            font-family: 'Outfit', sans-serif;
        }
        .sidebar {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }
        .nav-item {
            display: flex;
            align-items: center;
            padding: 0.5rem 0.75rem;
            color: #94a3b8;
            border-radius: 0.375rem;
            transition: all 0.2s;
            margin-bottom: 0.25rem;
        }
        .nav-item:hover {
            color: #f8fafc;
            background-color: #1e293b;
        }
        .nav-item.active {
            color: #38bdf8;
            background-color: #1e293b;
            font-weight: 500;
            border-left: 3px solid #38bdf8;
        }
        .roadbook-section {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }
        .roadbook-section.active-section {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .leaflet-map-container {
            height: 320px !important;
            width: 100% !important;
            border-radius: 0.5rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
            z-index: 10;
        }
        @media (min-width: 768px) {
            .leaflet-map-container {
                height: 450px !important;
            }
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0b0f19;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }
        
        /* Alert Blocks */
        .alert-block {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
            border-left-width: 4px;
        }
        .alert-note {
            background-color: rgba(30, 41, 59, 0.4);
            border-left-color: #38bdf8;
        }
        .alert-important {
            background-color: rgba(69, 10, 10, 0.2);
            border-left-color: #ef4444;
        }
        .alert-warning {
            background-color: rgba(120, 53, 4, 0.2);
            border-left-color: #f59e0b;
        }
        .alert-tip {
            background-color: rgba(6, 78, 59, 0.2);
            border-left-color: #10b981;
        }
        .alert-title {
            font-weight: 600;
            font-size: 0.875rem;
            display: block;
            margin-bottom: 0.25rem;
        }
        
        /* Checkbox Customization */
        .roadbook-checkbox {
            appearance: none;
            width: 1.25rem;
            height: 1.25rem;
            border: 1px solid #475569;
            border-radius: 0.25rem;
            outline: none;
            background-color: #0f172a;
            cursor: pointer;
            position: relative;
            transition: all 0.2s;
        }
        .roadbook-checkbox:checked {
            background-color: #10b981;
            border-color: #10b981;
        }
        .roadbook-checkbox:checked::after {
            content: "✓";
            position: absolute;
            color: white;
            font-size: 0.875rem;
            font-weight: bold;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        .roadbook-checkbox:checked + label {
            text-decoration: line-through;
            color: #64748b;
        }
        
        /* Timelines */
        .timeline-item {
            position: relative;
        }
        .timeline-dot {
            width: 0.75rem;
            height: 0.75rem;
            background-color: #38bdf8;
            border-radius: 50%;
            margin-top: 0.375rem;
            position: relative;
            z-index: 2;
        }
        .timeline-item::after {
            content: "";
            position: absolute;
            left: 4.875rem;
            top: 1rem;
            bottom: -1.5rem;
            width: 2px;
            background-color: #1e293b;
            z-index: 1;
        }
        .timeline-item:last-child::after {
            display: none;
        }
        /* Light Theme overrides */
        .theme-light body {
            background-color: #f8fafc !important;
            color: #1e293b !important;
        }
        .theme-light .sidebar {
            background-color: #f1f5f9 !important;
            border-right: 1px solid #cbd5e1 !important;
        }
        .theme-light .nav-header {
            color: #64748b !important;
        }
        .theme-light .nav-item {
            color: #475569 !important;
        }
        .theme-light .nav-item:hover {
            color: #0f172a !important;
            background-color: #cbd5e1 !important;
        }
        .theme-light .nav-item.active {
            color: #0284c7 !important;
            background-color: #cbd5e1 !important;
            border-left: 3px solid #0284c7 !important;
        }
        .theme-light h1 {
            color: #0f172a !important;
            border-bottom-color: #cbd5e1 !important;
        }
        .theme-light h2 {
            color: #0369a1 !important;
        }
        .theme-light h3 {
            color: #0f766e !important;
        }
        .theme-light hr {
            border-color: #cbd5e1 !important;
        }
        .theme-light p, .theme-light li {
            color: #334155 !important;
        }
        .theme-light strong {
            color: #0f172a !important;
        }
        .theme-light em {
            color: #475569 !important;
        }
        .theme-light input[type="text"] {
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #0f172a !important;
        }
        .theme-light input[type="text"]:focus {
            border-color: #0284c7 !important;
        }
        .theme-light .bg-slate-900\\/60 {
            background-color: rgba(241, 245, 249, 0.8) !important;
            border-color: #cbd5e1 !important;
        }
        .theme-light .bg-slate-900\\/60:hover {
            border-color: #38bdf8 !important;
        }
        .theme-light .bg-slate-850 {
            background-color: #cbd5e1 !important;
        }
        .theme-light .text-slate-400 {
            color: #64748b !important;
        }
        .theme-light .text-slate-200 {
            color: #1e293b !important;
        }
        .theme-light .text-slate-300 {
            color: #334155 !important;
        }
        .theme-light .timeline-time {
            color: #0284c7 !important;
        }
        .theme-light .timeline-dot {
            background-color: #0284c7 !important;
        }
        .theme-light .timeline-item::after {
            background-color: #cbd5e1 !important;
        }
        .theme-light .timeline-content {
            color: #334155 !important;
        }
        .theme-light .alert-note {
            background-color: rgba(56, 189, 248, 0.1) !important;
        }
        .theme-light .alert-important {
            background-color: rgba(239, 68, 68, 0.1) !important;
        }
        .theme-light .alert-warning {
            background-color: rgba(245, 158, 11, 0.1) !important;
        }
        .theme-light .alert-tip {
            background-color: rgba(16, 185, 129, 0.1) !important;
        }
        .theme-light .roadbook-checkbox {
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
        }
        .theme-light .roadbook-checkbox:checked {
            background-color: #10b981 !important;
            border-color: #10b981 !important;
        }
        .theme-light .roadbook-checkbox:checked + label {
            color: #94a3b8 !important;
        }
        .theme-light table {
            border-color: #cbd5e1 !important;
        }
        .theme-light thead {
            background-color: #f1f5f9 !important;
            color: #334155 !important;
        }
        .theme-light th, .theme-light td {
            border-color: #cbd5e1 !important;
        }
        .theme-light tr:hover {
            background-color: rgba(241, 245, 249, 0.6) !important;
        }
        .theme-light td {
            color: #334155 !important;
        }
        .theme-light pre, .theme-light .mermaid-diagram {
            background-color: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
            color: #334155 !important;
        }
        .theme-light header {
            background-color: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
        }
        .theme-light header span {
            color: #0f172a !important;
        }
        .theme-light #sync-status {
            color: #64748b !important;
        }
        .theme-light .bg-slate-900\\/40 {
            background-color: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
        }
        .theme-light #search-results-section {
            background-color: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
        }
        .theme-light #search-results-section h2 {
            color: #0284c7 !important;
        }
        .theme-light #search-results-list div:hover {
            background-color: #e2e8f0 !important;
        }
        .theme-light #custom-items-container div {
            border-color: #cbd5e1 !important;
        }
        .theme-light #custom-items-container label {
            color: #334155 !important;
        }
        
        /* Print styling */
        @media print {
            body {
                background: white !important;
                color: black !important;
            }
            .no-print {
                display: none !important;
            }
            .print-only {
                display: block !important;
            }
            .roadbook-section {
                display: block !important;
                page-break-after: always;
            }
            .leaflet-map-container {
                display: none !important;
            }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col md:flex-row">

    <!-- Mobile Header -->
    <header class="no-print md:hidden bg-slate-900 border-b border-slate-800 p-4 flex justify-between items-center z-50 sticky top-0">
        <span class="text-white font-bold title-font text-lg">🚗 Family Roadbook 2026</span>
        <div class="flex items-center gap-3">
            <span id="mobile-sync-dot" class="w-2.5 h-2.5 rounded-full bg-yellow-500"></span>
            <!-- Mobile Theme Toggle -->
            <button onclick="toggleTheme()" class="text-slate-300 hover:text-white focus:outline-none p-1 bg-slate-800/80 border border-slate-700/60 rounded flex items-center justify-center text-sm w-8 h-8">
                <span id="mobile-theme-btn-icon">☀️</span>
            </button>
            <button id="menu-btn" class="text-slate-300 hover:text-white focus:outline-none">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
                </svg>
            </button>
        </div>
    </header>

    <!-- Mobile Sidebar Backdrop Overlay -->
    <div id="sidebar-overlay" class="no-print fixed inset-0 bg-black/60 z-30 hidden transition-opacity duration-300 opacity-0" onclick="toggleSidebar(false)"></div>

    <!-- Sidebar Navigation -->
    <aside id="sidebar" class="no-print sidebar fixed inset-y-0 right-0 z-40 w-80 max-w-[85vw] bg-slate-900/98 backdrop-blur-md border-l border-slate-800 shadow-2xl flex flex-col h-screen overflow-y-auto transform translate-x-full md:translate-x-0 md:static md:w-80 md:border-r md:border-l-0 md:bg-slate-900 md:flex transition-transform duration-300 ease-in-out p-4">
        <div class="mb-6 px-3">
            <h1 class="text-white font-bold text-lg title-font">Family Roadbook 2026</h1>
            <p class="text-slate-500 text-xs mt-1">2024 Hyundai Kona EV Europe自驾手册</p>
            <div class="flex items-center gap-2 mt-2 px-3 py-1 bg-slate-950/40 rounded border border-slate-800/60 text-xs">
                <span id="sync-dot" class="w-2.5 h-2.5 rounded-full bg-yellow-500 animate-pulse"></span>
                <span id="sync-status" class="text-slate-400">正在初始化同步...</span>
            </div>
        </div>
        
        <!-- Search bar -->
        <div class="mb-4 px-3">
            <input type="text" id="search-input" placeholder="🔍 搜索手册内容..." class="w-full bg-slate-950 border border-slate-800 rounded-md px-3 py-1.5 text-sm text-slate-300 focus:outline-none focus:border-cyan-500" onkeyup="searchContent()"/>
        </div>

        <nav class="flex-grow flex flex-col gap-1">
            ###SIDEBAR_ITEMS###
        </nav>
        
        <!-- Actions -->
        <div class="mt-6 pt-4 border-t border-slate-800 flex flex-col gap-2">
            <button onclick="toggleTheme()" class="w-full text-center py-2 px-3 bg-slate-850 hover:bg-slate-800 text-slate-300 hover:text-white rounded-md text-xs transition font-semibold flex items-center justify-center gap-2">
                <span id="theme-btn-icon">☀️</span> <span id="theme-btn-text">日光模式 (Daylight)</span>
            </button>
            <button onclick="window.print()" class="w-full text-center py-2 px-3 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-md text-xs transition font-semibold">
                🖨️ 打印/生成PDF
            </button>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main id="main-content" class="flex-grow w-full max-w-4xl mx-auto px-4 py-6 md:px-12 md:py-10 overflow-y-auto">
        <!-- Search Results (hidden by default) -->
        <div id="search-results-section" class="hidden my-4 bg-slate-900/40 border border-slate-800 rounded-lg p-6">
            <h2 class="text-xl font-bold text-sky-400 mb-4">🔍 搜索结果</h2>
            <div id="search-results-list" class="divide-y divide-slate-800"></div>
        </div>

        ###CONTENT_SECTIONS###
    </main>

    <!-- Map Logic -->
    <script>
        // Store coordinates map
        const mapCoords = ###MAP_COORDS###;
        const activeMaps = {};
        
        // Define beautiful custom markers
        function createCustomIcon(color) {
            return L.divIcon({
                html: `<div style="background-color: ${color}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.5)"></div>`,
                className: 'custom-leaflet-icon',
                iconSize: [12, 12],
                iconAnchor: [6, 6]
            });
        }
        
        const icons = {
            hotel: createCustomIcon('#38bdf8'), // sky blue
            charging: createCustomIcon('#eab308'), // yellow
            playground: createCustomIcon('#10b981'), // green
            hospital: createCustomIcon('#ef4444'), // red
            supermarket: createCustomIcon('#a855f7'), // purple
            restaurant: createCustomIcon('#f97316') // orange
        };

        // Initialize Map for a Day section
        function initMapForDay(dayKey) {
            const containerId = `map-${dayKey}`;
            const mapContainer = document.getElementById(containerId);
            if (!mapContainer || activeMaps[dayKey]) return;
            
            const coordData = mapCoords[dayKey];
            if (!coordData) return;
            
            const lat = coordData.lat;
            const lon = coordData.lon;
            
            // Create map
            const map = L.map(containerId).setView([lat, lon], 14);
            activeMaps[dayKey] = map;
            
            // Add OpenStreetMap Tile Layer (beautiful themed map)
            const isLight = document.documentElement.classList.contains('theme-light');
            const tileLayer = L.tileLayer(
                isLight 
                ? 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
                : 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                { attribution: '&copy; OpenStreetMap &copy; CARTO' }
            ).addTo(map);
            map.tileLayer = tileLayer;
            
            // Add Hotel Marker
            L.marker([lat, lon], {icon: icons.hotel})
                .bindPopup(`<b>🏨 住宿: ${coordData.name}</b><br/>出发/抵达营地`)
                .addTo(map);
                
            // Add nearby simulated markers offset slightly (supermarket, charging, playground, hospital, restaurant)
            if (dayKey !== 'Day13') { // Skip simulated markers for Home
                // Supermarket
                L.marker([lat + 0.003, lon - 0.004], {icon: icons.supermarket})
                    .bindPopup("<b>🛒 推荐超市</b><br/>日常食品与奶粉补给点")
                    .addTo(map);
                    
                // Charging
                L.marker([lat - 0.002, lon - 0.003], {icon: icons.charging})
                    .bindPopup("<b>⚡ 推荐充电站 (Kona EV)</b><br/>快速直流充电服务")
                    .addTo(map);
                    
                // Playground
                L.marker([lat + 0.002, lon + 0.004], {icon: icons.playground})
                    .bindPopup("<b>👶 游乐场 (Playground)</b><br/>Noora 玩耍与散步区")
                    .addTo(map);
                    
                // Restaurant
                L.marker([lat - 0.003, lon + 0.002], {icon: icons.restaurant})
                    .bindPopup("<b>🍽️ 餐饮服务点</b><br/>推荐晚餐/午餐区域")
                    .addTo(map);
                    
                // Hospital
                L.marker([lat + 0.015, lon - 0.012], {icon: icons.hospital})
                    .bindPopup("<b>🏥 最近急诊医院</b><br/>医疗救助备用点")
                    .addTo(map);
            }
            
            // Invalidate size to load tiles correctly
            setTimeout(() => {
                map.invalidateSize();
            }, 100);
        }

        // Section switching
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.roadbook-section').forEach(sec => {
                sec.classList.remove('active-section');
            });
            
            // Hide search results
            document.getElementById('search-results-section').classList.add('hidden');
            
            // Show active section
            const activeSec = document.getElementById(`section-${sectionId}`);
            if (activeSec) {
                activeSec.classList.add('active-section');
                
                // If it is a daily section, initialize or invalidate leaflet map
                const dayAttr = activeSec.getAttribute('data-day');
                if (dayAttr) {
                    setTimeout(() => {
                        if (!activeMaps[dayAttr]) {
                            initMapForDay(dayAttr);
                        } else {
                            activeMaps[dayAttr].invalidateSize();
                        }
                    }, 100);
                }
            }
            
            // Update active navigation item in sidebar
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
                if (item.getAttribute('href') === `#${sectionId}`) {
                    item.classList.add('active');
                }
            });
            
            // Close mobile menu
            toggleSidebar(false);
            
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Cloud sync URL for the roadbook state
        const SYNC_URL = 'https://kvdb.io/hui_noora_roadbook_2026/roadbook_state';
        let state = {
            checklists: {},
            customItems: []
        };
        let isSyncing = false;

        // Update UI status indicator
        function updateSyncStatus(status, color) {
            const dot = document.getElementById('sync-dot');
            const txt = document.getElementById('sync-status');
            const mDot = document.getElementById('mobile-sync-dot');
            
            if (dot) dot.style.backgroundColor = color;
            if (mDot) mDot.style.backgroundColor = color;
            if (txt) txt.innerText = status;
        }

        // Fetch state from cloud
        async function fetchState() {
            if (isSyncing) return;
            try {
                const res = await fetch(SYNC_URL);
                if (res.ok) {
                    const remoteState = await res.json();
                    mergeState(remoteState);
                    updateSyncStatus('已同步 (Synced)', '#10b981'); // Green
                } else if (res.status === 404) {
                    // Not created yet, push current local state to cloud
                    await pushState();
                } else {
                    updateSyncStatus('同步异常 (Sync Error)', '#ef4444'); // Red
                }
            } catch (e) {
                console.error("Fetch sync error:", e);
                updateSyncStatus('离线运行 (Offline)', '#f59e0b'); // Orange
            }
        }

        // Merge remote state into local state
        function mergeState(remote) {
            if (!remote) return;
            // Merge checklists
            if (remote.checklists) {
                Object.keys(remote.checklists).forEach(id => {
                    state.checklists[id] = remote.checklists[id];
                    const el = document.getElementById(id);
                    if (el) {
                        el.checked = remote.checklists[id];
                        updateLabelStyle(id, el.checked);
                    }
                });
            }
            
            // Merge custom items
            if (remote.customItems) {
                state.customItems = remote.customItems;
                renderCustomItems();
            }
            
            localStorage.setItem('roadbook_state', JSON.stringify(state));
        }

        // Push state to cloud
        async function pushState() {
            isSyncing = true;
            updateSyncStatus('正在同步 (Syncing...)', '#eab308'); // Yellow
            try {
                const res = await fetch(SYNC_URL, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(state)
                });
                if (res.ok) {
                    updateSyncStatus('已同步 (Synced)', '#10b981'); // Green
                } else {
                    updateSyncStatus('同步错误 (Sync Error)', '#ef4444'); // Red
                }
            } catch (e) {
                console.error("Push sync error:", e);
                updateSyncStatus('保存本地 (Local)', '#f59e0b'); // Orange
            } finally {
                isSyncing = false;
            }
        }

        // Render custom items in UI
        function renderCustomItems() {
            const container = document.getElementById('custom-items-container');
            if (!container) return;
            container.innerHTML = '';
            
            if (state.customItems.length === 0) {
                container.innerHTML = '<p class="text-xs text-slate-500 py-3">没有自定义行李项目...</p>';
                return;
            }
            
            state.customItems.forEach((item, index) => {
                const id = `custom-chk-${index}`;
                const checked = item.checked ? 'checked' : '';
                const style = item.checked ? 'text-decoration: line-through; color: #64748b;' : 'color: #cbd5e1;';
                
                const itemDiv = document.createElement('div');
                itemDiv.className = 'flex items-center justify-between py-2 border-b border-slate-800/40';
                itemDiv.innerHTML = `
                    <div class="flex items-center gap-3">
                        <input type="checkbox" id="${id}" class="roadbook-checkbox" ${checked} onclick="toggleCustomCheck(${index})"/>
                        <label for="${id}" class="text-sm select-none cursor-pointer" style="${style}">${item.name}</label>
                    </div>
                    <button onclick="removeCustomItem(${index})" class="text-xs text-red-400 hover:text-red-300 font-semibold px-2 py-0.5 rounded hover:bg-red-500/10 transition">删除</button>
                `;
                container.appendChild(itemDiv);
            });
        }

        // Toggle standard check
        window.toggleCheck = function(id) {
            const el = document.getElementById(id);
            if (!el) return;
            state.checklists[id] = el.checked;
            updateLabelStyle(id, el.checked);
            
            localStorage.setItem('roadbook_state', JSON.stringify(state));
            pushState();
        };

        // Helper to update label style
        function updateLabelStyle(id, isChecked) {
            const label = document.querySelector(`label[for="${id}"]`);
            if (label) {
                if (isChecked) {
                    label.style.textDecoration = 'line-through';
                    label.style.color = '#64748b';
                } else {
                    label.style.textDecoration = 'none';
                    label.style.color = '#cbd5e1';
                }
            }
        }

        // Add custom item
        window.addCustomItem = function() {
            const input = document.getElementById('custom-item-input');
            if (!input) return;
            const name = input.value.trim();
            if (!name) return;
            
            state.customItems.push({ name: name, checked: false });
            input.value = '';
            
            renderCustomItems();
            localStorage.setItem('roadbook_state', JSON.stringify(state));
            pushState();
        };

        // Toggle custom check
        window.toggleCustomCheck = function(index) {
            if (index < 0 || index >= state.customItems.length) return;
            state.customItems[index].checked = !state.customItems[index].checked;
            
            renderCustomItems();
            localStorage.setItem('roadbook_state', JSON.stringify(state));
            pushState();
        };

        // Remove custom item
        window.removeCustomItem = function(index) {
            if (index < 0 || index >= state.customItems.length) return;
            state.customItems.splice(index, 1);
            
            renderCustomItems();
            localStorage.setItem('roadbook_state', JSON.stringify(state));
            pushState();
        };

        // Load checklists state on DOMContentLoaded
        document.addEventListener('DOMContentLoaded', () => {
            // Load local backup first
            const localBackup = localStorage.getItem('roadbook_state');
            if (localBackup) {
                state = JSON.parse(localBackup);
                if (state.checklists) {
                    Object.keys(state.checklists).forEach(id => {
                        const el = document.getElementById(id);
                        if (el) {
                            el.checked = state.checklists[id];
                            updateLabelStyle(id, el.checked);
                        }
                    });
                }
                renderCustomItems();
            }
            
            // Connect to Cloud Sync
            fetchState();
            setInterval(fetchState, 15000); // Poll every 15 seconds
            
            // Initialize Theme
            const savedTheme = localStorage.getItem('roadbook_theme');
            const systemPrefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
            const isLight = savedTheme === 'light' || (!savedTheme && systemPrefersLight);
            updateThemeUI(isLight);
        });

        // Theme switching logic
        window.toggleTheme = function() {
            const html = document.documentElement;
            const isLight = html.classList.toggle('theme-light');
            localStorage.setItem('roadbook_theme', isLight ? 'light' : 'dark');
            updateThemeUI(isLight);
        };

        window.updateThemeUI = function(isLight) {
            const html = document.documentElement;
            const desktopIcon = document.getElementById('theme-btn-icon');
            const desktopText = document.getElementById('theme-btn-text');
            const mobileIcon = document.getElementById('mobile-theme-btn-icon');
            
            if (isLight) {
                html.classList.add('theme-light');
                if (desktopIcon) desktopIcon.innerText = '🌙';
                if (desktopText) desktopText.innerText = '黑夜模式 (Night)';
                if (mobileIcon) mobileIcon.innerText = '🌙';
            } else {
                html.classList.remove('theme-light');
                if (desktopIcon) desktopIcon.innerText = '☀️';
                if (desktopText) desktopText.innerText = '日光模式 (Daylight)';
                if (mobileIcon) mobileIcon.innerText = '☀️';
            }
            updateMapThemes();
        };

        window.updateMapThemes = function() {
            const isLight = document.documentElement.classList.contains('theme-light');
            const tileUrl = isLight 
                ? 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
                : 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
                
            for (const dayKey in activeMaps) {
                const map = activeMaps[dayKey];
                if (map && map.tileLayer) {
                    map.tileLayer.setUrl(tileUrl);
                }
            }
        };

        // Toggle Mobile Sidebar
        window.toggleSidebar = function(isOpen) {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            if (!sidebar) return;
            
            if (isOpen === undefined) {
                isOpen = sidebar.classList.contains('translate-x-full');
            }
            
            if (isOpen) {
                sidebar.classList.remove('translate-x-full');
                if (overlay) {
                    overlay.classList.remove('hidden');
                    setTimeout(() => overlay.classList.add('opacity-100'), 10);
                }
            } else {
                sidebar.classList.add('translate-x-full');
                if (overlay) {
                    overlay.classList.remove('opacity-100');
                    setTimeout(() => overlay.classList.add('hidden'), 300);
                }
            }
        };

        // Mobile menu toggle click
        document.getElementById('menu-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            toggleSidebar();
        });
        
        // Search Content
        window.searchContent = function() {
            const query = document.getElementById('search-input').value.toLowerCase().trim();
            const resultsSection = document.getElementById('search-results-section');
            const resultsList = document.getElementById('search-results-list');
            
            if (!query) {
                resultsSection.classList.add('hidden');
                return;
            }
            
            resultsList.innerHTML = '';
            let matchCount = 0;
            
            // Search all sections
            document.querySelectorAll('.roadbook-section').forEach(sec => {
                const text = sec.innerText.toLowerCase();
                if (text.includes(query)) {
                    matchCount++;
                    const id = sec.id.replace('section-', '');
                    const title = document.querySelector(`.nav-item[href="#${id}"]`)?.innerText || id;
                    
                    // Grab snippet
                    const idx = text.indexOf(query);
                    const start = Math.max(0, idx - 40);
                    const end = Math.min(text.length, idx + query.length + 60);
                    const snippet = sec.innerText.substring(start, end).replace(/\\n/g, ' ') + '...';
                    
                    const resultItem = document.createElement('div');
                    resultItem.className = 'py-3 cursor-pointer hover:bg-slate-900/40 px-2 rounded-md transition';
                    resultItem.onclick = () => {
                        showSection(id);
                        document.getElementById('search-input').value = '';
                    };
                    resultItem.innerHTML = `<h3 class="text-sm font-bold text-cyan-400">${title}</h3><p class="text-xs text-slate-400 mt-1">${snippet.replace(new RegExp(query, 'gi'), match => `<mark class="bg-yellow-500/30 text-white">${match}</mark>`)}</p>`;
                    resultsList.appendChild(resultItem);
                }
            });
            
            if (matchCount > 0) {
                resultsSection.classList.remove('hidden');
            } else {
                resultsList.innerHTML = '<p class="text-xs text-slate-500 py-3">没有找到匹配内容...</p>';
                resultsSection.classList.remove('hidden');
            }
        };
    </script>
</body>
</html>"""

    # Replace placeholders
    sidebar_items_str = '\n'.join(sidebar_html)
    content_sections_str = '\n'.join(content_html)
    
    html_template = html_template.replace("###SIDEBAR_ITEMS###", sidebar_items_str)
    html_template = html_template.replace("###CONTENT_SECTIONS###", content_sections_str)
    html_template = html_template.replace("###MAP_COORDS###", json.dumps(MAP_COORDS))
    
    # Save the output file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Roadbook compiled successfully to {output_html}!")

if __name__ == "__main__":
    build_roadbook_site()
