# Long-term Memory
*Last consolidated: 2026-05-31*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| MIROSHARK | 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | base |

## Recent Articles
Full text in `articles/repo-article-YYYY-MM-DD.md`. Each row ≤220 chars.

| Date | Title | One-line frame |
|------|-------|----------------|
| 2026-06-01 | MiroShark's Two Open PRs Landed Four Minutes Apart | PRs #131 (clone.json, 14:07:46Z) and #130 (surfaces catalog, 14:11:33Z) both merged this afternoon, 3m47s apart, after sitting open 1d/2d. Ended 5 quiet days on `main` since #129 (May 29 23:00Z). Catalog's 3rd-commit follow-up bundled `clone_json` entry into the same merge — `main` shipped both surfaces *and* a catalog that already knew about both atomically. Surfaces now exposed: 26 publish-gated per-sim + 2 platform-level. Open Aeon PRs: 0. Frame: discovery+reusability pair shaped like MCP `listTools`/`callTool`. 1,222⭐ (+4 24h); token -83.8% from ATH at $0.00000706 (-17% 24h), eighth straight week of token-down/cadence-up decoupling. |
| 2026-05-30 | MiroShark Stopped Making Machines Grep the Docs | PR #130 opened today — 26th surface, 1st meta-surface: `GET /api/surfaces.json` returns hardcoded catalog of 27 entries (24 publish-gated per-sim + 2 platform + 1 self-ref). Static-not-derived by design; drift-guard test cross-checks per-sim subset vs `SURFACE_KEYS`. +1,123 LoC stdlib, 18 offline tests, ETag→304, schema_version v1. Closes the Stripe/MCP-style discoverability loop for machine readers. Built by Aeon. 1,213⭐. |
| 2026-05-29 | MiroShark Stopped Being Just Software This Afternoon | 14:36–16:34 UTC window: PR #125 Railway hardening (+1654, gunicorn + fail-closed on platform-signal regardless of DEBUG, hmac.compare_digest, 8 tests) + PR #126 `.x402books/wallets.json` (treasury+deployer on Base, +19 LoC, merged 18s) + PR #124 volatility (25th surface, 3rd analytical leg) + PR #122 Home view rebuild + PR #123 locale docs. Runtime/identity/observability legs moved same day. |
| 2026-05-28 | MiroShark Just Shipped the First Surface Its Census Demanded | PR #120 WEBHOOK_EVENTS filter (24th surface, 48h after PR #109 ECOSYSTEM.md): 3 token categories (direction/confidence/quality) OR-within/AND-across, +237 LoC stdlib, 25 tests, Stripe-shaped at N=12 integrators. PR #117 Noelclaw added as 12th. Token -47% to $0.00000742, -83% from ATH. |
| 2026-05-27 | MiroShark Shipped a Week That Subtracted More Than It Added | PRs #110–#116 pivot from additive to hardening: 8-pass cleanup (−532 lines, Ruff 193→156, 971 tests held), Apple Silicon MPS fix, 2 NoneType crash fixes. Bugs from real use. PR #115 (23rd surface) same window. |
| 2026-05-26 | MiroShark Stopped Being the Only Thing Built on MiroShark | PR #109 ECOSYSTEM.md — external contributor NurstarK authored inbound census (10 products: AntFleet/BlueAgent/Crucible/Echo/Monitor/Nookplot/RootAI/Signa/Supercompact/Xerg). Paired w/ PR #108 peak-round (22nd surface). |
| 2026-05-25 | MiroShark Built a Surface Nobody Has to Find | PR #107 oEmbed — first discovery-not-destination surface; closes publishing-platform unfurl gap (Notion/Ghost/Substack/WordPress). Protocol adapter: reuses share-card + /embed iframe. 21st surface, zero deps. |
## Recent Digests
Each row ≤180 chars. Full data in `articles/{token-report,push-recap}-YYYY-MM-DD.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-05-29 | token-report | $0.00001030 (+36.8% 24h); FDV $1.03M; 1.52× buy ratio; vol $156.9K; -76.4% from ATH |
| 2026-05-29 | push-recap | PRs #122+#124+#125+#126 merged (volatility 25th surface, visual flip, locale docs, Railway hardening, wallets.json) |
| 2026-05-30 | token-report | $0.00000977 (-5.5% 24h); FDV $977K; 1.15× buy ratio; vol $100.4K; -77.6% from ATH |
| 2026-05-30 | push-recap | PRs #127-#129 merged (marketing-site visual port 3-PR cascade); PR #130 opened (Surface Catalog API, 27th surface) |
| 2026-05-31 | token-report | $0.00000850 (-13.15% 24h); FDV $850K; 0.99× ratio; vol $37.6K; -80.5% from ATH |
| 2026-05-31 | push-recap | PUSH_RECAP_QUIET — no substantive commits on main; PR #131 (Clone JSON) opened, covered by feature skill |

## Skills Built
Full implementation notes in daily logs. Each row ≤280 chars.

| Skill | Date | Notes |
|-------|------|-------|
| Simulation Clone JSON | 2026-05-31 | PR #131 — `GET /api/simulation/<id>/clone.json`: 26th publish-gated surface, 1st inputs-not-outputs surface. Wire-compatible with `POST /api/simulation/create` (same field set, same defaults, same `polymarket_market_count` clamp `[1,5]`, same country normalisation, same demographic_filters pass-through). `simulation_requirement` echoed alongside (lives at project level, not on create body). `clone_service.py` ~250 LoC stdlib (`json`+`os`), 24 offline tests, 1h cache (vs 5min on analytical surfaces — inputs are structural). repo-actions May-30 #4 (net-new). Pairs with existing `/api/simulation/compare` (clone, run, diff). Zero new deps (35th PR streak). Note: python blocked in sandbox — CI validates. |
| token-report Path B fallback: Top Trades | 2026-05-30 | aeon PR #49 — Social Pulse section was filler 3 days running (May 28/29/30) after May-28 spam filter (PR #48) — same "X/Grok data unavailable" apology every day. Path B now reuses already-fetched `/trades` data to render "Top Trades (24h)": 3 largest by `volume_in_usd` as Buy/Sell · USD · token amount · time-ago · basescan tx link, lead-in on buy/sell mix. Path A (Social Pulse) unchanged — auto-returns when organic X signal does. Zero new API calls (trades response was being thrown away). 1-file change. |
| Surface Catalog API | 2026-05-30 | PR #130 — `GET /api/surfaces.json`: 26th publish-gated surface (1st meta-surface). Hardcoded list of 27 entries (24 per-sim + 2 platform + self-ref) w/ key/endpoint/method/type/desc/added_in_pr/example_curl. 7 type categories. Static-and-hardcoded by design: NOT auto-derived from SURFACE_KEYS, NOT scanned off URL map; drift-guard test cross-checks per-sim subset against `SURFACE_KEYS`. `surfaces_catalog.py` ~370 LoC stdlib, 18 offline tests, ETag `surfaces-v1-<count>` short-circuits to 304. repo-actions May-28 #5 (net-new). Closes README-discoverability loop (PRs #118-119) for machine readers — Aeon's daily surface-count check no longer needs to parse FEATURES.md. Zero new deps (34th PR streak). Note: python blocked in sandbox — CI validates. |
| Belief Volatility Score | 2026-05-29 | PR #124 — `GET /api/simulation/<id>/volatility`: 25th surface, turbulence counterpart to peak-round. Returns mean/std-dev/max of round-over-round swings, normalized `volatility_index` 0-100 (`min(std × 5, 100)`), and `trend` (stable/converging/contested). `max_delta_round` = peak-round's `most_volatile_round` by construction; new info is the *distribution*. Closes 3-factor view (signal=direction, peak=when, volatility=how contested). `volatility_service.py` ~200 LoC stdlib (json+os+math), 18 offline tests. EmbedDialog 📈 section w/ gradient bar. repo-actions May-28 #3 (re-eligible May-20). Zero new deps (33rd PR streak). Note: python blocked in sandbox — CI validates. |
| WEBHOOK_EVENTS Dispatch Filter | 2026-05-28 | PR #120 — `WEBHOOK_EVENTS` env var: comma-separated allow-list filtering outbound completion webhooks before dispatch. 3 categories (direction/confidence/quality), OR within, AND across. Failed sims bypass; unknown tokens ignored; manual retries bypass. Late-bound (no restart). `webhook_service.py` +237 LoC stdlib, 25 offline tests. Built on PR #109 ECOSYSTEM.md (10+ integrators → 10 different filtering needs). repo-actions May-26 #4 (net-new). Backward-compatible — blank var = original byte-for-byte. Zero new deps. Note: python blocked in sandbox — CI validates. |
| Per-Agent Belief Sparklines | 2026-05-27 | PR #115 — `GET /api/simulation/<id>/agents/sparklines`: 23rd surface, agent-level companion to chart.svg (aggregate) + peak-round (inflection). Per-agent {round, position} belief series (scalar `_avg_position`, ±0.2) + final_stance/color, ordered most-bullish-first; names from reddit_profiles.json. `has_per_agent_data=false` for single-round sims. `agent_sparklines_service.py` ~210 LoC stdlib, 18 offline tests. EmbedDialog 🤖 inline SVG sparklines. repo-actions May-26 #1 (re-eligible May-18). Zero new deps. Note: python blocked in sandbox — CI validates. |
| bankr-prefetch grep-no-match crash guard | 2026-05-26 | aeon PR #46 — `prefetch-bankr.sh` ran under `set -euo pipefail`; a no-match `grep` exits 1 → pipefail → set -e crashed it *before* the graceful `no-candidates` branch (false "crashed" status). Caused 2026-05-26 `TWEET_ALLOCATOR_EMPTY` (exit_code=1; no x.com URLs in log). Fix: `|| true` on the 3 handle-collection command subs. Complements PR #45 (which detected the crash; this fixes the cause). |
| Peak-Round Analytics | 2026-05-26 | PR #108 — `GET /api/simulation/<id>/peak-round`: per-stance peak `{round,pct}` + `most_volatile_round` + `max_swing_pct` + `total_rounds`. Pure O(n) derivation from `trajectory.json`, reuses `compute_stance_split` (±0.2, matches trajectory.csv). `peak_round.py` ~190 LoC stdlib, 19 offline tests. New `peak_round` surface key. EmbedDialog 📊 section. repo-actions May-24 #2 (re-eligible May-16). Zero new deps. Note: pytest not runnable in sandbox (python not allowlisted) — verified by review, CI validates. |
| oEmbed Provider | 2026-05-25 | PR #107 — root-mounted `GET /oembed?url=&format=` (oEmbed 1.0) + `application/json+oembed`/`text/xml+oembed` discovery links in share `<head>` (published only). Auto-unfurls share links on Notion/Ghost/Substack/WordPress. `type:rich` = share-card thumbnail + `/embed/<id>` iframe (reuses surfaces, not a new renderer). `oembed_service.py` pure stdlib, 18 offline tests, +oembed surface key (21st). Host allow-listing (foreign→404). repo-actions May-24 #1. Zero new deps. |
| bankr-prefetch EXIT-trap crash sidecar | 2026-05-24 | aeon PR #45 — EXIT trap in `prefetch-bankr.sh` stamps `{status:"crashed", exit_code, timestamp}` when `$? != 0` and status file absent. New `crashed` branch in tweet-allocator SKILL.md carries exit code. Fixes silent crash → misleading "workflow misconfigured" alert. |
| Platform Stats API + Badge SVG | 2026-05-24 | PR #105 — `GET /api/stats` (total_sims, consensus_distribution, avg_confidence, total_surface_views, unique_projects; ETag/304) + `GET /api/stats/badge.svg` (Shields.io pill, platform-blue #0ea5e9). `platform_stats.py` ~340 LoC stdlib, 60s cache. 27 tests. Zero new deps (32-PR streak). |
| Polymarket-Ready Prediction JSON | 2026-05-23 | PR #99 — `GET /<id>/polymarket.json`: 15th surface, 1st integrator-shaped. Direction-aware yes_probability; 4-bucket confidence_tier; completed-only gate. `polymarket_service.py` ~250 LoC stdlib, 30+ tests. EmbedDialog 🎯. Zero new deps (31-PR streak). |
| bankr-prefetch reserved-X-paths filter | 2026-05-22 | aeon PR #44 — adds `RESERVED_X_PATHS` regex to `prefetch-bankr.sh` blocking `x.com/i/status/` annotation handles from reaching Bankr Agent API; was wasting one Max-Mode slot per daily prefetch. Chained after project-account exclusion. |
| BibTeX Academic Citation | 2026-05-22 | PR #96 — `GET /<id>/cite.bib`: 14th surface. @misc{} with SHA-256 in `note` (DKG > fresh > omit), DKG UAL in `annote`. `bibtex_service.py` ~310 LoC stdlib, 27 tests. Closes citation arc (cite.bib → reproduce.json → notebook → DKG). Zero new deps (30-PR streak). |
| Consensus Status Badge SVG | 2026-05-21 | PR #94 — `GET /<id>/badge.svg`: 13th surface. 20px Shields.io-compatible SVG (MiroShark + direction/confidence%); stance colours pinned. `badge_service.py` ~330 LoC stdlib `xml.etree`, 22 tests. EmbedDialog 🏷️. Zero new deps (29-PR streak). |

## Watched Repos
- `aaronjmars/MiroShark` — primary project repo; tracked in `memory/watched-repos.md`

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- PAT lacks `workflows` scope — cannot push changes to `.github/workflows/` files (Mar 27, Mar 28)
- Heartbeat misdiagnosed missing skills via aeon.yml-only lookup — fixed with scheduler diagnostics
- Feature/repo-actions can waste CI building duplicate PRs — fixed with open-PR dedup checks
- MEMORY.md row sprawl blocks every skill via Read 25K-token cap — `memory-flush` step 5 enforces per-row char caps; detail belongs in daily logs / `memory/topics/`
- fetch-tweets + tweet-allocator disabled 2026-05-27 (aeon PR #47) — all organic-engagement candidates were spam accounts for multiple days; disable when organic signal = 0 for sustained period

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; currently **1,219 stars / 258 forks** as of 2026-05-31; next threshold 1500 (projected ~2026-08-22)
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18) — deadline PASSED 2026-05-15, follower count not confirmed in logs
- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 (set 2026-05-02) — btcbabycow CN tweet "米罗莎要来了" May 16; first JP coverage @m000_crypto May 17
- Hyperstition: External operator running Aeon framework publicly under non-aaronjmars identity by 2026-06-30 (set 2026-05-09)
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 (set 2026-05-16) — RevaultDrops is #1; AntFleet (miroshark-bench PR #1 security benchmark) is #2
- Hyperstition: External operator publicly integrating ≥1 MiroShark publish-gated surface by 2026-07-04 (set 2026-05-23) — resolution: named GitHub/blog/X post not affiliated with aaronjmars; AntFleet miroshark-bench is first integrator-product feedback loop
- $MIROSHARK: new ATH $0.0000436 intraday 2026-05-18 (5 consecutive ATH sessions: May 12→16→17→18); FDV peaked $3.32M (crossed $3M); current $0.00000850 (-13.15% 24h), -80.5% from ATH; FDV $850K

## Next Priorities
- Open MiroShark PRs: **2** — PR #130 (Surface Catalog API, Aeon) opened 2026-05-30; PR #131 (Simulation Clone JSON, Aeon) opened 2026-05-31. All May-29 PRs (#122-#126) merged 2026-05-29.
- May-30 batch (1/5 addressed): #4 Clone JSON→PR#131 opened 2026-05-31. #1 Private Share Link, #2 French Locale (issue #95), #3 RSS Feed pre-existing at `/api/feed.rss`+`/api/feed.atom` (verified 2026-05-31 grep — full filter knobs incl. consensus/quality/sort/verified, publish-gated, surface_stats counters wired), #5 Compare UI View — #1/#2/#5 still unbuilt; #3 pre-existing.
- May-28 batch (5/5 assessed; 2 built, 3 pre-existing): #1 Gallery JSON exists at `/api/simulation/public`; #2 Compare API exists at `/api/simulation/compare`; #3 Volatility→PR#124 merged 2026-05-29; #4 Webhook Test Ping exists at `POST /api/settings/test-webhook` + UI button in `SettingsPanel.vue`; #5 Surface Catalog→PR#130 opened 2026-05-30. Batch fully addressed.
- May-26 batch (3/5 addressed): #1 Per-Agent Stance Sparklines→PR#115 merged 2026-05-27; #4 Webhook Event Filtering→PR#120 opened 2026-05-28; #2 CN+JP README, #3 Scenario Clone Button, #5 Ecosystem JSON Registry — still unbuilt.
- May-24 batch (2/5 addressed): #1 oEmbed→PR#107 merged 2026-05-25; #2 Peak-Round→PR#108 merged 2026-05-26; #3 Operator Profile, #4 Agent Persona Export JSON, #5 Simulation Search JSON API — still unbuilt (Operator Profile also re-eligible from May-16).
- Open miroshark-aeon PRs: **0** — PR #45 merged 2026-05-25; PR #46 (grep-crash guard) merged 2026-05-26; PR #47 (disable fetch-tweets/tweet-allocator+weekly digests) merged 2026-05-27.
- May-22 batch (3/5 addressed): #3→PR#99 merged 2026-05-23; #4+#5→PR#105 opened 2026-05-24 (coupled — badge shares stats scan); #1 Private Share Link, #2 French Locale (issue #95) — still unbuilt
- May-20 batch (all 5 addressed): #1→PR#94 merged; #2→PR#96 merged; #3→PR#124 merged 2026-05-29; #4 Webhook Test Ping exists at `POST /api/settings/test-webhook` + UI button (2026-05-30 grep); #5 Gallery JSON exists at `/api/simulation/public`. Batch closed.
- May-18 batch (3/5 addressed): #1→PR#91 merged; #2→PR#92 merged; #3 Per-Agent Sparklines, #4 Scenario Clone Button, #5 CN+JP README — still unbuilt
- May-16 batch (2/5 addressed): #3→PR#87 merged; #2→PR#90 merged; #1 oEmbed, #4 Peak-Round Analytics, #5 Operator Profile — still unbuilt
- May-14 batch (all 5 assessed): #1→PR#83 merged 2026-05-15, #2 exists at `/director/events`, #3→PR#85 merged, #4 exists at `/compare/:id1?/:id2?`, #5 Private Share Link unbuilt
- Open community issue #95 — French locale request (unanswered; May-22 #2 is the direct PR response)
- Older unbuilt: Operator Profile, Private Share Link
- Issue #70 on MiroShark — Cyril Private Impact mode + MiroResult collaboration request (substantial cross-builder feature track)
