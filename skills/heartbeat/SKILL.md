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
- [ ] Scan aeon.yml for scheduled skills — cross-reference with recent logs to find any that haven't run when expected. **Important:** GitHub Actions cron has ±10 minute jitter and skills may take 5-15 minutes to complete and commit logs. Only flag a skill as missing if it was expected to run **more than 2 hours ago** and has no log entry for today. Also check `gh run list --workflow=aeon.yml --created=$(date -u +%Y-%m-%d) --json displayTitle,status` to see if the skill is currently running or queued before flagging it as missing.
  **Scheduler diagnostics:** Skills are dispatched by the scheduler job in `messages.yml` (not by cron triggers in `aeon.yml` directly). If multiple skills are missing, check the scheduler first:
  - Run `gh run list --workflow=messages.yml --created=$(date -u +%Y-%m-%d) --json event,status,conclusion --jq '[.[] | select(.event=="schedule")]'` to see if scheduled runs are firing.
  - If zero scheduled runs appear for today, the root cause is likely that the `messages.yml` scheduler isn't triggering (GitHub may have disabled the cron — check if the workflow needs re-enabling via the Actions tab).
  - If scheduled runs exist but skills still didn't run, check the scheduler logs for dispatch errors.
  **Log header aliases:** Some skills log under a different header than their aeon.yml name. Known aliases:
  - `monitor-polymarket` → may log as `## Polymarket Comments`
  - `hacker-news-digest` / `hn-digest` → may log as `## HN Digest`
  When checking if a skill ran, match against both the skill name AND its known aliases.

Before sending any notification, grep memory/logs/ for the same item. If it appears in the last 48h of logs, skip it. Never notify about the same item twice. Batch missing-skill alerts into a single notification — don't send one per skill.

If nothing needs attention, log "HEARTBEAT_OK" and end your response.

If something needs attention:
1. Send a concise notification via `./notify`
2. Log the finding and action taken to memory/logs/${today}.md
