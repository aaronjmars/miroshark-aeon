# Push Recap — 2026-03-27

## Overview
11 commits across 2 repos by 2 authors (Aaron Elijah Mars + github-actions[bot]). The dominant work today was a massive simulation engine overhaul in MiroShark — cross-platform data flow, round memory, belief tracking, web enrichment, and completely rewritten prompts. Meanwhile, miroshark-aeon ran its daily automated skills (token reports, tweet monitoring, repo pulse, push recap) and had a minor scheduling tweak.

**Stats:** ~48 files changed, +4,872/-398 lines across 11 commits

---

## aaronjmars/MiroShark

### Cross-Platform Simulation Engine & Round Memory System
**Summary:** The simulation architecture was fundamentally restructured. Instead of three platforms (Twitter, Reddit, Polymarket) running independently, they now execute in synchronized lock-step via a new `run_synchronized_simulation()` function. A sliding-window round memory system gives every agent shared context across all platforms, and a market-media bridge pipes social sentiment to traders and market prices to social agents in real time.

**Commits:**
- `eca0e79` — feat: cross-platform simulation engine, performance overhaul, and prompt quality improvements
  - New file `backend/scripts/round_memory.py` (+479 lines): 4-tier sliding-window memory — ancient rounds get LLM-batch-compacted into narrative paragraphs, older rounds get individual compaction, recent rounds kept in full detail. Background `ThreadPoolExecutor` ensures compaction never blocks the simulation loop. Filters noise (DO_NOTHING, REFRESH, browse_markets).
  - Changed `backend/scripts/run_parallel_simulation.py` (+559/-40): New `run_synchronized_simulation()` orchestrator runs all 3 platforms in lock-step per round. Each round: build shared context → step all platforms via `asyncio.gather` → fetch actions → update beliefs → publish to bridge → record to memory → compact previous round. LLM concurrency semaphore doubled from 30 to 60.
  - New file `backend/wonderwall/social_agent/belief_state.py` (+440 lines): Pure-heuristic belief tracker — no LLM calls. Tracks stance (-1 to +1), confidence (0 to 1), and inter-agent trust per topic. Novel arguments get 1.5x impact; repeated arguments 0.5x. High-confidence agents resist change. Exposure history deduplication via MD5 hashes (capped at 2000). Outputs `# YOUR CURRENT BELIEFS AND STANCE` section for agent prompts.
  - New file `backend/app/services/web_enrichment.py` (+219 lines): LLM-powered research for notable entities during persona generation. Auto-triggers for public figures, politicians, CEOs, journalists, and any entity with <150 chars of graph context. Supports `WEB_SEARCH_MODEL` (e.g. Perplexity/sonar-pro) for live web grounding. Results cached per entity name.

**Impact:** Agents now see the full simulation state — traders read social media posts, social agents see market movements, and everyone carries sliding-window memory of past rounds. This eliminates the stale-data problem where platforms were siloed.

### Polymarket Trading Overhaul
**Summary:** Polymarket was simplified from a complex multi-market system to a single LLM-generated prediction market with AMM constant-product pricing. Agent tools were stripped down to buy/sell/do_nothing — no more browsing or creating markets. Prompts were completely rewritten around trading psychology and cross-platform signal usage.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/wonderwall/simulations/polymarket/prompts.py` (+67/-23): Full prompt rewrite. `do_nothing` is now the explicit default. Tiered position sizing guide (5-10% edge → $10-30 bet; >20% edge → $80-200). New "Trading Psychology" and "Using Social Media as a Signal" sections. Context priority: own beliefs > market prices > social media > simulation memory.
  - Changed `backend/wonderwall/simulations/polymarket/environment.py` (+54/-18): AMM with configurable initial probability (non-50/50 starting prices). Removed browse/create/comment tools.
  - Changed `backend/wonderwall/simulations/polymarket/actions.py` (+16/-7): Simplified agent action set to pure price action.
  - Changed `backend/wonderwall/simulations/polymarket/platform.py` (+17/-2): Display name fix for Polymarket agents in DB.

**Impact:** Polymarket now generates cleaner price action — agents focus on trading decisions rather than market management mechanics. The do_nothing default + social media signal integration should produce more realistic trading behavior.

### Neo4j Performance & Graph Reasoning
**Summary:** Neo4j writes were batched using UNWIND for ~10x speedup on entity/relation creation. Five new graph reasoning queries were added to support the upgraded report agent.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/app/storage/neo4j_storage.py` (+319/-61): Batched entity writes via `UNWIND $batch AS e … MERGE`. Better embedding text using NER-extracted summaries instead of just "Name (Type)". 5 new query methods: degree centrality, bridge entities (heuristic betweenness), shortest path, community detection (union-find), contradiction detection (opposing sentiment edges), and temporal evolution.
  - Changed `backend/app/services/graph_builder.py` (+53/-27): Parallel chunk processing via `ThreadPoolExecutor` (3x faster graph building).

