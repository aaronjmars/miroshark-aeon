---
name: Deal Flow
description: Weekly funding round tracker across configurable verticals
var: ""
tags: [research]
---

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating deals.

## Steps

1. **Search for recent funding rounds** across verticals tracked in MEMORY.md (default: AI, crypto, infrastructure). Read MEMORY.md for tracked verticals, then run WebSearches in parallel using those verticals. If no verticals are configured, use these defaults:

   - `"AI startup funding round ${month} ${year}"` — frontier AI, agents, infra
   - `"crypto funding round ${month} ${year}"` — DeFi, tokens, exchanges, wallets
   - `"infrastructure funding round ${year}" OR "developer tools funding ${year}"` — infra, devtools, compute

   Also check:
   - `crypto-fundraising.info` for the latest crypto-specific rounds
   - `aifundingtracker.com` for AI-specific rounds

2. **Filter and rank deals.** From all results, select the top 10 most relevant deals based on:
   - **Relevance to tracked verticals in MEMORY.md**
   - **Signal strength:** unusually large rounds, notable investors (a16z, Paradigm, Founders Fund, etc.), contrarian plays, first-of-kind categories
   - **Recency:** prioritize last 7 days, include up to 14 days if slow week
   - **Deduplicate** against previous logs

3. **For each deal, capture:**
   - Company name and one-line description
   - Round type (pre-seed, seed, Series A/B/C, etc.)
   - Amount raised and valuation if available
   - Lead investors
   - Why it matters (one sentence — what signal does this send?)

4. **Add editorial commentary.** After listing deals, write 2-3 sentences of editorial commentary:
   - What's the capital telling us? Where is smart money clustering?
   - What's overfunded vs underfunded?
   - Any deals that validate or contradict emerging theses?

5. **Send via `./notify`** (under 4000 chars):
   ```
   *Deal Flow — ${today}*

   1. **Company** — one-line description
      Round: Series X, $XXM | Lead: Investor
      Signal: why it matters

   2. ...

   *Reading the capital:* 2-3 sentences of commentary.
   ```

6. **Log to memory/logs/${today}.md.**

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Guidelines

- Skip acqui-hires, grants under $1M, and token sales (token-pick covers those)
- Flag any deal in prediction markets, coordination markets, or agentic payments — these are always relevant regardless of size
- Compare week-over-week: is capital accelerating or decelerating in each vertical?

## Environment Variables Required
- None (uses WebSearch)
