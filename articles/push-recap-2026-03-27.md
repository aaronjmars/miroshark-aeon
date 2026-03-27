# Push Recap — 2026-03-27

## Overview
13 commits by 2 authors (Aaron Elijah Mars, github-actions[bot]) across two repos. The day's headline is a massive cross-platform simulation engine overhaul in MiroShark — round memory, belief tracking, market-media bridging, and a 10x Neo4j performance boost — while miroshark-aeon ran its daily automated skills and had a minor scheduling fix.

**Stats:** ~35 files changed, +5,071/-399 lines across 13 commits

---

## aaronjmars/MiroShark

### Cross-Platform Simulation Engine & Round Memory
**Summary:** The simulation architecture was fundamentally restructured. Instead of three platforms (Twitter, Reddit, Polymarket) running independently, they now execute in synchronized lock-step via a new `run_synchronized_simulation()` function. A sliding-window round memory system gives every agent shared context across all platforms, and a market-media bridge pipes social sentiment to traders and market prices to social agents in real time.

**Commits:**
- `eca0e79` — feat: cross-platform simulation engine, performance overhaul, and prompt quality improvements
  - New file `backend/scripts/round_memory.py` (+479 lines): `RoundMemory` class implementing 4-tier sliding-window memory. Ancient rounds get LLM-batch-compacted into narrative paragraphs, older rounds get individual compaction, recent rounds kept in full detail. Background `ThreadPoolExecutor` ensures compaction never blocks the simulation loop. Filters noise (DO_NOTHING, REFRESH, browse_markets).
  - New file `backend/wonderwall/social_agent/belief_state.py` (+440 lines): Pure-heuristic belief tracker — no LLM calls. Tracks stance (-1 to +1), confidence (0 to 1), and inter-agent trust per topic. Novel arguments get 1.5x impact; repeated arguments 0.5x. High-confidence agents resist change. Exposure history deduplication via MD5 hashes (capped at 2000). Outputs `# YOUR CURRENT BELIEFS AND STANCE` section for agent prompts.
  - New file `backend/app/services/web_enrichment.py` (+219 lines): LLM-powered research for notable entities during persona generation. Auto-triggers for public figures, politicians, CEOs, journalists, and any entity with <150 chars of graph context. Supports `WEB_SEARCH_MODEL` (e.g. Perplexity/sonar-pro) for live web grounding. Results cached per entity name.
  - Changed `backend/scripts/run_parallel_simulation.py` (+559/-40): New `run_synchronized_simulation()` orchestrator runs all 3 platforms in lock-step per round. Each round: build shared context → step all platforms via `asyncio.gather` → fetch actions → update beliefs → publish to bridge → record to memory → compact previous round. `_build_social_summary_for_traders()` extracts top posts for Polymarket agents. LLM concurrency semaphore doubled from 30 to 60.

**Impact:** Agents now see the full simulation state — traders read social media posts, social agents see market movements, and everyone carries sliding-window memory of past rounds. This eliminates the stale-data problem where platforms were siloed.

