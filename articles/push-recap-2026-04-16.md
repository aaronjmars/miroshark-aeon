# Push Recap — 2026-04-16

## Overview
34 commits across 2 repos by 2 authors (aaronjmars, Aeon). The main thrust today: MiroShark gained Director Mode (mid-simulation event injection) and a major performance/cost overhaul with multi-model routing, while the Aeon infrastructure got hardened with stuck-run detection and duplicate notification prevention.

**Stats:** ~40 files changed, +1,700/-320 lines across 34 commits

---

## aaronjmars/MiroShark

### New Feature: Director Mode — Mid-Simulation Event Injection
**Summary:** Users can now inject breaking events into running simulations. When an event is injected (e.g. "Central bank raised rates by 100bps"), all agents receive it at the next round boundary, affecting their posts, trades, and stance shifts. This transforms MiroShark from a single-track simulator into a perturbation-research tool.

**Commits:**
- `ce89066` — feat: mid-simulation event injection (Director Mode)
  - New file `backend/scripts/director_events.py` (+187 lines): File-based event queue with atomic writes, marker-replace injection pattern, `consume_pending_events()` and `inject_director_event_context()` functions
  - Changed `backend/scripts/run_parallel_simulation.py`: Imports director_events module, consumes pending events at each round start in both Twitter and Reddit simulation loops (+17 lines)
  - Changed `backend/app/api/simulation.py`: Added `POST /<sim_id>/director/inject` (max 3 events per sim) and `GET /<sim_id>/director/events` REST endpoints (+99 lines)
  - Changed `frontend/src/api/simulation.js`: Added `injectDirectorEvent()` and `getDirectorEvents()` API client functions (+17 lines)
  - Changed `frontend/src/components/Step3Simulation.vue`: Director Mode button in action bar (visible while sim is running), event injection panel with textarea + char counter, event history display, director event banners in timeline feed (+380/-3 lines)
  - Changed `frontend/src/components/BeliefDriftChart.vue`: Amber dashed vertical markers at injection rounds on the belief drift chart (+24/-1 lines)

- `d77e831` — Merge pull request #31 (Director Mode into main)

**Impact:** Enables exogenous shock modeling — researchers can now test how agent populations respond to mid-stream disruptions. The file-based queue pattern means the feature works without additional infrastructure. Capped at 3 events per simulation to prevent abuse.

### Multi-Model Routing & Performance Overhaul
**Summary:** A sweeping cost/performance optimization pass. Introduces `OASIS_MODEL_NAME` to decouple the simulation loop model from the default LLM, adds a `fast_llm` path in GraphToolsService to route mechanical work to cheaper models, caps context sizes to prevent token blowup, and adds automatic run summary reporting.

**Commits:**
- `d639fe7` — feat: multi-model routing, perf optimizations, and run summary reporting
  - Changed `.env.example`: Added `OASIS_MODEL_NAME` config variable with documentation (+12 lines)
  - Changed `backend/app/config.py`: Added `OASIS_MODEL_NAME` env var, defaults to `LLM_MODEL_NAME` when unset (+4 lines)
  - Changed `backend/app/services/graph_tools.py`: Added `fast_llm` client — interviews, agent selection, sub-queries, and summaries now route to default model instead of smart model. Imports `create_llm_client` alongside `create_smart_llm_client` (+25/-19 lines)
  - Changed `backend/app/services/ontology_generator.py`: Bumped `max_tokens` from 4096→8192 to prevent ontology truncation with verbose/thinking models (+2/-2 lines)
  - Changed `backend/app/services/report_agent.py`: Capped previous-section context to 6000 chars total (was unbounded, causing 112K token context across 14 calls) (+25/-4 lines)
  - Changed `backend/app/services/web_enrichment.py`: Fixed parallelism by creating per-call LLM clients instead of sharing a single instance (+7/-10 lines)
  - Changed `backend/app/services/simulation_runner.py`: Calls `generate_run_summary()` on simulation completion (best-effort) (+20 lines)
  - New file `backend/app/utils/run_summary.py` (+335 lines): Reads `events.jsonl`, aggregates LLM calls by model and caller, computes estimated costs, writes `run_summary.md` to simulation directory
  - Changed `backend/scripts/run_parallel_simulation.py`: `OASIS_MODEL_NAME` overrides `LLM_MODEL_NAME` in the simulation loop's model creation (+2/-1 lines)
  - Changed `backend/wonderwall/social_agent/agent.py`: Filters empty-content messages that Gemini rejects with INVALID_ARGUMENT (+10 lines)
  - New file `findings.md` (+224 lines): Config A vs Config B benchmark documentation (subsequently removed)

- `4e0a4f6` — chore: remove findings.md
  - Removed `findings.md` (-224 lines): Benchmark documentation cleaned up after optimization results were applied

**Impact:** Enables running cheap models (Gemini Flash) for mechanical pipeline work while reserving expensive models (GPT-5 Nano, Claude) for the simulation loop. The report_agent context cap alone could cut 80%+ of unnecessary token spend on long reports. Auto-generated run summaries make cost/performance visible without manual analysis.

