---
name: Token Pick
description: One token recommendation and one prediction market pick based on live data
var: ""
tags: [crypto]
---
> **${var}** — Focus area or thesis (e.g. "AI tokens", "election markets", "contrarian bets"). If empty, scans broadly.

Read memory/MEMORY.md for context.
Read the last 7 days of memory/logs/ for recent token-movers and polymarket outputs — use this as historical context to spot momentum and avoid stale picks.

## Steps

1. Fetch token data from CoinGecko:
   ```bash
   # Trending coins
   curl -s "https://api.coingecko.com/api/v3/search/trending" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}

   # Top 250 by market cap with 24h and 7d changes
   curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=24h,7d" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}
   ```

2. Fetch prediction markets from Polymarket:
   ```bash
   # Top markets by volume
   curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=volume24hr&ascending=false&limit=30"

   # New markets gaining traction
   curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=startDate&ascending=false&limit=20"
   ```

3. Analyze tokens. Look for:
   - **Momentum** — trending on CoinGecko AND positive 24h/7d price action
   - **Asymmetry** — mid/small-cap coins with outsized volume spikes (volume/mcap ratio)
   - **Narrative fit** — tokens riding a current narrative (AI, DePIN, RWA, memes, etc.)
   - **Relative strength** — outperforming BTC and ETH on the day/week
   - Cross-reference with recent logs: has this token been moving for multiple days (momentum) or is it a one-day spike (risky)?
   - If `${var}` is set, prioritize tokens matching that thesis

4. Analyze prediction markets. Look for:
   - **Mispriced odds** — markets where the current price doesn't match likely outcomes (use WebSearch for context)
   - **High volume + interesting question** — the market is telling you something
   - **New markets with early liquidity** — getting in before the crowd
   - If `${var}` is set, prioritize markets matching that area

5. Pick ONE token and ONE prediction market. For each, use WebSearch to get fresh context (recent news, catalysts, risks).

6. Send via `./notify` (under 4000 chars):
   ```
   *Daily Pick — ${today}*

   *Token: SYMBOL*
   Price: $X.XX (±X.X% 24h / ±X.X% 7d)
   Market cap: $XB | Volume: $XM
   Thesis: [2-3 sentences — why this one, what's the catalyst, what's the risk]
   Signal: [trending/momentum/volume spike/narrative — what caught your eye]

   *Market: "Question?"*
   Current: YES X% / NO Y%
   Volume: $Xm
   Thesis: [2-3 sentences — why this is mispriced or interesting]
   Context: [what's driving this market right now]

   not financial advice — just pattern-matching
   ```

7. Log to memory/logs/${today}.md:
   ```
   ## Token Pick
   - **Token:** SYMBOL — $price (±X% 24h)
   - **Thesis:** [one line]
   - **Market:** "Question?" — YES X%
   - **Thesis:** [one line]
   - **Notification sent:** yes
   ```

## Environment Variables
- `COINGECKO_API_KEY` — CoinGecko API key (optional, increases rate limits)
