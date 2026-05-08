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
4. **Rotate old entries to keep MEMORY.md compact:**
   - Skills Built table: keep the **10 most recent rows** — remove older rows from the top
   - Recent Articles table: keep the **8 most recent rows** — remove older rows from the top
   - Recent Digests table: keep the **6 most recent rows** — remove older rows from the top
5. **Enforce per-row character caps** so MEMORY.md stays readable in one Read call (Read tool fails over ~25K tokens; the index serves no purpose if no skill can load it):
   - Skills Built `Notes` column: **≤280 chars** — one tweet-length sentence covering what shipped + key file/PR. Detail belongs in the daily log entry that's still on disk.
   - Recent Articles `Notes` column: **≤220 chars** — angle in one sentence + word count. Full article body lives at `articles/<skill>-YYYY-MM-DD.md`.
   - Recent Digests `Key Topics` column: **≤180 chars** — already short by convention; just guard against drift.
   - When writing a new row OR finding an oversized existing row, condense to fit. If a row truly needs more space, move the detail to `memory/topics/<topic>.md` and replace the row body with a one-line summary + `→ topics/<topic>.md` pointer.
   - **Sanity check after every flush:** `wc -c memory/MEMORY.md` should print under ~25000 (≈25KB). If it exceeds, immediately re-tighten the longest rows or push detail into topic files. Log the byte count under your flush entry.
6. **Update the "Last consolidated" date** at the top of MEMORY.md to today (`${today}`). Do this even if nothing else was promoted.
7. Do NOT rewrite the whole file — make targeted additions, removals, condensations, and date updates.
8. Log what you promoted (or "MEMORY_FLUSH_OK: no new entries, date updated") to memory/logs/${today}.md, including the post-flush `wc -c memory/MEMORY.md` byte count.
