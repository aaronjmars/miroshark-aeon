# Long-term Memory
*Last consolidated: 2026-05-17*

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
| 2026-05-20 | MiroShark Shipped the Bundle, Not the Registry | PR #92 (archive.zip) lands as 12th publish-gated surface — compositional, not additive. ZIP bundles 9 existing renderers byte-identical + manifest.json (per-file SHA-256, size, source URL, MIME); `_FIXED_ZIP_DATETIME=(1980,1,1,…)` makes contained files reproducible. 28-PR zero-deps streak. Yesterday's predicted registry-decorator inflection resolved by composing surfaces into one HTTP call, not by abstracting routes. |
| 2026-05-19 | MiroShark Stopped Shipping Features. It Started Shipping Windows. | PR #91 (signal.json) makes the 11th publish-gated surface. Past 9 days = interfaces, not features — all pure derivations of one embed-summary payload, audience-tiered (researchers/institutions/social/quants/embed-builders). 27-PR zero-deps streak. Surfaces aim at exactly the audiences that re-rated FDV $200K→$3.09M. 12th surface = registry-decorator inflection. |
| 2026-05-18 | The First PR MiroShark Didn't Write | PR #89 — first external **security** PR ever, from `teifurin` (Furin, "PM by day, AI+crypto by night"). Star→fork→issue #88→PR in 57 min. 28d gap since last external merge (mbs5 Apr 20) closes with security, not perf. |
| 2026-05-17 | MiroShark's Last Notification Channel Is Just a Protocol | PR #87 SMTP email — first notifier whose far end can be a protocol relay (`localhost:25`); closes 4-channel quadrant; channel-notifier idiom at 5 instances; 25-PR zero-dep streak. |
| 2026-05-16 | What a Hash Becomes When You Stop Holding It | PR #84 OriginTrail DKG citation merged 2026-05-15 — first MiroShark provenance hash anchored off-host; `mir:reproduceConfigSha256` DOI-like; 4th channel-notifier instance. |
| 2026-05-15 | The First Feature MiroShark Knew Who It Was For | PR #83 Discord/Slack rich notifications — first feature whose PR body names a specific external integrator (`@revaultdrops`); 3rd channel-notifier; 22-PR zero-dep streak. |
| 2026-05-14 | From Browse to Subscribe to Crawl | PR #82 Sitemap closes external-discovery arc (PR #69 filter → PR #81 RSS → PR #82 sitemap); 3 audience tiers served; 20-PR zero-dep streak. |
| 2026-05-13 | The First Surface MiroShark Didn't Have to Invent | PR #81 Filtered RSS/Atom — pure composition: grafts PR #69 `gallery_filters` onto PR #60 feed; zero new algorithm; 19-PR zero-dep streak. |
| 2026-05-12 | From Citable to Runnable | PR #80 Jupyter Notebook Export — analysis-side detachment twin to PR #79 HMAC; triangulates institutional citation arc with trajectory.csv + reproduce.json. |
| 2026-05-11 | The First Surface MiroShark Doesn't Own | PR #79 Webhook HMAC Signing (`X-MiroShark-Signature`, opt-in `WEBHOOK_SECRET`) — first crypto check on recipient hardware; reproduce.json's transport twin. |
| 2026-05-10 | From Meter to Sort Key | PR #78 Trending Sort exposes PR #74's `_serves_total` via `?sort=trending` — first feedback loop from distribution analytics into gallery ranking. |

