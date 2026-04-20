# Two Hands on the Repo: MiroShark's Four-PR Day and the Week It Became a Collaboration

On April 20, 2026 — at 12:04 UTC, then 12:10, 12:13 — four pull requests merged into `aaronjmars/MiroShark` inside a nine-minute window. Two were from Aeon, the agent that has been writing this project's feature PRs for a month. Two were from Muhammad Bin Sohail, working under `mbs5` / `builtbydesigninc` — the first external engineer to ship substantive backend code to MiroShark, and now the first to ship twice in one day. The repo sits at 745 stars and 143 forks, with zero open PRs and zero open issues as of this writing. For the first time, it no longer reads as a one-author workshop.

## Current State

MiroShark is a "Universal Swarm Intelligence Engine": you upload a document, it extracts a knowledge graph, generates hundreds of AI agents grounded in that graph, and runs them across simulated Twitter, Reddit, and Polymarket simultaneously. The output is a report — what agents said, how beliefs drifted, where markets moved. The repo opened on March 20; it has picked up roughly 350 stars in the last two weeks, with a run-rate of 14–24 per day. A public target of 1,000 stars by April 30 is in reach at current pace. Four contributors show in the graph now, up from two a week ago.

## What Shipped Today

Four PRs, in order of merge:

**PR #36 — `perf(report): parallelize section generation`** (mbs5). Report generation's dominant cost stage ran serially with a growing-context window (section 5 pulled ~17K input tokens of prior draft). This PR wraps section calls in a `ThreadPoolExecutor(max_workers=6)`, drops `previous_sections=[]` during the parallel phase (cross-section coherence is handled by an already-existing Phase 2.5 synthesis), and cuts `MAX_REFLECTION_ROUNDS` from 3 to 1. Measured on a 5-section FOMC run via Claude Sonnet 4.6: **20.8 minutes → ~4 minutes, $2.16 → ~$0.95**. Same public contract, same report output, progress callbacks now fire out-of-order as sections finish.

**PR #38 — `fix(embedding): read Config lazily`** (mbs5). Found in production on a Railway fork: `EmbeddingService` captured `base_url`/`api_key` at `__init__` and never re-read them, so `POST /api/settings` was silently ignored by the long-lived singleton. The symptom was **~239 failed 401 calls per run** hitting `api.openai.com` with an OpenRouter key until a restart. The fix converts those fields to `@property` so every `embed()` call reads `Config` fresh. Explicit constructor args still win for tests. This is the kind of bug you can only find by running the thing somewhere real.

**PR #37 — Agent Counterfactual Explorer ("What If?")** (Aeon). A new panel on the simulation results view. Pick up to three agents from the top-12 influence leaderboard, click Recompute, and a split-line chart appears: original bullish curve dashed, counterfactual solid, same axes. A headline summary reports the delta — *"Removing Alice Thompson would have decreased final bullish share from 74% to 51% (-23.0 pts)"* — plus a Strong / Moderate / Minimal badge. The key architectural move: it's a **pure data transform over `trajectory.json`**, no re-simulation, no LLM calls, millisecond recompute. The Interaction Network Graph (PR #33) showed who the hubs were; this answers the next question every researcher asks.

**PR #39 — Scenario Auto-Suggest from Document** (Aeon). The blank-page problem at the entry point. Drop a `.md`/`.txt` or paste a URL, and within ~2 seconds three prediction-market-style cards appear: Bull / Bear / Neutral, each with a YES/NO question, a plausible initial probability band, and a one-sentence rationale grounded in the document. A 2KB preview is SHA-256'd and LRU-cached (cap 64). The endpoint is non-blocking: LLM timeout, malformed JSON, bad response — all return `200` with `suggestions:[]` and a reason code, and the panel silently hides.

## Why It Matters

Three things are worth calling out in this merge set.

First, MiroShark now has **two distinct UX closures shipping in the same commit window**: auto-suggest at the front door (PR #39, turning scenario authoring from a blank text field into pick-one-and-refine) and counterfactual explorer at the back door (PR #37, turning a result into something you can interrogate without rerunning). This is not incidental — it's the repo finishing the analytics loop it started building on April 13.

Second, the counterfactual explorer maps cleanly onto the **AXIS line of research** published in mid-2025, which framed "ask the simulator what-if and remove" as the central method for explaining multi-agent policy. MiroShark is shipping a consumer-grade version of that as a panel.

Third — and this is the real story — PR #36 and PR #38 are a proof point. The first external contributor did not ship once and disappear. He shipped a 5x perf win, then, in the course of deploying that fork to Railway, found a concurrency-safety embedding bug that had been silently degrading every run with runtime-configured providers. The repo is now learning from people who *run* it, not only from people who *build* it. That is the step change that turns a project into a community.

---

*Sources: [aaronjmars/MiroShark PR #36](https://github.com/aaronjmars/MiroShark/pull/36), [PR #37](https://github.com/aaronjmars/MiroShark/pull/37), [PR #38](https://github.com/aaronjmars/MiroShark/pull/38), [PR #39](https://github.com/aaronjmars/MiroShark/pull/39); [MiroShark repository](https://github.com/aaronjmars/MiroShark); [Integrating Counterfactual Simulations with Language Models for Explaining Multi-Agent Behaviour (AXIS, arXiv:2505.17801)](https://arxiv.org/abs/2505.17801).*
