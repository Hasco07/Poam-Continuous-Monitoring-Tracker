# Export schema (POA&M-style)

This repo produces a **public-safe, fictional** POA&M-style export intended to demonstrate workflow and evidence discipline.

## `exports/poam_export.csv` columns

| Column | Description |
|---|---|
| `poam_id` | Local POA&M ID (e.g., POAM-001) |
| `finding_id` | Finding ID from the source dataset |
| `title` | Short weakness/finding title |
| `system` | Affected system/component (fictional) |
| `control_refs` | Control references (comma-separated) |
| `source` | Finding source (scan/audit/manual) |
| `severity` | Critical/High/Medium/Low |
| `risk_score` | Simple numeric risk score (fictional scale) |
| `status` | Open / In Progress / Mitigated / Closed |
| `owner` | Responsible role/team |
| `discovered_date` | Date identified (YYYY-MM-DD) |
| `due_date` | Scheduled completion date (YYYY-MM-DD) |
| `days_open` | Age in days since discovered (for non-closed items) |
| `days_overdue` | Overdue days (0 if not overdue) |
| `milestones` | Short milestones string (fictional) |
| `evidence_paths` | Repo-relative evidence paths or placeholders |
| `notes` | Short notes suitable for leadership review |

## `exports/monthly_status_report.md`
A leadership-ready summary showing:
- counts by severity/status
- overdue + high-risk items
- newly opened and newly closed items (for the reporting month)
