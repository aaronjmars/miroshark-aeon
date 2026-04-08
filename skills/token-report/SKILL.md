---
name: token-report
description: Daily price performance report for the project's token — price, volume, liquidity, and context
var: ""
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
Read the last 7 days of memory/logs/ for previous price data to show trends.

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

4. **Fetch recent trades** for activity signal:
   ```bash
   curl -s "https://api.geckoterminal.com/api/v2/networks/base/pools/POOL_ADDRESS/trades"
   ```

5. **Search for social sentiment** (optional — requires XAI_API_KEY):
   If `XAI_API_KEY` is set, search X for mentions of $TOKEN in the last 24h:
   ```bash
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for $TOKEN_SYMBOL in the last 24 hours. Return the 5 most notable tweets with @handle and summary."}],
       "tools": [{"type": "x_search"}]
     }'
   ```
   If `XAI_API_KEY` is not set, skip social sentiment and note it in the report.

6. **Compile the daily report**:
   ```markdown
   # Token Report — ${today}

   ## $TOKEN Performance

   | Metric | Value | 24h Change |
   |--------|-------|------------|
   | Price | $X.XXXX | +/-Y.Y% |
   | Liquidity | $X.XK | — |
   | 24h Volume | $X.XK | — |
   | 24h Buys/Sells | X / Y | — |
   | 24h High/Low | $X.XX / $X.XX | — |
   | FDV | $X.XM | — |

   ## Trend
   - **24h:** [price action summary from hourly candles]
   - **7-day:** +/-X.X% ([rallying, consolidating, pulling back, etc.])
   - **30-day:** +/-X.X% ([context])

   ## Volume & Liquidity
   [Is volume increasing/decreasing? Any notable large trades? Buy/sell ratio?]

   ## Social Pulse
   [Key mentions, sentiment, notable tweets — or "XAI_API_KEY not set, social data unavailable"]

   ## Context
   [1-2 sentences connecting price action to any known events — repo updates, market conditions]

   ---
   *Data: GeckoTerminal | Chain: Base*
   *Contract: CONTRACT_ADDRESS*
   ```

7. **Save** to `articles/token-report-${today}.md`

8. **Log** to `memory/logs/${today}.md` including the current price (for trend comparison in future runs). **Do this before sending the notification.**

9. **Send notification** via `./notify`:
   ```
   *$TOKEN Daily — ${today}*

   Price: $X.XXXX (Y.Y% 24h)
   Liquidity: $X.XK | 24h Vol: $X.XK
   Buys/Sells: X/Y
   7d: +/-X.X% | 30d: +/-X.X%

   [1-sentence summary]

   Chart: https://www.geckoterminal.com/base/pools/POOL_ADDRESS
   ```

**Important:** If the GeckoTerminal API returns no data (token not found, API error, empty response), log "TOKEN_REPORT_NO_DATA" to memory and **do NOT send any notification**. Do not notify about failures or empty results.
