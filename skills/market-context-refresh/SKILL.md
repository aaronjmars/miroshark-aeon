---
name: Market Context Refresh
description: Fetch live crypto macro data and update memory/topics/market-context.md
schedule: "0 10 * * *"
commits: true
permissions:
  - contents:write
tags: [crypto]
---

Refresh `memory/topics/market-context.md` with current market data. This file is used as context by token-pick, narrative-tracker, and other skills — it must stay current.

Read `memory/MEMORY.md` for prior context.

## Sandbox note

The sandbox may block curl. For every curl call below, if it fails or returns empty, use **WebFetch** for the same URL (omit the API key header — free tier works). WebFetch is a built-in tool that works reliably in the sandbox.

## Steps

1. **Fetch macro crypto data from CoinGecko:**
   ```bash
   # BTC and ETH prices with 24h change
   curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}

   # Top 20 by market cap (to track TVL leaders and movers)
   curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=24h,7d" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}

   # Global market stats (total market cap, volume, dominance)
   curl -s "https://api.coingecko.com/api/v3/global" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}

   # Trending coins
   curl -s "https://api.coingecko.com/api/v3/search/trending" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}
   ```
   **Fallback:** If curl fails, use WebFetch for each URL (without the API key header).

2. **Fetch DeFi data:**
   Use WebSearch for current DeFi stats: "DeFi TVL today $(date +%Y)", "top DeFi protocols TVL", "DEX volume today". Look for:
   - Total TVL (DeFiLlama)
   - Top 5 protocols by TVL
   - DEX 24h volume
   - Stablecoin market caps (USDT, USDC, USDe, USDS)

3. **Fetch prediction market highlights from Polymarket:**
   ```bash
   # Top by 24h volume
   curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=volume24hr&ascending=false&limit=10"

   # Highest liquidity
   curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=liquidity&ascending=false&limit=10"
   ```
   **Fallback:** If curl fails, use WebFetch for the same URLs.
   Pull top 3-5 markets: question, current YES%, 24h volume, liquidity. Note any notable shifts.

4. **Scan for macro signals.** Use WebSearch for:
   - "crypto market today ${today}"
   - "BTC price analysis ${today}"
   - Any major regulatory, macro, or geopolitical events affecting markets

5. **Identify key narratives currently running.** Based on trending coins and web search: which 3-5 meta-narratives are driving price action right now? (e.g., AI tokens, DePIN, RWA, memecoins, restaking)

6. **Write the updated market-context.md.** Overwrite `memory/topics/market-context.md` completely:
   ```markdown
   # Market Context (as of ${today})

   ## Macro
   - BTC $X (±X% 24h) — [one-line observation]
   - ETH $X (±X% 24h) — [one-line observation]
   - Total market cap: $XB (±X% 24h)
   - BTC dominance: X%
   - Total DeFi TVL: ~$XB
   - DEX volume 24h: $XB
   - Stablecoins: USDT $XB, USDC $XB, [others if notable]

   ## Top DeFi Protocols (by TVL)
   - [Protocol]: $XB (±X% 7d)
   - [Protocol]: $XB (±X% 7d)
   - [Protocol]: $XB (±X% 7d)
   - [Protocol]: $XB (±X% 7d)
   - [Protocol]: $XB (±X% 7d)

   ## Trending Coins
   - [COIN]: [why trending, price context]
   - [COIN]: [why trending, price context]
   - [COIN]: [why trending, price context]

   ## Active Narratives
   - [Narrative]: [what's driving it, phase: emerging/rising/peak/fading]
   - [Narrative]: [what's driving it, phase]
   - [Narrative]: [what's driving it, phase]

   ## Prediction Markets (top by volume)
   | Market | YES% | Volume 24h | Liquidity |
   |--------|------|------------|-----------|
   | [question] | X% | $Xm | $Xm |
   | [question] | X% | $Xm | $Xm |
   | [question] | X% | $Xm | $Xm |

   ## Token Picks Made
   [Keep existing rows — do not delete history. Append new picks from recent logs if not already present.]
   | Date | Token | Price | Thesis |
   |------|-------|-------|--------|
   ```
   Preserve the Token Picks table from the prior file. Do not truncate history.

7. **Log to `memory/logs/${today}.md`:**
   ```
   ## Market Context Refresh
   - BTC: $X (±X%), ETH: $X (±X%)
   - Top narrative: [name]
   - Polymarket highlight: "[question]" YES X%
   - Updated memory/topics/market-context.md
   ```

8. **Send notification via `./notify`** (concise, under 500 chars):
   ```
   market context refreshed — ${today}

   BTC $X (±X%) / ETH $X (±X%)
   TVL ~$XB | DEX vol $XB
   top narrative: [name]
   hot market: "[polymarket question]" YES X%
   ```

## Environment Variables

- `COINGECKO_API_KEY` — CoinGecko Pro API key (optional, increases rate limits)
- Notification channels configured via repo secrets (see CLAUDE.md)
