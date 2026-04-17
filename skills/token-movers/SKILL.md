---
name: Token Movers
description: Top movers, losers, and trending coins from CoinGecko
var: ""
tags: [crypto]
---
> **${var}** — Token symbol or category to highlight (e.g. "SOL", "layer-2", "meme coins"). If empty, shows top movers, losers, and trending coins.

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating items.

## Steps

1. Fetch market data and trending coins in parallel:
   ```bash
   # Top 250 coins by market cap with 24h price change
   curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=24h" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}

   # Trending searches (top coins people are searching for)
   curl -s "https://api.coingecko.com/api/v3/search/trending" \
     ${COINGECKO_API_KEY:+-H "x-cg-pro-api-key: $COINGECKO_API_KEY"}
   ```

2. From market data, sort by `price_change_percentage_24h`:
   - **Top 10 winners**: highest 24h % change
   - **Top 10 losers**: lowest 24h % change
   - For each coin: name, symbol, current price (USD), 24h % change

3. From trending data, extract the top trending coins:
   - Name, symbol, market cap rank, current price (USD), 24h % change
   - Cross-reference with market data: flag any coin that is both trending AND a top mover (strong signal)

4. If `${var}` is set, highlight that specific token or filter to that category, and add its detailed stats (price, volume, market cap, 7d change) at the top.

5. Send via `./notify` (under 4000 chars):
   ```
   *Token Movers — ${today}*

   *Top 10 Winners (24h)*
   1. SYMBOL: $price (+X.X%)
   2. ...

   *Top 10 Losers (24h)*
   1. SYMBOL: $price (-X.X%)
   2. ...

   *Trending (Most Searched)*
   1. NAME (SYMBOL) — #X mcap rank, $price (±X.X%)
   2. ...

   *Notable:* SYMBOL trending + up XX%
   ```

6. Log to memory/logs/${today}.md.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
