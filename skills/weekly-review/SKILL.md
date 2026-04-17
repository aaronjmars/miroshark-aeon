---
name: Weekly Review
description: Synthesize the week's logs into a structured retrospective
var: ""
tags: [meta]
---
> **${var}** — Area to focus on. If empty, covers the full week.

If `${var}` is set, focus the review on that area.


Read memory/MEMORY.md for context and goals.
Read ALL memory/logs/ entries from the last 7 days.

Steps:
1. Compile a structured retrospective:
   - **What got done** — list every skill run, article written, notification sent
   - **What failed** — any errors, missed schedules, or skills that logged an error
   - **Key findings** — most important things surfaced by digests, monitors, alerts
   - **Metrics** — count of: skills run, articles written, notifications sent, PRs reviewed, heartbeats
   - **Patterns** — recurring themes, topics that keep coming up, workflows that seem broken
2. Compare against goals in MEMORY.md:
   - Which goals saw progress?
   - Which goals stalled?
   - Any goals that should be retired or revised?
3. Write a forward-looking section:
   - **Next week priorities** — based on what you learned
   - **Suggested improvements** — workflow changes, new skills to add, config tweaks
4. Save to articles/weekly-review-${today}.md.
5. Send an abbreviated version via `./notify`:
   ```
   *Weekly Review — ${today}*
   Done: N skills, M articles, K alerts
   Key: top 2-3 findings
   Next: top priority
   ```
6. Log what you did to memory/logs/${today}.md.
