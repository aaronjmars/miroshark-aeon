---
name: Evening Recap
description: End-of-day operational summary — what Aeon shipped, what failed, what needs follow-up
var: ""
tags: [meta]
---
> **${var}** — Optional date override (YYYY-MM-DD). If empty, recaps today.

Read memory/MEMORY.md for context and open issues.

## Steps

1. **Determine the date.**
   ```bash
   TODAY=${var:-$(date -u +%Y-%m-%d)}
   ```

2. **Read today's activity log.**
   Read `memory/logs/${TODAY}.md`. If it doesn't exist, log "No activity log for ${TODAY}" and exit.

3. **Extract key metrics from the log.** Count and collect:
   - Skills that ran (every `## ` header is one skill run)
   - Content produced: articles written, tweet drafts, explainers, ideas
   - Issues filed or resolved (check for ISS- references)
   - Failures or errors (look for "failed", "blocked", "error", "timeout", "zero output")
   - Anything flagged as needing follow-up

4. **Check open issues** from `memory/issues/INDEX.md` — note any that appear in today's log.

5. **Write and send the recap notification** via `./notify`. Format:

   ```
   *Evening Recap — ${TODAY}*

   *What ran:* N skills

   *Shipped:*
   - [concrete output 1 — keep to one line]
   - [concrete output 2]
   ...

   *Issues:*
   - [any new issues filed, or "none"]

   *Blockers:*
   - [any failures or errors, or "clean"]

   *Follow-up:*
   - [anything flagged for attention, or "none"]
   ```

   Rules:
   - Keep under 2000 chars
   - Each bullet is one line — no sub-bullets
   - Skip sections that are empty (don't include "Follow-up: none" if there's nothing)
   - Lead with what actually shipped, not what was attempted

6. **Log to memory.**
   Append to `memory/logs/${TODAY}.md`:
   ```
   ## Evening Recap
   - Recap sent for ${TODAY}: N skills, M outputs, K issues
   ```

## Sandbox note

`./notify` uses `.pending-notify/` fallback — recap delivery is reliable even if curl is blocked.
