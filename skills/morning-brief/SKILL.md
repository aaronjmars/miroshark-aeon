---
name: Morning Brief
description: Aggregated daily briefing — digests, priorities, and what's ahead
var: ""
tags: [meta]
---
> **${var}** — Area to emphasize. If empty, covers all areas.

If `${var}` is set, emphasize that area in the briefing.


Read memory/MEMORY.md for goals, priorities, and tracked items.
Read yesterday's and today's memory/logs/ entries.

Steps:
1. Gather inputs:
   - **Priorities**: top 3 items from MEMORY.md "Next Priorities"
   - **Yesterday's activity**: summarize what Aeon did yesterday from logs
   - **Pending items**: any stalled PRs, unresolved alerts, or open issues from recent logs
   - **Scheduled today**: check aeon.yml for what skills run today
2. Check for quick headlines:
   - Use WebSearch for 2-3 top headlines in AI and crypto
   - Keep headlines to one line each
3. Format and send via `./notify`:
   ```
   *Morning Brief — ${today}*

   *Priorities*
   1. priority one
   2. priority two
   3. priority three

   *Yesterday*
   - what happened

   *Pending*
   - items needing attention

   *Headlines*
   - headline 1
   - headline 2

   *Today's schedule*
   - skill at time
   ```
4. Log to memory/logs/${today}.md.
