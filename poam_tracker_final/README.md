# POA&M + Continuous Monitoring Tracker

A lightweight tracker that models how I operationalize continuous monitoring:  
**findings → risk → owner → milestones → due dates → POA&M export → monthly status reporting**.

This repo is designed to be **reviewer-friendly**. You can understand the workflow by opening the sample exports without running any code.

> **OPSEC / confidentiality:** Everything here is **fictionalized/sanitized**. No real program data, no customer names, and no eMASS exports.

---

## For Hiring Managers

### What this demonstrates
- Practical POA&M mechanics: ownership, deadlines, milestones, aging, and accountability
- Continuous monitoring reporting: turning raw findings into leadership-ready summaries
- Evidence discipline: consistent IDs, timestamps, exportable artifacts

### What to review first (5–10 minutes)
1) Sample POA&M export (CSV): [`exports/poam_export.sample.csv`](exports/poam_export.sample.csv)  
2) Sample monthly status report (Markdown): [`exports/monthly_status_report.sample.md`](exports/monthly_status_report.sample.md)  
3) Sample dataset (fictional findings): [`sample-data/findings.sample.csv`](sample-data/findings.sample.csv)  
4) Clickable evidence stubs: [`evidence/`](evidence/)  
5) Workflow overview: [`docs/workflow.md`](docs/workflow.md)  
6) Export schema: [`docs/exports/export-schema.md`](docs/exports/export-schema.md)  

Optional (demo UI): [`app/streamlit_app.py`](app/streamlit_app.py)

---

## How it works (simple)
1) Findings are captured in a normalized CSV (scan, audit, or manual review).
2) Each finding is mapped to controls, assigned an owner, and tracked to closure.
3) The tool generates:
   - a POA&M-style export (CSV)
   - a monthly continuous monitoring status report (Markdown)

---

## Quick start (local)

Requires Python 3.10+.

```bash
# (optional) create a venv
python -m venv .venv
source .venv/bin/activate

# generate exports from the sample dataset (current month by default)
python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports

# deterministic output (useful for screenshots / consistency)
python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports --month 2026-02 --today 2026-02-13
```

---

## Repository map

```text
sample-data/                              Fictional findings dataset
evidence/                                 Clickable stub evidence artifacts
exports/                                  Sample outputs (static examples)
tools/generate_exports.py                 CLI that generates POA&M export + monthly report
docs/workflow.md                          Workflow overview
docs/exports/export-schema.md             Definition of export columns
docs/reporting/monthly-report-format.md   Reporting format and intent
app/streamlit_app.py                      Optional demo UI
```

---

## Roadmap (optional enhancements)
- Add append-only audit trail for status changes (who/when/what changed)
- Add charts for monthly trend reporting (overdue aging, severity distribution)
- Add import adapters (CSV/JSON) for scan results and ticketing exports
