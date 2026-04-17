---
name: Goal Tracker
description: Compare current progress against goals stored in MEMORY.md
var: ""
tags: [meta]
---
> **${var}** — Specific goal to track. If empty, tracks all goals in MEMORY.md.

If `${var}` is set, focus only on that specific goal.


Read memory/MEMORY.md — specifically the "Goals" or "Next Priorities" section.
Read the last 14 days of memory/logs/ for evidence of progress.

Steps:
1. For each goal in MEMORY.md:
   - Search recent logs for activity related to this goal
   - Assess status: **on track**, **stalled**, **completed**, or **blocked**
   - Note specific evidence (dates, log entries, files created)
2. Format a progress report:
   ```markdown
   # Goal Tracker — ${today}

   ## On Track
   - Goal: evidence of recent progress

   ## Stalled
   - Goal: last activity was DATE, possible reason

   ## Completed
   - Goal: completed on DATE

   ## Blocked
   - Goal: what's blocking it
   ```
3. Update MEMORY.md:
   - Move completed goals to a "Completed" section (with date)
   - Add notes on blocked goals
4. Send a summary via `./notify`.
5. Log what you did to memory/logs/${today}.md.
