# POA&M + Continuous Monitoring Tracker

A lightweight tracker modeling how I operationalize continuous monitoring:
**findings → risk → owner → milestones → due dates → POA&M export → monthly status reporting**.

This is built to demonstrate real-world mechanics (not just a spreadsheet) while staying public-safe using fictional sample data.

---

## For Hiring Managers

### What this demonstrates
- How I run POA&Ms like an operational system:
  - ownership, deadlines, aging, milestones, and accountability
- A repeatable approach to **monthly continuous monitoring reporting**
- Evidence discipline: **consistent IDs**, timestamps, and exportable outputs

### What to review first (3–7 minutes)
1. **Workflow overview:** see “How it works” below
2. **Sample data:** `sample-data/findings.sample.csv`
3. **Exports:** `exports/poam_export.sample.csv` and `exports/monthly_status_report.sample.md`
4. **Reporting format:** `docs/reporting/monthly-report-format.md`

### What’s intentionally omitted (OPSEC / proprietary)
- No real program data, no eMASS exports, and no customer findings
- All sample data is fictional and structured solely for demonstration

---

## How it works (concept)
1. **Ingest** findings (from scans, tickets, audits, manual reviews)
2. **Normalize** fields (severity, impact, control mapping, owner)
3. **Track** status + milestones over time
4. **Export** a POA&M-style report (CSV/JSON)
5. **Generate** a monthly summary suitable for leadership briefs

---

## Data model (high-level)
Each finding contains:
- `finding_id` (unique)
- `source` (scan/audit/manual)
- `severity` and `risk_score` (demo scale)
- `control_refs` (e.g., AC-2, SI-2)
- `system` / `boundary` (fictional)
- `owner` (team or role)
- `milestones` + `scheduled_completion_date`
- `status` (Open / In Progress / Mitigated / Closed)
- `evidence_links` (paths to supporting artifacts)

---

## Repository map

```text
app/                         (implementation: UI/API/CLI)
sample-data/
  findings.sample.csv
  owners.sample.csv
docs/
  reporting/
    monthly-report-format.md
  exports/
    export-schema.md
exports/
  poam_export.sample.csv
  monthly_status_report.sample.md
tests/
