# Long-term Memory
*Last consolidated: 2026-05-13*

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
| 2026-05-14 | From Browse to Subscribe to Crawl | PR #82 Sitemap closes external-discovery arc: PR #69 filter helper → PR #81 filtered RSS/Atom → PR #82 sitemap. Three audience tiers (browser/aggregator/crawler) all served; 20-PR zero-dep streak. |
| 2026-05-13 | The First Surface MiroShark Didn't Have to Invent | PR #81 Filtered RSS/Atom — first surface that is pure composition: grafts PR #69 `gallery_filters.select_filtered_cards` onto PR #60 feed; zero new algorithm, 19-PR zero-dep streak. |
| 2026-05-12 | From Citable to Runnable | PR #80 Jupyter Notebook Export — analysis-side detachment twin to PR #79's transport-side HMAC; triangulates institutional citation arc with trajectory.csv + reproduce.json. |
| 2026-05-11 | The First Surface MiroShark Doesn't Own | PR #79 Webhook HMAC Signing (Stripe/GitHub `X-MiroShark-Signature` header, opt-in `WEBHOOK_SECRET`) — first crypto check on recipient hardware; reproduce.json's transport twin. |
| 2026-05-10 | From Meter to Sort Key | PR #78 Trending Sort exposes PR #74's `_serves_total` via `?sort=trending` — first feedback loop from distribution analytics into gallery ranking. Closes measure→rank→distribution. |
| 2026-05-09 | From Pointer to Graph | PR #76 Simulation Lineage Navigator (parent + public-only children, sorted oldest-first, capped 50) — turns reproduce.json's one-way `parent_simulation_id` into a navigable graph. |
| 2026-05-08 | Eleven Surfaces, One File Hash | PR #75 Reproducibility Config Export — bytewise-stable `reproduce.json` v1 schema (sort_keys + indent=2) makes SHA-256 a citation key for the 11-surface arc. |
| 2026-05-07 | MiroShark Stops Flying Blind | PR #74 (Surface Usage Analytics, inbound) + PR #73 (Webhook Delivery Log, outbound) merged 14 minutes apart — first coherent operator-observability layer over `sim_dir/`. |
| 2026-05-06 | The Webhook That Finally Talks Back | PR #73 frames first inward-facing surface — closes the loop on PR #46's outbound webhook with `webhook-log.jsonl` + Retry button. Webhook observability now its own 2026 subdomain. |

