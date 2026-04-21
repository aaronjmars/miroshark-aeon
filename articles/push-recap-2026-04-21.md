# Push Recap — 2026-04-21

## Overview
Thirteen substantive commits across both repos in the last 24 hours, driven primarily by Aaron Mars going maximalist on MiroShark — a production-grade graph memory stack with 11 capabilities (Hindsight/Graphiti/Letta/HippoRAG-inspired) landed as a direct push, then a 14-feature sibling-repo integration bundle merged as PR #41 less than 18 hours later. Aeon shipped PR #40 (Trending Topics Auto-Discovery) to close the blank-page onboarding gap and spent its own repo time hardening the XAI cache plumbing with three back-to-back PRs (#19/#20/#21).

**Stats:** ~82 files changed, +7,953 / −184 lines across 13 substantive commits (plus 7 README cosmetic commits on MiroShark and ~30 auto-chore commits by aeonframework)

---

## aaronjmars/MiroShark

### Theme 1: The Graph Memory Stack — Production-Grade Retrieval and Reasoning
**Summary:** Aaron went deep on the storage layer overnight (2026-04-20 22:50 UTC), pushing a single commit that bolts on 11 capabilities inspired by the current crop of agent-memory research. It is the largest cohesive expansion of MiroShark's backend retrieval pipeline since the graph itself shipped. No PR — direct push to main.

**Commits:**
- `b20f955` — *feat: production-grade graph memory stack + MCP server* (+2,690 / −93 across 17 files)
  - **New file `backend/app/storage/reranker_service.py` (+111)**: BGE-reranker-v2-m3 cross-encoder layer that re-scores hybrid-search hits before they reach the LLM. Last-mile precision on top of vector + BM25.
  - **New file `backend/app/storage/entity_resolver.py` (+308)**: fuzzy + vector candidate generation with an LLM-reflection adjudicator for ambiguous matches — the "is `Justin Sun` the same node as `justin_sun` or `J Sun`?" problem handled explicitly instead of praying for exact-string hits.
  - **New file `backend/app/storage/contradiction_detector.py` (+182)**: at ingest time, same-endpoint edge pairs get LLM-adjudicated; superseded edges are *invalidated*, not deleted — keeps the history auditable.
  - **New file `backend/app/storage/community_builder.py` (+386)**: Leiden clustering over the graph, LLM-generated community summaries stored as `:Community` nodes with `MEMBER_OF` edges and their own vector index. Enables the zoom-out view.
  - **New file `backend/app/storage/reasoning_trace.py` (+235)**: the report agent's ReACT loop is now persisted as a traversable subgraph `(:Report)-[:HAS_SECTION]->(:ReportSection)-[:HAS_STEP]`. Reasoning is a first-class graph citizen — you can query why a conclusion was reached, not just what it was.
  - **Changed `backend/app/storage/search_service.py` (+319 / −60)**: BFS graph-traversal retrieval from seed entities now runs alongside vector + BM25; `kinds=[...]` filter and `as_of` point-in-time search surface the new edge metadata.
  - **Changed `backend/app/storage/neo4j_storage.py` (+258 / −10)** and **`neo4j_schema.py` (+74)**: bi-temporal edges (`valid_at` / `invalid_at` / `created_at` / `expired_at`) plus `invalidate_edge()` API. The schema now supports "what did we believe on Apr 15" queries instead of only "what do we currently believe".
  - **Changed `backend/app/services/graph_memory_updater.py` (+39 / −2)**: Wonderwall agent activities tagged with `kind="belief"` (expressive) vs `kind="observation"` (engagement) at write time.
  - **New file `backend/mcp_server.py` (+353)**: 8-tool MCP server over stdio for Claude Desktop integration.
  - **Changed `backend/app/services/report_agent.py` (+139 / −20)**: gains `browse_clusters` tool with auto-build-on-first-call; the `simulation_feed` prompt was softened so `browse_clusters` can actually compete for the agent's first tool call instead of being permanently outshouted.
  - **Changed `README.md` (+104)** and **`.env.example` (+48)**: full config documentation plus a Claude Desktop integration section.

