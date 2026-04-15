---
name: Regulatory Monitor
description: Track legislation, regulatory actions, and legal developments affecting prediction markets, crypto, and AI agents
var: ""
tags: [crypto, research]
---
> **${var}** — Specific regulatory topic to focus on (e.g. "prediction markets", "stablecoins", "AI agents"). If empty, scans all tracked domains.

If `${var}` is set, narrow the search to that specific regulatory area.

Read memory/MEMORY.md for context on current positions and interests.
Read the last 2 days of memory/logs/ to avoid repeating items.

## Steps

1. **Search for recent regulatory developments.** Use WebSearch to find legislation, enforcement actions, regulatory guidance, and legal developments from the last 7 days across these domains:

   **Primary domains** (always search):
   - Prediction markets — bills, CFTC actions, state-level bans, Polymarket/Kalshi regulatory status
   - Crypto/DeFi — SEC enforcement, stablecoin legislation, exchange regulations, token classification
   - AI agents — autonomous agent regulations, AI liability frameworks, AI governance bills

   **Secondary domains** (include if relevant hits):
   - Privacy/surveillance — financial surveillance laws, KYC/AML changes
   - Open source — software liability, AI open-source restrictions

   Run these searches (use the current year dynamically — `date +%Y`):
   ```
   WebSearch: "prediction market regulation OR legislation OR ban $(date +%Y)"
   WebSearch: "CFTC prediction market OR Polymarket OR Kalshi $(date +%Y)"
   WebSearch: "crypto regulation OR legislation OR SEC enforcement $(date +%Y)"
   WebSearch: "stablecoin bill OR regulation $(date +%Y)"
   WebSearch: "AI agent regulation OR autonomous agent legislation $(date +%Y)"
   ```

   If `${var}` is set, replace the above with 2-3 targeted searches for that specific topic.

2. **Filter and deduplicate.** From all results:
   - Keep only developments from the last 7 days
   - Deduplicate against recent logs — skip anything already reported
   - Discard opinion pieces and speculation — keep only actual legislative/regulatory actions, proposed bills, enforcement actions, court rulings, or official guidance
   - Flag anything that directly impacts prediction markets or coordination markets as HIGH PRIORITY

3. **Rank by impact.** Score each item on:
   - **Direct impact on tracked domains** — prediction market regulation > crypto regulation > AI regulation
   - **Stage of action** — enacted law > passed committee > introduced bill > proposed rule > leaked draft
   - **Jurisdiction weight** — US federal > EU > US state > UK > other G7 > rest of world
   - **Enforcement severity** — ban/shutdown > heavy restriction > licensing requirement > reporting requirement > guidance

4. **Enrich top items.** For the top 3-5 items:
   - Use WebFetch on the source URL for more detail
   - Identify: what exactly changed, who introduced/enacted it, what's the timeline, who's affected
   - Note any prediction market angles — does this create a tradeable event? does it affect existing markets?

5. **Format and send via `./notify`** (keep under 4000 chars):
   ```
   *Reg Monitor — ${today}*

   *HIGH PRIORITY*
   - [Bill/Action name](url) — jurisdiction
     what changed. who's affected. timeline.
     prediction market angle: [if applicable]

   *NOTABLE*
   - [Bill/Action name](url) — jurisdiction
     one-line summary. stage: [introduced/committee/passed/enacted]

   *WATCH LIST*
   - brief mention of developing stories not yet actionable

   ${count} regulatory developments tracked
   ```

6. **Log to memory/logs/${today}.md.** Record which items were included and their current stage.

   If nothing found, log "REG_MONITOR_OK" and end.

## What Counts as a Regulatory Development

Include:
- Bills introduced or advancing in any legislature
- Regulatory agency actions (CFTC, SEC, ESMA, FCA, etc.)
- Enforcement actions, fines, cease-and-desist orders
- Court rulings affecting crypto, prediction markets, or AI
- Official regulatory guidance or frameworks published
- International regulatory coordination (FATF, G7, Basel)

Exclude:
- Opinion pieces, think tank reports (unless cited in actual legislation)
- Industry lobbying announcements (unless tied to specific bill)
- Rumors of future regulation without concrete action
- Academic papers on regulation

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables

No environment variables required — uses WebSearch and WebFetch.
