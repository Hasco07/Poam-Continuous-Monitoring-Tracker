# POA&M + Continuous Monitoring Tracker

A lightweight tracker that models how I operationalize continuous monitoring:
**findings → risk → owner → milestones → due dates → POA&M export → monthly status reporting**.

This repo is designed to be **reviewer-friendly**. You can understand the workflow by reading the README and opening the sample exports without running any code.

> **OPSEC / confidentiality:** Everything here is **fictionalized/sanitized**. No real program data, no customer names, and no eMASS exports.

---

## For Hiring Managers

### What this demonstrates
- Practical POA&M mechanics: ownership, deadlines, milestones, aging, and accountability
- Continuous monitoring reporting: turning raw findings into leadership-ready summaries
- Evidence discipline: consistent IDs, timestamps, exportable artifacts

### What to review first (5–10 minutes)
1) Sample POA&M export: [`exports/poam_export.sample.csv`](exports/poam_export.sample.csv)  
2) Sample monthly report: [`exports/monthly_status_report.sample.md`](exports/monthly_status_report.sample.md)  
3) Evidence stubs (clickable): [`evidence/`](evidence/)  
3) Sample dataset (fictional findings): [`sample-data/findings.sample.csv`](sample-data/findings.sample.csv)  
4) Export schema: [`docs/exports/export-schema.md`](docs/exports/export-schema.md)  

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

# generate exports from the sample dataset
python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports
```

---

## Repository map

```text
sample-data/                         Fictional findings dataset
evidence/                            Clickable stub evidence artifacts
exports/                             Generated sample outputs
tools/generate_exports.py            CLI that generates POA&M export + monthly report
docs/exports/export-schema.md        Definition of export columns
docs/reporting/monthly-report-format.md  Reporting format and intent
```

---

## Roadmap (optional enhancements)
- Add a small Streamlit UI (filters, owner views, export button)
- Add audit trail for status changes (append-only log)
- Add charts for monthly trend reporting (overdue aging, severity distribution)
