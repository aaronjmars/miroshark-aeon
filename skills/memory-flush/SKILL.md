---
name: Memory Flush
description: Promote important recent log entries into MEMORY.md
var: ""
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
5. **Update the "Last consolidated" date** at the top of MEMORY.md to today (`${today}`). Do this even if nothing else was promoted.
6. Do NOT rewrite the whole file — make targeted additions, removals, and date updates.
7. Log what you promoted (or "MEMORY_FLUSH_OK: no new entries, date updated") to memory/logs/${today}.md.
