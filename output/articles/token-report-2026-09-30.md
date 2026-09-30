# $MIROSHARK — 2026-09-30

**Verdict:** CONSOLIDATING — price down 5.2% 24h on thin volume (0.2x avg), but the real story is pool liquidity dropping 57% overnight.

## 24h at a glance

| Metric | Now | 24h Δ | vs 7d avg |
|--------|-----|-------|-----------|
| Price | $0.000002569 | −5.2% | — |
| Liquidity | $137.9K | −57.0% | — |
| Volume (24h) | $3.6K | — | 0.2× |
| Buys / Sells | 14 / 11 | ratio 1.27 (yest 1.64) | — |
| Whale trades (≥$1k) | 1 | — | — |
| FDV | $256.9K | — | — |

## Trend
- **7d:** −20.2% (rolling over — this week erased last week's +32.6% bounce, now the steepest 7d decline logged since before 09-22)
- **30d:** −15.9% (~30d, daily-close fallback) (roughly in line with the 7d move — most of the 30-day decline happened in the last week, not a slow bleed)

## What changed
Tracked-pool liquidity (MiroShark/WETH) fell from $320.6K to $137.9K overnight — a 57.0% drop with no matching swap activity: the trades feed shows nothing larger than a $1.1K sell in the last 24h, so this isn't a sell-driven price impact, it's an LP-side move (add/remove liquidity events don't appear in the swap trade feed). The one whale trade was a $1,073 sell (403.2M tokens, wallet 0x749f…c5c) at 08:38 UTC on 09-29; the same wallet came back with four buys totaling ~$713 between 05:25–05:26 UTC on 09-30. Price drifted down 5.2% to $0.000002569 on volume that stayed at just 0.2x the 7-day average ($3.6K vs $14.9K mean) — a quiet, thin session, not a broad sell-off. Order flow stayed buy-skewed (14/11, ratio 1.27) but softer than yesterday's 1.64.

## Context
The GeckoTerminal-vs-DexScreener pool liquidity gap that persisted for 14 straight sessions (09-16→09-29, GT running $278–350K against DS's $120–159K) has closed: GT now reports $137.9K and DS reports $137.8K for the same pool — a 0.07% gap. Price cross-check stays clean (1.2% deviation, within the low-volume 10% threshold). This looks like GT's reserve figure converging down to reality rather than DS catching up, which reframes the last two weeks: DS's lower figure may have been closer to the true reserve the whole time. Worth the operator's attention as the open decision item — pick a canonical source now that they agree, or watch one more session to confirm the convergence holds.

---
*Chart: https://www.geckoterminal.com/base/pools/0x83a29b6619907f80e5a47d40f53d4af239a69980f22a08b10f43d357a9f06209*
*Contract: 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | Chain: base*
*Sources: gt=ok · ds=ok · xai=skip · treasury=skip*
