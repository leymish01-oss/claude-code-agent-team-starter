# Claude Code Agent Team Starter

A CEO agent that runs your project's daily standup on GitHub Actions. Every morning it reads your
strategy, backlog and journal, decides what matters most today, re-orders the backlog and writes a
short journal entry. It commits the result to your repo, so you open GitHub and see the plan.

It's one agent, one skill and one workflow, and you can read all of it in ten minutes. It's the
planning core of the [Autonomous Company Kit](https://www.leymish.com/claude-code/), cut down so it works on
its own.

## What it does, concretely

```
06:00 (your cron)  GitHub Actions starts  →  Claude Code runs /daily-standup as the `ceo` agent
                   reads company/STRATEGY.md, BACKLOG.md, top of JOURNAL.md
                   writes: re-ordered BACKLOG.md, a JOURNAL.md entry, DECISIONS.md if strategy changed
                   scripts/check.py validates the files  →  commit "ceo: standup <date>"
```

A journal entry looks like this:

```markdown
## 2026-10-02 22:00 UTC — ceo
- Constraint: nobody has seen the landing page yet (0 visits logged in metrics/). Distribution beats polish.
- Moved T-004 (write the launch post) above T-002 (dark mode). Added T-006: submit to 2 directories.
- Blocked T-003 on the owner: needs a Stripe account (free, 10 min). Cheapest alternative: Gumroad.
- Next: owner ships T-004 today; I re-check the constraint tomorrow.
```

The agent plans; it doesn't build. You, or your own Claude Code session, pick up the top `READY` task.

## Setup (about 10 minutes)

1. **Use this template** (green button) or copy the files into an existing repo.
2. **Connect Claude.** In a terminal, run `claude setup-token` (works with a Claude Pro, Max or Team
   plan) and save the token as a repository secret named `CLAUDE_CODE_OAUTH_TOKEN`: Settings →
   Secrets and variables → Actions → New repository secret, or `gh secret set CLAUDE_CODE_OAUTH_TOKEN`.
   No GitHub App is needed; the workflow commits with its own token. Using an API key instead? Add
   the secret `ANTHROPIC_API_KEY` and change the one marked line in `.github/workflows/standup.yml`.
3. **Tell it about your project.** Edit `company/STRATEGY.md` (goal, current bet, the one metric) and
   put your real tasks in `company/BACKLOG.md`. Five honest lines beat a page of aspirations.
4. **Run it once.** Actions tab → *Daily standup* → *Run workflow*. After a couple of minutes you'll
   have a new commit with a journal entry.
5. **Set the time.** The cron in `standup.yml` is UTC. Change it to just before your morning.

Check your files locally at any time: `python3 scripts/check.py` (standard library only).

## Files

| Path | What it is |
|---|---|
| `CLAUDE.md` | The rules every run follows: read first, write down what you did, no invented numbers |
| `.claude/agents/ceo.md` | The CEO role: diagnose the constraint, pick 1–3 tasks, keep the backlog honest |
| `.claude/skills/daily-standup/SKILL.md` | The step-by-step routine the workflow triggers |
| `.claude/settings.json` | Permissions: the agent can edit files; it can't push, read `.env` or touch workflows |
| `.github/workflows/standup.yml` | The daily schedule, a validation step, and the commit |
| `company/` | Strategy, backlog, journal, decisions: the project's memory between runs |
| `scripts/check.py` | Fails the run if the backlog or journal is malformed or a secret slipped in |

## Cost

GitHub Actions minutes are free for public repos and cover this easily on the free plan for private
ones (a run takes 2–3 minutes). Claude usage counts against your plan or API key; one standup is a
short session with about 10–20 tool calls.

## Want the rest of the team?

This starter is one agent that plans. The [Autonomous Company Kit](https://www.leymish.com/claude-code/) is the
full system behind [LeyMish Labs](https://www.leymish.com), a small business that Claude Code
agents run in public, with the ledger and journal on the site:

| | Starter (free) | Full kit |
|---|---|---|
| CEO agent + daily standup | ✓ | ✓ |
| Builder that ships the top task, with a separate Verifier | | ✓ |
| Growth agent: articles and posts, auto-published to dev.to, Bluesky and your blog | | ✓ |
| Treasury: Gumroad sales sync, ledger, reserve policy | | ✓ |
| Weekly board review that opens a GitHub issue listing what needs you | | ✓ |
| Static site with live ledger and journal, deploy workflows | | ✓ |
| Guardrails against leaked secrets, hype and fake social proof | basic | full |
| Operator's guide, `init.py` setup, 3 starter variants | | ✓ |

## Licence

MIT, see `LICENSE`. Use it for anything.
