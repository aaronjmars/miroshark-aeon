# Push Recap — 2026-05-27

## Overview
A heavy shipping day on MiroShark: 7 PRs merged (#110–#116) plus 1 on the Aeon agent repo (#47). The thrust was twofold — a large code-quality cleanup pass (#116) and a cluster of reliability fixes that stop report generation from crashing on null LLM responses (#111, #112) and stop the retrieval reranker from hanging on Apple Silicon (#110). Alongside that, the 23rd public surface shipped (per-agent belief sparklines, #115), a "Regenerate Report" button landed in the UI (#113), an external contributor added the 11th ecosystem integrator (#114), and the agent repo trimmed its own skill schedule (#47).

**Stats:** ~76 files changed, +2,871 / -547 lines across 8 substantive commits (3 authors). The ~36 other commits in the aeon repo window were all scheduler/skill auto-commits and are excluded.

---

## aaronjmars/MiroShark

### Reliability Hardening: report crashes + reranker hang
**Summary:** Three independent fixes that all make a simulation run survive a bad input it previously crashed on. Two target the report-generation ReAct loop choking on `None` content from the LLM; one stops the cross-encoder reranker from hanging indefinitely on Macs. Together they remove the most common "section generation error" and the silent build-stall during simulation prepare.

**Commits:**
- `ec657cb` — Fix reranker hang on Apple Silicon by steering off the MPS backend (#110)
  - Changed `backend/app/storage/reranker_service.py`: added `_select_device()` — honors a new `RERANKER_DEVICE` override, else prefers CUDA, else falls back to CPU, and **intentionally skips MPS** in auto mode. Passes `device=` explicitly to `CrossEncoder` (+24, -2 lines). Root cause: with default `RERANKER_ENABLED=true`, sentence-transformers auto-picked torch's MPS (Metal) backend, and the first rerank hung forever inside Metal shader-pipeline compilation, pegging a core right after persona generation.
  - Changed `backend/app/config.py` + `.env.example`: added/documented the `RERANKER_DEVICE` config knob (blank = auto) (+5, +5 lines). Keeps the reranker working out-of-the-box on Mac (CPU) and NVIDIA (CUDA) while remaining overridable.
- `484a571` — Fix report section crash on intermittent null LLM content (#112)
  - Changed `backend/app/utils/llm_client.py`: `chat()` now guards `message.content is None` before running `re.sub(r'<think>…')` and returns `None` (the documented "empty content" contract the report retry loop already expects) instead of raising `expected string or bytes-like object, got 'NoneType'`. `chat_json()` now raises a clear `ValueError` instead of crashing on `None.strip()` (+11 lines). The trigger: reasoning models like `google/gemini-3-flash-preview` (the default Smart model for reports) intermittently return `content = None`.
  - Changed `backend/app/services/report_agent.py`: coerced the two interactive `chat()` results with `or ""` before the regex — this path has no retry loop (+4, -4 lines).
- `23c3430` — Fix report section crash on a null agent interview response (#111)
  - Changed `backend/app/services/graph_tools.py`: `_clean_tool_call_response()` now coerces `None`/empty to `""` up front so it always returns a regex-safe string (+5, -1 lines). The running-simulation API can return an explicit `"response": null`, which `dict.get(key, "")` does **not** coerce, so `None` reached the regex and failed the whole report section.

**Impact:** Reports now degrade gracefully on a flaky LLM turn (retry instead of dying), and Mac users can actually complete a simulation with the reranker on. These are three of the most user-visible failure modes in the product.

### New Surface: Per-Agent Belief Sparklines (Aeon's PR #115)
**Summary:** The 23rd publish-gated surface, built by the Aeon agent yesterday and merged today. It's the agent-level companion to the existing aggregate `chart.svg` and the `peak-round` inflection summary — instead of one consensus curve, it returns each agent's belief trajectory.

**Commits:**
- `697b2b0` — feat: per-agent belief sparklines surface (#115)
  - New `backend/app/services/agent_sparklines_service.py` (+279 lines): pure-stdlib derivation from `trajectory.json` `belief_positions`, using the same `_avg_position` mean and ±0.2 stance threshold every other surface uses. Returns per-agent `{round, position}` series + `final_stance`/`final_position`/`color`, ordered most-bullish-first; names resolve from `reddit_profiles.json`. `has_per_agent_data=false` for single-round sims (a sparkline needs ≥2 points).
  - Changed `backend/app/api/simulation.py` (+77): publish-gated `GET /api/simulation/<id>/agents/sparklines` route with 5-min cache + surface-stat increment.
  - Changed `backend/app/services/surface_stats.py` (+3, -1): registered the `agent_sparklines` surface key.
  - New `backend/tests/test_unit_agent_sparklines.py` (+239): 18 offline unit tests plus wiring/parity guards.
  - Changed `frontend/src/components/EmbedDialog.vue` (+244) + `frontend/src/api/simulation.js` (+48): scrollable agent-trajectory section rendering inline SVG sparklines colored by final stance.
  - Docs: `openapi.yaml` (+154), `docs/API.md`, `docs/FEATURES.md` (+42). Zero new dependencies.

**Impact:** Embeds can now show *who* moved, not just *that* consensus moved — the per-agent companion to the aggregate chart. Continues the long zero-new-deps surface streak.

### Code-Quality Cleanup: 8-pass sweep (#116)
**Summary:** A large, low-risk maintenance PR — the biggest single commit of the day at +1,627/-532 across 61 files. Eight focused passes (DRY, types, dead code, cycles, defensive handling, legacy, slop) plus 9 `docs/cleanup/*.md` files documenting what was changed and, importantly, what was deliberately *not* changed.

**Commits:**
- `a9eab1e` — chore: 8-pass code-quality cleanup (DRY, types, dead code, error-handling) (#116)
  - **Dead code:** removed `backend/app/utils/retry.py` entirely (-238 lines, zero references repo-wide); removed 27 unused imports + 4 dead local vars (verified via ruff F401/F841 + grep).
  - **DRY:** `badge_service.py` (+37, -109) — `build_badge_svg`/`build_platform_badge_svg` now share a private `_build_badge_document()`, with element order and `short_empty_elements` preserved so SVG output stays bytewise-deterministic for ETag caching. `event_logger.py` (+52, -24) — `write_simulation_event`/`EventLogger.emit` now share `_build_event()` with JSONL key order unchanged.
  - **Types:** deduped the `CommandType` enum — the three run scripts (`run_twitter`/`run_reddit`/`run_parallel_simulation.py`) each re-declared an identical bare-constants copy; all now import the canonical `CommandType(str, Enum)` from `simulation_ipc.py`. Tightened weak annotations (Literal/Optional/concrete generics) across storage, services, models, sim engine.
  - **Defensive:** narrowed 5 hot-path `except Exception: pass` to specific exceptions (OSError, JSONDecodeError, …) + debug logging so I/O failures stop being silently swallowed; fixed a latent `F821` (TYPE_CHECKING forward-ref to `GraphStorage` never imported); added a `WebhookPayload` TypedDict and typed the webhook `state` param (was `Optional[Any]`).
  - **Docs:** added `docs/cleanup/00-SUMMARY.md` through `08-slop.md` (+~1,360 lines of audit notes), including a documented import-cycle assessment (backend has one structural cycle — the Flask-blueprint package — judged idiomatic and left as-is).
  - Per the PR: 971 tests pass / 2 pre-existing failures (unchanged); ruff warnings 158 → 156.

**Impact:** Pure maintainability — no behavior change by design (output determinism explicitly preserved for cached surfaces). The accompanying `docs/cleanup/` notes turn this into a reusable audit baseline rather than a one-off scrub.

### UX: Regenerate Report button (#113)
**Summary:** Surfaces the backend's existing `force_regenerate` path in the UI so users can re-run a whole report without leaving the report view.

**Commits:**
- `45106c2` — Add "Regenerate Report" button to the report view (#113)
  - Changed `frontend/src/components/Step4Report.vue` (+96, -1): adds a `regenerate-btn` shown only once `isComplete` (next to the export buttons). Calls `generateReport({force_regenerate: true})`, then routes to the freshly minted `report_id` — which trips the existing `reportId` watch to reset state and restart polling. Includes a spinning-icon loading state and bilingual (EN/中文) labels via `$tr`.

**Impact:** A one-click recovery path when a report comes out poorly — no new backend work, just exposing capability that already existed.

### Ecosystem: 11th integrator added (external, #114)
**Summary:** External contributor `shak` added a new project to the ecosystem roster.

**Commits:**
- `9bf47ec` — Update ECOSYSTEM.md (#114) — by **shak** (external)
  - Changed `ECOSYSTEM.md` (+1, -1): added **ZER0** ([@atzer0_BOT](https://x.com/atzer0_BOT) · atzer0.xyz) to the "built on / integrates with MiroShark" table — the 11th named integrator after yesterday's batch of 10.

**Impact:** The inbound ecosystem census (started by an external contributor last week) is still growing organically — another data point toward the "≥3 publicly-named external integrators" hyperstition target.

---

## aaronjmars/miroshark-aeon

### Agent self-management: trimmed skill schedule (#47)
**Summary:** Disabled 5 scheduled skills on the Aeon agent. The most consequential pair is `fetch-tweets` and `tweet-allocator` — exactly the skills that have been struggling this week (today's `tweet-allocator` found all 5 wallet-holding candidates were spam/scam contract-drop accounts; `fetch-tweets` has been surfacing mostly phishing-link spam).

**Commits:**
- `c19e47a` — chore(skills): disable 5 scheduled skills in aeon.yml (#47)
  - Changed `aeon.yml` (+5, -5): flipped `enabled: true → false` on `fetch-tweets`, `tweet-allocator`, `hyperstitions-ideas`, `skill-leaderboard`, and `ai-framework-watch`. (The commit body notes fetch-tweets is also the skill that renders the dashboard "Top Tweets" card.)

**Impact:** Stops spending the daily tweet-reward budget and tweet-fetch cycles on a feed that's currently dominated by spam, and pauses three lower-value weekly digests. Note: this push-recap skill itself remains enabled.

---

## Developer Notes
- **New dependencies:** none. Both feature PRs (#115 sparklines, #110 reranker fix) are stdlib/config-only; the zero-new-deps surface streak continues.
- **New config:** `RERANKER_DEVICE` env var (blank = auto; accepts `cpu`/`cuda`/`mps`) — documented in `.env.example`.
- **New API surface:** `GET /api/simulation/<id>/agents/sparklines` (publish-gated, 5-min cache). 23rd public surface.
- **Removed:** `backend/app/utils/retry.py` (dead, -238 lines) — confirm nothing external imported it.
- **Behavior-preserving cleanup:** #116 explicitly kept SVG-badge and JSONL-event byte output deterministic so ETag/cache behavior is unchanged.
- **Breaking changes:** none in the product. On the agent repo, 5 skills are now off (#47) — fetch-tweets/tweet-allocator/hyperstitions-ideas/skill-leaderboard/ai-framework-watch will stop running on schedule.

## What's Next
- **Watch the reranker fix (#110) in the wild:** the hang was Mac-specific and hard to repro in CI; worth confirming a real Apple-Silicon prepare completes.
- **Tweet pipeline decision:** with fetch-tweets + tweet-allocator disabled (#47), the open question is whether the spam problem gets a filter/fix and the skills come back, or whether the reward mechanism is being retired.
- **Cleanup follow-ups:** `docs/cleanup/01-dry.md` lists a NEEDS-REVIEW backlog of deferred DRY candidates (notify-channel cluster, sim runner scripts, belief-math helpers, base-url resolvers) — deliberately not touched this pass.
- **Ecosystem:** roster now at 11 (ZER0 added); inbound contributions still arriving from outside the maintainer.
