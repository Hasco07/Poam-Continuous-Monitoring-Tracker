#!/usr/bin/env python3
"""Generate POA&M export + monthly report from a normalized findings CSV.

This is intentionally simple so reviewers can read and trust it.

Usage:
  python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports
  python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports --month 2026-02
  python tools/generate_exports.py --in sample-data/findings.sample.csv --out exports --month 2026-02 --today 2026-02-13

Notes:
- This repo uses fictional/sanitized data.
- Evidence links in the monthly report are generated as relative links from the report location.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
from pathlib import Path
from collections import Counter

REQUIRED_FIELDS = [
    "finding_id","title","system","control_refs","source","severity","risk_score","status","owner",
    "discovered_date","due_date","milestones","evidence_paths","notes"
]

STATUS_ORDER = ["Open", "In Progress", "Mitigated", "Closed"]
SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]


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


def _first_evidence_path(evidence_paths: str) -> str | None:
    # evidence_paths can be a single repo-relative path or multiple separated by ';'
    parts = [p.strip() for p in (evidence_paths or "").split(";") if p.strip()]
    return parts[0] if parts else None


def _evidence_markdown_link(repo_root: Path, report_dir: Path, evidence_rel: str) -> str:
    """Return a markdown link suitable for a report living in report_dir."""
    evidence_file = (repo_root / evidence_rel).resolve()
    rel = Path(os.path.relpath(evidence_file, report_dir)).as_posix()
    label = Path(evidence_rel).name
    return f"[{label}]({rel})"


def write_monthly_report(
    poam: list[dict[str,object]],
    out_md: Path,
    month: str,
    today: dt.date,
    report_system_label: str,
    repo_root: Path,
) -> None:
    start, end = month_window(month)

    def in_month(date_str: str) -> bool:
        d = parse_date(date_str)
        return start <= d < end

    open_items = [r for r in poam if str(r["status"]).lower() != "closed"]
    overdue = [r for r in open_items if int(r["days_overdue"]) > 0]
    overdue_sorted = sorted(overdue, key=lambda x: (-int(x["risk_score"]), -int(x["days_overdue"])))[:5]

    status_counts = Counter([str(r["status"]) for r in poam])
    severity_counts = Counter([str(r["severity"]) for r in open_items])

    # "Newly opened" = discovered in month window
    newly_opened = [r for r in poam if in_month(str(r["discovered_date"]))]

    # Demo only: without close_date we approximate using due_date within month.
    newly_closed = [r for r in poam if str(r["status"]).lower() == "closed" and in_month(str(r["due_date"]))]

    lines: list[str] = []
    lines.append("# Monthly Continuous Monitoring Status Report (Fictional)")
    lines.append("")
    lines.append(f"**System/Scope:** {report_system_label}  ")
    lines.append(f"**Reporting period:** {start.isoformat()} to {(end - dt.timedelta(days=1)).isoformat()}  ")
    lines.append(f"**Report generated:** {today.isoformat()}  ")
    lines.append("")
    lines.append("## Executive summary")
    lines.append(f"- Open items: {len(open_items)}")
    lines.append(f"- Overdue items: {len(overdue)}")
    if severity_counts:
        lines.append("- Open severity mix: " + ", ".join([f"{k}={v}" for k,v in severity_counts.most_common()]))
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append("### By status")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    # Deterministic-ish ordering
    for st in STATUS_ORDER:
        if st in status_counts:
            lines.append(f"| {st} | {status_counts[st]} |")
    for st in sorted([k for k in status_counts.keys() if k not in STATUS_ORDER]):
        lines.append(f"| {st} | {status_counts[st]} |")

    lines.append("")
    lines.append("### Open items by severity")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---:|")
    for sev in SEVERITY_ORDER:
        if sev in severity_counts:
            lines.append(f"| {sev} | {severity_counts[sev]} |")
    for sev in sorted([k for k in severity_counts.keys() if k not in SEVERITY_ORDER]):
        lines.append(f"| {sev} | {severity_counts[sev]} |")

    lines.append("")
    lines.append("## Top overdue / high-risk items")
    lines.append("")
    if overdue_sorted:
        lines.append("| POA&M | Finding | Severity | Risk | Days overdue | Owner | Due date | Evidence |")
        lines.append("|---|---|---|---:|---:|---|---|---|")
        for r in overdue_sorted:
            ev = _first_evidence_path(str(r.get("evidence_paths","")))
            ev_cell = ""
            if ev:
                try:
                    ev_cell = _evidence_markdown_link(repo_root, out_md.parent, ev)
                except Exception:
                    # fallback to raw path if rel-link generation fails
                    ev_cell = ev
            lines.append(
                f"| {r['poam_id']} | {r['finding_id']} | {r['severity']} | {r['risk_score']} | "
                f"{r['days_overdue']} | {r['owner']} | {r['due_date']} | {ev_cell} |"
            )
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
    lines.append("## Newly closed this period (demo approximation)")
    lines.append("")
    if newly_closed:
        lines.append("| Finding | Severity | Owner | Due date (used as close proxy) |")
        lines.append("|---|---|---|---|")
        for r in newly_closed:
            lines.append(f"| {r['finding_id']} | {r['severity']} | {r['owner']} | {r['due_date']} |")
    else:
        lines.append("_No closures recorded for this period (or close dates not tracked in this simplified demo)._")

    lines.append("")
    lines.append("## Notes / constraints")
    lines.append("- This is a public demonstration dataset; some fields are simplified.")
    lines.append("- A production tracker would include a close_date field and an append-only audit trail of status changes.")
    lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    today_default = dt.date.today()

    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True, help="Input findings CSV")
    p.add_argument("--out", dest="out", required=True, help="Output directory")
    p.add_argument("--month", dest="month", default=f"{today_default.year:04d}-{today_default.month:02d}", help="Reporting month YYYY-MM (default: current month)")
    p.add_argument("--today", dest="today", default=today_default.isoformat(), help="Override 'today' for deterministic output (YYYY-MM-DD)")
    p.add_argument("--system-label", dest="system_label", default="Kitsune LAN (fictional)", help="System/scope label for the report header")
    args = p.parse_args()

    today = parse_date(args.today)
    inp = Path(args.inp)
    out_dir = Path(args.out)

    repo_root = Path(__file__).resolve().parents[1]

    rows = load_rows(inp)
    poam = write_poam_export(rows, out_dir / "poam_export.csv", today)
    write_monthly_report(poam, out_dir / "monthly_status_report.md", args.month, today, args.system_label, repo_root)

    print(f"Wrote: {out_dir/'poam_export.csv'}")
    print(f"Wrote: {out_dir/'monthly_status_report.md'}")


if __name__ == "__main__":
    main()
