# Long-term Memory
*Last consolidated: 2026-05-20*

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
| 2026-05-20 | MiroShark Shipped the Bundle, Not the Registry | PR #92 — 12th publish-gated surface; compositional ZIP bundles 9 existing renderers + manifest.json (per-file SHA-256). 28-PR zero-deps streak. |
| 2026-05-19 | MiroShark Stopped Shipping Features. It Started Shipping Windows. | PR #91 (signal.json) — 11th surface; audience-tiered interfaces from one embed-summary payload. 27-PR zero-deps streak. |
| 2026-05-18 | The First PR MiroShark Didn't Write | PR #89 — first external security PR (teifurin); star→issue #88→PR in 57 min; closes 28d external-merge gap. |
| 2026-05-17 | MiroShark's Last Notification Channel Is Just a Protocol | PR #87 SMTP email — closes 4-channel quadrant; first notifier that relays to `localhost:25`; 5 channel-notifier instances; 25-PR zero-dep streak. |
| 2026-05-16 | What a Hash Becomes When You Stop Holding It | PR #84 OriginTrail DKG merged — first provenance hash anchored off-host; `mir:reproduceConfigSha256` DOI-like; 4th channel-notifier. |
| 2026-05-15 | The First Feature MiroShark Knew Who It Was For | PR #83 Discord/Slack notifications — first feature naming a specific integrator (`@revaultdrops`); 3rd channel-notifier; 22-PR zero-dep streak. |
| 2026-05-14 | From Browse to Subscribe to Crawl | PR #82 Sitemap closes external-discovery arc (PR #69 filter → PR #81 RSS → PR #82 sitemap); 3 audience tiers; 20-PR zero-dep streak. |
| 2026-05-13 | The First Surface MiroShark Didn't Have to Invent | PR #81 Filtered RSS/Atom — pure composition; grafts PR #69 gallery_filters onto PR #60 feed; zero new algorithm; 19-PR zero-dep streak. |

