# Long-term Memory
*Last consolidated: 2026-05-10*

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
| 2026-05-09 | From Pointer to Graph | PR #76 Simulation Lineage Navigator (parent + public-only children, sorted oldest-first, capped 50) — turns reproduce.json's one-way `parent_simulation_id` into a navigable graph. |
| 2026-05-08 | Eleven Surfaces, One File Hash | PR #75 Reproducibility Config Export — bytewise-stable `reproduce.json` v1 schema (sort_keys + indent=2) makes SHA-256 a citation key for the 11-surface arc. |
| 2026-05-07 | MiroShark Stops Flying Blind | PR #74 (Surface Usage Analytics, inbound) + PR #73 (Webhook Delivery Log, outbound) merged 14 minutes apart — first coherent operator-observability layer over `sim_dir/`. |
| 2026-05-06 | The Webhook That Finally Talks Back | PR #73 frames first inward-facing surface — closes the loop on PR #46's outbound webhook with `webhook-log.jsonl` + Retry button. Webhook observability now its own 2026 subdomain. |
| 2026-05-05 | Aeon, Two Days Running | PR #71 + PR #72 both authored by Aeon — first time two consecutive same-day MiroShark distribution surfaces ship from the autonomous agent. Externally noticed by @russian_acai. |
| 2026-05-04 | The Way In | PR #71 Shareable Scenario Links (ninth surface, the *inverse* one — pre-fills New Sim form from `?scenario=`) + Issue #70 (Cyril Private Impact mode collab request, first cross-builder ask). |
| 2026-05-03 | The 1,001st Star and the Index That Followed | 1K-stars-crossed-3-days-late frame paired with PR #69 Gallery Search/Filter — first **multiplicative** surface, the index across the prior seven serializing surfaces. |
| 2026-05-02 | Live Was the Missing Tense | PR #67 Live Spectator Watch Page on first quiet-mainline day in 12+ days — first surface that updates *while sim is running*, the first with a present tense. |

