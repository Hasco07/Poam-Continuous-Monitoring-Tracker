#!/usr/bin/env python3
"""Generate POA&M export + monthly report from a normalized findings CSV.

This is intentionally simple so reviewers can read and trust it.

Usage:
  python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports
  python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports --month 2026-02
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path
from collections import Counter

TODAY = dt.date.today()

REQUIRED_FIELDS = [
    "finding_id","title","system","control_refs","source","severity","risk_score","status","owner",
    "discovered_date","due_date","milestones","evidence_paths","notes"
]

def parse_date(s: str) -> dt.date:
    try:
        return dt.date.fromisoformat(s)
    except ValueError as e:
        raise SystemExit(f"Invalid date '{s}'. Use YYYY-MM-DD.") from e

def month_window(month: str) -> tuple[dt.date, dt.date]:
    """month: YYYY-MM"""
    year, m = month.split("-")
    year_i = int(year); m_i = int(m)
    start = dt.date(year_i, m_i, 1)
    end = dt.date(year_i + 1, 1, 1) if m_i == 12 else dt.date(year_i, m_i + 1, 1)
    return start, end

def load_rows(path: Path) -> list[dict[str,str]]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SystemExit("CSV has no header row.")
        missing = [c for c in REQUIRED_FIELDS if c not in reader.fieldnames]
        if missing:
            raise SystemExit(f"Missing required columns: {missing}")
        return list(reader)

def write_poam_export(rows: list[dict[str,str]], out_csv: Path, today: dt.date) -> list[dict[str,object]]:
    poam_export: list[dict[str,object]] = []
    for idx, r in enumerate(rows, start=1):
        discovered = parse_date(r["discovered_date"])
        due = parse_date(r["due_date"])
        status = r["status"].strip()
        is_closed = status.lower() == "closed"

        days_open = "" if is_closed else (today - discovered).days
        days_overdue = 0 if is_closed else max(0, (today - due).days)

        poam_export.append({
            "poam_id": f"POAM-{idx:03d}",
            "finding_id": r["finding_id"].strip(),
            "title": r["title"].strip(),
            "system": r["system"].strip(),
            "control_refs": r["control_refs"].strip(),
            "source": r["source"].strip(),
            "severity": r["severity"].strip(),
            "risk_score": int(float(r["risk_score"])) if r["risk_score"].strip() else 0,
            "status": status,
            "owner": r["owner"].strip(),
            "discovered_date": r["discovered_date"].strip(),
            "due_date": r["due_date"].strip(),
            "days_open": days_open,
            "days_overdue": days_overdue,
            "milestones": r["milestones"].strip(),
            "evidence_paths": r["evidence_paths"].strip(),
            "notes": r["notes"].strip(),
        })

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(poam_export[0].keys()))
        writer.writeheader()
        writer.writerows(poam_export)

    return poam_export

def write_monthly_report(poam: list[dict[str,object]], out_md: Path, month: str, today: dt.date) -> None:
    start, end = month_window(month)

    def in_month(date_str: str) -> bool:
        d = parse_date(date_str)
        return start <= d < end

    status_counts = Counter([r["status"] for r in poam])
    open_items = [r for r in poam if str(r["status"]).lower() != "closed"]
    severity_counts = Counter([r["severity"] for r in open_items])
    overdue = [r for r in open_items if int(r["days_overdue"]) > 0]
    overdue_sorted = sorted(overdue, key=lambda x: (-int(x["risk_score"]), -int(x["days_overdue"])))[:5]

    newly_opened = [r for r in poam if in_month(str(r["discovered_date"]))]
    # NOTE: demo only: without a close_date field, we approximate closures using due_date within month
    newly_closed = [r for r in poam if str(r["status"]).lower() == "closed" and in_month(str(r["due_date"]))]

    lines: list[str] = []
    lines.append("# Monthly Continuous Monitoring Status Report (Fictional)")
    lines.append("")
    lines.append(f"**Reporting period:** {start.isoformat()} to {(end - dt.timedelta(days=1)).isoformat()}  ")
    lines.append(f"**Report generated:** {today.isoformat()}  ")
    lines.append("")
    lines.append("## Executive summary")
    lines.append(f"- Open items: {len(open_items)}")
    lines.append(f"- Overdue items: {len(overdue)}")
    if severity_counts:
        lines.append(f"- Open severity mix: " + ", ".join([f"{k}={v}" for k,v in severity_counts.most_common()]))
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append("### By status")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    for st, c in status_counts.items():
        lines.append(f"| {st} | {c} |")
    lines.append("")
    lines.append("### Open items by severity")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---:|")
    for sev in ["Critical","High","Medium","Low"]:
        if sev in severity_counts:
            lines.append(f"| {sev} | {severity_counts[sev]} |")
    lines.append("")
    lines.append("## Top overdue / high-risk items")
    lines.append("")
    if overdue_sorted:
        lines.append("| POA&M | Finding | Severity | Risk | Days overdue | Owner | Due date |")
        lines.append("|---|---|---|---:|---:|---|---|")
        for r in overdue_sorted:
            lines.append(f"| {r['poam_id']} | {r['finding_id']} | {r['severity']} | {r['risk_score']} | {r['days_overdue']} | {r['owner']} | {r['due_date']} |")
    else:
        lines.append("_No overdue items for this period._")
    lines.append("")
    lines.append("## Newly opened this period")
    lines.append("")
    if newly_opened:
        lines.append("| Finding | Severity | Status | Owner | Discovered | Due |")
        lines.append("|---|---|---|---|---|---|")
        for r in newly_opened:
            lines.append(f"| {r['finding_id']} | {r['severity']} | {r['status']} | {r['owner']} | {r['discovered_date']} | {r['due_date']} |")
    else:
        lines.append("_No new findings recorded in this period._")
    lines.append("")
    lines.append("## Newly closed this period (approx.)")
    lines.append("")
    if newly_closed:
        lines.append("| Finding | Severity | Owner | Due date (used as close proxy) |")
        lines.append("|---|---|---|---|")
        for r in newly_closed:
            lines.append(f"| {r['finding_id']} | {r['severity']} | {r['owner']} | {r['due_date']} |")
    else:
        lines.append("_No closures recorded for this period (or close dates not tracked in this simplified demo)._")
    lines.append("")
    lines.append("## Notes")
    lines.append("- This is a demo. A production tracker would include a close_date field and an audit trail of status changes.")
    lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True, help="Input findings CSV")
    p.add_argument("--out", dest="out", required=True, help="Output directory")
    p.add_argument("--month", dest="month", default=f"{TODAY.year:04d}-{TODAY.month:02d}", help="Reporting month YYYY-MM (default: current month)")
    args = p.parse_args()

    inp = Path(args.inp)
    out_dir = Path(args.out)

    rows = load_rows(inp)
    poam = write_poam_export(rows, out_dir / "poam_export.csv", TODAY)
    write_monthly_report(poam, out_dir / "monthly_status_report.md", args.month, TODAY)

    print(f"Wrote: {out_dir/'poam_export.csv'}")
    print(f"Wrote: {out_dir/'monthly_status_report.md'}")

if __name__ == "__main__":
    main()