**Impact:** MiroShark's graph is no longer just a store of entities and relations — it now carries temporal validity, provenance (fact/belief/observation), contradiction resolution, multi-resolution community structure, and persisted reasoning traces. The report agent can answer "why did we conclude X" by walking its own trace. The MCP server means an outside Claude client can query the graph directly — the first outside-the-app surface for this data.

### Theme 2: PR #41 — The Sibling-Repo Capability Siphon
**Summary:** Aeon-authored, merged 2026-04-21 15:14 UTC. Bundles 14 capabilities cherry-picked from the broader MiroShark-family forks (MiroJiang, MiroWhale, OpenMiro, oracle-seeds). Every new feature is gated behind an env flag or a per-sim opt-in, so existing deployments see zero behavior change until they flip a switch.

**Commits:**
- `a3486d4` — *feat: integrate capabilities from sibling repos (MiroJiang/MiroWhale/OpenMiro/oracle-seeds) (#41)* (+4,005 / −29 across 43 files)
  - **Onboarding — `POST /api/simulation/ask`** (MiroWhale-style, in `backend/app/api/simulation.py` +429): question-only pipeline. User asks "what happens if…" and the LLM researches the topic, producing a 1500-3000 char briefing that feeds the existing ontology → graph → sim pipeline unchanged. Home.vue gets the entry point (+71).
  - **Analysis — counterfactual branching**: **New `backend/scripts/counterfactual_loader.py` (+72)** + changes to `director_events.py` (+52) add `_promote_counterfactual_if_due` so forked sims inject narrative events at a scheduled future round by riding the existing director-event pipeline — zero runner-loop rewrite. **New `CounterfactualBranchPanel.vue` (+402)** wires it into Step3. Preset templates gain an optional `counterfactual_branches[]` field.
  - **Analysis — per-round frame API**: `GET /api/simulation/<id>/frame/<round>` returns a compact snapshot (actions + market prices + belief state) for scrubbing UIs on large sims without re-loading full trajectory.json.
  - **Analysis — `analyze_equilibrium`** in `backend/app/services/report_agent.py` (+195 / −0): fits a 2-player stance game on the final belief distribution and enumerates Nash equilibria via `nashpy`. Report-agent tool table in README grows by one row.
  - **Live data — `ORACLE_SEED_ENABLED`**: **New `backend/app/services/oracle_seed.py` (+187)**. Templates' `oracle_tools[]` dispatch FeedOracle MCP (`mcp.feedoracle.io`) calls at template load time and append a markdown evidence block to the seed document. TemplateGallery gets a per-template "Use live oracle data" toggle, gated by a new `/api/templates/capabilities` endpoint. Two preset templates (`corporate_crisis.json`, `crypto_launch.json`) get `oracle_tools` and `counterfactual_branches` fields demonstrating the shape.
  - **Live data — `MCP_AGENT_TOOLS_ENABLED`** (OpenMiro-style): **New `backend/app/services/agent_mcp_tools.py` (+148)** + **new `backend/scripts/mcp_agent_bridge.py` (+324)** + **`mcp_agent_injection.py` (+103)**. Personas with `tools_enabled: true` get a tool catalogue injected each round; the runner parses `<mcp_call …/>` tags from their posts, dispatches via pooled stdio subprocesses, and injects results on the next activation. This is the first time agents can call outside-world tools mid-sim.
  - **Security — publish gate**: `is_public` flag on simulations + `POST /api/simulation/<id>/publish`. Embed endpoints now 403 until published; EmbedDialog (+42 / −3) gets a toggle.
  - **Perf — embedding batch size** bumped 32 → 128 (configurable via `EMBEDDING_BATCH_SIZE`).
  - **Cost — Anthropic prompt caching**: `LLM_PROMPT_CACHING_ENABLED` attaches `cache_control` to the system message on Claude-family models; silent no-op elsewhere. Big win on the ReACT report loop, which replays the same system prompt dozens of times per run.
  - **Correctness — no more silent fallback**: `run_parallel_simulation.py` (+139 / −1) used to silently downgrade to `gpt-4o-mini` when no model was configured; now it raises loudly. One less way to end up with a sim that "ran" but not on the model you thought.
  - **Tooling — CLI**: **New `backend/cli.py` (+282)** + `miroshark-cli` entry point via `pyproject.toml` (+5). Dependency-light HTTP client covering `ask / list / status / frame / publish / report / trending / health`.
  - **Tooling — pytest suite**: **New `backend/tests/` directory (10 new files, ~884 lines)** covering CLI, counterfactual loader, director events, MCP bridge, MCP registry, oracle seed, prompt cache, templates schema — 62 unit tests offline, integration markers wrap existing hand-run `test_*.py` scripts. **New `.github/workflows/tests.yml` (+44)** runs unit tests on every push/PR. This is MiroShark's first standing CI test suite.
  - **Docs** — README gains sections for Just Ask, Counterfactual Branching, Live Oracle Data, Per-Agent MCP Tools, Publishing for Embed, Per-Round Frame API, Report Agent Tools table (with `analyze_equilibrium`), CLI, and Testing (+132 / −2). All new env vars in `.env.example` (+27).

**Impact:** This is a consolidation move. The sibling repos were prototype surfaces; the useful bits are now in main, gated so nothing breaks. Three are load-bearing for MiroShark's next phase: (1) per-agent MCP tools turn the sim from a closed simulator into an open one where agents can query live data mid-round, (2) the test suite is the first durable quality gate in the backend, (3) prompt caching is a cost cut in the loudest hot path.

### Theme 3: PR #40 — Trending Topics Auto-Discovery (Blank-Page Onboarding)
**Summary:** Aeon-authored, merged 2026-04-21 13:43 UTC. The third and (probably) final piece of the "get a user from blank page to scenario cards in one click" trilogy — Scenario Auto-Suggest (PR #39) solved the "I have a document" path; this solves the "I have nothing" path.

**Commits:**
- `f426c46` — *feat: trending topics auto-discovery for blank-page onboarding (#40)* (+864 / −0 across 6 files; already detailed in today's feature-skill log entry)
  - Backend: `GET /api/simulation/trending` in `backend/app/api/simulation.py` (+484). Stdlib-only RSS/Atom parser — `xml.etree.ElementTree` + `urllib.request`, zero new deps. Parallel fetch via ThreadPoolExecutor (5s per-feed timeout, 1MB body cap), URL-deduped + newest-first, in-memory cache (15min TTL / 60s on empty), per-IP sliding-window rate limit (30/min) mirroring suggest-scenarios. Never 5xxes.
  - **Mid-PR security harden** (follow-up commit folded in): Reuters RSS feed was swapped for TechCrunch (Reuters shut the public endpoint years ago, leaving the default one-feed-silently-empty). SSRF protection added on `?feeds=` override: http(s)-only, reject loopback/private/link-local/reserved hosts, and normalize IPv4 via `inet_aton` so obfuscated encodings (integer `2130706433`, hex `0x7f000001`, octal `0177.0.0.1`) can't bypass to `127.0.0.1`.
  - Frontend: new `TrendingTopics.vue` (+315) as a 5-card grid below URL Import on Home.vue (+20). Click → pushes URL into `fetchUrlDoc()` pipeline → Scenario Auto-Suggest auto-fires on the resulting text.

**Impact:** The blank-canvas problem is closed. A user who lands on the site with no document and no idea now sees five clickable trending headlines; one click produces three scenario cards. Zero new runtime dependencies to maintain.

### Theme 4: Wizard UX Polish — Status During Long Steps
**Summary:** Direct push, 2026-04-20 21:31 UTC. Small but user-visible: Step 2's preparation phase could run silently for a long time; users had no indication which sub-step was active.

**Commits:**
- `a0a7dfd` — *Show descriptive status in Step 2 header and renumber wizard to 4 steps* (+63 / −30 across 6 files)
  - `Step2EnvSetup.vue` (+36 / −16): top-right indicator + browser tab title now report the active sub-step (Initializing, Generating Profiles, Generating Config, Orchestrating, Ready). Pulsing status dots inside every sub-step badge.
  - Five View components (`InteractionView`, `MainView`, `ReportView`, `SimulationRunView`, `SimulationView`): step counters re-renumbered — Deep Interaction collapsed into the final step so the wizard reads 1/4 through 4/4 consistently instead of the prior 1/5-with-a-skip.

**Impact:** Eliminates the "is this thing frozen?" moment on slow prep steps. The kind of polish that costs almost nothing and removes a real drop-off point.

### Theme 5: README Badges & Cosmetic Cleanup
**Summary:** A seven-commit micro-burst 2026-04-20 20:18 → 20:24 UTC adding project-visibility badges, then iterating on badge formatting and link correctness. Same-hour direct pushes.

**Commits:**
- `97e8640` — Add Star History chart
- `8f2bc47` — Add badges (license, stars, forks, social follow, TAKA on Bankr)
- `889370f` — Fix Bankr badge link
- `a0025b8` — Fix badge link formatting
- `352cfab` — Remove AGPL v3 badge (license ambiguity?)
- `f0fdb0e` — Restore project description and demo image (undo accidental removal during badge work)
- `8e4b7e6` — Enhance README with badges and follow links

**Impact:** Cosmetic — but this is the surface visitors see first. With the repo crossing 745+ stars and sitting on a community contribution streak, signalling credibility via social/build badges compounds.

---

## aaronjmars/miroshark-aeon

### Theme 1: XAI Cache Pipeline — Three-Round Hardening
**Summary:** Yesterday's fetch-tweets triple-run revealed two orthogonal bugs in the XAI cache pipeline. Today's three PRs (#19 → #20 → #21) are the postmortem: detect wrong-query caches, recover truncated Grok responses, and stop the heartbeat from re-flagging a resolved issue.

**Commits:**
- `d2ed3e3` — *improve: validate XAI cache query to prevent stale-cache silent failures in fetch-tweets (#19)* (+163 / −11 across 7 files; branch merged 2026-04-21 13:47 UTC)
  - `scripts/prefetch-xai.sh` (+13 / −2): fetch-tweets branch now `rm -f`s the cache + sidecar before `xai_search`, so a failed API call can't leave stale content. On success, writes the current `$VAR` verbatim to `.xai-cache/fetch-tweets.query`.
  - `skills/fetch-tweets/SKILL.md` (+8 / −1): Path A now reads the sidecar and only consumes the cache if it matches current `${var}`; mismatch falls through to Path B (live API) instead of serving wrong-query results. Eliminates the silent-fail mode that burned two of yesterday's three fetch-tweets invocations under `$AEON`-era cache content.

- `fcb75b9` — *improve: harvest XAI annotation citations into fetch-tweets cache (#20)* (+131 / −14 across 2 files; merged 2026-04-21 13:54 UTC)
  - `scripts/filter-xai-tweets.py` (+129 / −14): after the existing bare-word filter, scan `content.annotations[]` for tweet URLs (`x.com`/`twitter.com` + `/status/ID`), dedupe against URLs already rendered in `.text`, and splice missing ones back in as synthesized numbered blocks. Annotation-derived blocks skip the bare-word filter — Grok's search is already var-scoped, so citations are relevant by construction. Shape-defensive: tolerates any annotation carrying a tweet URL regardless of declared type, missing title/text.
  - `skills/fetch-tweets/SKILL.md` (+2): documents the citation-source block format so step 7 renders annotation-only entries without the Likes/RTs line and falls back to the raw URL when the handle isn't parseable (`x.com/i/status/…` URLs).
  - **Why this commit exists**: yesterday's log (Apr 21 fetch-tweets entry) shows the exact failure — "Cache text truncated after tweet 2; 38 additional tweet URLs captured as annotation citations". Grok's `output_text.text` has a length cap; when it runs multiple x_search calls (7 in today's case), the rendered tweet blocks get truncated mid-stream even though every surfaced URL is still in `output_text.annotations[]`. This fix moves those citation URLs back into the skill's input so dedup and notification handle them uniformly.

- `1177f2d` — *fix: remove stale XAI_API_KEY flag from MEMORY.md (#21)* (+0 / −1 across 1 file; merged 2026-04-21 14:00 UTC)
  - `memory/MEMORY.md` (−1): strikes the "XAI_API_KEY not set" line from Next Priorities. The secret has been wired since 2026-03-25 and the prefetch pipeline uses it successfully on every run; the stale line was from before the prefetch pattern existed (back when skills curled XAI inline and hit the env-var-in-curl-header sandbox block). Heartbeat was re-emitting it as an ongoing flag every run.
  - **Known residual**: token-report's Social Pulse section still tries to curl XAI inline and will keep reporting "XAI_API_KEY not set" in its own output until migrated — explicitly flagged in the PR body as separate scope.

**Impact:** Together, #19 + #20 + #21 close the XAI cache feedback loop that consumed three fetch-tweets runs yesterday. #19 prevents wrong-query caches from silently serving stale results. #20 surfaces every tweet URL Grok actually cited, even when the rendered text blocks get truncated — raising effective recall from "whatever fit in the text cap" to "everything Grok surfaced". #21 silences the false-positive heartbeat flag that was making the whole system look sicker than it was.

---

## Developer Notes

- **New dependencies (MiroShark):**
  - `nashpy` (via `pyproject.toml` +5, `requirements.txt` +5) — for Nash-equilibrium analysis in `report_agent.analyze_equilibrium`.
  - BGE-reranker-v2-m3 (referenced by new `reranker_service.py` — pulled via existing transformers/sentence-transformers stack, no new top-level requirement).
  - FeedOracle MCP client (`oracle_seed.py` — runtime dispatch, no hard dep).
  - Explicitly zero new deps in PR #40 (Trending Topics) — stdlib-only RSS parsing was a design constraint.
- **Breaking changes:**
  - `run_parallel_simulation.py` no longer silently falls back to `gpt-4o-mini` — raises if no model is configured. Deployments relying on the implicit default will break on first run.
  - Embed endpoints now 403 until a sim is explicitly published via `POST /api/simulation/<id>/publish`. Existing shared embed links on unpublished sims will stop working; EmbedDialog exposes a toggle to publish.
- **Architecture shifts:**
  - Graph storage is now bi-temporal with first-class reasoning-trace nodes. This is a genuine substrate change — future retrieval and audit features build on edges-as-history rather than edges-as-current-state.
  - Agents can now call MCP tools mid-simulation (`MCP_AGENT_TOOLS_ENABLED`). This is the first time the simulator's epistemic boundary leaks outward.
  - Prompt caching is a config flag, not a code path — matches the pattern "features ship off-by-default, operators opt in" that ran through PR #41.
- **Tech debt / follow-ups flagged in-PR:**
  - token-report's inline-curl XAI call still needs the prefetch migration (PR #21 body).
  - PDF-only uploads still don't trigger Scenario Auto-Suggest (noted yesterday); no change today.
  - PR #41 gates everything behind flags — defaults are conservative, but ramp of each flag in production will be its own rollout.

## What's Next
- **MiroShark**: The next obvious move is turning on at least one of PR #41's gated features in production. Prompt caching has the lowest risk / highest cost impact and would be a natural first flip. Per-agent MCP tools is the most interesting but also the biggest behavior change — needs a test sim before default-on.
- **MiroShark community**: Zero open PRs at day's end. mbs5 (builtbydesigninc) shipped twice on 2026-04-20; watch for whether they come back after this week's feature wave settles.
- **miroshark-aeon**: The XAI cache pipeline is now well-hardened. Next self-improvement target per yesterday's signal would be token-report's Social Pulse XAI-curl migration — the only remaining place where the "stale env / silent fail" anti-pattern still lives.
- **1K-star pace**: MiroShark sits at 748 stars / 145 forks (Apr 21 repo-pulse). Needs ~25/day through Apr 30 to clear the hyperstition target; today added 5. PR #41 + #40 landing means the repo has a lot of newly-shippable demo material for organic growth.
