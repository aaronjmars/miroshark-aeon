# $MIROSHARK — 2026-09-29

**Verdict:** CONSOLIDATING — price down 11.9% 24h on a single whale sell, but volume held at 0.6x average.

## 24h at a glance

| Metric | Now | 24h Δ | vs 7d avg |
|--------|-----|-------|-----------|
| Price | $0.000002710 | −11.9% | — |
| Liquidity | $320.6K | −6.0% | — |
| Volume (24h) | $12.7K | — | 0.6× |
| Buys / Sells | 18 / 11 | ratio 1.64 (yest 0.75) | — |
| Whale trades (≥$1k) | 2 | — | — |
| FDV | $271.0K | — | — |

## Trend
- **7d:** −18.2% (rolling over — most of the decline is recent, not a slow bleed)
- **30d:** −11.3% (~30d, daily-close fallback) (roughly matches the 7d move, meaning price was flat for the first three weeks of the window before this week's drop)

## What changed
A single sell of 3.0B tokens (~$8.3K, wallet 0x73d3…9c5) hit the MiroShark/WETH pool at 06:49 UTC on 09-28, dropping price from ~$0.00000276 straight to ~$0.00000259 in one block — the entire 24h price move traces to that one trade. A $1.0K buy (wallet 0x796e…0fd7) at 00:33 UTC on 09-29 partially offset it, and price has since drifted up to $0.00000271. Order flow actually flipped buy-skewed for the session (18/11, ratio 1.64, vs yesterday's 0.75), but total volume ($12.7K) stayed at 0.6x the 7-day average — this was a thin book getting knocked around by one seller, not a broad move. Liquidity in the tracked pool eased −6.0% to $320.6K, tracking the price move rather than signaling an LP exit.

## Context
GeckoTerminal pool-level liquidity ($320.6K) continues to diverge sharply from DexScreener's figure ($140.2K) for the same pair — this gap has now persisted for 14 straight sessions (09-16→09-29). Price cross-check between the two sources stays clean (1.1% deviation, within threshold). Continuing to track GT pool-level for continuity per the standing note; the source discrepancy itself remains unresolved.

---
*Chart: https://www.geckoterminal.com/base/pools/0x83a29b6619907f80e5a47d40f53d4af239a69980f22a08b10f43d357a9f06209*
*Contract: 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | Chain: base*
*Sources: gt=ok · ds=ok · xai=skip · treasury=skip*
