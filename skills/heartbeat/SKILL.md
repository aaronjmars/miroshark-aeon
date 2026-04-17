---
name: Heartbeat
description: Proactive ambient check — surface anything worth attention
var: ""
tags: [meta]
---
> **${var}** — Area to focus on. If empty, runs all checks.

If `${var}` is set, focus checks on that specific area.


Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.

Check the following:
- [ ] Any open PRs stalled > 24h? (use `gh pr list` to check)
- [ ] Anything flagged in memory that needs follow-up?
- [ ] Check recent GitHub issues for anything labeled urgent (use `gh issue list`)
- [ ] Scan aeon.yml for enabled scheduled skills — cross-reference with today's log (`memory/logs/${today}.md`) to find any that haven't run when expected.

  **Matching skill names to log entries:**
  Skills log under human-readable `## Headers`, not their aeon.yml kebab-case names. To check if a skill ran, do a **case-insensitive search** of the log file for the skill name with hyphens replaced by spaces. Examples:
  - `token-report` → search for "token report" (matches `## Token Report`, `## Token Report (Update)`)
  - `push-recap` → search for "push recap" (matches `## Push Recap`, `## Push Recap (MiroShark)`)
  - `fetch-tweets` → search for "fetch tweets" (matches `## Fetch Tweets — MIROSHARK`)
  - `feature` → search for "feature" (matches `## Feature Build — ...`)
  - `hyperstitions-ideas` → search for "hyperstitions" (matches `## Hyperstitions Ideas`)
  - `memory-flush` → search for "memory flush"
  - `self-improve` → search for "self-improve" or "self improve" or "agent self-improvement"

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
