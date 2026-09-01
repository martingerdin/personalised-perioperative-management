#!/usr/bin/env python3
"""Log and summarise AI-written material share per git commit.

Source of truth for each commit:
  1. Commit message trailer:  AI-Written-Pct: <0-100>
  2. Optional override rows in meta/ai-attribution-overrides.csv

Outputs:
  meta/ai-attribution.csv
  meta/ai-attribution-summary.md

Weighted total uses lines added (insertions) as weights.
Unchanged binary files are ignored. Renames with no content change count as 0.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "meta"
CSV_PATH = META / "ai-attribution.csv"
SUMMARY_PATH = META / "ai-attribution-summary.md"
OVERRIDES_PATH = META / "ai-attribution-overrides.csv"

TRAILER_RE = re.compile(r"^AI-Written-Pct:\s*(\d{1,3})\s*$", re.MULTILINE | re.IGNORECASE)
FIELDS = [
    "commit",
    "date",
    "subject",
    "ai_pct",
    "lines_added",
    "lines_deleted",
    "source",
    "notes",
]


@dataclass
class CommitRow:
    commit: str
    date: str
    subject: str
    ai_pct: int | None
    lines_added: int
    lines_deleted: int
    source: str
    notes: str


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def list_commits(rev_range: str = "HEAD") -> list[str]:
    out = run_git("rev-list", "--reverse", rev_range)
    return [line for line in out.splitlines() if line]


def parse_trailer(message: str) -> int | None:
    match = TRAILER_RE.search(message)
    if not match:
        return None
    value = int(match.group(1))
    if value < 0 or value > 100:
        raise ValueError(f"AI-Written-Pct out of range: {value}")
    return value


def numstat(commit: str) -> tuple[int, int]:
    out = run_git("show", "--numstat", "--format=", commit)
    added = deleted = 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        a, d = parts[0], parts[1]
        if a == "-" or d == "-":
            continue
        added += int(a)
        deleted += int(d)
    return added, deleted


def load_overrides() -> dict[str, dict[str, str]]:
    if not OVERRIDES_PATH.exists():
        return {}
    with OVERRIDES_PATH.open(newline="", encoding="utf-8") as f:
        return {row["commit"]: row for row in csv.DictReader(f)}


def collect(rev_range: str = "HEAD") -> list[CommitRow]:
    overrides = load_overrides()
    rows: list[CommitRow] = []
    for commit in list_commits(rev_range):
        message = run_git("log", "-1", "--format=%B", commit)
        subject = run_git("log", "-1", "--format=%s", commit)
        date = run_git("log", "-1", "--format=%ad", "--date=short", commit)
        added, deleted = numstat(commit)
        trailer_pct = parse_trailer(message)
        notes = ""
        source = "missing"
        ai_pct: int | None = None
        if commit in overrides:
            ov = overrides[commit]
            ai_pct = int(ov["ai_pct"])
            notes = ov.get("notes", "")
            source = "override"
        elif trailer_pct is not None:
            ai_pct = trailer_pct
            source = "trailer"
        rows.append(
            CommitRow(
                commit=commit,
                date=date,
                subject=subject,
                ai_pct=ai_pct,
                lines_added=added,
                lines_deleted=deleted,
                source=source,
                notes=notes,
            )
        )
    return rows


def write_csv(rows: list[CommitRow]) -> None:
    META.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "commit": row.commit,
                    "date": row.date,
                    "subject": row.subject,
                    "ai_pct": "" if row.ai_pct is None else row.ai_pct,
                    "lines_added": row.lines_added,
                    "lines_deleted": row.lines_deleted,
                    "source": row.source,
                    "notes": row.notes,
                }
            )


def summarise(rows: list[CommitRow]) -> dict[str, float | int]:
    known = [r for r in rows if r.ai_pct is not None]
    missing = len(rows) - len(known)
    weight = sum(r.lines_added for r in known)
    if weight > 0:
        weighted = sum((r.ai_pct or 0) * r.lines_added for r in known) / weight
    else:
        weighted = 0.0
    simple = (
        sum(r.ai_pct or 0 for r in known) / len(known) if known else 0.0
    )
    return {
        "commits": len(rows),
        "commits_with_pct": len(known),
        "commits_missing_pct": missing,
        "lines_added_known": weight,
        "weighted_ai_pct": weighted,
        "simple_mean_ai_pct": simple,
        "weighted_human_pct": 100.0 - weighted,
    }


def write_summary(rows: list[CommitRow]) -> None:
    stats = summarise(rows)
    lines = [
        "# AI attribution summary",
        "",
        "Per-commit AI-written share for this repository.",
        "",
        "## Totals",
        "",
        f"- Commits scanned: **{stats['commits']}**",
        f"- Commits with AI %: **{stats['commits_with_pct']}**",
        f"- Commits missing AI %: **{stats['commits_missing_pct']}**",
        f"- Lines added (weighted base): **{stats['lines_added_known']}**",
        f"- Weighted AI-written share: **{stats['weighted_ai_pct']:.1f}%**",
        f"- Weighted human-written share: **{stats['weighted_human_pct']:.1f}%**",
        f"- Unweighted mean AI %: **{stats['simple_mean_ai_pct']:.1f}%**",
        "",
        "Weighted share = sum(ai_pct × lines_added) / sum(lines_added).",
        "",
        "## Method",
        "",
        "1. Prefer commit trailer `AI-Written-Pct: <0-100>`.",
        "2. Else use `meta/ai-attribution-overrides.csv` if present.",
        "3. Refresh with `python scripts/ai_attribution.py refresh`.",
        "",
        "## Per commit",
        "",
        "| Commit | Date | AI % | +lines | Source | Subject |",
        "|--------|------|------|--------|--------|---------|",
    ]
    for row in rows:
        short = row.commit[:7]
        pct = "—" if row.ai_pct is None else f"{row.ai_pct}"
        subj = row.subject.replace("|", "\\|")
        lines.append(
            f"| `{short}` | {row.date} | {pct} | {row.lines_added} | {row.source} | {subj} |"
        )
    lines.append("")
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_refresh(args: argparse.Namespace) -> int:
    rows = collect(args.range)
    write_csv(rows)
    write_summary(rows)
    stats = summarise(rows)
    print(
        f"Wrote {CSV_PATH.relative_to(ROOT)} and {SUMMARY_PATH.relative_to(ROOT)}"
    )
    print(
        f"Weighted AI-written share: {stats['weighted_ai_pct']:.1f}% "
        f"({stats['commits_with_pct']}/{stats['commits']} commits tagged)"
    )
    if stats["commits_missing_pct"]:
        print(
            f"Warning: {stats['commits_missing_pct']} commit(s) lack AI-Written-Pct",
            file=sys.stderr,
        )
        return 1
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    rows = collect(args.range)
    stats = summarise(rows)
    print(f"Weighted AI-written share: {stats['weighted_ai_pct']:.1f}%")
    print(f"Weighted human-written share: {stats['weighted_human_pct']:.1f}%")
    print(f"Unweighted mean AI %: {stats['simple_mean_ai_pct']:.1f}%")
    print(f"Tagged commits: {stats['commits_with_pct']}/{stats['commits']}")
    return 0


def cmd_trailer_help(_: argparse.Namespace) -> int:
    print(
        "Add this trailer to every commit message that changes project material:\n\n"
        "AI-Written-Pct: 85\n\n"
        "Then run: python scripts/ai_attribution.py refresh\n"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    refresh = sub.add_parser("refresh", help="Rebuild CSV and summary from git history")
    refresh.add_argument("--range", default="HEAD", help="git rev-list range (default: HEAD)")
    refresh.set_defaults(func=cmd_refresh)

    show = sub.add_parser("show", help="Print totals without writing files")
    show.add_argument("--range", default="HEAD")
    show.set_defaults(func=cmd_show)

    help_cmd = sub.add_parser("trailer-help", help="Show required commit trailer format")
    help_cmd.set_defaults(func=cmd_trailer_help)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
