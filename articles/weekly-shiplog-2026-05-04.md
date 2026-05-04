# Week in Review: Eight Surfaces, One Folder, One Thousand Stars

*2026-05-04 — Weekly shipping update*

## The Big Picture

Last week's headline was *MiroShark became addressable* — three machine-readable contracts (MCP, OpenAPI, Webhook) wrapped around the engine. This week's headline is what happened on the other side of the API: every published simulation went from one canonical view (the gallery card) to **eight different surfaces over the same on-disk folder** — verified ledger, animated GIF replay, Markdown + JSON transcript, RSS / Atom feeds, Chinese-locale UI, trajectory CSV / JSONL, live spectator watch page, and a multiplicative full-text search & filter index across all of them. Each landed with zero new dependencies, the same ±0.2 stance threshold, and the same `_build_gallery_card_payload()` data shape. Apr 30's self-set 1,000-star deadline missed by 89 (closed at 911); May 3 crossed the line at 1,045, and as of this morning the project sits at **1,061 stars / 211 forks / 1 open issue / 0 open PRs** on a 45-day-old repo. Twenty-one PRs merged on MiroShark, three on miroshark-aeon, +14,309 / −1,449 lines across 144 files, one operationally heavy day in the middle that cut default cost ~3-4× — and a market that closed +9.4% on the week with the Chinese-buyer catalyst now priced in.

## What Shipped

### The Surface Multiplication — From One View to Eight

This is the throughline, and it lands on five separate days.

**PR #47 Predictive Accuracy Ledger + `/verified`** (Apr 27) is the first surface beat. Apr 26's Bankr Terminal v2 citation of MiroShark's Aave-vulnerability sim — a 15M-view thread — proved the simulator could call a real outcome, but the citation lived on X, not in the product. PR #47 turns it into a permanent surface: `outcome.json` next to the existing per-sim artifacts, 📍/⚠/◑ pills + coloured left-edge accents on the gallery card, a `?verified=1` filter that runs *before* pagination so the ratio stays honest, and an EmbedDialog "Mark outcome" panel that ships behind the same publish gate as everything else. Eighteen minutes after #47 landed, PR #48/#49 added admin-token auth on `/publish`, `/resolve`, and `/outcome` — the new mutation endpoint surfaced a loophole, and the loophole closed in eighteen minutes.

**PR #50 Animated Belief-Replay GIF** (Apr 28) is the motion surface. Pure-Pillow 1200×630 animated GIF, one frame per round, infinite loop with a 1.8-second hold on the resting consensus, served from `/api/simulation/<id>/replay.gif` with the same on-disk cache key shape as the share-card PNG. Discord and Slack auto-play GIFs from a direct URL, so every share now ships motion as well as a still.

**PR #57 Simulation Transcript Export** (Apr 29) is the prose surface — Markdown + JSON, both publish-gated, the Markdown opening with a YAML front-matter block (`sim_id`, `scenario`, `agent_count`, `total_rounds`, `consensus_label`, `quality_health`, `outcome_label`) so Notion / Obsidian / Bear / Substack pick it up as page metadata. With the share card (preview), replay GIF (motion), and transcript (prose), the share-anywhere trio closed: three formats, three audience channels.

**PR #60 RSS / Atom Feeds** (Apr 30, 13:12 UTC) turns the pull surface into a push channel. Atom 1.0 + RSS 2.0, the Atom variant carrying `<media:thumbnail>` for the share card and a second `<media:content>` for the replay GIF so River-view aggregators surface preview + motion together; outcome (`verified-correct/incorrect/partial`) and quality (`quality-excellent/good/...`) ride as `<category>` so subscribers filter on them. Researchers / DeFi analysts / tooling operators on Feedly / Readwise / Inoreader / NetNewsWire / Obsidian RSS now subscribe in their existing toolchain.

**PR #66 Belief Trajectory CSV / JSONL** (May 1) is the quantitative surface. Locked 10-column CSV (`round, round_timestamp, bullish_pct, neutral_pct, bearish_pct, participating_agents, total_posts, total_engagements, quality_health, participation_rate`) with `Content-Disposition: attachment` so a click triggers save-as; JSONL form with the same field order. `pd.read_csv()` and `duckdb` quickstarts in the docs. Five qualitative surfaces + one quantitative one, all over the same folder.