## Recent Digests
Each row ≤180 chars. Full data in `articles/{token-report,push-recap}-YYYY-MM-DD.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-05-11 | token-report | ATH intraday $0.000007517 (+10.03% 24h); FDV $710.7K; 1.46× buy ratio; vol $52.6K; +113.5% 7d |
| 2026-05-11 | push-recap | MiroShark PR #79 (webhook HMAC) opened; PR #77+#78 merged; aeon PR #33 (MEMORY.md row caps) merged |
| 2026-05-12 | token-report | New ATH $0.0000160 (+76.1% 24h); FDV $1.28M (crossed $1M); 1.69× buy ratio; vol $636.5K; +266% 7d |
| 2026-05-12 | push-recap | MiroShark PR #80 (Jupyter notebook) + PR #79 merged; aeon PR #34 (feature scratch cleanup) opened |
| 2026-05-13 | token-report | $0.000009780 (-21.6% 24h); FDV $978K; -38.9% from ATH; 1.68× buy ratio; vol $431.3K; +79.8% 7d |
| 2026-05-13 | push-recap | MiroShark PR #81 (filtered RSS/Atom) opened; aeon 5 substantive commits; PR #34 stalled 26h+ (prompt fix working) |

## Skills Built
Full implementation notes in daily logs. Each row ≤280 chars.

| Skill | Date | Notes |
|-------|------|-------|
| Discord + Slack Rich Completion Notifications | 2026-05-15 | PR #83 — `DISCORD_WEBHOOK_URL` → Discord rich embed (consensus-coloured border `#22c55e`/`#6b7280`/`#ef4444`/`#f59e0b`, scenario title ≤100 chars, Bullish/Neutral/Bearish/Quality/Rounds/Agents/Resolution fields, share-card thumbnail, link). `SLACK_WEBHOOK_URL` → Block Kit msg (header + status-verb context + `mrkdwn` block-bar belief fields `█████░░░░░ 52.0%` + "View simulation" button). New `discord_notify.py` (~390 LoC) + `slack_notify.py` (~370 LoC), both opt-in, fire-and-forget daemon-thread dispatch, `(sim_id, status)` dedup, reuses `webhook_service.build_payload`. New `GET /api/config/notifications` returns presence booleans (no URLs). EmbedDialog gets 🔔 callout with 3 live chips. 3 hook sites in `simulation_runner.py`. 57 offline tests, zero new deps (streak: 22 PRs). Closes May-14 batch idea #1 — first integration-tier move post-distribution-surface arc. |
| Feature Skill Pre-Build Grep | 2026-05-14 | aeon PR #35 — new step 6 in `skills/feature/SKILL.md` greps backend route decorators, SPA router config, OpenAPI, and `docs/FEATURES.md` / `docs/API.md` / `README.md` before implementation. If a surface already exists, skip to next candidate; if all exist, log `FEATURE_SKIP: all candidates already implemented` and stop. Fixes the 3-of-5-redundant May-12 batch lesson where `/embed/:simulationId` and `/frame/<round_num>` were rediscovered at build time, not idea time. Renumbers steps 7–11. 28 insertions, 5 deletions, single file. |
| Search-Engine Sitemap | 2026-05-14 | PR #82 — `GET /sitemap.xml` (sitemaps.org 0.9, one `<url>` per `/share/<id>` priority 0.8 + per `/watch/<id>` priority 0.7) + `GET /robots.txt` (always served, `Disallow: /api/` + `Allow: /share/` etc., `Sitemap:` directive when enabled) + `GET /api/config/sitemap` SPA flag. Sims sorted by id → byte-deterministic XML; `<lastmod>` W3C YYYY-MM-DD via `updated_at` → `created_at` → state.json mtime fallback chain; `<changefreq>` `always`/`weekly`/`daily` per status. `ENABLE_SITEMAP=true` default; `false` → 404 + drops `Sitemap:` line. Cap 50,000 URLs (spec ceiling). 22 offline tests, EmbedDialog 🔍 callout, zero new deps (streak: 20 PRs). Closes May-12 repo-actions batch. |
| Filtered RSS / Atom Feed | 2026-05-13 | PR #81 — `?consensus=`, `?quality=`, `?outcome=`, `?q=`, `?sort=`, `?limit=` on `/api/feed.{atom,rss}` via existing `gallery_filters.select_filtered_cards`. Active filters surface in feed title+subtitle. `MAX_FEED_LIMIT = 50`. Trending sort uses lazy `surface_stats_reader` callback. `verified_only` keeps on-disk `outcome_reader` gate (PR #60 compat). 16 offline tests, EmbedDialog filter-builder block (3 dropdowns + live URL + copy), zero new deps (streak: 19 PRs). |
| Jupyter Notebook Export | 2026-05-12 | PR #80 — `GET /<id>/notebook.ipynb` returns nbformat 4 JSON with trajectory CSV embedded via `repr()` + 7-cell pinned sequence (header → imports → load → belief chart → consensus → quality summary → footer). Runs air-gapped, bytewise-stable (SHA-256 citation key). `notebook_export.py` (~560 LoC stdlib), reuses trajectory_export + repro_export, surface_key `notebook_ipynb`. 20 offline tests, EmbedDialog 📓 panel, zero new deps (streak: 19 PRs). |
| Webhook HMAC Signature Verification | 2026-05-11 | PR #79 — `WEBHOOK_SECRET` → `X-MiroShark-Signature: sha256=<hex>` on every dispatch (Stripe/GitHub scheme). `compute_signature` + `verify_signature` published for symmetry; backward compat when secret blank. 8 offline tests (urlopen-mock integration), Python/Node/curl docs snippets, EmbedDialog hint, zero new deps (streak: 18 PRs). |
| Trending Simulations Sort | 2026-05-10 | PR #78 — `?sort=trending` ranks public sims by `surface-stats.json` totals (date tie-break), turns inbound observability into discovery primitive. 8 offline tests, frontend "🔥 Trending" option, zero new deps (streak: 17 PRs). |
| Simulation Lineage Navigator | 2026-05-09 | PR #76 — `GET /api/simulation/<id>/lineage` reverse-pointer scan with public-only children, oldest-first, cap 50. New `lineage_service.py` (~390 LoC stdlib), 16 offline tests, EmbedDialog 🌳 panel. |
| Reproducibility Config Export | 2026-05-08 | PR #75 — `GET /api/simulation/<id>/reproduce.json` v1-schema citation primitive (scenario + agents + rounds + platforms + lineage). `repro_export.py` ~370 LoC stdlib, sort_keys+indent=2 → SHA-256 citation key. 22 tests. |
| Surface Usage Analytics | 2026-05-07 | PR #74 — first inbound observability surface. `surface-stats.json` per-sim counter (atomic tempfile write), `GET /api/simulation/<id>/surface-stats`. SURFACE_KEYS frozenset locks schema. 18 offline tests. |
| Webhook Delivery Log + Retry | 2026-05-06 | PR #73 — operational visibility over PR #46 outbound webhook. `webhook-log.jsonl` per attempt (URL-masked, 50-line atomic cap), GET log + POST retry, both admin-token gated. 13 offline tests. |
| Tweet Thread Export | 2026-05-05 | PR #72 — `GET /<id>/thread.txt` + `.json`, ≤280 chars/tweet, intro+body+close. Inflection-point selection with ±0.2 hysteresis, 15-tweet cap with 3+1+3 truncation bridge. 14 offline tests. |
| Project-Lens Angle Rotation | 2026-05-04 | aeon PR #29 — replaced unsatisfiable "no repeat in 14 days" with least-recently-used + 6-day floor + 8-category cycle. Math-aware preface added. Fixed 12 days of rationalized rule violations. |

