# $MIROSHARK — 2026-09-22

**Verdict:** BREAKOUT — +16.9% 24h on 9.1× average volume, buy-skewed whale flow ($16.7K buys vs $8.7K sells).

## 24h at a glance

| Metric | Now | 24h Δ | vs 7d avg |
|--------|-----|-------|-----------|
| Price | $0.000003312 | +16.9% | — |
| Liquidity | $355.3K | +14.6% | — |
| Volume (24h) | $49.2K | — | 9.1× |
| Buys / Sells | 83 / 68 | ratio 1.22 (yest 0.55) | — |
| Whale trades (≥$1k) | 16 | — | — |
| FDV | $331.2K | — | — |

## Trend
- **7d:** +29.1% (rallying)
- **30d:** -3.9% (range-bound — the month is a round trip despite today's spike)

## What changed
Volume on the primary MiroShark/WETH pool ran 9.1× the 7-day average ($49.2K vs a $5.4K typical day), with 16 whale trades (≥$1K) split buy-heavy: $16.7K in whale buys against $8.7K in whale sells. Top three: buy $3.91K @ $0.00000298 · 06:12 UTC, buy $2.71K @ $0.00000352 · 11:59 UTC, buy $2.70K @ $0.00000277 · 06:04 UTC. Liquidity in the same pool rose 14.6% to $355.3K, in step with the price move rather than draining into it. Note: `token-movers` had 4 failed runs earlier today (harness returned zero-token completions, tracked as issue #182) — the last successful snapshot was ~37h ago (2026-09-21T06:19 UTC), so the 24h Δ above uses GeckoTerminal's native rolling h24 field rather than the stale stored-price comparison (which would read +29.9% across the full ~37h gap) — consistent with the 2026-08-04 gap-handling precedent in memory.

---
*Chart: https://www.geckoterminal.com/base/pools/0x83a29b6619907f80e5a47d40f53d4af239a69980f22a08b10f43d357a9f06209*
*Contract: 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | Chain: base*
*Sources: gt=ok · ds=ok · xai=skip · treasury=skip*
