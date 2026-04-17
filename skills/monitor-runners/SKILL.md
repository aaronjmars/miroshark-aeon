---
name: Monitor Runners
description: Find the top 5 tokens that ran hardest in the past 24h across major chains using GeckoTerminal
var: ""
tags: [crypto]
---
> **${var}** — Filter by chain (e.g. "solana", "eth", "base", "bsc"). If empty, scans all major networks.

Read `memory/MEMORY.md` for context.
Read the last 2 days of `memory/logs/` to see if any of these tokens were flagged before (repeat runners are interesting).

## Data Source

GeckoTerminal API (free, no API key). Docs: https://api.geckoterminal.com/api/v2

Key endpoints:
- `GET /networks/trending_pools?page=1` — trending pools across all networks
- `GET /networks/{network}/trending_pools?page=1` — per-network trending pools
- `GET /networks/{network}/new_pools?page=1` — newly created pools

Each pool object includes:
- `attributes.name` — pool name (e.g. "TOKEN / SOL")
- `attributes.price_change_percentage.{m5,m15,m30,h1,h6,h24}` — price changes
- `attributes.volume_usd.{m5,m15,m30,h1,h6,h24}` — volume
- `attributes.market_cap_usd` / `attributes.fdv_usd` — market cap
- `attributes.transactions.h24.{buys,sells}` — transaction counts
- `attributes.pool_created_at` — pool creation timestamp
- `attributes.reserve_in_usd` — liquidity
- `relationships.network.data.id` — chain name

## Steps

### 1. Fetch trending pools from multiple networks

Pull trending pools from global + individual chains sequentially:

```bash
TMPDIR=$(mktemp -d)

# Fetch sequentially with 1s delay to avoid GeckoTerminal 429 rate limits
for NETWORK in "" solana eth base bsc arbitrum; do
  if [ -z "$NETWORK" ]; then
    URL="https://api.geckoterminal.com/api/v2/networks/trending_pools?page=1"
    OUT="$TMPDIR/global.json"
  else
    URL="https://api.geckoterminal.com/api/v2/networks/${NETWORK}/trending_pools?page=1"
    OUT="$TMPDIR/${NETWORK}.json"
  fi
  curl -s "$URL" > "$OUT"
  # If 429, wait 2s and retry once
  if grep -q '"status":"429"' "$OUT" 2>/dev/null; then
    sleep 2
    curl -s "$URL" > "$OUT"
  fi
  sleep 1
done
```

If `${var}` is set to a specific chain, only fetch that chain's trending pools.

Also fetch new pools to catch tokens that just launched and are already running:
```bash
curl -s "https://api.geckoterminal.com/api/v2/networks/new_pools?page=1" > "$TMPDIR/new.json"
```

### 2. Merge, dedupe, and rank

From all fetched data:

1. **Dedupe** by pool address — same pool can appear in global + per-network results
2. **Filter** to positive 24h movers only (we want runners, not dumps)
3. **Sort** by `price_change_percentage.h24` descending
4. **Apply quality filters** — skip pools that look like obvious rugs or noise:
   - Skip if 24h volume < $50,000 (too thin)
   - Skip if pool created < 1 hour ago and no meaningful volume (too new to judge)
   - Skip if buy/sell ratio is extreme (>10:1 sells = probably dumping)
   - Flag but don't skip if mcap is null/zero (might be very new)

### 3. Select the top 5 runners

Pick the **5 tokens with the largest 24h price increase** that pass the quality filters.

For each runner, collect:
- **Token name** and pair (e.g. "TOKEN / SOL")
- **Chain** (solana, eth, base, etc.)
- **24h change** — the big number
- **1h change** — is it still running or cooling off?
- **5m change** — real-time momentum
- **24h volume** — how much money flowed through
- **Market cap / FDV** — size context
- **Buy/sell ratio** — demand signal
- **Pool age** — when was the pool created
- **Liquidity** (reserve_in_usd) — how much is backing it

### 4. Analyze each runner

For each of the 5, write a quick assessment:
- **Momentum** — is it accelerating (1h > 0 and 5m > 0) or fading?
- **Volume** — proportional to mcap? Over-traded is suspicious, under-traded means thin.
- **Buy pressure** — more buys than sells = continued demand
- **Age** — brand new (<24h) = speculative; older = something changed
- **Risk** — low liquidity, no mcap data, extreme moves (>1000%) = high risk

### 5. Notify

Send via `./notify` (under 4000 chars). No leading spaces on any line:
```
*runners — ${today}*

1. TOKEN (chain) +X,XXX% 24h
vol $Xm | fdv $Xm | still running / cooling off — [1-2 sentence analysis]

2. TOKEN (chain) +XXX% 24h
vol $Xm | fdv $Xm | momentum note — [1-2 sentence analysis]

3. ...
4. ...
5. ...

vibe: [one line on overall market mood]
```

### 6. Log

Append to `memory/logs/${today}.md`:
```
## Monitor Runners
- **Networks scanned:** N
- **Positive movers found:** N
- **Top 5:**
  1. TOKEN (chain) +X% — $Xm vol, $Xm mcap — [momentum note]
  2. ...
- **Repeat runners from previous days:** [list any or "none"]
- **Notification sent:** yes
```

If any token appears as a runner on multiple days in a row, flag it in `memory/MEMORY.md` — sustained momentum is notable.
