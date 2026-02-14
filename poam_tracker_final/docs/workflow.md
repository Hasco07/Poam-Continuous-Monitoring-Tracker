# Workflow (concept)

This repo is an intentionally simplified public demonstration.

## Intake
- Findings can come from scans, audits, or manual reviews.
- Each finding is normalized into a single record with:
  - severity and risk score
  - control mapping
  - owner
  - due date
  - status
  - evidence paths (what proof exists)

## Tracking
- Status changes should be time-stamped.
- High/critical items are reviewed more frequently.
- Closure requires evidence (rescan results, patch report, config validation).

## Reporting
- POA&M export is generated for review.
- Monthly report summarizes changes and provides actionable visibility.
