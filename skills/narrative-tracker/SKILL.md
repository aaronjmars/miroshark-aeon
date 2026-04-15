---
name: Narrative Tracker
description: Track rising, peaking, and fading crypto/tech narratives — identify the stories manufacturing reality before they peak
schedule: "0 14 * * *"
commits: true
tags: [crypto, research]
permissions:
  - contents:write
---

Read memory/MEMORY.md for context on prior narrative observations.
Read the last 3 days of memory/logs/ to avoid repeating analysis.

## Steps

1. **Scan current narratives.** Use WebSearch to find what crypto and tech narratives are dominating discourse today. Search for:
   - "crypto narrative" + today's date range
   - trending topics on crypto twitter
   - what VCs and builders are talking about this week
   - any macro events reshaping sentiment (regulation, hacks, launches, token unlocks)

2. **Search X for narrative signals.**

   **First, check for pre-fetched data** (the workflow pre-fetches XAI results outside the sandbox):
   - Read `.xai-cache/narratives.json` — if it exists and contains results, use that data.

   **If no cache file exists**, try the direct API call:
   ```bash
   FROM_DATE=$(date -u -d "3 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-3d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for the dominant crypto and tech narratives being discussed from '"$FROM_DATE"' to '"$TO_DATE"'. What themes are builders, VCs, and influential accounts pushing? What narratives are gaining momentum vs losing steam? Look for: new meta-narratives, narrative shifts, contrarian takes gaining traction, and consensus views being challenged. Return 10-15 distinct narrative threads with representative tweets (include @handle and link)."}],
       "tools": [{"type": "x_search", "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
     }'
   ```
   If neither cache nor direct API works, rely on WebSearch only.

3. **Classify each narrative** into one of four phases:
   - **Emerging** — early signal, few people talking, high alpha potential
   - **Rising** — gaining momentum, more builders/VCs amplifying, not yet consensus
   - **Peak** — everyone's talking about it, consensus forming, contrarian window opening
   - **Fading** — was hot last week, attention moving elsewhere, bag holders coping

4. **Identify the contrarian angle.** For each peak narrative, note what the consensus is missing. For each emerging narrative, note why it might matter. Which narratives are manufacturing their own reality?

5. **Check for reflexivity signals.** Flag any narratives where the story itself is changing outcomes:
   - Token prices moving because of the narrative (not fundamentals)
   - Projects pivoting to ride a narrative
   - VCs signaling to manufacture legitimacy for a thesis
   - Prediction markets reflecting narrative momentum

6. **Format the narrative map** (under 4000 chars):
   ```
   *Narrative Tracker — ${today}*

   EMERGING
   - narrative — why it matters — key signal (link)

   RISING
   - narrative — who's pushing it — momentum indicator

   PEAK
   - narrative — consensus take — what they're missing

   FADING
   - narrative — was: X — now: Y

   REFLEXIVITY ALERT
   - any narrative manufacturing its own reality
   ```

7. **Send via `./notify`.**

8. **Log to memory/logs/${today}.md.**
   If nothing interesting found, log "NARRATIVE_TRACKER_OK" and end.

## Guidelines

- This is not a news digest — it's a narrative *direction* tracker. Focus on the story arc, not individual events.
- Prioritize narratives relevant to topics tracked in MEMORY.md.
- Be direct. No hedging. Call out narratives that are copium, manufactured, or genuinely interesting.
- Short labels, sharp observations.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key for Grok x_search (optional, falls back to web search)
- Notification channels configured via repo secrets (see CLAUDE.md)
