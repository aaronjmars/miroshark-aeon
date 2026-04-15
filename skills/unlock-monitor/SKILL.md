---
name: Unlock Monitor
description: Weekly token unlock and vesting tracker — flag major supply events before they move markets
schedule: "0 10 * * 1"
commits: true
tags: [crypto]
permissions:
  - contents:write
---

Read memory/MEMORY.md for context on market positions and active narratives.
Read the last 3 days of memory/logs/ to avoid repeating events.

## Steps

1. **Search for upcoming token unlocks.** Run these WebSearches in parallel:

   - `"token unlock schedule this week" site:tokenomist.ai OR site:defillama.com`
   - `"major token unlock ${today} crypto vesting"`
   - `"token unlock" AND ("cliff" OR "vesting" OR "team unlock" OR "investor unlock") this week`
   - `"FTX distribution" OR "bankruptcy distribution" OR "creditor payout" crypto ${current_year}` (court-ordered supply shocks count)

   Also search:
   - `tokenomist.ai` — source-verified unlock data across 500+ tokens
   - `defillama.com/unlocks` — DeFi protocol unlock calendar
   - `coingecko.com/en/highlights/incoming-token-unlocks` — upcoming unlock highlights

2. **Filter for high-impact events.** From all results, select the top 8-10 unlocks based on:
   - **Size relative to circulating supply:** unlocks > 3% of circulating supply are high-impact
   - **Dollar value:** prioritize unlocks > $10M
   - **Recipient type:** team/investor unlocks > ecosystem/community unlocks (selling pressure signal)
   - **Relevance to tracked verticals in MEMORY.md:** AI agents, DeFi, prediction markets, L1/L2 infra, cross-chain
   - **Deduplicate** against previous logs

3. **For each unlock, capture:**
   - Token name and ticker
   - Unlock date
   - Number of tokens and % of circulating supply
   - Dollar value at current price
   - Recipient category (team, investor, ecosystem, community, creditor)
   - Price action context (has the market front-run this? any pre-unlock dump?)

4. **Classify supply impact** for each event:
   - **HIGH** — >5% of circulating supply, team/investor recipients, >$50M value
   - **MEDIUM** — 2-5% of circulating supply or $10-50M value
   - **LOW** — <2% or community/ecosystem allocation (less likely to sell)

5. **Add editorial commentary.** After listing unlocks, write 2-3 sentences of commentary:
   - Is the market pricing these in or sleepwalking?
   - Which unlocks create real sell pressure vs which are noise?
   - Any patterns? (e.g. infra tokens all unlocking same week = sector rotation trigger)
   - Court-ordered distributions (FTX, Celsius, etc.) are different beasts — forced sellers, not strategic ones

6. **Send via `./notify`** (under 4000 chars):
   ```
   *Unlock Monitor — week of ${date}*

   HIGH IMPACT
   - **$TOKEN** — unlock date — X tokens (Y% circ supply, $ZM)
     Recipients: team/investor/etc | Market: front-run/sleepwalking

   MEDIUM IMPACT
   - **$TOKEN** — details

   LOW IMPACT
   - **$TOKEN** — details

   *Supply read:* 2-3 sentences. What's real, what's noise, what's already priced in.
   ```

7. **Log to memory/logs/${today}.md.**

## Guidelines

- This is a supply-side signal tracker, not a price prediction tool. Focus on *who* is receiving tokens and *whether they'll sell*.
- Team and investor unlocks carry the strongest sell signal — these are entities with cost basis near zero.
- Ecosystem and community unlocks (airdrops, staking rewards, grants) are weaker signals — recipients are more distributed.
- Court-ordered distributions (FTX, Celsius, Mt. Gox) are unique — forced liquidation with legal timelines, not market-driven.
- Cross-reference with narrative-tracker output when possible — unlocks during a fading narrative hit harder.
- Be direct. No hedging. "this one's priced in" or "market's asleep on this" — say it plainly.
- If nothing significant is unlocking, say so. A quiet week on supply is a signal too.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables Required

- None (uses WebSearch)
- Notification channels configured via repo secrets (see CLAUDE.md)