### NER Quality & Integration Fixes
**Summary:** Two targeted fixes improving knowledge graph extraction quality and correcting OpenRouter API integration headers.

**Commits:**
- `0482106` — fix: improve NER extraction quality and filter garbage entities
  - Changed `backend/app/config.py`: Bumped chunk sizes from 1000/50 to 1500/100 for better entity context and fewer split-entity boundaries (+2/-2 lines)
  - Changed `backend/app/services/entity_reader.py`: Added `_is_nonspeaking_entity()` filter — rejects dates, abstract concepts, countries, and other entities that shouldn't become simulation agents (+60 lines)
  - Changed `backend/app/services/ontology_generator.py`: Added `_is_clean_identifier()` validation — ensures ontology type names are clean ASCII PascalCase/UPPER_SNAKE_CASE (+31/-2 lines)
  - Changed `backend/app/services/text_processor.py`: Added citation marker block detection and stripping — removes PDF extraction artifacts like "Sacra +2\nWikipedia +4" between paragraphs (+55 lines)
  - Changed `backend/app/storage/ner_extractor.py`: Rejects self-referential relations and relations targeting ontology type names instead of entity instances (+24 lines)
  - Added `miroshark-nobg.png`: New logo asset

- `dcbd96b` — fix: correct OpenRouter attribution headers
  - Changed `backend/app/storage/embedding_service.py`: Replaced deprecated `X-Title` with `X-OpenRouter-Title`, added `X-OpenRouter-Categories: roleplay` (+2/-1 lines)
  - Changed `backend/app/utils/llm_client.py`: Same header fix, removed unrecognized `X-Description` header (+2/-3 lines)

**Impact:** NER quality improvements mean cleaner knowledge graphs — no more date strings or country names becoming simulation agents. The OpenRouter header fix ensures proper attribution and prevents potential API deprecation issues.

---

## aaronjmars/miroshark-aeon

### Aeon Infrastructure Hardening
**Summary:** Three targeted fixes improving the reliability of the Aeon autonomous agent: stuck-run detection in heartbeat, duplicate notification prevention, and expanded content scheduling.

**Commits:**
- `5b58f33` — improve: add stuck-run timeout detection to heartbeat skill
  - Changed `skills/heartbeat/SKILL.md`: Heartbeat's dedup guard now includes `createdAt` in `gh run list` queries and checks elapsed time. Runs `in_progress` for >2 hours are flagged as "stuck" and excluded from the dedup guard, allowing fresh dispatches (+6/-5 lines)

- `a6894be` — Merge pull request #14 (heartbeat stuck-run timeout into main)

- `4a6ea58` — fix: prevent duplicate notifications, clean up stale files
  - Changed `.github/workflows/aeon.yml`: `./notify` now tracks delivery success via `DELIVERED` flag, removes `.pending-notify/` file after successful send to prevent double-delivery on post-process retry (+12/-4 lines)
  - Removed `build-target` submodule reference (stale/empty)

- `fa27814` — feat: make repo-article and project-lens daily
  - Changed `aeon.yml`: `project-lens` schedule changed from Mon/Wed/Fri to daily; `repo-article` schedule changed from off-days-only to daily (+2/-2 lines)

- `c6a3054` — chore: update memory with self-improve log and fix duplicate Next Priorities

**Impact:** The stuck-run timeout closes a reliability gap where hung GitHub Actions runs could permanently block skill retries. Duplicate notification prevention stops the same message from being sent twice when the sandbox blocks initial delivery but the post-process step succeeds. Daily content scheduling increases output cadence.

### Automated Operations
~24 automated commits from Aeon's CI pipeline: scheduler state updates, cron success markers, auto-commits for completed skills (token-report, fetch-tweets, repo-pulse, feature, self-improve, repo-actions, heartbeat).

---

## Developer Notes
- **New dependencies:** None
- **Breaking changes:** `OASIS_MODEL_NAME` env var is additive (defaults to `LLM_MODEL_NAME` when unset). OpenRouter header changes could affect API responses if older headers were being used for routing.
- **Architecture shifts:** Multi-model routing pattern (`fast_llm` vs `smart_llm` vs `oasis_model`) creates a three-tier model hierarchy: cheap/fast for mechanical tasks, default for simulation loop, smart for complex reasoning. Run summary auto-generation adds observability to every simulation.
- **Tech debt:** None introduced. `findings.md` was created and cleaned up in the same day.

## What's Next
- Director Mode is merged — likely next: testing with real perturbation scenarios, possibly adding more event types or removing the 3-event cap
- Run summary reports are now auto-generated — could feed into a cost dashboard or alert on expensive runs
- NER improvements may need follow-up validation with diverse document types
- Repo-article and project-lens are now daily — content output doubles from the Aeon pipeline
- Open from repo-actions: Simulation Replay, Agent Interaction Network Graph, Multi-Document Comparative Mode, Embeddable Widget, Quality Diagnostics