## Recent Digests
Each row ≤180 chars. Full data in `articles/{token-report,push-recap}-YYYY-MM-DD.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-05-07 | push-recap | MiroShark PR #73 (webhook log) + PR #74 (surface analytics) merged; aeon PR #31 heartbeat header-line fix merged |
| 2026-05-08 | token-report | $0.00000437 (+1.17% 24h); FDV $436.6K; -37% from May 6 ATH; 1.35× buy ratio; vol $60.1K |
| 2026-05-08 | push-recap | MiroShark PR #75 (reproduce.json) merged; aeon PR #32 (MEMORY.md row caps) opened |
| 2026-05-09 | token-report | $0.000005080 (+15.48% 24h); FDV $508K; -26.6% from May 6 ATH; 1.24× buy ratio; vol $29.2K; +671% 30d |
| 2026-05-09 | push-recap | MiroShark PR #76 (lineage navigator) opened; aeon chore-only |
| 2026-05-10 | token-report | $0.00000646 (+30.6% 24h); FDV $645.9K; -6.7% from ATH; 1.19× buy ratio; vol $37.5K; +93.7% 7d / +443% 30d |

## Skills Built
Full implementation notes in daily logs. Each row ≤280 chars.

| Skill | Date | Notes |
|-------|------|-------|
| Webhook HMAC Signature Verification | 2026-05-11 | PR #79 — `WEBHOOK_SECRET` → `X-MiroShark-Signature: sha256=<hex>` on every dispatch (Stripe/GitHub scheme). `compute_signature` + `verify_signature` published for symmetry; backward compat when secret blank. 8 offline tests (urlopen-mock integration), Python/Node/curl docs snippets, EmbedDialog hint, zero new deps (streak: 18 PRs). |
| Trending Simulations Sort | 2026-05-10 | PR #78 — `?sort=trending` ranks public sims by `surface-stats.json` totals (date tie-break), turns inbound observability into discovery primitive. 8 offline tests, frontend "🔥 Trending" option, zero new deps (streak: 17 PRs). |
| Simulation Lineage Navigator | 2026-05-09 | PR #76 — `GET /api/simulation/<id>/lineage` reverse-pointer scan with public-only children, oldest-first, cap 50. New `lineage_service.py` (~390 LoC stdlib), 16 offline tests, EmbedDialog 🌳 panel. |
| Reproducibility Config Export | 2026-05-08 | PR #75 — `GET /api/simulation/<id>/reproduce.json` v1-schema citation primitive (scenario + agents + rounds + platforms + lineage). `repro_export.py` ~370 LoC stdlib, sort_keys+indent=2 → SHA-256 citation key. 22 tests. |
| Surface Usage Analytics | 2026-05-07 | PR #74 — first inbound observability surface. `surface-stats.json` per-sim counter (atomic tempfile write), `GET /api/simulation/<id>/surface-stats`. SURFACE_KEYS frozenset locks schema. 18 offline tests. |
| Webhook Delivery Log + Retry | 2026-05-06 | PR #73 — operational visibility over PR #46 outbound webhook. `webhook-log.jsonl` per attempt (URL-masked, 50-line atomic cap), GET log + POST retry, both admin-token gated. 13 offline tests. |
| Tweet Thread Export | 2026-05-05 | PR #72 — `GET /<id>/thread.txt` + `.json`, ≤280 chars/tweet, intro+body+close. Inflection-point selection with ±0.2 hysteresis, 15-tweet cap with 3+1+3 truncation bridge. 14 offline tests. |
| Project-Lens Angle Rotation | 2026-05-04 | aeon PR #29 — replaced unsatisfiable "no repeat in 14 days" with least-recently-used + 6-day floor + 8-category cycle. Math-aware preface added. Fixed 12 days of rationalized rule violations. |
| Shareable Scenario Links | 2026-05-04 | PR #71 — `?scenario=&url=&ask=&template=` query params pre-fill New Sim form, the *un-run scenario* counterpart to `/share/<id>`. Pure frontend, DOMPurify sanitization, zero new deps. 27 parser tests. |
| Gallery Search & Filtering | 2026-05-03 | PR #69 — `GET /api/simulation/public` extended with q/consensus/quality/outcome/sort/page (logical AND). New `gallery_filters.py` (~320 LoC stdlib), ±0.2 stance threshold parity. 33 offline tests. |
| Hyperstitions Log Header Resilience | 2026-05-02 | aeon PR #28 — mandates literal `## Hyperstitions Ideas` header + dedup-guard fallback for missing-header runs. Triggered by today's hyperstitions run that dropped its header. |

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
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; currently **1,126 stars / 224 forks** as of 2026-05-10
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18)
- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 (set 2026-05-02)
- Hyperstition: External operator running Aeon framework publicly under non-aaronjmars identity by 2026-06-30 (set 2026-05-09)
- $MIROSHARK ATH $0.000006926 set 2026-05-06 intraday; current $0.00000646 (+30.6% 24h on 2026-05-10, -6.7% from ATH, near-retest)

## Next Priorities
- Open MiroShark PRs: #79 (webhook HMAC signing, opened 2026-05-11)
- Open miroshark-aeon PRs: today's self-improve (re-doing closed PR #32 work — owner instruction)
- Unbuilt repo-actions ideas (2026-05-10 batch): #2 Jupyter Notebook Export, #3 Trading Signal JSON, #4 Per-Agent Stance Sparklines, #5 Simulation Archive Bundle (#1 Webhook HMAC shipped 2026-05-11 PR #79). Earlier batch (2026-05-08): #2 oEmbed Endpoint, #4 Peak-Round Snapshot, #5 Operator Profile
- Issue #70 on MiroShark — Cyril Private Impact mode + MiroResult collaboration request (substantial cross-builder feature track)
