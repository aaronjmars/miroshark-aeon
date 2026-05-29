# Token Report — 2026-05-29

## $MIROSHARK Performance

| Metric | Value | 24h Change |
|--------|-------|------------|
| Price | $0.00001030 | +36.8% |
| Liquidity | $513.0K | — |
| 24h Volume | $156.9K | -2.2% |
| 24h Buys/Sells | 241 / 159 | — |
| 24h High/Low | $0.0000107 / $0.00000771 | — |
| FDV | $1.03M | — |

## Trend

**Price**
- **24h:** Opened around $7.87–8.20e-6, hit a low of $0.00000771 early in the window, then progressively recovered through midday, spiking to a high of $0.0000107, and settling near $0.0000103 — a partial reversal of yesterday's -47% sell-off.
- **7-day:** -25.9% (May 22 close $0.00001386 → $0.00001030 today; continued downtrend from ATH, though today's session breaks the streak of red closes)
- **30-day:** +152.5% (April 29 close $0.00000408 → $0.00001030; token has more than doubled vs its late-April base despite ATH drawdown)

**Volume (daily, main pool)**
- **24h:** $156.9K (-2.2% vs prior day $160.5K; effectively flat, minimal change in activity level)
- **7-day avg:** $305.9K/day (May 22–28)
- **30-day avg:** $314.5K/day (trend: volume peaked mid-May during the ATH run, has been normalizing since; 7d avg now roughly in line with 30d avg)

## Volume & Liquidity

Buy/sell ratio on the main MiroShark/WETH pool (Uniswap v4) sits at 1.52× (241 buys vs 159 sells in 24h), up from 1.37× yesterday — the strongest buyer-side lean in three sessions. Liquidity recovered to $513.0K from $409.2K yesterday (+25.3%), which suggests LP positions moved back in after yesterday's volatility. Volume at $156.9K is nearly flat vs yesterday's $160.5K; the bounce was more a price move than a volume event. No outsized single trades visible in the pool data.

## Social Pulse

X/Grok data wasn't available for this run. The updated spam filter in `scripts/prefetch-xai.sh` (aeon PR #48, merged May 28) screened out all candidates — all mentions passing through the date window were zero-engagement contract-drop or bot accounts. No organic signal surfaced.

## Context

Today's +36.8% bounce follows yesterday's sharp -47% session, which took the token from $0.0000129 down to $0.00000742. The partial recovery lands at $0.0000103 — still -76.4% from the May 18 ATH of $0.0000436 and -76.4% from the $1.75M FDV peak. On the repo side, PR #120 (WEBHOOK_EVENTS dispatch filter, 24th surface) merged yesterday and PR #106 (Railway deploy, external, stalled) remains open. No new merge activity since then.

---
*Data: GeckoTerminal | Chain: Base*
*Contract: 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3*