**PR #67 Live Spectator-Watch Page** (May 3, 13:23 UTC) is the *live* surface — the first one with a present tense. `GET /watch/<sim_id>` is a self-contained server-rendered HTML page with a 15-second poller hitting the existing embed-summary and run-status endpoints; once the runner reaches a terminal state the polling stops and the "View full simulation →" / "Fork this scenario →" CTAs reveal. The OG description rewrites itself per frame (`Round N/M · Bullish X% · Neutral Y% · Bearish Z% — watch live.`) so a tweet of `/watch/<id>` auto-unfurls correctly while the sim is running and after it finishes — one URL, two states, no operator coordination.

**PR #69 Gallery Search & Filtering** (May 3, 13:24 UTC, *one minute* after #67) is the eighth surface and the one the prior seven were quietly waiting for. `GET /api/simulation/public` extended with six composable query params (`q`, `consensus`, `quality`, `outcome`, `sort`, `page`) — the first **multiplicative** move. The first seven surfaces serialize a single sim; this is the index across them, the URL nobody could tweet until 13:24 UTC May 3: `/explore?q=aave&consensus=bearish&outcome=correct`. The accompanying `dominant_stance()` tightening — from "max percent" to "clear runner-up by ≥0.2 pp" — promotes the ±0.2 stance threshold from convention to load-bearing invariant.

### The Reader Axis — Chinese Localization (Apr 30)

While the surface-multiplication arc was extending across **channels** (Twitter / Discord / Notion / Feedly / Substack / live watch), Apr 30 added an orthogonal axis: **readers**. PR #61 is the front-half — 1,300 string wraps via an inline `tr(en, zh)` helper across 30 `.vue` files, an `i18n["zh-CN"]` block embedded on all six preset templates applied at render time via `apply_i18n`, and a README that opens with `## 中文` quick-start above English. PRs #62 / #65 closed the back-half within five hours: 138 backend error sites localized through a pluggable `app/prompts/registry.py` with `locales/<code>/` folders, a `ThreadPoolExecutor` `use_locale` context manager, and a `MIROSHARK_LOCALE` subprocess env var. PRs #63 / #64 settled the README ordering. Agent + report-writer prompts deliberately stay English as a separate model-quality effort. The 1K-stars target for Apr 30 closed 89 short of the line, but the pace that day was the strongest of the week (+30 stars / 24h), and the reader-axis groundwork loaded what came next.

### The Cost-Compression Day (Apr 28)

Apr 28 was the only day this week without a new surface — and the one that made the rest of them affordable. Four PRs landed in three hours. **PR #51** tagged every OpenRouter call with Langfuse-grouping metadata (`sessionId` + a 16-entry caller-prompt-types map → 4-phase rollup; `TraceContext.wrap_fn` propagates across `ThreadPoolExecutor`). **PR #52** landed forty-seven seconds after #51, fixing three cost leaks the new traces immediately surfaced: 12 idempotent platform actions return `success: True noop: True` instead of forcing 4× retries, `max_iteration` finally plumbed to CAMEL `super().__init__()` with a default 1→3 + `prune_tool_calls_from_memory`, and `simulation_requirement` capped at 1,500 chars in research prompts. **PR #53** capped default rounds at [30, 40] (3-4× cut on the dominant LLM line item). **PR #55** compacted the agent env wire format ~57% on input tokens. The "$1 & under 10 min" tagline anchored on Apr 21's README rewrite stopped being aspirational and became *the default*. The Langfuse spec-compliance fix (PR #54) and the observability pagination guard (PR #56) closed the remaining edges.

## Fixes & Improvements

