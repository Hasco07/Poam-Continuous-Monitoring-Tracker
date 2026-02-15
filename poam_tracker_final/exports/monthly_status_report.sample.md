# Monthly Continuous Monitoring Status Report (Fictional)

**System/Scope:** Kitsune LAN (fictional)  
**Reporting period:** 2026-02-01 to 2026-02-28  
**Report generated:** 2026-02-13  

## Executive summary
- Open items: 9
- Overdue items: 9
- Open severity mix: Medium=4, High=3, Low=2

## Metrics

### By status

| Status | Count |
|---|---:|
| Open | 4 |
| In Progress | 3 |
| Mitigated | 2 |
| Closed | 3 |

### Open items by severity

| Severity | Count |
|---|---:|
| High | 3 |
| Medium | 4 |
| Low | 2 |

## Top overdue / high-risk items

| POA&M | Finding | Severity | Risk | Days overdue | Owner | Due date | Evidence |
|---|---|---|---:|---:|---|---|---|
| POAM-001 | VULN-001 | High | 85 | 10 | ISSO | 2026-02-03 | [patch-compliance-summary_2026-02-01.md](../evidence/patching/patch-compliance-summary_2026-02-01.md) |
| POAM-002 | VULN-002 | High | 80 | 5 | ISSO | 2026-02-08 | [log-forwarding-config_2026-01-28.md](../evidence/logging/log-forwarding-config_2026-01-28.md) |
| POAM-007 | VULN-007 | High | 78 | 2 | ISSO | 2026-02-11 | [service-account-rotation_2026-02-10.md](../evidence/auth/service-account-rotation_2026-02-10.md) |
| POAM-004 | MAN-004 | Medium | 60 | 3 | ISSO | 2026-02-10 | [log-review-checklist.md](../evidence/logging/log-review-checklist.md) |
| POAM-009 | VULN-009 | Medium | 58 | 7 | ISSO | 2026-02-06 | [change-ticket-example_2026-02-03.md](../evidence/change-control/change-ticket-example_2026-02-03.md) |

## Newly opened this period

| Finding | Severity | Status | Owner | Discovered | Due |
|---|---|---|---|---|---|
| VULN-007 | High | Open | Integration Team | 2026-02-01 | 2026-02-11 |

## Newly closed this period (demo approximation)

_No closures recorded for this period (or close dates not tracked in this simplified demo)._

## Notes / constraints
- This is a public demonstration dataset; some fields are simplified.
- A production tracker would include a close_date field and an append-only audit trail of status changes.
