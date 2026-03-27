---
name: Heartbeat
description: Proactive ambient check — surface anything worth attention
var: ""
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
  - Also check `gh run list --workflow=aeon.yml --created=$(date -u +%Y-%m-%d) --json displayTitle,status` — if the skill is currently `in_progress` or `queued`, don't flag it.
  - For day-of-week schedules (e.g. `0 20 * * 0` for Sundays), only check on the matching day.

Before sending any notification, grep the last 48h of logs for the same issue. If the same missing-skill or stalled-PR was already reported, skip it. Batch all findings into a single notification.

If nothing needs attention, log "HEARTBEAT_OK" and end your response.

If something needs attention:
1. Send a concise notification via `./notify`
2. Log the finding and action taken to memory/logs/${today}.md
