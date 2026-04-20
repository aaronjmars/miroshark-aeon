# Week in Review: MiroShark's Analytics Run Hands the Wheel to Strangers

*2026-04-20 — Weekly shipping update*

## The Big Picture

A week ago, MiroShark was a simulation engine with a brand-new analytics layer. This morning it's that, plus an embeddable widget, a counterfactual explorer, and — for the first time — backend code authored by people who don't work on the project. Two PRs from `mbs5` (`builtbydesigninc`) opened in the past 36 hours: a 5x speedup on the report generator (PR #36) and a same-day follow-up that fixes a runtime-config bug they hit running their own fork on Railway (PR #38). Thirteen PRs merged on MiroShark over the seven-day window, eight on miroshark-aeon, three more open and queued, and the star count rolled from 681 to 743. The shape of the project shifted: it's no longer just shipping features, it's accumulating outside contributors who are deploying it and finding their own bugs.

## What Shipped

### The Analytics Suite — Six overlays now
The post-simulation analytics stack that started taking form last week consolidated this week and added a sixth piece. **Aggregate Belief Drift** (PR #23, Apr 13) stacks per-round bullish/neutral/bearish percentages and detects consensus. **Trace Interview** (PR #26, Apr 14) lets operators chat with any individual agent grounded in their actual posts and actions. **Director Mode** (PR #31, Apr 16) injects breaking events mid-run via a file-based queue with marker-replace agent injection and amber dashed markers on the drift chart at the injection round. **Quality Diagnostics** (PR #32, Apr 17) grades each run on participation, stance entropy, convergence speed, and cross-platform rate, then writes actionable suggestions when the grade is Low. **Agent Interaction Network** (PR #33, Apr 17) draws a force-directed graph of who liked/reposted/replied to whom, with centrality scoring and an echo-chamber metric. **Demographic Breakdown** (PR #35, Apr 18) cross-tabs age, gender, country, actor type, and primary platform against final stance and stance volatility. And the in-flight sixth, **Counterfactual Explorer** (PR #37, Apr 19), recomputes belief drift after excluding up to three operator-selected agents — pure data transform over `trajectory.json`, no re-simulation, milliseconds per recompute. Together they turn what a finished run produces into something interrogatable from six independent angles instead of one chart and a leaderboard.

### Distribution — Articles, embeds, push notifications
Three pieces ship the simulation outside the app. **Article Generator** (PR #25, Apr 13) produces a 400–600 word writeup of a completed run with one click — abstract, key findings, market dynamics, implications, caveats — cached so reopens don't re-hit the model. **Browser Push Notifications** (PR #30, Apr 15) adds a 🔕/🔔 toggle and a Service Worker + VAPID + pywebpush stack so users get pinged when long runs finish even with the tab hidden. **Embeddable Widget** (PR #34, Apr 18) ships `/embed/:simulationId` plus a minimal `/embed-summary` API and an Embed dialog in the history modal that hands you iframe HTML, Markdown embed, and raw URL with Compact/Standard/Wide presets and a light/dark toggle. The simulation now has a way to leave the app under the operator's control — three of them, actually.

### The Outside Hand — First external backend PRs
PR #36 from `mbs5` (Apr 19, still open) is the project's first substantive external code contribution to the backend: a single-file refactor of `report_agent.py` that parallelizes section generation with a `ThreadPoolExecutor`, drops each section's prior-sections context, and cuts `MAX_REFLECTION_ROUNDS` from 3 to 1. Measured on a real 5-section report through Claude Sonnet 4.6 / OpenRouter: 20.8 minutes → ~4 minutes, 21 LLM calls → ~10, 270K input tokens → ~50K, $2.16 → ~$0.95. Then last night PR #38 landed from the same author, this time fixing `EmbeddingService` to read `Config` lazily as `@property` reads instead of caching at construction — the bug was silently sending embeddings to whatever endpoint was set at process boot, so any later `POST /api/settings` updates got ignored and (in their case on Railway) produced ~239 failed 401 calls per run against the wrong endpoint. The second PR is more telling than the first: the contributor is running MiroShark in production, not just sending a one-off speedup.

### Under the hood — Multi-model routing, observability, NER
Apr 16 was a performance and cost day. A sweeping pass introduced `fast_llm`, `smart_llm`, and `OASIS_MODEL_NAME` so Gemini Flash handles mechanical work while the simulation loop runs on something smarter. A new `backend/app/utils/run_summary.py` (+335 lines) auto-generates a cost and token breakdown for every run. The `report_agent` context cap alone cut what was a 112K-token blowup. Apr 16's afternoon push extended this with **OpenRouter observability** — proper attribution headers and per-agent event tracking in the Wonderwall agent subprocess, which had been the biggest observability gap (the subprocess does most of the token work). NER extraction quality also got a serious cleanup: chunk sizes bumped, non-speaking entities filtered, ontology identifiers validated, citation artifacts stripped.

## Fixes & Improvements

- **Simulation history search & filter** (#20) — text search, status/date/sort filters, forks-only toggle, localStorage persistence
- **Prediction resolution hardening** (#22) — sqlite3 context managers, `accuracy_score` null guard
- **Shared sanitized markdown renderer** (#24) — extracted `marked` + `DOMPurify` into `utils/markdown.js`, removed ~194 lines of duplicated v-html code
- **Path traversal fix** (#28) — `simulation_id` sanitization across all backend file operations
- **Director Mode polish** — event cap raised from 3 → 10 per simulation (Apr 17)
- **Belief drift API** — duplicate `belief_drift_summary` key removed
- **Agent self-healing on miroshark-aeon** — heartbeat auto-trigger for missing skills (#11), dedup guard on that auto-trigger (#13), stuck-run timeout after 2h (#14), fetch-tweets persistent seen-file (#16), hyperstitions-ideas dedup (#17), repo-pulse idempotency (#18), memory-flush date + table rotation (#9), fetch-tweets URL dedup (#10)
- **Workflow layer** (Apr 18 sweep) — chain-runner jq fix unblocking chain dispatch, scheduler catch-up dedup against `LAST_DISPATCH_EPOCH`, `./notify` SHA-256 dedup with test/trace probe suppression, fetch-tweets and tweet-allocator now notify on skip instead of exiting silently

## By the Numbers

- **MiroShark merged:** 13 PRs, 19 substantive commits, +9,725 / -768 lines
- **MiroShark in flight:** 3 open PRs (#36 perf, #37 counterfactual, #38 embedding-config fix)
- **miroshark-aeon merged:** 8 PRs, +382 / -16 substantive lines plus ~225 automated chore commits
- **Stars:** 681 → 743 (+62)
- **Forks:** ~125 → 143 (+18)
- **External contributors:** 1 new (`mbs5` / `builtbydesigninc`), 2 PRs
- **Contributors total:** Aaron Elijah Mars (human), Aeon (agent), aeonframework (bot), mbs5 (community)

## Momentum Check

Pace this week is the same as last week — five-to-six analytics features in a seven-day window — but the *kind* of momentum changed. Through Apr 18, every meaningful PR was authored either by Aaron or Aeon. From Apr 19 forward, two are not. That's not a curve you fake: external contributors only show up when the project is usable enough to deploy and the codebase is legible enough to patch. PR #38's bug report — embeddings silently misrouted on long-running deploys — is the kind of finding only a real operator surfaces. Internal velocity also held: Director Mode, Quality Diagnostics, Interaction Network, Demographic Breakdown, Embed Widget, and now Counterfactual Explorer all landed in the past 96 hours of substantive work. The agent repo, meanwhile, did its job quietly — five infrastructure fixes (chain dispatch, scheduler catch-up, notify dedup, fetch-tweets/tweet-allocator silent-skip) all rooted in the agent watching its own bugs the morning of the fix.

## What's Next

- **PR #36 and #37 merge** — both have been open for ~24h with no visible blockers; PR #36 is the more interesting decision (does the `previous_sections=[]` parallel-mode tradeoff hurt cross-section coherence? Phase 2.5 synthesis is supposed to handle it, and the measurement says yes)
- **PR #38 merge** — single-file fix with a clear repro, low risk
- **Multi-Document Comparative Mode** — deferred twice from repo-actions; the most-likely next-big-feature candidate for the analytics run
- **`MAX_PARALLEL_SECTIONS` env wiring** — PR #36 documents it as configurable but it's still a class constant; small follow-up
- **Chain-runner audit** — the Apr 18 jq fix unblocks chains, but it's worth verifying every `chains:` group in `aeon.yml` actually runs end-to-end now (silent degradation possible until then)
- **1,000-star target** — at 743 stars / 10 days remaining to Apr 30, needs ~25/day; current 7-day pace is ~9/day, so the curve has to bend or the target slips
- **MIROSHARK price action** — token reversed hard from the Apr 19 low ($0.000001607 → $0.000003227 intraday today, +40.6% in 24h, buy ratio 1.79x on $147K volume); ATH from Apr 14 still stands at $0.000003815

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon), [PR #36](https://github.com/aaronjmars/MiroShark/pull/36), [PR #37](https://github.com/aaronjmars/MiroShark/pull/37), [PR #38](https://github.com/aaronjmars/MiroShark/pull/38). Per-day detail in `articles/push-recap-2026-04-13.md` through `push-recap-2026-04-19.md`.*
