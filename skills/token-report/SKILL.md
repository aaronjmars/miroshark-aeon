---
name: token-report
description: Daily price performance report for the project's token — price, volume, liquidity, and context
var: ""
tags: [crypto]
---
> **${var}** — Token contract address. If empty, uses tracked token from MEMORY.md.

## Config

This skill reads the token to track from the "Tracked Token" section in `memory/MEMORY.md`.

```markdown
## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e... | base |
```

---

Read memory/MEMORY.md for the tracked token.
Read the last 7 days of memory/logs/ for previous price and volume data to show trends.

## Steps

1. **Fetch token info** from GeckoTerminal (free, no API key needed):
   ```bash
   # Token metadata + price
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/tokens/CONTRACT_ADDRESS"
   ```

2. **Fetch pool data** for the token (top liquidity pools):
   ```bash
   # Top pools for this token
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/tokens/CONTRACT_ADDRESS/pools?page=1"
   ```

3. **Fetch OHLCV data** for trend analysis:
   ```bash
   # Get the top pool address from step 2, then fetch candles
   # Daily candles for the last 30 days
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/ohlcv/day?aggregate=1&limit=30"

   # Hourly candles for the last 24h
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/ohlcv/hour?aggregate=1&limit=24"
   ```

4. **Fetch recent trades** for activity signal (also used as Path B fallback in step 5):
   ```bash
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/trades"
   ```
   Each trade entry has `attributes.kind` (`buy`/`sell`), `volume_in_usd`, `block_timestamp`, and `tx_from_address` — enough to render a "top trades" view without any other call.

5. **Search for social sentiment** (optional — requires XAI_API_KEY):
   The sandbox blocks `$XAI_API_KEY` expansion in curl headers, so this skill consumes results that `scripts/prefetch-xai.sh` fetched before Claude started.

   **Path A (cache present):** If `.xai-cache/token-report-social.json` exists AND `.xai-cache/token-report-social.symbol` matches the token symbol you just read from MEMORY.md (strip any leading `$`), parse `output[].content[].text` / `output_text` from the JSON and use those tweets + sentiment for the Social Pulse section. Cite @handles and paste permalinks verbatim.

   **Path B (no cache / symbol mismatch / empty results):** Drop the "Social Pulse" heading entirely and replace it with a **"Top Trades (24h)"** section built from the step-4 trades response — the 3 largest trades by `volume_in_usd` in the last 24h, one bullet each: `kind` (Buy/Sell), USD value, token amount, time-ago (e.g. "3h ago"), and a [tx](https://basescan.org/tx/0x...) link from `tx_hash`. Lead with one sentence on the buy/sell mix in those top 3 (e.g. "Top flows were 2 buys + 1 sell"). Do **not** write a "X/Grok data unavailable" apology — the trades data is the section now. Skip the section entirely only if the trades response is empty.
   Log the path you took as `Social: Path A` or `Social: Path B (top-trades fallback)` so future self-improve runs can see which fired.

6. **Compile the daily report**:
   ```markdown
   # Token Report — ${today}

   ## $TOKEN Performance

   | Metric | Value | 24h Change |
   |--------|-------|------------|
   | Price | $X.XXXX | +/-Y.Y% |
   | Liquidity | $X.XK | — |
   | 24h Volume | $X.XK | +/-Y.Y% |
   | 24h Buys/Sells | X / Y | — |
   | 24h High/Low | $X.XX / $X.XX | — |
   | FDV | $X.XM | — |

   ## Trend

   **Price**
   - **24h:** [price action summary from hourly candles]
   - **7-day:** +/-X.X% ([rallying, consolidating, pulling back, etc.])
   - **30-day:** +/-X.X% ([context])

   **Volume (daily)**
   - **24h:** $X.XK ([+/-Y.Y% vs prior day])
   - **7-day avg:** $X.XK ([+/-Y.Y% vs prior 7d])
   - **30-day avg:** $X.XK ([context — sustained, spiking, drying up, etc.])

   ## Volume & Liquidity
   [Is volume increasing/decreasing? Any notable large trades? Buy/sell ratio?]

   ## Social Pulse  *(Path A only — when XAI cache present + symbol matches + non-empty after spam filter)*
   [Key mentions, sentiment, notable tweets from the `.xai-cache/token-report-social.json` Path A cache]

   ## Top Trades (24h)  *(Path B only — when cache missing / symbol mismatch / all candidates filtered)*
   [One-sentence flow summary, then 3 bullets — the 3 largest trades by USD from step 4, each: Buy/Sell · $X · N.NM TOKEN · Xh ago · [tx](https://basescan.org/tx/...)]

   ## Context
   [1-2 sentences connecting price action to any known events — repo updates, market conditions]

   ---
   *Data: GeckoTerminal | Chain: Base*
   *Contract: CONTRACT_ADDRESS*
   ```

7. **Save** to `articles/token-report-${today}.md`

8. **Log** to `memory/logs/${today}.md` including the current price and 24h volume (for price/volume trend comparison in future runs). **Do this before sending the notification.**

9. **Send notification** via `./notify`:
   ```
   *$TOKEN Daily — ${today}*

   Price: $X.XXXX (Y.Y% 24h)
   Liquidity: $X.XK | 24h Vol: $X.XK (Y.Y% 24h)
   Buys/Sells: X/Y
   7d: +/-X.X% price, +/-X.X% vol | 30d: +/-X.X% price

   [1-sentence summary]

   Chart: https://www.geckoterminal.com/base/pools/POOL_ADDRESS
   ```

**Important:** If the GeckoTerminal API returns no data (token not found, API error, empty response), log "TOKEN_REPORT_NO_DATA" to memory and **do NOT send any notification**. Do not notify about failures or empty results.
