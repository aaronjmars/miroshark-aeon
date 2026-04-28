# Push Recap — 2026-04-28

## Overview

Three PRs merged on MiroShark in a 75-minute window today (12:56 → 14:10 UTC), all authored by aaronjmars and co-authored by aeonframework + Claude Opus 4.7 (1M context). The day split cleanly into one distribution-side ship — PR #50 Animated Belief Replay GIF — and a paired observability/cost cycle that landed back-to-back: PR #51 wired Langfuse-grouping metadata onto every OpenRouter call, and PR #52, merged 47 seconds later, fixed the retry-loop and context-bleed bugs that PR #51's traces had exposed. miroshark-aeon shipped no substantive commits today (only ~25 chore auto-commits from the cron scheduler).

**Stats:** 21 files changed, +1,513 / −59 lines across 3 substantive commits.

---

## aaronjmars/MiroShark

### Distribution: Animated Belief Replay GIF (PR #50)

**Summary:** New `GET /api/simulation/<id>/replay.gif` endpoint and an Embed-dialog player render per-round belief drift as a 1200×630 animated GIF — same OG aspect as the existing share card, so unfurl shapes stay consistent across static and animated formats. Discord and Slack auto-play GIFs from a direct file URL, so dropping the link in a channel renders the animation inline. This is the third of three "publishing-loop" surfaces in two days (Apr 27 share-card refinements → Apr 27 `/verified` page → today's GIF).

**Commits:**
- `28bf97f` — *feat: animated belief-replay GIF endpoint + Embed dialog player (#50)* — merged 12:56 UTC
  - New `backend/app/services/replay_gif.py` (+519 lines): pure-Pillow renderer (zero new deps; Pillow already pinned for the share card). One frame per round with bullish/neutral/bearish bars, round counter, progress bar. `loop=0` infinite repeat, `disposal=2` to clear ghosting on shrinking bars, `FRAME_MS=600` per frame with `FINAL_HOLD_MS=1800` final hold so the resting consensus reads as the punch-line. `MAX_FRAMES=60` cap with even subsampling that always preserves the final round (so 200-round sims compress to ≤60 frames and stay under ~36 s playback).
  - Modified `backend/app/api/simulation.py` (+61 lines): new `/<sim_id>/replay.gif` route on `simulation_bp`, same publish gate + 403/404 envelope as the share card, cached on disk by content hash at `<sim_dir>/replay-gifs/<hash>.gif`, `Cache-Control: public, max-age=3600`. Empty trajectory falls back to a single-frame "Belief trajectory not available yet" poster so the endpoint never 500s on a freshly published READY run.
  - New `backend/tests/test_unit_replay_gif.py` (+326 lines): 14 offline tests including GIF signature + dimension via raw byte parse, frame count via `PIL.ImageSequence`, MAX_FRAMES subsampling preserving final round, empty/missing/misaligned belief arrays, single-round case, oversized scenario wrap, cache-key stability under float jitter, route-decorator presence.
  - Modified `backend/openapi.yaml` (+24 lines): adds `/api/simulation/{id}/replay.gif` under the Publish & Embed tag with `image/gif` response — drift-detection test passes on first run.
  - Modified `frontend/src/api/simulation.js` (+21 lines): new `getReplayGifUrl()` helper.
  - Modified `frontend/src/components/EmbedDialog.vue` (+241 lines): "Belief replay (animated)" section beneath the share card with paused tap-to-play overlay (so opening the dialog doesn't pull GIF bytes for every viewer — the `<img>` mounts only on click, not just hidden via CSS), copyable URL, Download GIF button, dark color palette to differentiate from the static-card row above.
  - Plus `README.md` Features row + `docs/FEATURES.md` "Animated Belief Replay (GIF)" section.

**Impact:** Distribution multiplier for the 1K-stars-by-Apr-30 sprint (2 days left) — every share now ships motion as well as a still. Source: repo-actions Apr 26 idea #2; idea #1 (Predictive Accuracy Ledger) shipped yesterday as PR #47.

---

### Observability + cost cycle: tag every call, then plug the leaks (PR #51 → PR #52, merged 47 seconds apart)

**Summary:** PR #51 (merged 14:09:24 UTC) and PR #52 (merged 14:10:10 UTC) are a paired "diagnose-then-fix" sequence built off a Langfuse cost investigation. PR #51 mirrors the existing miroshark-api Langfuse setup so every OpenRouter call lands in Langfuse with a `sessionId`, useful tags, and a meaningful `traceName` instead of a flat list of "OpenRouter Request" rows — which is what made the next step possible. PR #52, merged 47 seconds later, applies the three fixes that PR #51's traces had just surfaced: an idempotent-tool retry loop in Wonderwall agents, an unbounded ReAct iteration count, and a multi-KB simulation-requirement leak into every entity-research prompt. The "find it, then fix it" cadence shows up cleanly in the merge timestamps.

**Commits:**

- `66a85ba` — *feat: tag every OpenRouter call with Langfuse-grouping metadata (#51)* — merged 14:09:24 UTC, +225 / −17 across 10 files
  - `backend/app/utils/llm_client.py` (+90, −7 lines): new `_CALLER_PROMPT_TYPES` map (16 entries: `report_outline`, `report_section`, `report_synthesis`, `report_chat`, `ontology_design`, `ner_extraction`, `persona_generation`, `sim_config`, `graph_extract`, `web_research`, `agent_action`) and `_PROMPT_TYPE_PHASES` map (`setup` / `round` / `report`). Every chat call now writes `extra["metadata"]` with `caller / prompt_type / sim_phase / run_id / simulation_id / agent_name / agent_id / round`, sets `extra["user"] = sim_id` (OpenRouter forwards `user` to Langfuse as `sessionId`, which is how every call from one sim ends up under one session), populates `extra["tags"] = ["miroshark", prompt_type, f"phase:{sim_phase}", f"run:{run_id}"]` for the Langfuse filter sidebar, and sets `extra["name"] = prompt_type or caller` so the trace list shows a useful label per row instead of every line reading "OpenRouter Request".
  - `backend/app/utils/trace_context.py` (+35, −1): new `TraceContext.wrap_fn(fn)` helper that snapshots the parent thread's context and re-applies it inside `ThreadPoolExecutor` workers (Python's `threading.local` does not propagate across pool workers — the wrapper also explicitly clears existing context first because thread-pool threads are reused and stale context from a previous task would otherwise leak into the next). Three new context fields: `run_id`, `sim_phase`, `prompt_type`.
  - `backend/app/services/graph_builder.py` (+14, −1): tags `add_text_batches` with `sim_phase="setup", prompt_type="graph_extract"` and uses `TraceContext.wrap_fn(_process_chunk)` so the per-chunk worker pool inherits the tags. Clears the tags after the call so a follow-up phase doesn't inherit "setup".
  - `backend/app/services/wonderwall_profile_generator.py` (+7, −1): same `TraceContext.wrap_fn` pattern around `generate_single_profile` so the persona-generation worker pool keeps its tags.
  - `backend/app/services/simulation_manager.py` (+14, −1): pins `simulation_id` for the whole `prepare_simulation` pipeline so every downstream LLM call (entity research, persona generation, sim config) lands under the same session; sets `sim_phase="setup"` + the matching `prompt_type` in front of each phase, then clears at the end.
  - `backend/app/services/simulation_runner.py` (+12, −1): forwards `MIROSHARK_RUN_ID` env var to the simulation subprocess so subprocess-side calls use the same `run_id` tag.
  - `backend/wonderwall/social_agent/agent.py` (+20, −4 in `_aget_model_response`): subprocess-side metadata path mirrors the orchestrator-side one — reads `MIROSHARK_SIMULATION_ID` / `MIROSHARK_RUN_ID` / `MIROSHARK_ROUND_NUM` env vars, fills `prompt_type='agent_action'` + `sim_phase='round'`, sets `extra['user'] = sim_id`, builds `tags = ['miroshark', 'agent_action', 'phase:round', f'run:{run_id}']`, sets `extra['name'] = 'agent_action'`. Wraps in a try/except so a metadata bug never breaks the actual agent action.
  - `backend/scripts/run_parallel_simulation.py` (+20): writes `os.environ['MIROSHARK_ROUND_NUM']` at the top of every per-round loop in all four scenario variants — the only context channel that reaches CAMEL's OpenRouter call site cleanly without reworking its signature.
  - `backend/scripts/run_reddit_simulation.py` and `backend/scripts/run_twitter_simulation.py` (+4, +3): same one-liner.

- `b0a0b0c` — *fix: stop tool retry loop and bound research-call context (#52)* — merged 14:10:10 UTC (47 s after #51), +87 / −42 across 3 files
  - `backend/wonderwall/social_platform/platform.py` (+61, −40): twelve idempotent platform actions — `repost` (×2 branches), `like_post`, `unlike_post`, `dislike_post`, `undo_dislike_post`, `follow`, `unfollow`, `mute`, `report_post`, `like_comment`, `unlike_comment`, `dislike_comment`, `undo_dislike_comment` — used to return `{success: False, error: "X record already exists." }` (or "does not exist") whenever the action was already in the desired state. Returning `success=False` made agents retry the same tool 4+ times per round, ballooning conversation history to 40k+ input tokens. All twelve now return `{success: True, noop: True, reason: ...}` so the agent moves on instead of looping. The contract change is: "already in desired state" is no longer an error — it's a no-op success.
  - `backend/wonderwall/social_agent/agent.py` (+14, −1 in `__init__`): `max_iteration` parameter was stored on `self` but never passed to CAMEL's `ChatAgent.super().__init__()` — so the per-step ReAct loop was unbounded at runtime. Now plumbed through `super().__init__(..., max_iteration=max_iteration, prune_tool_calls_from_memory=True)`. Default raised from 1 to 3 (covers observe → tool → synthesize while bounding the blast radius of any future loop bug). `prune_tool_calls_from_memory=True` keeps old tool messages from accumulating across iterations.
  - `backend/app/services/web_enrichment.py` (+12, −1): caps `simulation_requirement` at 1,500 chars in `_research()` per-entity prompts (`sr[:1500].rstrip() + " […]"`). Previous Langfuse traces showed 60–80k input tokens per entity from a multi-KB user briefing getting pasted into every entity-research call.

**Impact:** Three direct cost-and-latency wins driven off the same Langfuse instrumentation surface. Each retry-stuck idempotent action used to cost roughly 4× the round budget; an unbounded `max_iteration` could amplify that further. The web-enrichment cap alone removes ~60–80k tokens of duplicated input per entity from the `setup` phase. Beyond the immediate fixes, the architectural payoff is the metadata schema: every future call now lands in Langfuse pre-tagged by `prompt_type` / `sim_phase` / `run_id`, so the next cost question is answered by a Langfuse filter instead of a rerun-with-instrumentation. The 47-second gap between merges is the diagnostic loop running in real time — instrument it, see the leak, plug it.

---

## aaronjmars/miroshark-aeon

No substantive commits in the 24-hour window. The branch saw ~25 `aeonframework` chore auto-commits (cron scheduler state updates and per-skill log + article auto-commits for token-report, fetch-tweets, tweet-allocator, repo-pulse, feature, push-recap, repo-article, project-lens, heartbeat, self-improve). All are noise.

---

## Developer Notes

- **New dependencies:** None. PR #50 reuses Pillow (already pinned for share-card); PR #51/#52 use only stdlib + existing CAMEL/OpenRouter integration.
- **Breaking changes:** The platform.py change in PR #52 is technically a contract change — twelve idempotent actions previously returned `{success: False, error: ...}` for "already in desired state" and now return `{success: True, noop: True, reason: ...}`. The Wonderwall social agent is the sole caller, so the blast radius is contained.
- **Architecture shifts:**
  - `TraceContext.wrap_fn` is a new reusable primitive for any future thread-pool work that needs Langfuse correlation. The `threading.local`-doesn't-propagate caveat is documented in the module docstring.
  - "Sim dir as the schema" beat continues in PR #50: replay GIFs cached at `<sim_dir>/replay-gifs/<hash>.gif`, alongside `share-cards/`, `outcome.json`, etc. — same projection-not-DB pattern the share-card and `/verified` features established.
  - Every OpenRouter-reachable LLM call site (orchestrator + subprocess) now passes through metadata — the contract is uniform across `llm_client.chat`, `web_enrichment._research`, persona generation, graph extract, sim config, report agent, and the Wonderwall subprocess. New call sites should slot in by setting `TraceContext.set(prompt_type=..., sim_phase=...)` before the call.
- **Tech debt:** The PR #51 round-number plumbing currently uses an env var (`MIROSHARK_ROUND_NUM`) that's mutated mid-loop in 4 entry-point scripts. It's the cleanest reach into CAMEL's OpenRouter call site without reworking its signature, but it's also the one piece of the metadata pipeline that isn't request-scoped — if Wonderwall ever runs multiple rounds concurrently in one process, this would leak. Worth revisiting when a multi-round-concurrent runner shape comes up.

## What's Next

- repo-actions Apr 26 idea #3 (Share-as-Thread Formatter) is the natural next distribution shipper after PR #50; idea #1 (Predictive Accuracy Ledger) shipped Apr 27 as PR #47, idea #2 (GIF) shipped today as PR #50. With 2 days left in the 1K-stars-by-Apr-30 sprint, the surface that ties the share card + GIF + `/verified` page into one tweet-friendly post is the obvious follow-on.
- The Langfuse traces from PR #51 likely surface more cost/latency outliers than the three PR #52 fixed. A next-day pass over the new `prompt_type` filter could find more leaks of the "duplicated context in every call" or "tool retry loop" shape — the diagnostic surface is now standing.
- 0 open PRs at recap close. No branches in flight visible from the commit log.
