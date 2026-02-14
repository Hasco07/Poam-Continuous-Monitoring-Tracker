#!/usr/bin/env python3
"""Repo sanity checks for the POA&M + Continuous Monitoring Tracker.

This is meant to be readable and boring (in a good way).

Checks:
- Internal markdown links resolve (no 404s inside the repo)
- evidence_paths in the sample dataset point to real files
- The export generator runs and produces outputs

Run:
  python tools/check_repo.py
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil


RE_MD_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def iter_markdown_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if ".venv" not in p.parts and "__pycache__" not in p.parts]


def check_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    md_files = iter_markdown_files(root)

    for md in md_files:
        text = md.read_text(encoding="utf-8", errors="ignore")
        for raw_target in RE_MD_LINK.findall(text):
            target = raw_target.strip()

            # skip external links
            if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:"):
                continue

            # remove anchors
            target = target.split("#", 1)[0].strip()
            if not target:
                continue

            # GitHub also supports query params in links; strip them
            target = target.split("?", 1)[0].strip()
            if not target:
                continue

            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"BROKEN LINK: {md.relative_to(root)} -> {raw_target} (resolved to {resolved.relative_to(root) if resolved.is_absolute() else resolved})")
    return errors


def check_evidence_paths_csv(root: Path, csv_path: Path, column: str = "evidence_paths") -> list[str]:
    errors: list[str] = []
    if not csv_path.exists():
        return [f"MISSING CSV: {csv_path.relative_to(root)}"]

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or column not in reader.fieldnames:
            return [f"CSV missing required column '{column}': {csv_path.relative_to(root)}"]

        for row_idx, row in enumerate(reader, start=2):  # header is row 1
            raw = (row.get(column) or "").strip()
            if not raw:
                continue
            parts = [p.strip() for p in raw.split(";") if p.strip()]
            for part in parts:
                fp = (root / part)
                if not fp.exists():
                    errors.append(f"MISSING EVIDENCE: {csv_path.relative_to(root)} row {row_idx} -> {part}")
    return errors


def check_generator(root: Path) -> list[str]:
    errors: list[str] = []
    gen = root / "tools" / "generate_exports.py"
    sample = root / "sample-data" / "findings.sample.csv"
    if not gen.exists():
        return ["Missing tools/generate_exports.py"]
    if not sample.exists():
        return ["Missing sample-data/findings.sample.csv"]

    tmp_dir = root / ".tmp_exports_check"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, str(gen), "--in", str(sample), "--out", str(tmp_dir), "--month", "2026-02", "--today", "2026-02-13"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        errors.append("Generator failed:\n" + p.stderr.strip())
        return errors

    poam = tmp_dir / "poam_export.csv"
    report = tmp_dir / "monthly_status_report.md"
    if not poam.exists():
        errors.append("Generator did not produce poam_export.csv")
    if not report.exists():
        errors.append("Generator did not produce monthly_status_report.md")

    # quick content sanity checks
    if poam.exists():
        with poam.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if len(rows) < 5:
                errors.append(f"poam_export.csv seems too small ({len(rows)} rows)")
            required_cols = {"poam_id","finding_id","severity","risk_score","status","owner","due_date","days_overdue","evidence_paths"}
            if reader.fieldnames is None or not required_cols.issubset(set(reader.fieldnames)):
                errors.append("poam_export.csv missing expected columns")

    # cleanup
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return errors


def main() -> int:
    root = repo_root()
    all_errors: list[str] = []

    all_errors += check_markdown_links(root)
    all_errors += check_evidence_paths_csv(root, root / "sample-data" / "findings.sample.csv")
    all_errors += check_evidence_paths_csv(root, root / "exports" / "poam_export.sample.csv")
    all_errors += check_generator(root)

    if all_errors:
        print("\n".join(all_errors))
        print(f"\nFAILED: {len(all_errors)} issue(s) found.")
        return 1

    print("OK: repo link + evidence checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