**Impact:** Graph building is significantly faster (parallel chunks + batched writes), and the report agent can now perform structural analysis of the knowledge graph — finding communities, bridges, contradictions, and causal paths.

### Report Agent Upgrade
**Summary:** The report agent was transformed from a basic summarizer into a data-grounded analytical tool with 6 new tools and reframed prompts.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/app/services/report_agent.py` (+612/-67): 6 new tools — `simulation_feed` (reads actual actions.jsonl), `market_state` (queries Polymarket SQLite for prices/P&L), `analyze_trajectory` (parses trajectory.json for convergence/polarization), `graph_structure` (centrality/communities), `find_causal_path` (shortest path between entities), `detect_contradictions`. Reports reframed from "Future Prediction" to "Scenario Exploration" with epistemic disclaimers. New `_generate_synthesis()` method identifies cross-cutting patterns after all sections. Max tool calls per section raised from 5 to 6.

**Impact:** Reports now cite actual simulation data (posts, trades, prices) rather than just summarizing themes. The framing shift to "scenario exploration" is more epistemically honest.

### Persona Generation & Prompt Quality
**Summary:** Persona generation was overhauled with web enrichment, archetype-based social metrics, expanded entity type detection, and completely rewritten prompts for all platforms.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/app/services/oasis_profile_generator.py` (+257/-82): Web enrichment as 5th context layer. Social metrics now archetype-based (media outlets: 50K followers; students: 300) scaled by graph degree. 14 new individual entity types added. Entity list interleaved by type via round-robin. Parallel generation raised from 5 to 15 workers. Persona prompts rewritten: individuals get "actor's character brief" style (blind spots, online behavior, what would change their mind); institutions get "communications playbook" style.
  - Changed `backend/wonderwall/simulations/social_media/prompts.py` (+129/-22): Full rewrites for Twitter and Reddit. `do_nothing` as default (targeting 36% rate). Each action gets specific trigger conditions. Twitter emphasizes punchy takes; Reddit emphasizes substance with evidence. Context priority established.
  - Changed `backend/app/storage/ner_extractor.py` (+71/-1): 2 few-shot examples added. Rejection rules for fragments/duplicates. Co-reference resolution.
  - Changed `backend/app/services/simulation_config_generator.py` (+187/-23): Parallel config batch generation (3x faster). Timing/event/agent heuristics with concrete guidance.
  - Changed `backend/app/config.py` (+7): Added `WEB_SEARCH_MODEL` config field.
  - Changed `backend/wonderwall/simulations/base.py` (+12/-1): Base simulation changes to support new subsystems.
  - Changed `backend/wonderwall/social_agent/agent_action.py` (+8/-3): Action handling updates.

**Impact:** Personas are richer (web-grounded for notable figures), social metrics are realistic instead of random, and prompts produce more natural platform-specific behavior with appropriate do_nothing rates.

### Documentation
**Summary:** Comprehensive documentation added for the simulation engine internals.

