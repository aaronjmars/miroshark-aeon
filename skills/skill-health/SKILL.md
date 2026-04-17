---
name: Skill Health
description: Check which scheduled skills haven't run recently
var: ""
tags: [meta]
---
> **${var}** — Skill name to check. If empty, checks all scheduled skills.

If `${var}` is set, only check that specific skill.


Read aeon.yml for the full list of scheduled skills.
Read the last 7 days of memory/logs/ for evidence of skill runs.

Steps:
1. For each skill in aeon.yml that has a schedule:
   - Search recent logs for evidence it ran (look for the skill name or its outputs)
   - Calculate expected runs based on its cron schedule
   - Compare expected vs actual
2. Flag any skills that:
   - Haven't run in their expected window (e.g., daily skill missing > 1 day)
   - Logged errors on their last run
   - Logged an ack (OK) every time — might need more interesting inputs
3. Check for workflow-level issues:
   - Look at recent GitHub Actions runs: `gh run list --limit 20 --json status,conclusion,name,createdAt`
   - Flag any failed runs
4. Format a health report:
   ```
   *Skill Health — ${today}*

   OK: skill1, skill2, skill3
   MISSED: skill4 (last ran DATE)
   ERRORS: skill5 (error description)
   ```
5. Send via `./notify` if any skills are missed or erroring.
6. Log to memory/logs/${today}.md.
If all skills healthy, log "SKILL_HEALTH_OK" and end.