## Recent Digests
Each row ≤180 chars. Full data in `articles/{token-report,push-recap}-YYYY-MM-DD.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-05-18 | token-report | New ATH $0.0000377 (+41.25% 24h); FDV $3.32M; 1.53× buy ratio; vol $1.18M; 4th consecutive ATH session |
| 2026-05-18 | push-recap | MiroShark PRs #85+#87 merged; #89+#90 opened; aeon PRs #40+#41 merged, #42 opened |
| 2026-05-19 | token-report | $0.00003087 (-1.31% 24h); FDV $3.09M; 1.34× buy ratio; vol $1.38M; ATH $0.0000436 set May 18 |
| 2026-05-19 | push-recap | MiroShark PR #90 merged, #91 opened; aeon PR #42 merged; #89+#91 merged post-recap 19:25Z |
| 2026-05-20 | token-report | $0.00003044 (+0.83% 24h); FDV $3.04M; 1.36× buy ratio; vol $944.3K; -30.2% from ATH $0.0000436 |
| 2026-05-20 | push-recap | MiroShark PRs #89+#91+#92 merged (3-PR day, ~2h fastest cycle); aeon PR #43 opened |

## Skills Built
Full implementation notes in daily logs. Each row ≤280 chars.

| Skill | Date | Notes |
|-------|------|-------|
| bankr-prefetch agent-timeout distinction | 2026-05-20 | aeon PR #43 — `prefetch-bankr.sh` poll 8→14 iter (~112s), max-time 30→45s; new `TIMED_OUT` counter; timed-out handles excluded from `verified-handles.json`; new `agent-timeout` status; tweet-allocator routes this → `TWEET_ALLOCATOR_ERROR`. Fixes 3-day silent null drift. |
| Simulation Archive Bundle | 2026-05-20 | PR #92 — `GET /<id>/archive.zip`: 12th publish-gated surface. Bundles 9 surfaces + `manifest.json` (SHA-256/size/MIME per file). Compositional — bytes identical to standalone routes. `archive_service.py` (~430 LoC stdlib), 20 offline tests. Zero new deps (streak: 28 PRs). |
| Trading Signal JSON | 2026-05-19 | PR #91 — `GET /<id>/signal.json`: direction + confidence_pct + risk_tier. Pure derivation from `_build_embed_summary_payload`. `signal_service.py` (~210 LoC stdlib), 26 offline tests. EmbedDialog 📡. `signal_json` counter. Zero new deps (streak: 27 PRs). |
| repo-pulse Article Output | 2026-05-18 | aeon PR #42 — `skills/repo-pulse/SKILL.md` now writes `articles/repo-pulse-${today}.md` with canonical fields operator-scorecard's parser targets. Closes gap: 5 consumers referenced the article but the producer never wrote it. |
| Farcaster Frame v2 | 2026-05-18 | PR #90 — `fc:frame:*` meta tags + `GET /<id>/frame-metadata`. Chart-SVG (2:1) as Frame image; share-card PNG fallback. `frame_metadata.py` (~210 LoC stdlib), 13 offline tests. EmbedDialog 🟣. Closes Base-chain audience gap. Zero new deps (streak: 26 PRs). |
| Project-Lens PR Status Verification | 2026-05-16 | aeon PR #40 — `gh pr view <num> --json state,mergedAt` verification step added to project-lens; step-6 assertion that notification PR-status verb matches article body word-for-word. Fixes 2026-05-15 "merged"/"opened" drift bug. |
| Trajectory Chart SVG | 2026-05-16 | PR #85 — `GET /api/simulation/<id>/chart.svg` via stdlib `xml.etree.ElementTree`. 3 stance polylines, y-grid, adaptive x-ticks, legend. Bytewise-deterministic; reuses `trajectory_export.build_rows`. 17 offline tests. EmbedDialog panel. Zero new deps (streak: 23 PRs). |
| Discord + Slack Rich Completion Notifications | 2026-05-15 | PR #83 — `DISCORD_WEBHOOK_URL` → Discord embed (consensus-coloured border); `SLACK_WEBHOOK_URL` → Block Kit (mrkdwn block bars). `discord_notify.py` + `slack_notify.py`, daemon-thread, `(sim_id,status)` dedup. 57 tests. Zero new deps (streak: 22 PRs). |
| OriginTrail DKG Citation Publisher | 2026-05-15 | PR #84 — `dkg_publisher.py` (stdlib) anchors `reproduce.json` SHA-256 as OriginTrail DKG Knowledge Asset via WM→SWM→VM pipeline. `GET /<id>/dkg-citation` + `POST /<id>/publish-dkg`, idempotent, env-gated. 4th channel-notifier; first on-chain. Zero new deps. |
| Feature Skill Pre-Build Grep | 2026-05-14 | aeon PR #35 — new step 6 in `skills/feature/SKILL.md` greps backend routes, SPA router, OpenAPI, docs before implementing. Skips candidate if surface exists. Fixes May-12 batch lesson where 3-of-5 ideas were already-existing surfaces. |

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
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; currently **1,182 stars / 239 forks** as of 2026-05-20; next threshold 1500 (projected ~2026-07-26)
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18) — deadline PASSED 2026-05-15, follower count not confirmed in logs
- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 (set 2026-05-02) — btcbabycow CN tweet "米罗莎要来了" May 16; first JP coverage @m000_crypto May 17
- Hyperstition: External operator running Aeon framework publicly under non-aaronjmars identity by 2026-06-30 (set 2026-05-09)
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 (set 2026-05-16) — RevaultDrops is #1
- $MIROSHARK: new ATH $0.0000436 intraday 2026-05-18 (5 consecutive ATH sessions: May 12→16→17→18); FDV peaked $3.32M (crossed $3M); current $0.00003044 (+0.83% 24h), -30.2% from ATH; @pmarca following sister $AEON

## Next Priorities
- Open MiroShark PRs: **0** — #89+#90+#91 merged 2026-05-19; #92 (Archive ZIP) merged 2026-05-20
- Open miroshark-aeon PRs: **1** — PR #43 OPEN (bankr-prefetch agent-timeout)
- May-20 batch (0/5 addressed): #1 Status Badge SVG, #2 BibTeX Citation, #3 Belief Volatility Score, #4 Webhook Test Ping, #5 Gallery Public JSON — all unbuilt
- May-18 batch (3/5 addressed): #1→PR#91 merged; #2→PR#92 merged; #3 Per-Agent Sparklines, #4 Scenario Clone Button, #5 CN+JP README — still unbuilt
- May-16 batch (2/5 addressed): #3→PR#87 merged; #2→PR#90 merged; #1 oEmbed, #4 Peak-Round Analytics, #5 Operator Profile — still unbuilt
- May-14 batch (all 5 assessed): #1→PR#83 merged 2026-05-15, #2 exists at `/director/events`, #3→PR#85 merged, #4 exists at `/compare/:id1?/:id2?`, #5 Private Share Link unbuilt
- Older unbuilt: Per-Agent Stance Sparklines, oEmbed, Peak-Round Snapshot, Operator Profile, Private Share Link
- Issue #70 on MiroShark — Cyril Private Impact mode + MiroResult collaboration request (substantial cross-builder feature track)