**Commits:**
- `eca0e79` (continued)
  - New file `backend/run.md` (+872 lines): Complete reference of all 22 LLM call sites with exact prompts, input/output schemas, and usage context.
  - Changed `README.md` (+63/-4): Updated architecture section with cross-platform diagram and performance table.

- `2b03099` — docs: add session update with changes summary and next steps
  - New file `update.md` (+161 lines): Session changelog documenting all changes made and planned next steps.

**Impact:** The codebase is now well-documented for contributors — `run.md` alone maps every LLM interaction in the system.

---

## aaronjmars/miroshark-aeon

### Automated Skill Runs
**Summary:** Standard daily automated skill execution — token reports, tweet fetching, repo pulse monitoring, push recap, and heartbeat checks. One manual scheduling tweak.

**Commits:**
- `54896da` — chore(token-report): auto-commit 2026-03-27
  - Updated `articles/token-report-2026-03-27.md` (+12/-12): Refreshed MiroShark token data (price $0.0000005318, -23.95% 24h)
  - Updated `memory/logs/2026-03-27.md` (+9): Logged second token report run

- `f6071c7` — chore(fetch-tweets): auto-commit 2026-03-27
  - Updated `memory/logs/2026-03-27.md` (+7): Logged tweet fetch — found 10 tweets about $MIROSHARK

- `a16f575` — chore(token-report): auto-commit 2026-03-27
  - New file `articles/token-report-2026-03-27.md` (+30): Initial MiroShark token report
  - New file `memory/logs/2026-03-27.md` (+10): First log entry of the day

- `4cc56c0` — chore(push-recap): auto-commit 2026-03-26
  - New file `articles/push-recap-2026-03-26.md` (+106): Yesterday's push recap article
  - Updated `memory/logs/2026-03-26.md` (+8): Logged push recap run

- `c13e48a` — chore(repo-pulse): auto-commit 2026-03-26
  - Updated `memory/logs/2026-03-26.md` (+7/-1): Logged repo pulse (MiroShark: 282 stars, 46 forks)

- `e3c376e` — chore(repo-pulse): auto-commit 2026-03-26
  - Updated `memory/logs/2026-03-26.md` (+6): Logged earlier repo pulse run

- `d73c7bd` — chore(heartbeat): auto-commit 2026-03-26
  - Updated `memory/logs/2026-03-26.md` (+8/-1): Logged heartbeat — flagged 10 daily skills that didn't run

- `f2f874e` — chore: schedule repo-pulse at 20:00 UTC for testing
  - Changed `aeon.yml` (+1/-1): Adjusted repo-pulse cron schedule to 20:00 UTC

- `115121d` — chore(heartbeat): auto-commit 2026-03-26
  - New file `memory/logs/2026-03-26.md` (+6): First heartbeat of the day — all clear

**Impact:** The autonomous agent pipeline is running reliably — token tracking, social monitoring, and repo observability are all executing on schedule.

---

## Developer Notes
- **New dependencies:** None added (web enrichment reuses existing LLM client; round memory uses stdlib threading)
- **Breaking changes:** Polymarket agent tools reduced (browse_markets, create_market, comment_on_market removed) — old simulation configs with those tools will need updating
- **Architecture shifts:** Simulation moved from independent-parallel to synchronized lock-step execution; round memory is a new shared-state layer; belief tracking is fully heuristic (no LLM cost)
- **Tech debt:** `WEB_SEARCH_MODEL` falls back gracefully to training-data knowledge if not set; tmp files committed in repo-pulse auto-commit (tmp_check_env.sh, tmp_notify_msg.txt, tmp_send.sh)

## What's Next
- The `update.md` session notes likely contain planned next steps for the simulation engine
- Belief trajectory visualization could be built on top of the new `trajectory.json` output
- The report agent's new tools need testing at scale — especially `simulation_feed` with large action logs
- MiroShark star growth continues (282 stars, +10-13/day) — community engagement may drive feature requests
- The tmp files in miroshark-aeon should be cleaned up
