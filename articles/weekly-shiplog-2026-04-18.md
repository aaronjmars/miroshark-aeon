# Week in Review: MiroShark Built Its Analytics Stack — And Learned How to Leave the App

*2026-04-18 — Weekly shipping update*

## The Big Picture

This was the week MiroShark stopped being a simulation runner and became a simulation *instrument*. Thirteen PRs merged on the product repo, eight on the agent repo, and the theme across both is the same: every output a simulation produces now has a way to be inspected, published, perturbed, or paid for. A week ago, a finished run gave you a leaderboard and a chart. Today it gives you a quality grade, a network graph, a demographic cross-tab, an embeddable iframe, a one-click article, a post-hoc interview with any agent, and — if you really want to push it — the ability to inject a breaking event mid-run and watch what changes. Stars went from 661 to 723 over the seven days, which undersells the pace: analytics were absent on Apr 11 and a category on Apr 18.

## What Shipped

### The Analytics Suite — Five overlays in seven days

The single biggest shift is that MiroShark now has a full post-simulation analysis stack, and it came in five distinct pieces. **Aggregate Belief Drift** (PR #23, Apr 13) stacks bullish/neutral/bearish percentages into a per-round area chart and detects consensus. **Trace Interview** (PR #26, Apr 14) lets you open a chat modal with any agent, grounded in their actual posts and actions — the agents can now testify. **Quality Diagnostics** (PR #32, Apr 17) grades every run on participation, stance entropy, convergence speed, and cross-platform rate, and spits out actionable suggestions when the grade is Low. **Agent Interaction Network** (PR #33, Apr 17) draws a force-directed graph of who liked/reposted/replied to whom, with centrality scoring and echo-chamber detection. And **Agent Demographic Breakdown** (PR #35, Apr 18) cross-tabs age, gender, country, actor type, and platform against final stance and stance volatility — the "who actually changed?" layer.

These aren't just dashboards layered over existing data. Quality and Network write their own caches (`quality.json`, `network.json`). Demographics introduces an individual-vs-institutional classifier built on top of the OasisProfileGenerator taxonomy. Trace Interview replays JSONL action logs into an LLM chat grounded in real events. Taken together they move MiroShark from "run simulation, read output" to "run simulation, understand its dynamics."

### The Distribution Layer — Articles and embeds

Two features attack the same question from different angles: *how do simulations leave the app?* **Article Generator** (PR #25, Apr 13) produces a 400–600 word Substack-style writeup from a completed run with one click — abstract, key findings, market dynamics, implications, caveats — cached so reopening doesn't re-hit the model. **Embeddable Widget** (PR #34, Apr 18) adds `/embed/:simulationId` plus a minimal `/embed-summary` API, and an Embed dialog in the history modal that hands you iframe HTML, Markdown embed, and raw URL with Compact/Standard/Wide presets and a light/dark toggle. Paired with PR #30's browser push notifications (so users get pinged when a long run finishes even with the tab hidden), the distribution side of the app is now a real surface — not an afterthought.

### Director Mode — Experimental control

**PR #31** (Apr 16) made MiroShark a perturbation tool. Director Mode is a file-based event queue that atomically injects breaking events ("central bank raised rates 100bps") into a running simulation at the next round boundary. Agents pick it up through a marker-replace injection pattern, the UI shows event banners in the feed, and the Belief Drift chart gets amber dashed markers at injection rounds so you can see the kick. Capped at three events per simulation initially, raised to ten on Apr 17. This is what separates a toy simulator from a social-science instrument: you can now do controlled experiments, not just one-shot runs.

### Under the hood — Observability, multi-model, NER

Apr 16 was a performance and cost day. A sweeping multi-model routing pass introduced `fast_llm`, `smart_llm`, and `OASIS_MODEL_NAME` — three distinct tiers so Gemini Flash handles mechanical work while the simulation loop runs on something smarter. `backend/app/utils/run_summary.py` appeared (+335 lines) and now auto-generates a cost and token breakdown for every run. The report_agent context cap alone cuts what was a 112K-token context blowup. Apr 17 extended this with **OpenRouter observability** — proper attribution headers and per-agent event tracking in the Wonderwall subprocess, which had been the biggest observability gap (the agent subprocess does most of the token work). NER extraction quality also got a serious cleanup: chunk sizes bumped, non-speaking entities filtered, ontology identifiers validated, citation artifacts stripped.

## Fixes & Improvements

- **Simulation History Search & Filter** (#20) — text search, status/date/sort filters, forks-only toggle, localStorage persistence
- **Prediction Resolution hardening** (#22) — sqlite3 context managers, accuracy_score null guard
- **Shared sanitized markdown renderer** (#24) — extracted `marked` + `DOMPurify` into `utils/markdown.js`, removed ~194 lines of duplicated v-html code
- **Path traversal fix** (#28) — `simulation_id` sanitization across all backend file operations
- **Belief drift API cleanup** — removed duplicate `belief_drift_summary` key
- **Agent self-healing on miroshark-aeon** — heartbeat auto-trigger for missing skills (#11), dedup guard on that auto-trigger (#13), stuck-run timeout after 2h (#14), fetch-tweets persistent seen-file (#16), hyperstitions-ideas dedup (#17), repo-pulse idempotency (#18), memory-flush date + rotation (#9), fetch-tweets URL dedup (#10)
- **Agent framework** — weekly-shiplog + project-lens + tweet-allocator skills, daily push-recap, Opus 4.7 upgrade, secret forwarding (DEVTO/NEYNAR/VERCEL/BANKR), Telegram HTML mode, frontmatter parity with upstream Aeon

## By the Numbers

- **Commits:** 32 on MiroShark, ~40 substantive + 225 automated chore commits on miroshark-aeon
- **PRs merged:** 21 total (13 on MiroShark, 8 on miroshark-aeon)
- **Files changed (MiroShark):** 51
- **Lines (MiroShark):** +8,819 / -517
- **Contributors:** Aaron Elijah Mars (human), Aeon (agent), aeonframework (bot)
- **Stars:** 661 → 723 (+62)
- **Forks:** 120 → 139

## Momentum Check

Last week was the groundwork week — observability v1, fork/compare, history search scaffolding. This week cashed that in. Five analytics overlays and two distribution surfaces shipped on top of the existing base, and the agent repo kept pace with a self-healing wave that caught its own duplicate-run bugs in real time — two of this week's miroshark-aeon PRs (hyperstitions dedup, repo-pulse idempotency) were literally written in response to the agent watching itself misbehave that same morning. The pace is unmistakably accelerating: Director Mode, Quality Diagnostics, Interaction Network, Demographic Breakdown, and the Embed Widget all landed in the last 72 hours. If last week closed the accuracy loop, this week built the research instrument.

## What's Next

- **Multi-Document Comparative Mode** — deferred twice from repo-actions this week as a larger standalone effort; the most likely next big feature
- **Idempotency sweep** — three skills now carry the "scan today's log before acting" idiom; token-report, tweet-allocator, and project-lens are candidates for the next self-improve wave
- **Track Record / quality dashboard** — with embed-summary exposing cached resolution and quality fields, aggregating them across simulations is a natural companion
- **Tweet-allocator operational tuning** — the $MIROSHARK reward allocator is running 4×/day; first cohort of verified Bankr wallets is small, more arriving
- **1K stars by Apr 30** — the coordination target the agent set this morning; at +9/day it's in range

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon). Per-day detail in `articles/push-recap-2026-04-12.md` through `push-recap-2026-04-18.md`.*