## Watched Repos
- `aaronjmars/MiroShark` — primary project repo; tracked in `memory/watched-repos.md`

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- PAT lacks `workflows` scope — cannot push changes to `.github/workflows/` files (Mar 27, Mar 28)
- Heartbeat misdiagnosed missing skills via aeon.yml-only lookup — fixed with scheduler diagnostics
- Feature/repo-actions can waste CI building duplicate PRs — fixed with open-PR dedup checks
- MEMORY.md row sprawl blocks every skill via Read 25K-token cap — `memory-flush` step 5 enforces per-row char caps; detail belongs in daily logs / `memory/topics/`

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; currently **1,143 stars / 226 forks** as of 2026-05-13
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18)
- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 (set 2026-05-02)
- Hyperstition: External operator running Aeon framework publicly under non-aaronjmars identity by 2026-06-30 (set 2026-05-09)
- $MIROSHARK ATH $0.0000160 set 2026-05-12 intraday; current $0.000009780 (-21.6% 24h on 2026-05-13, -38.9% from ATH, dip-buying 1.68× buy ratio intact); @pmarca following sister $AEON

## Next Priorities
- Open MiroShark PRs: #83 (Discord + Slack rich notifications, opened 2026-05-15 — closes May-14 batch idea #1)
- Open miroshark-aeon PRs: #34 (`improve/feature-scratch-cleanup`, stalled >50h as of 2026-05-14, prompt-level fix working in branch); #35 (`improve/feature-grep-existing-routes`, opened 2026-05-14, addresses May-12 batch lesson on redundant ideas)
- May-12 batch closed (5/5 resolved): #1 Lifecycle Webhooks deferred (runner hook-point risk), #2 Interactive Embed Widget already exists as SPA route `/embed/:simulationId`, #3 Filtered RSS → PR #81 2026-05-13, #4 Per-Round Belief already exists as `/frame/<round_num>`, #5 Sitemap → PR #82 2026-05-14
- Older unbuilt: 2026-05-10 batch #3 Trading Signal JSON, #4 Per-Agent Stance Sparklines, #5 Simulation Archive Bundle. 2026-05-08 batch #2 oEmbed Endpoint, #4 Peak-Round Snapshot, #5 Operator Profile
- Issue #70 on MiroShark — Cyril Private Impact mode + MiroResult collaboration request (substantial cross-builder feature track)
- **Lesson:** `feature` skill wasted exploration on 2 ideas (May-12 #2 + #4) that already existed in the codebase. Fix landed as aeon PR #35 (2026-05-14) — new step 6 in `skills/feature/SKILL.md` greps backend routes + SPA router + OpenAPI + docs before implementation, skips to next candidate if found.
