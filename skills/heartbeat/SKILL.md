---
name: Heartbeat
description: Proactive ambient check — surface anything worth attention
var: ""
tags: [meta]
---
> **${var}** — Area to focus on. If empty, runs all checks.

If `${var}` is set, focus checks on that specific area.


Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.

## Step 0: Compute today's day-of-week from the shell — do not infer it

Before checking any schedules, run:

```bash
date -u +%A          # full name, e.g. "Wednesday"
date -u +%u          # numeric, 1=Mon … 7=Sun
date -u +%d          # day-of-month, e.g. "30"
```

Use the **shell-computed** day-of-week as the source of truth in every "is this skill scheduled today?" comparison below. **Do not infer the day-of-week from `${today}` or the YYYY-MM-DD date** — past heartbeat runs have hallucinated the wrong weekday from the date (Apr 29 2026 was logged as "Tuesday" when it was actually Wednesday, which then mis-classified `memory-flush`'s on-schedule Wed run as "off-schedule" because the skill thought Wed wasn't a memory-flush day). The shell value is deterministic; the inferred value is not.

Anchor the heartbeat report header on the shell output: `Date: <%A> <Mon DD>, <YYYY> — <HH:MM> UTC`.

Translate cron expressions before checking schedules:
- Weekday (`0 N * * D`) — `D` is `0=Sun, 1=Mon, …, 6=Sat`. Compare against `date -u +%u` (which is `1=Mon … 7=Sun` — Sunday differs).
- Every-other-day (`0 N */2 * *`) — when in doubt, ground-truth against the last 7 days of `cron-state.json` `last_dispatch` timestamps for that skill. Do **not** assume which parity (odd / even days-of-month) the cron resolves to without checking.

## Checks

Check the following:
- [ ] Any open PRs stalled > 24h? (use `gh pr list` to check)
- [ ] Anything flagged in memory that needs follow-up?
- [ ] Check recent GitHub issues for anything labeled urgent (use `gh issue list`)
- [ ] Scan aeon.yml for enabled scheduled skills — cross-reference with today's log (`memory/logs/${today}.md`) to find any that haven't run when expected.

  **Matching skill names to log entries:**
  Skills log under human-readable `## Headers`, not their aeon.yml kebab-case names. To check if a skill ran, do a **case-insensitive match against `## ` header lines only** — `grep -iE '^## …'`, not a free-text substring search of the full file. Header-only matching matters for short skill names: substring-searching the whole file for `feature` matches body text like "added a feature" in push-recap, falsely concluding the `feature` skill ran on a day it actually failed and masking the outage. Build the regex by replacing hyphens in the kebab-case name with `[ -]?` so both `## Feature Built` and `## Self-Improve` are accepted. Examples:
  - `token-report` → `^## token[ -]?report` (matches `## Token Report`, `## Token Report (Update)`)
  - `push-recap` → `^## push[ -]?recap` (matches `## Push Recap`, `## Push Recap (MiroShark)`)
  - `fetch-tweets` → `^## fetch[ -]?tweets` (matches `## Fetch Tweets — MIROSHARK`)
  - `feature` → `^## feature\b` (matches `## Feature Built — ...`, `## feature skill run` — and **does not** match the bare word "feature" inside other sections' body text)
  - `hyperstitions-ideas` → `^## hyperstitions` (matches `## Hyperstitions Ideas`)
  - `memory-flush` → `^## memory[ -]?flush`
  - `self-improve` → `^## (self[ -]?improve|agent self-improvement)` (matches `## Self-Improve — 2026-05-04`, `## Agent Self-Improvement`)
  - `repo-pulse` → `^## repo[ -]?pulse`
  - `repo-article` → `^## repo[ -]?article`
  - `repo-actions` → `^## repo[ -]?actions`
  - `project-lens` → `^## project[ -]?lens`
  - `tweet-allocator` → `^## tweet[ -]?allocator`
  - `weekly-shiplog` → `^## weekly[ -]?shiplog`
  - `skill-leaderboard` → `^## skill[ -]?leaderboard`

  **Timing rules (avoid false positives):**
  - GitHub Actions cron has ±10 min jitter and skills take 5-15 min to complete.
  - Only flag a skill as missing if its scheduled time was **more than 2 hours ago**.
  - Also check `gh run list --workflow=aeon.yml --created=$(date -u +%Y-%m-%d) --json displayTitle,status,createdAt` — if the skill is currently `in_progress` or `queued` **and was created less than 2 hours ago**, don't flag it.
  - **Stuck-run detection:** If a run has been `in_progress` for **more than 2 hours** (compare `createdAt` against current time), treat it as stuck. Flag it in the report as "stuck (in_progress > 2h)" and allow auto-trigger of a fresh run. Do NOT cancel the stuck run — just dispatch a new one alongside it.
  - For day-of-week schedules (e.g. `0 20 * * 0` for Sundays), only check on the matching day.

Before sending any notification, grep the last 48h of logs for the same issue. If the same missing-skill or stalled-PR was already reported, skip it. Batch all findings into a single notification.

If nothing needs attention, log "HEARTBEAT_OK" and end your response.

If something needs attention:
1. **Auto-trigger missing skills** — for each skill confirmed missing (not just stalled PRs or issues), dispatch it if not already running:

   **Dedup guard — check before dispatching:**
   Before firing `gh workflow run` for a skill, check whether a run for that skill is already `queued` or `in_progress` **and was started less than 2 hours ago**:
   ```bash
   gh run list --workflow=aeon.yml --json displayTitle,status,createdAt --jq \
     '.[] | select((.status == "queued" or .status == "in_progress") and ((now - (.createdAt | fromdateiso8601)) < 7200)) | .displayTitle'
   ```
   If the output contains the skill name (case-insensitive), **skip the dispatch** — the skill is already pending. Runs older than 2 hours are considered stuck and ignored by this guard (a fresh dispatch is allowed). Only dispatch skills that have no active-and-recent or queued run:
   ```bash
   gh workflow run aeon.yml -f skill="SKILL_NAME"
   ```
   Skip auto-trigger for: `heartbeat` itself, `memory-flush`, `self-improve`, `reflect`, `self-review` (meta/housekeeping skills). For all other confirmed-missing daily or weekly skills that pass the dedup check, dispatch them.

2. Send a concise notification via `./notify` listing what was flagged, what was auto-triggered, and what was skipped (already queued/in-progress).
3. Log the finding and action taken to memory/logs/${today}.md.
