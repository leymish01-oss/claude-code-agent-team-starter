---
name: daily-standup
description: The CEO's daily run. Review the state files, decide today's priorities, update the backlog and journal.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash
---
Act as the `ceo` agent defined in `.claude/agents/ceo.md`, following `CLAUDE.md`.

1. Read `company/STRATEGY.md`, `company/BACKLOG.md`, the top of `company/JOURNAL.md`,
   `company/DECISIONS.md` (latest three entries) and `metrics/` if it exists.
2. Note, for yourself, five lines: the goal, the one metric and its latest real value, the
   constraint, what changed since the last entry, and what the owner is waiting on.
3. Update `BACKLOG.md`: add or re-order tasks so each owner's first `READY` task is the most valuable
   one. Keep the table format and the status words exactly as the file defines them. Give every new
   task the next free ID.
4. Update `STRATEGY.md` and `DECISIONS.md` only if the evidence warrants it. Most days it doesn't.
5. Prepend a JOURNAL entry under the file's intro text:
   `## YYYY-MM-DD HH:MM UTC — ceo` (get the time with `date -u +'%F %H:%M'`) followed by 2–5 bullets:
   the constraint, what you changed and why, what's blocked on the owner, and what's next.
6. Run `python3 scripts/check.py` and fix anything it reports. Don't run git.