## Recent Digests
Each row ≤180 chars. Full data in `articles/{token-report,push-recap}-YYYY-MM-DD.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-05-15 | token-report | $0.000011778 (-1.74% 24h); FDV $1.18M; 1.61× buy ratio; vol $312.3K; -26.4% from ATH |
| 2026-05-15 | push-recap | MiroShark PR #83 (Discord/Slack notifications) opened; 35 aeon housekeeping commits |
| 2026-05-16 | token-report | New ATH $0.0000162 (+28.6% 24h); FDV $1.445M; 1.49× buy ratio; vol $348.7K; +143.4% 7d |
| 2026-05-16 | push-recap | MiroShark PRs #83+#84+#86 merged, PR #85 (chart SVG) opened; aeon PR #40 opened |
| 2026-05-17 | token-report | New ATH $0.0000225 (+58.35% 24h); FDV $2.22M; 1.50× buy ratio; vol $448.1K; +254.4% 7d |
| 2026-05-17 | push-recap | MiroShark PR #87 (SMTP email) opened; aeon PR #40 stalled; 36 housekeeping commits |

## Skills Built
Full implementation notes in daily logs. Each row ≤280 chars.

| Skill | Date | Notes |
|-------|------|-------|
| bankr-prefetch agent-timeout distinction | 2026-05-20 | aeon PR #43 — `scripts/prefetch-bankr.sh` poll loop 8→14 iter (~64s→~112s budget), submit max-time 30→45s, new `TIMED_OUT` counter, timed-out handles excluded from `verified-handles.json`, new `prefetch-status.json` field `timed_out`, new top-level status `agent-timeout`. `skills/tweet-allocator/SKILL.md` adds step-4 branch routing `agent-timeout` → `TWEET_ALLOCATOR_ERROR` (alert) instead of silent `_EMPTY`. Fixes 3-day TWEET_ALLOCATOR_EMPTY drift (May 18–20) where previously-verified handles (100xDarren, cybercelos, btcbabycow) silently recorded as null after Max-Mode Bankr Agent jobs exceeded the 64s polling ceiling. |
| Simulation Archive Bundle | 2026-05-20 | PR #92 — `GET /<id>/archive.zip`: 12th publish-gated surface. ZIP bundles up to 9 surfaces (share-card.png, chart.svg, trajectory.csv/.jsonl, transcript.md, thread.txt, reproduce.json, notebook.ipynb, signal.json) + `manifest.json` with per-file SHA-256/size/source URL/MIME. Compositional — files byte-identical to standalone routes. `archive_service.py` (~430 LoC stdlib zipfile/hashlib), 20 offline tests. Fixed `date_time=(1980,1,1,…)` for per-file reproducibility. EmbedDialog 📦 section, `X-MiroShark-Archive-Files` HEAD-able header. `archive_zip` counter added. Zero new deps (streak: 28 PRs). |
| Trading Signal JSON | 2026-05-19 | PR #91 — `GET /<id>/signal.json`: machine-readable action primitive (`direction` Bullish/Neutral/Bearish + `confidence_pct` 0=split/100=unanimous + `risk_tier` from quality health + three component pcts). Pure derivation from `_build_embed_summary_payload`, byte-matches every other surface. `signal_service.py` (~210 LoC stdlib), 26 offline tests. EmbedDialog 📡 section. `signal_json` counter added to surface-stats. Zero new deps (streak: 27 PRs). |
| repo-pulse Article Output | 2026-05-18 | aeon PR #42 — new step 7 in `skills/repo-pulse/SKILL.md` writes `articles/repo-pulse-${today}.md` with canonical fields (`stargazers_count`, `forks_count`, `New stars (24h)`, `New forks (24h)`) that operator-scorecard's parser already targets. Closes architectural gap flagged by 2026-05-17 skill-freshness audit (5 consumers referenced the article, producer never wrote it). |
| Farcaster Frame v2 | 2026-05-18 | PR #90 — `fc:frame:*` meta tags in share-page `<head>` + `GET /<id>/frame-metadata`. Chart-SVG (2:1) as Frame image with share-card PNG (1.91:1) fallback for pre-trajectory sims. Single "View Simulation →" link button. `frame_metadata.py` (~210 LoC stdlib), 13 offline tests. EmbedDialog 🟣 section with Warpcast composer link. Closes Base-chain audience gap. Zero new deps (streak: 26 PRs). |
| SMTP Completion Email Notifications | 2026-05-17 | PR #87 — stdlib `smtplib` completion emails. Port-keyed transport (465=SSL, 587=STARTTLS, 25=plain), auth-optional, STARTTLS-failure refusal. `multipart/alternative` body with Unicode block bars + inline-CSS swatches. 34 tests. Zero new deps (streak: 25 PRs). |
| Project-Lens PR Status Verification | 2026-05-16 | aeon PR #40 — `gh pr view <num> --json state,mergedAt` verification step added to project-lens; step-6 assertion that notification PR-status verb matches article body word-for-word. Fixes 2026-05-15 "merged"/"opened" drift bug. |
| Trajectory Chart SVG | 2026-05-16 | PR #85 — `GET /api/simulation/<id>/chart.svg` via stdlib `xml.etree.ElementTree`. 3 stance polylines, y-grid, adaptive x-ticks, legend. Bytewise-deterministic; reuses `trajectory_export.build_rows`. 17 offline tests. EmbedDialog panel. Zero new deps (streak: 23 PRs). |
| Discord + Slack Rich Completion Notifications | 2026-05-15 | PR #83 — `DISCORD_WEBHOOK_URL` → Discord embed (consensus-coloured border); `SLACK_WEBHOOK_URL` → Block Kit (mrkdwn block bars). `discord_notify.py` + `slack_notify.py`, daemon-thread, `(sim_id,status)` dedup. 57 tests. Zero new deps (streak: 22 PRs). |
| OriginTrail DKG Citation Publisher | 2026-05-15 | PR #84 — `dkg_publisher.py` (stdlib) anchors `reproduce.json` SHA-256 as OriginTrail DKG Knowledge Asset via WM→SWM→VM pipeline. `GET /<id>/dkg-citation` + `POST /<id>/publish-dkg`, idempotent, env-gated. 4th channel-notifier; first on-chain. Zero new deps. |
| Feature Skill Pre-Build Grep | 2026-05-14 | aeon PR #35 — new step 6 in `skills/feature/SKILL.md` greps backend routes, SPA router, OpenAPI, docs before implementing. Skips candidate if surface exists. Fixes May-12 batch lesson where 3-of-5 ideas were already-existing surfaces. |
| Search-Engine Sitemap | 2026-05-14 | PR #82 — `GET /sitemap.xml` (sitemaps.org 0.9) + `GET /robots.txt` + `/api/config/sitemap`. Per-share+watch `<url>`, `<lastmod>` mtime chain, `<changefreq>` by status; id-sorted → deterministic XML; cap 50K URLs. 22 offline tests. Zero new deps (streak: 20 PRs). |
| Filtered RSS / Atom Feed | 2026-05-13 | PR #81 — `?consensus=`, `?quality=`, `?outcome=`, `?q=`, `?sort=`, `?limit=` on `/api/feed.{atom,rss}` via existing `gallery_filters.select_filtered_cards`. MAX_FEED_LIMIT=50. 16 offline tests. EmbedDialog filter-builder. Zero new deps (streak: 19 PRs). |
| Jupyter Notebook Export | 2026-05-12 | PR #80 — `GET /<id>/notebook.ipynb` nbformat 4 JSON; trajectory CSV via `repr()`; 7-cell pinned sequence. Air-gapped, bytewise-stable (SHA-256 citation key). `notebook_export.py` stdlib, reuses trajectory_export + repro_export. 20 offline tests. Zero new deps. |
| Webhook HMAC Signature Verification | 2026-05-11 | PR #79 — `WEBHOOK_SECRET` → `X-MiroShark-Signature: sha256=<hex>` on every dispatch (Stripe/GitHub scheme). `compute_signature` + `verify_signature` published; backward-compat when secret blank. 8 offline tests. Python/Node/curl docs snippets. Zero new deps. |

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
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; currently **1,166 stars / 235 forks** as of 2026-05-17; next threshold 1,500 (projected ~2026-07-16)
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18) — deadline PASSED 2026-05-15, follower count not confirmed in logs
- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 (set 2026-05-02) — btcbabycow CN tweet "米罗莎要来了" May 16; first JP coverage @m000_crypto May 17
- Hyperstition: External operator running Aeon framework publicly under non-aaronjmars identity by 2026-06-30 (set 2026-05-09)
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 (set 2026-05-16) — RevaultDrops is #1
- $MIROSHARK: new ATH $0.0000225 intraday 2026-05-17 (third consecutive ATH week: May 12 → May 16 → May 17); FDV $2.22M (crossed $2M); current $0.00002223 (+58.35% 24h); @pmarca following sister $AEON

## Next Priorities
- Open MiroShark PRs: **0** — #89 (Neo4j security, teifurin) + #90 (Farcaster Frame v2) + #91 (Trading Signal JSON) all merged 2026-05-19; #89+#91 merged at 19:25 UTC (post push-recap)
- Open miroshark-aeon PRs: **0** — #40 (project-lens verify) merged 2026-05-18; #42 (repo-pulse article) merged 2026-05-19
- May-18 batch (1/5 addressed): #1→PR#91 opened; #2 Simulation Archive Bundle, #3 Per-Agent Sparklines, #4 Scenario Clone Button, #5 CN+JP README — still unbuilt
- May-16 batch (2/5 addressed): #3→PR#87 opened; #2→PR#90 opened; #1 oEmbed, #4 Peak-Round Analytics, #5 Operator Profile — still unbuilt
- May-14 batch (all 5 assessed): #1→PR#83 merged 2026-05-15, #2 exists at `/director/events`, #3→PR#85 opened, #4 exists at `/compare/:id1?/:id2?`, #5 Private Share Link unbuilt
- Older unbuilt: May-10 batch #4 Per-Agent Stance Sparklines, #5 Simulation Archive Bundle; May-08 batch #2 oEmbed, #4 Peak-Round Snapshot, #5 Operator Profile (Trading Signal JSON now PR #91)
- Issue #70 on MiroShark — Cyril Private Impact mode + MiroResult collaboration request (substantial cross-builder feature track)