### Polymarket Trading Overhaul
**Summary:** Polymarket was simplified from a complex multi-market system to a single LLM-generated prediction market with AMM constant-product pricing. Agent tools were stripped down to buy/sell/do_nothing — no more browsing or creating markets.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/wonderwall/simulations/polymarket/prompts.py` (+67/-23): Full prompt rewrite. `do_nothing` is now the explicit default. Tiered position sizing guide (5-10% edge → $10-30 bet; >20% edge → $80-200). New "Trading Psychology" and "Using Social Media as a Signal" sections. Context priority: own beliefs > market prices > social media > simulation memory.
  - Changed `backend/wonderwall/simulations/polymarket/environment.py` (+54/-18): Observation prompt now shows P&L per position with cost basis, flags actionable positions, highlights contrarian opportunities at extreme prices, and injects social media summary context.
  - Changed `backend/wonderwall/simulations/polymarket/actions.py` (+16/-7): `sell_shares()` rewritten with explicit use cases (take profit, cut losses, rebalance). `create_market()` accepts `initial_probability` parameter (0.1–0.9) for non-50/50 seeding.
  - Changed `backend/wonderwall/simulations/polymarket/platform.py` (+17/-2): Display name fix for Polymarket agents in DB.

**Impact:** Polymarket now generates cleaner price action — agents focus on trading decisions rather than market management. The do_nothing default + social media signal integration should produce more realistic trading behavior.

### Neo4j Performance & Graph Reasoning
**Summary:** Neo4j writes were batched using UNWIND for ~10x speedup on entity/relation creation. Six new graph reasoning queries were added to support the upgraded report agent.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/app/storage/neo4j_storage.py` (+319/-61): Batched entity writes via `UNWIND $batch AS e … MERGE`. Entity summaries now prefer NER-extracted attributes over generic "Name (Type)" labels. 6 new query methods: degree centrality, bridge entities (heuristic betweenness), shortest path, community detection (union-find), contradiction detection (opposing sentiment edges), and temporal evolution.
  - Changed `backend/app/services/graph_builder.py` (+53/-27): Parallel chunk processing via `ThreadPoolExecutor` with `as_completed()` for progress tracking (3x faster graph building).

**Impact:** Graph building is significantly faster (parallel chunks + batched writes), and the report agent can now perform structural analysis of the knowledge graph — finding communities, bridges, contradictions, and causal paths.

