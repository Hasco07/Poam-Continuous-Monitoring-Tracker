# POA&M + Continuous Monitoring Tracker

A lightweight tracker that models how I operationalize continuous monitoring:

**findings → risk → owner → milestones → due dates → POA&M export → monthly status reporting**.

This repo is built to demonstrate real-world POA&M / ConMon mechanics (not just a spreadsheet) while staying **public-safe** using **fictional sample data**.

> **OPSEC / confidentiality:** Everything here is fictionalized/sanitized. No real program data, no customer names, and no eMASS exports.

---

## Start here

The project files are in this folder:

- **Project Root:** [Project Root](poam_tracker_final/)
- **Project README:** [Project README](poam_tracker_final/README.md)

---

## For Hiring Managers

### What this demonstrates
- Practical POA&M mechanics: ownership, due dates, milestones, aging, and accountability
- Continuous monitoring reporting: turning raw findings into leadership-ready summaries
- Evidence discipline: consistent IDs, timestamps, exportable outputs

### What to review first (5–10 minutes)
1) Sample POA&M Export (CSV): [Sample POA&M Export](poam_tracker_final/exports/poam_export.sample.csv)  
2) Sample Monthly Status Report (Markdown): [Sample Monthly Status Report](poam_tracker_final/exports/monthly_status_report.sample.md)  
3) Sample Dataset (Fictional Findings): [Sample Dataset (Fictional Findings)](poam_tracker_final/sample-data/findings.sample.csv)  
4) Clickable Evidence Stubs: [Clickable Evidence Stubs](poam_tracker_final/evidence/)  
5) Workflow Overview: [Workflow Overview](poam_tracker_final/docs/workflow.md)  
6) Export Schema: [Export Schema](poam_tracker_final/docs/exports/export-schema.md)  
7) Monthly Report Format: [Monthly Report Format](poam_tracker_final/docs/reporting/monthly-report-format.md)  

Optional (Demo UI): [Demo UI](poam_tracker_final/app/streamlit_app.py)

---

## Quick start (local)

Requires Python 3.10+.

```bash
cd poam_tracker_final

# optional: check links + evidence references
python tools/check_repo.py

# generate exports from the sample dataset (current month by default)
python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports

# output (useful for screenshots / consistency)
python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports --month 2026-02 --today 2026-02-13