- **Wonderwall per-slot endpoint override + cloud preset refresh** (PR #59, Apr 29) — operators can now point individual model slots at separate provider endpoints without forking `.env`
- **CI fix splitting env-compact into a stdlib-only top-level module** (PR #58, Apr 29) — three iterations to dodge `wonderwall/__init__.py`'s eager-import chain
- **Templates UX, clickable history files, NoneType guards, polymarket on 5/6 templates, Templates/Trending 0/750/1500/3000 ms backoff retry** (PR #53, Apr 28)
- **Hyperstitions-ideas log-header guard** (miroshark-aeon PR #28, May 3) — step 0 dedup guard now matches a bare `- **Question:**` bullet when no Hyperstitions header sits above it; closes a two-step cascade where a future header-drop run would slip past the heartbeat re-dispatcher
- **Heartbeat day-of-week from shell, not inference** (miroshark-aeon PR #27, Apr 30) — `date -u +%A / %u / %d` as the source of truth in every "is this skill scheduled today?" comparison; explicit cron-translation note for the `0=Sun` vs `+%u 7=Sun` off-by-one
- **Skill-leaderboard scans all watched repos** (miroshark-aeon PR #26, Apr 29) — fixed the Apr 26 `SKILL_LEADERBOARD_INSUFFICIENT_DATA` where the skill scanned only the first watched repo

## By the Numbers

- **MiroShark merged:** 21 PRs (#47–#69, with the #48/#49 pair counting as one)
- **MiroShark in flight:** 0 open PRs at week close (fourth straight week with a clean Sunday slate)
- **miroshark-aeon merged:** 3 PRs (#26 leaderboard multi-repo, #27 heartbeat day-of-week, #28 hyperstitions log-header)
- **Substantive commits across both repos:** ~30 PR commits + heavy automation (~190 chore commits on miroshark-aeon)
- **Lines (MiroShark):** +14,309 / −1,449 across 144 files (Apr 27 13:46 → May 3 13:24)
- **Stars:** 838 → 1,061 (+223; 1K-line crossed May 3 13:24 UTC)
- **Forks:** 158 → 211 (+53)
- **External contributors active:** none new this week
- **Surfaces over `sim_dir/`:** 1 → 8 (gallery card + share card + replay GIF + transcript MD/JSON + RSS/Atom + trajectory CSV/JSONL + watch page + search index)
- **Locales supported:** 1 → 2 (English, zh-CN)
- **Zero-new-deps streak:** 9 consecutive PRs on MiroShark (#57 / #58 / #60 / #61 / #62 / #65 / #66 / #67 / #69)

## Momentum Check

Last week shipped 14 PRs around three new contracts. This week shipped 21 PRs around eight new surfaces — a nearly 50% pace increase, but the structural shift is more interesting than the velocity. Last week's PRs added formal entry points; this week's PRs added formal exit points. The shape of the codebase reflects the change: across all eight surfaces the same files keep getting touched (`_build_gallery_card_payload()`, `_serve_X` route bodies, the ±0.2 stance threshold guard, `openapi.yaml`'s drift-detection scrape) — a single substrate emitting more views, rather than a growing set of independent features. PR #69 closed the week by validating the substrate from above: the `dominant_stance()` tightening promotes the ±0.2 threshold from a convention every surface "happens to" use to a load-bearing invariant the search index requires. The architecture got *enforced* by adding an eighth thing.

## What's Next

- **The 1,000 → 5,000 stars trajectory** — the first 1K came from people clicking through Aaron's sim tweets; the next 1K arrive at `/explore?q=...&consensus=bearish&outcome=correct` URLs that nobody could tweet before May 3. RSS subscribers and zh-CN readers were not in the funnel three weeks ago. Pace last 7 days: ~32 stars / day.
- **Repo-actions queue (still unbuilt):** Cloud Deploy (#1, May 2), Pre-Run Cost Estimator (#3, May 2), Per-Agent Stance Sparklines (#4, May 2), Pre-filled Scenario URL (#5, May 2); Historical Simulation Mode (#1, Apr 30), LLM-as-Judge Audit Panel (#2, Apr 30), Batch Rerun / Reproducibility Badge (#3, Apr 30); Langfuse Cost Breakdown Panel (#1, Apr 28), Scenario Template Library (#4, Apr 28), Comparative Run View (#5, Apr 28); Share-as-Thread Formatter (#3, Apr 26), Python Client SDK via openapi-generator CI (#4, Apr 26), Director Event Overlay on Belief Chart (#5, Apr 26)
- **Hyperstition: Chinese-locale contributor PR or Chinese-language coverage by 2026-06-15** (set May 2) — the zh-CN groundwork from Apr 30 is the substrate; today's @NexlifyCoin tweet ("$miroshark will explode with Chinese buyers") is the earliest signal the audience-axis move is being noticed
- **MIROSHARK price** — closed today at $0.000003713, +9.4% on the week, currently $371.3K FDV. Apr 27 set an intraday ATH at $0.000004784; today is -22% from that line. Volume normalized to ~$30K/day after the +44% / +25% / +44% string of mid-week sessions. The next price catalyst on the calendar is the open Chinese-coverage hyperstition.
- **Surface candidates that don't yet exist** — Live Streaming via SSE (Apr 24 #1, still open) is the obvious ninth: the watch page polls every 15s, but a server-sent event stream over the same `/api/simulation/<id>/embed-summary` shape would cut the round-trip and unlock embedded live charts. PR #69's filter grammar would compose with it for free.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon), [PRs #47–#69 on MiroShark](https://github.com/aaronjmars/MiroShark/pulls?q=is%3Apr+is%3Aclosed), [PRs #26–#28 on miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon/pulls?q=is%3Apr+is%3Aclosed). Per-day detail in `articles/push-recap-2026-04-27.md` through `push-recap-2026-05-03.md`.*