### Report Agent Upgrade
**Summary:** The report agent was transformed from a basic summarizer into a data-grounded analytical tool with 6 new tools and reframed prompts.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/app/services/report_agent.py` (+612/-67): 6 new tools — `simulation_feed` (reads actual actions.jsonl), `market_state` (queries Polymarket SQLite for prices/P&L), `analyze_trajectory` (parses trajectory.json for convergence/polarization), `graph_structure` (centrality/communities), `find_causal_path` (shortest path between entities), `detect_contradictions`. Reports reframed from "Future Prediction" to "Scenario Exploration" with epistemic disclaimers. New `_generate_synthesis()` method identifies cross-cutting patterns after all sections. Max tool calls per section raised from 5 to 6. Minimum sections increased from 2 to 3.

**Impact:** Reports now cite actual simulation data (posts, trades, prices) rather than just summarizing themes. The framing shift to "scenario exploration" is more epistemically honest about what LLM-driven agent simulations can actually tell us.

### Persona Generation & Prompt Quality
**Summary:** Persona generation was overhauled with web enrichment, archetype-based social metrics, expanded entity type detection, and completely rewritten prompts for all platforms.

**Commits:**
- `eca0e79` (continued)
  - Changed `backend/app/services/oasis_profile_generator.py` (+257/-82): Web enrichment as 5th context layer for notable figures. Social metrics now archetype-based (media outlets: 50K followers; students: 300) scaled by graph degree instead of random. 14 new individual entity types recognized. Entity list interleaved by type via round-robin for diverse early results. Parallel generation raised from 5 to 15 workers. Persona prompts rewritten: individuals get "actor's character brief" style (blind spots, online behavior, what would change their mind); institutions get "communications playbook" style.
  - Changed `backend/wonderwall/simulations/social_media/prompts.py` (+129/-22): Full rewrites for Twitter and Reddit. `do_nothing` as default (targeting 36% rate). Twitter emphasizes punchy takes and platform-native language; Reddit emphasizes substance with evidence, paragraph form, citing sources.
  - Changed `backend/app/storage/ner_extractor.py` (+71/-1): 2 few-shot examples added (Tesla/Elon Musk, Senator Warren/AI Accountability Act). 6 new NER rules: co-reference merging, reject fragments/abstract concepts, canonical names, extract summary attribute. Validation rejects entities ≤2 chars, single lowercase words, and descriptive phrases.
  - Changed `backend/app/services/simulation_config_generator.py` (+187/-23): Added `_generate_prediction_markets()` for LLM-generated markets per simulation. Agent config batches now generated in parallel (ThreadPoolExecutor, max 3 concurrent, 3x faster). Heuristic guidance added to system prompts for timing, events, and agent counts.

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
**Summary:** Standard daily automated skill execution — token reports, tweet fetching, repo pulse monitoring, push recap, repo article, and heartbeat checks. One manual scheduling tweak by Aaron.

**Commits:**
- `e5d2083` — chore(repo-article): auto-commit 2026-03-27
  - New article `articles/repo-article-2026-03-27.md` (+44 lines) on MiroShark's week-two divergence from MiroFish
  - Updated `memory/MEMORY.md` and `memory/logs/2026-03-27.md`

- `ba77a41` — chore(push-recap): auto-commit 2026-03-27
  - New article `articles/push-recap-2026-03-27.md` (+136 lines) covering the previous cycle's pushes
  - Added `memory/extract_patches.py` (+34 lines) helper script

- `54896da` — chore(token-report): auto-commit 2026-03-27
  - Updated `articles/token-report-2026-03-27.md` (+21/-12): Refreshed MiroShark price data ($0.0000005318, -23.95% 24h)

- `f6071c7` — chore(fetch-tweets): auto-commit 2026-03-27
  - Updated `memory/logs/2026-03-27.md` (+7): Logged tweet fetch — found 10 $MIROSHARK tweets

- `a16f575` — chore(token-report): auto-commit 2026-03-27
  - Initial token report: price $0.0000005222, FDV $52.2K, volume $39K (+40 lines)

- `c13e48a` — chore(repo-pulse): auto-commit 2026-03-26
  - Logged repo pulse (MiroShark: 282 stars, 46 forks, +10 stars/day)

- `4cc56c0` — chore(push-recap): auto-commit 2026-03-26
  - Push recap for 2026-03-26 covering Wonderwall/Polymarket integration (+114 lines)

- `e3c376e` — chore(repo-pulse): auto-commit 2026-03-26
  - Earlier repo pulse run (+6 lines)

- `d73c7bd` — chore(heartbeat): auto-commit 2026-03-26
  - Heartbeat flagged 10 daily skills that didn't run due to missing cron trigger

- `f2f874e` — chore: schedule repo-pulse at 20:00 UTC for testing
  - Changed `aeon.yml` (+1/-1): Adjusted repo-pulse cron schedule

- `115121d` — chore(heartbeat): auto-commit 2026-03-26
  - First heartbeat of the day — all clear (+6 lines)

**Impact:** The autonomous agent pipeline is running reliably — token tracking, social monitoring, and repo observability are all executing on schedule.

---

## Developer Notes
- **New dependencies:** None (web enrichment reuses existing LLM client; round memory uses stdlib threading)
- **Breaking changes:** Polymarket agent tools reduced (browse_markets, create_market, comment_on_market removed) — old simulation configs referencing those tools will need updating. Report framing changed from "Future Prediction" to "Scenario Exploration."
- **Architecture shifts:** Simulation moved from independent-parallel to synchronized lock-step execution. Three new subsystems: RoundMemory (sliding-window context), BeliefState (heuristic stance tracking), MarketMediaBridge (cross-platform data flow). WebEnricher added as optional persona enrichment layer.
- **Tech debt:** `update.md` in MiroShark root is a session note that should probably be cleaned up. `memory/extract_patches.py` in miroshark-aeon may be temporary.

## What's Next
- Belief trajectory visualization — data is being saved to `trajectory.json` but no tooling exists to explore it yet
- Web enrichment could extend beyond "notable" entity types to all entities with thin graph context
- Report agent's new tools need testing at scale — especially `simulation_feed` with large action logs
- The `do_nothing` default (36% rate from testing) needs validation across different simulation topics
- MiroShark star growth continues (~10-13/day) — community engagement may drive feature requests
