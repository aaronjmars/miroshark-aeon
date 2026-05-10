---
name: Memory Flush
description: Promote important recent log entries into MEMORY.md
var: ""
tags: [meta]
---
> **${var}** — Topic to focus on. If empty, flushes all recent activity.

If `${var}` is set, only flush entries related to that topic.


Read memory/MEMORY.md for current memory state.
Read the last 3 days of memory/logs/ for recent activity.

Steps:
1. Scan recent logs for entries worth promoting to long-term memory:
   - New lessons learned (errors encountered, workarounds found)
   - Topics covered (articles, digests) — add to the recent articles/digests tables
   - Features built or tools created
   - Important findings from monitors (on-chain, GitHub, papers)
   - Ideas captured that are still relevant
   - Goals completed or progress milestones
2. Check each candidate against existing MEMORY.md content — skip if already recorded.
3. Update memory:
   - Add brief entries to MEMORY.md
   - If a topic needs more detail, write to `memory/topics/<topic>.md` instead
   - Update the Recent Digests table with any new token-report or push-recap entries from logs
4. **Rotate old entries to keep MEMORY.md under ~50 lines:**
   - Skills Built table: keep the **10 most recent rows** — remove older rows from the top
   - Recent Articles table: keep the **8 most recent rows** — remove older rows from the top
   - Recent Digests table: keep the **6 most recent rows** — remove older rows from the top
5. **Enforce per-row character caps.** MEMORY.md is loaded by every skill at task start, so a single sprawling row blows out the Read tool's 25K-token cap and breaks every skill's first read. Caps apply to each row body (the cells after the first):
   - Skills Built rows: ≤ **280 chars** per row body
   - Recent Articles rows: ≤ **220 chars** per row body
   - Recent Digests rows: ≤ **180 chars** per row body

   When promoting a new row, write a one-sentence summary plus the PR number / article-file pointer — the full implementation notes already live in `memory/logs/YYYY-MM-DD.md` and `articles/<skill>-YYYY-MM-DD.md`. If detail is worth preserving beyond the daily log, push it into `memory/topics/<topic>.md` and link from MEMORY.md — **never** by inlining a paragraph into a table row.

   When trimming a row that already exceeds its cap, condense to one sentence + the same pointers. Detail is not lost — daily logs and articles carry the original write-up verbatim.

   **Sanity check after editing:** run `wc -c memory/MEMORY.md` and confirm the file is **under 25 KB** (and ideally under 20 KB). If not, condense the longest rows further. Past incident: 2026-05-08 MEMORY.md grew to 76 KB / 31K+ tokens, blocking every skill's at-task-start read until self-improve cut it back.

6. **Update the "Last consolidated" date** at the top of MEMORY.md to today (`${today}`). Do this even if nothing else was promoted.
7. Do NOT rewrite the whole file when promoting / rotating — make targeted additions, removals, and date updates. (A full rewrite is acceptable as a one-shot recovery when condensing existing oversized rows under step 5, not as the steady-state flow.)
8. Log what you promoted (or "MEMORY_FLUSH_OK: no new entries, date updated") to memory/logs/${today}.md.
