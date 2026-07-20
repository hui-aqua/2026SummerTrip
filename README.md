# Family Roadbook 2026 Europe (欧洲家庭自驾手册)

This repository contains the source code, automation scripts, and modular Markdown chapters for the **Europe Family Road Trip Handbook (Summer 2026)**. 

The roadbook compiles all details of a family road trip (2 adults + 1 toddler) starting and ending in Stavanger, Norway, driving through Denmark and Germany (with a stop for a conference in Berlin).

---

## 🌐 Live Web Application

The roadbook is compiled into a standalone, interactive single-page application and hosted on GitHub Pages:

👉 **[https://hui-aqua.github.io/2026SummerTrip/](https://hui-aqua.github.io/2026SummerTrip/)**

### Key Web Features
- **Responsive Layout**: Seamless reading on mobile, tablet, and desktop screens.
- **Interactive Maps**: Powered by Leaflet.js and OpenStreetMap, plotting hotels, chargers, parks, and routes for each day.
- **Progress Tracking & Sync**: Checkboxes and custom packing list items synchronize in real-time between devices via cloud storage.
- **Dynamic Visuals**: Clean dark mode aesthetics, timeline components, and automated Mermaid diagram rendering.

---

## 📂 Repository Structure

```text
2026SummerTrip/
├── .agents/          # Agent-specific customizations and workspace rules
├── assets/           # PDF attachments, images, and visual assets
├── docs/             # Core chapters (Cover, Overview, Family, Vehicle, Hotels, etc.)
│   └── days/         # Modular daily plans (Day01.md to Day13.md)
├── scripts/          # Automation and compilation scripts
├── AGENT.md          # AI agent system prompt and documentation rules
├── MANIFEST.yaml     # Metadata configuration and global todo tracking
├── index.html        # Output standalone web application (built from docs)
└── README.md         # This repository guide
```

---

## 🛠️ Automation & Build Scripts

Make sure you have Python 3.x installed. Run these scripts from the repository root:

### 1. Enrich Roadbook Content
Populates modular files in `docs/` and `docs/days/` with driving statistics, EV charging plans, hotel amenities, and local area Mermaid flowcharts:
```bash
python scripts/enrich_roadbook.py
```

### 2. Compile Web Application
Parses all Markdown chapters and compiles them into the interactive single-page app `index.html`:
```bash
python scripts/compile_roadbook.py
```

### 3. Compile Unified Markdown Document
Concatenates all modular chapters in sequence into a single master document `Family_Roadbook_V4.0_CN.md` (ideal for printing or converting to PDF):
```bash
python scripts/compile_consolidated_md.py
```

### 4. Sync Checklist States
Pulls checkbox selections and custom checklist items from cloud storage, updates the local Markdown files, compiles the latest artifacts, and commits/pushes to GitHub Pages:
```bash
python scripts/sync_roadbook.py
```
