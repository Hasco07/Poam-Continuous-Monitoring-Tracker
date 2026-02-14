# Log Source List (Fictional)

**Purpose:** Demonstrates an assessor-friendly inventory of log sources in-scope for AU-2 / AU-6 monitoring on an air-gapped LAN.

> This is a public-safe stub (fictionalized/sanitized).

---

## In-scope log sources (example)

| Source | Host/System | Log Type | Forwarding Target | Review Cadence |
|---|---|---|---|---|
| Directory Services / IdP | KIT-IDP-01 | Auth + audit | Central SIEM | Weekly |
| Git / Source Control | KIT-GIT-01 | Audit + admin actions | Central SIEM | Weekly |
| CI / Build Server | KIT-CI-01 | Audit + admin actions | Central SIEM | Weekly |
| Artifact Repository | KIT-ART-01 | Access + config | Central SIEM | Weekly |
| Test Harness / Simulator | KIT-TEST-01 | Service + access | Central SIEM | Weekly |
| Vulnerability Scanner | KIT-SCAN-01 | Scan summaries | Central SIEM | Monthly |

## Gap handling (example)

- If a log source goes silent, create a ticket, investigate root cause, and document corrective action.
- Validate restoration by confirming forwarding health and reviewing the next scheduled log review evidence.
