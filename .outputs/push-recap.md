*Push Recap — 2026-06-01*
aaronjmars/MiroShark — 2 commits · aaronjmars/miroshark-aeon — 1 commit · 3 substantive merges, all by Aeon

*MiroShark — two surfaces shipped paired (4 min apart):* PR #131 Clone JSON merged 14:07Z, PR #130 Surface Catalog API merged 14:11Z. Clone JSON returns a published sim's *inputs* (wire-compatible with POST /api/simulation/create, same field set + defaults + polymarket_market_count clamp [1,5] + country normalisation + demographic_filters pass-through, 1h cache vs 5min on analytical surfaces); Surface Catalog returns the machine-readable list of every surface this deployment exposes (28 entries: 26 publish-gated per-sim + 2 platform). Together they close the integrator discovery→reuse loop in two HTTP calls. PR #130's merge bundled a third commit that registered PR #131's clone_json in the catalog (27→28), so main ships both surfaces *and* the catalog already knows about both — no drift PR. Both pure stdlib + Flask, both zero new deps (36th consecutive zero-deps PR streak).

*Aeon — token-report Path B repaired:* PR #49 merged 12:45Z. The Social Pulse section had been filler 3 days running (May 28/29/30) — the May-28 spam filter (PR #48) correctly screened all Grok candidates, but Path B then printed "X/Grok data unavailable for this run" every day. Path B now replaces that line with "Top Trades (24h)": 3 largest trades by USD from the already-fetched GeckoTerminal /trades response, each as Buy/Sell · $value · token amount · time-ago · basescan tx link. Zero new API calls — data was in scope, being thrown away. Path A unchanged, auto-returns on organic X signal.

Key changes:
- `backend/app/services/clone_service.py` (new, +279 stdlib, 24 offline tests) — wire-compatible with create body, deterministic example_curl, 404 vs 403 distinguishes not-ready from not-allowed.
- `backend/app/services/surfaces_catalog.py` (new, +443 stdlib, 18 tests) — hardcoded list, NOT URL-map-scanned; drift-guard test cross-checks per-sim subset against SURFACE_KEYS so a new per-sim surface can't ship without an entry.
- `skills/token-report/SKILL.md` (+9/−4) — step-5 Path B rewrite; new mutually-exclusive Social Pulse / Top Trades headings in step-6 template; new Path A / Path B log convention.

Stats: 26 files changed, +2,603/−11 across 3 commits. 30+ cron auto-commits on miroshark-aeon excluded as noise.
Full recap: articles/push-recap-2026-06-01.md in https://github.com/aaronjmars/miroshark-aeon
