#!/usr/bin/env python3
"""Validate the company files before the workflow commits them. Standard library only.

Checks: required files exist, the backlog table is well-formed (unique IDs, known statuses and
owners), journal entries are dated and newest-first, and nothing that looks like a secret has been
written anywhere in the repo. Exits 1 and names the file on any problem.

Usage: python3 scripts/check.py [--root PATH]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = ["CLAUDE.md", "company/STRATEGY.md", "company/BACKLOG.md", "company/JOURNAL.md",
            "company/DECISIONS.md", ".claude/agents/ceo.md", ".claude/skills/daily-standup/SKILL.md"]
STATUS_RE = re.compile(r"^(READY|DOING|DONE|NEEDS-OWNER|BLOCKED(:.*)?)$")
ID_RE = re.compile(r"^T-\d{3,}$")
ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})(?: (\d{2}:\d{2}))?(?: UTC)? — \S+")
SECRET_RE = re.compile("|".join([
    r"ghp_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{40,}", r"sk-ant-[A-Za-z0-9_\-]{20,}",
    r"sk-[A-Za-z0-9]{40,}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"AKIA[0-9A-Z]{16}",
    r"xox[bpas]-[A-Za-z0-9-]{10,}",
]))
TEXT_EXT = {".md", ".txt", ".json", ".yml", ".yaml", ".csv", ".html", ".py", ".sh", ".toml"}


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and not re.match(r"^\|[\s\-:|]+\|$", s):
            rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows[1:]  # drop the header row


def check_backlog(text: str) -> list[str]:
    owners_line = next((ln for ln in text.splitlines() if ln.startswith("Owners:")), "")
    owners = set(re.findall(r"`([a-z][a-z0-9-]*)`", owners_line)) or {"owner", "ceo"}
    problems, seen = [], set()
    rows = table_rows(text)
    if not rows:
        problems.append("company/BACKLOG.md: no task rows found in the table")
    for r in rows:
        if len(r) < 5:
            problems.append(f"company/BACKLOG.md: row has {len(r)} columns, expected 5: {' | '.join(r)[:80]}")
            continue
        tid, status, owner = r[0], r[1], r[2]
        if not ID_RE.match(tid):
            problems.append(f"company/BACKLOG.md: bad task ID {tid!r} (use T-001, T-002, ...)")
        if tid in seen:
            problems.append(f"company/BACKLOG.md: duplicate task ID {tid}")
        seen.add(tid)
        if not STATUS_RE.match(status):
            problems.append(f"company/BACKLOG.md: {tid} has unknown status {status!r}")
        if owner not in owners:
            problems.append(f"company/BACKLOG.md: {tid} has unknown owner {owner!r} (known: {', '.join(sorted(owners))})")
        if not r[3] or not r[4]:
            problems.append(f"company/BACKLOG.md: {tid} needs both a task and acceptance criteria")
    return problems


def check_journal(text: str) -> list[str]:
    problems, stamps = [], []
    for line in text.splitlines():
        if line.startswith("## "):
            m = ENTRY_RE.match(line)
            if not m:
                problems.append(f"company/JOURNAL.md: heading not in the form '## YYYY-MM-DD HH:MM UTC — role': {line[:70]}")
                continue
            stamps.append((m.group(1), m.group(2) or ""))
    for above, below in zip(stamps, stamps[1:]):
        # compare times only when both entries have one
        a, b = (above, below) if above[1] and below[1] else (above[:1], below[:1])
        if a < b:
            problems.append(f"company/JOURNAL.md: newest entry must be on top, but {' '.join(below).strip()} "
                            f"sits below the older {' '.join(above).strip()}")
            break
    return problems


def check_secrets(root: Path) -> list[str]:
    problems = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in TEXT_EXT and ".git" not in p.parts and p.name != "check.py":
            if SECRET_RE.search(p.read_text(errors="ignore")):
                problems.append(f"{p.relative_to(root).as_posix()}: looks like it contains a secret")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path)
    root = ap.parse_args().root
    problems = [f"{rel}: missing" for rel in REQUIRED if not (root / rel).is_file()]
    if (root / "company/BACKLOG.md").is_file():
        problems += check_backlog((root / "company/BACKLOG.md").read_text(encoding="utf-8"))
    if (root / "company/JOURNAL.md").is_file():
        problems += check_journal((root / "company/JOURNAL.md").read_text(encoding="utf-8"))
    problems += check_secrets(root)
    if problems:
        print("check: FAILED")
        for pr in problems:
            print(" -", pr)
        return 1
    print("check: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
