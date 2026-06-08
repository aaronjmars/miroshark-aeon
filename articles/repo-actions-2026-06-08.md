# Repo Action Ideas — 2026-06-08

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,243 stars · 262 forks · 1 open issue (#95 French locale) · 0 open PRs (PR #152 signed-result.json merged Jun 08)
**Recent activity:** PR #152 (Signed Simulation Result, Aeon-built) merged Jun 08 — catalog 33→34; zero-deps streak 42 intact. Jun-06 batch: #1→PR#151 merged Jun 07, #3→PR#152 merged Jun 08. Unbuilt: #2 Payload Validator, #4 Monthly Time-Series, #5 Agent Behavior Census. Contributor 666ghj: 219 commits — most active external contributor by far.

## Ecosystem Context

Full catalog audit today via `surfaces_catalog.py` revealed 12 surfaces previously unknown to the pre-existing registry: platform_stats_badge, per-sim badge_svg, clone_json, polymarket_json, volatility, agent_sparklines, watch_page, oembed, peak_round, share_card, replay_gif, chart_svg. All added to `memory/topics/pre-existing-features.md` this run.

The catalog is now confirmed at 34 entries across 7 type categories (analytics, visualization, export, embed, integration, platform, discovery). The four categories with the fewest entries are **discovery** (feed_atom, feed_rss — 2 entries), **embed** (watch_page, oembed — 2 entries), **integration** (polymarket_json, batch_status, signed_result — 3 entries), and **platform** (7 entries). The discovery and integration categories are underserved relative to the size of the integrator ecosystem.

The MCP layer (`backend/app/api/mcp.py`) provides `GET /api/mcp/status` but no standalone tool catalog JSON. The report layer (`backend/app/api/report.py`) generates full async analysis reports. The graph layer (`backend/app/api/graph.py`) handles knowledge graph construction from documents/URLs. None of these surfaces are in the catalog — the mcp.py endpoint is present but not catalogued as a discovery surface.

Today's batch targets three distinct gaps: (1) a lightweight "what just happened" activity stream for integrators and monitoring tools, (2) a "what are people simulating?" topics surface for researchers and press, (3) a machine-readable MCP tool catalog for agent framework builders, (4) a preflight cost estimator for batch pipeline operators, and (5) a Chinese README at the repo root — the one document type that has English-only coverage despite all 12 docs/ files having zh-CN counterparts.

Pre-existence checks confirmed this run (all added to pre-existing registry above):
- Platform stats badge — already at `GET /api/stats/badge.svg` (surfaces_catalog.py: platform_stats_badge)
- Per-sim badge — already at `GET /api/simulation/<id>/badge.svg` (badge_svg)
- Simulation clone — already at `GET /api/simulation/<id>/clone.json` (clone_json)
- Polymarket integration — already at `GET /api/simulation/<id>/polymarket.json` (polymarket_json)
- Volatility analytics — already at `GET /api/simulation/<id>/volatility` (volatility)
- Agent sparklines — already at `GET /api/simulation/<id>/agents/sparklines` (agent_sparklines)
- Live watch page — already at `GET /watch/<id>` (watch_page, watch.py)
- oEmbed endpoint — already at `GET /oembed` (oembed)
- Peak round analytics — already at `GET /api/simulation/<id>/peak-round` (peak_round)
- Share card — already at `GET /api/simulation/<id>/share-card.png` (share_card)
- Replay GIF — already at `GET /api/simulation/<id>/replay.gif` (replay_gif)
- Chart SVG — already at `GET /api/simulation/<id>/chart.svg` (chart_svg)

7-day exclusion window (Jun 01–Jun 07) excluded: Simulation Payload Validator (Jun-06 #2, re-eligible Jun 13), Monthly Stats Time-Series (Jun-06 #4, re-eligible Jun 13), Platform Agent Behavior Census (Jun-06 #5, re-eligible Jun 13), All-Time Leaderboard (Jun-04 #4, re-eligible Jun 11), Scenario Clone Button (Jun-02 #2, re-eligible Jun 9), Japanese README (Jun-02 #3, re-eligible Jun 9), Simulation Batch Create API (Jun-02 #4, re-eligible Jun 9). All 5 ideas below are net-new and confirmed not pre-existing.

---

### 1. Simulation Activity Feed

**Type:** Integration / Discovery
**Effort:** Small (hours)
**Impact:** `GET /api/activity.json` returns the 20 most recently completed public simulations in reverse chronological order. The catalog has two "what's in the gallery?" surfaces already — `/api/simulation/public` (full filterable catalog) and `/api/feed.rss`+`/api/feed.atom` (RSS/Atom subscription feeds). Neither answers "what just completed in the last hour?" in a lightweight, machine-parseable way suited for monitoring integrations and polling loops. The activity feed closes this. Returns: `{count, results: [{sim_id, scenario_title, direction, confidence_pct, quality_health, total_rounds, completed_at, project_id}]}`, sorted newest-first. No auth. 30-second cache (faster than stats' 60s — the use case is near-real-time). Query param `?limit=N` (1–50, default 20). Enables: Aeon's push-recap skill checking whether any new sims completed since the last run without reading the full gallery; integrators (Capacitr, AntFleet) who run reaction logic when a sim completes but don't have webhooks configured; platform health monitors that need "did anything complete recently?" confirmation; social bots that post when a simulation finishes. Distinct from `/api/stats` (totals), `/api/feed.rss` (subscription), and `/api/simulation/public` (full gallery with all fields and filters).

**How:**
1. `backend/app/services/activity_feed.py` (~100 LoC, stdlib `json` + `os`). `build_activity_feed(sim_root, limit: int = 20) -> dict`: scan `WONDERWALL_SIMULATION_DATA_DIR`; filter `is_public=True` + `status="completed"`; sort by `completed_at` descending; return top `limit` (clamp silently to [1, 50]). Each entry: `{sim_id, scenario_title: str[:100], direction, confidence_pct, quality_health, total_rounds, completed_at, project_id}`. Empty platform → `{count: 0, results: []}`. Add `GET /api/activity.json` to `stats.py` on `stats_bp` (or a new `activity_bp`). `Cache-Control: public, max-age=30`. ETag `activity-{total_public_completed}-{newest_completed_at}`. 10 offline unit tests in `test_unit_activity_feed.py`: most-recent-first ordering, private sims excluded, running sims excluded, limit param clamped to [1,50], scenario_title truncated to 100 chars, empty platform → valid empty envelope, JSON-serialisable, ETag correct format, limit=1 returns only 1 entry, count matches results length. Zero new deps.
2. Add `getActivityFeed(limit?)` to `frontend/src/api/simulation.js`. Add `ActivityFeed` + `ActivityFeedEntry` schemas to `openapi.yaml`. Add `GET /api/activity.json` to `docs/API.md` under Platform, noting: 30s cache (vs 60s for stats), limit param, and the distinction from `/api/simulation/public` (full catalog) and `/api/feed.rss` (subscription). Add `activity_feed` to `surfaces_catalog.py` (35th entry, type: `discovery`). Zero new deps.

---

### 2. Trending Simulation Topics

**Type:** Analytics / Growth
**Effort:** Small (hours)
**Impact:** `GET /api/stats/topics.json` answers "what are people actually simulating on MiroShark?" across all public completed sims. The platform stats family now covers totals (`/api/stats`), result shape (`/api/stats/distribution.json`), health (`/api/status.json`), and project breakdown (`/api/project/<id>/stats`). None of them answer what *topics* the platform is being used for. This surface aggregates the `topic` field and key tokens from `scenario_title` using word frequency (stdlib only — tokenize on spaces and punctuation, lowercase, drop a hardcoded 30-word stop-word list, count). Returns `{generated_at, total_analyzed, top_topics: [{topic, count}], top_scenario_tokens: [{token, count}]}`. Both lists sorted by count desc, capped at top-20. Useful for: researchers citing MiroShark as AI simulation infrastructure who need to characterize the use-case distribution; journalists writing "what are investors using AI simulations to think about?"; directory builders showing a topic cloud; integrators checking whether their target topic has precedent before running a sim. Distinct from `distribution.json` (result *shape* — how bullish/bearish/confident) — this is *what* people simulate, not *how the results look*.

**How:**
1. `backend/app/services/topics_stats.py` (~140 LoC, stdlib `json` + `os` + `re`). `build_topics(sim_root, limit: int = 20) -> dict`: scan public+completed sims; extract `topic` field (full string, counted as-is); extract `scenario_title` tokens (tokenize on `\W+`, lowercase, filter against hardcoded 30-word stop-word list covering common English connectives); count both frequency tables. Return `{generated_at: ISO, total_analyzed: int, top_topics: list, top_scenario_tokens: list}`. Stop-word list hardcoded in the service: `{"the","a","an","in","of","to","for","and","or","is","are","was","will","with","on","at","by","from","this","that","it","as","be","has","have","had","not","but","if","do"}`. Both lists sorted by count desc, capped at `limit` (default 20, max 50, clamp). Empty platform → `{total_analyzed: 0, top_topics: [], top_scenario_tokens: []}`. Add `GET /api/stats/topics.json` to `stats.py` on `stats_bp`. `Cache-Control: public, max-age=300`. ETag `topics-{total_analyzed}-{newest_completed_at[:7]}`. 10 offline unit tests: top_topics sorted count desc, stop words excluded from scenario tokens, private+incomplete sims excluded, limit clamped to [1,50], punctuation stripped from tokens, empty platform → valid empty envelope, JSON-serialisable, ETag present, topic field returned as full string (not tokenized), count correct. Zero new deps.
2. Add `getTopicsStats(limit?)` to `frontend/src/api/simulation.js`. Add `TopicsStats` + `TopicEntry` schemas to `openapi.yaml`. Add to `docs/API.md` under Platform alongside `/api/stats`. Note stop-word methodology (hardcoded, English-biased) and that `top_topics` returns exact `topic` field values while `top_scenario_tokens` is NLP-light tokenization. Add `topics_stats` to `surfaces_catalog.py` (36th entry, type: `analytics`). Zero new deps.

---

### 3. MCP Tool Catalog JSON

**Type:** Integration / Discovery
**Effort:** Small (hours)
**Impact:** `GET /api/mcp/tools.json` returns MiroShark's MCP tool definitions — name, description, and inputSchema — as a JSON Schema-compatible document, without the host-specific config blocks and Neo4j health probes that `GET /api/mcp/status` includes. As AI agent frameworks (LangChain, CrewAI, AutoGen, OpenAI Assistants, Claude Projects) adopt MCP as a standard for tool discovery, a clean `tools.json` lets them auto-register MiroShark's graph and simulation tools in one HTTP call. The `/api/surfaces.json` endpoint plays this role for REST surfaces; `tools.json` does the same for the MCP tool layer. Integrators building multi-agent systems on top of MiroShark can fetch this endpoint at agent startup, dynamically configure their MCP client with the current tool list, and degrade gracefully when new tools are added without code changes. Distinction from `/api/mcp/status`: status is for the frontend UI to render copy-paste config snippets for Claude Desktop/Cursor/Windsurf; tools.json is for agent frameworks to programmatically register MiroShark's capabilities.

**How:**
1. In `backend/app/api/mcp.py`, add `GET /api/mcp/tools.json` alongside `/api/mcp/status`. Extract from the `_TOOLS` list already defined at module scope in `mcp.py`; for each tool, include the inputSchema from `mcp_server.py`'s `list_tools()` handler (import or re-declare as a module-level dict). Response: `{schema_version: "1", count: int, tools: [{name: str, description: str, inputSchema: {type: "object", properties: {...}, required: [...]}}]}`. `Cache-Control: public, max-age=3600` (tool definitions don't change between deploys). No auth. 8 offline unit tests in `test_unit_mcp_tools_api.py`: count matches len(tools), each tool has name/description/inputSchema keys, inputSchema has type:"object", JSON-serialisable, Cache-Control header present, schema_version field present, at least one known tool name present (regression guard against `_TOOLS` being emptied), drift test: API response tool names match `_TOOLS` list in mcp.py. Zero new deps.
2. Add `getMcpTools()` to `frontend/src/api/simulation.js`. Add `McpToolCatalog` + `McpToolEntry` schemas to `openapi.yaml`. Add `GET /api/mcp/tools.json` to `docs/MCP.md` and `docs/MCP.zh-CN.md` under a "Machine-Readable Tool Catalog" section — note the distinction from `/api/mcp/status` (config+health for the frontend) vs this endpoint (tool definitions for agent frameworks). Add `mcp_tools_catalog` to `surfaces_catalog.py` (37th entry, type: `discovery`). Zero new deps.

---

### 4. Simulation Pre-Run Cost Estimator

**Type:** DX
**Effort:** Small (hours)
**Impact:** `POST /api/simulation/estimate` takes the same body shape as `/api/simulation/create` and returns `{complexity_tier, estimated_agents, estimated_rounds, estimated_duration_min, notes: []}` without touching disk or running any LLM call. Integrators running automated sim pipelines (Capacitr's config-to-run loop, AntFleet's benchmark harness) currently have no pre-flight way to predict compute cost or run time before submitting a sim that may take up to 10 minutes. The Payload Validator from Jun-06 batch validates *correctness* (are required fields present and well-typed?); this estimates *complexity* (how much will this sim cost to run?). Different questions, different use cases: a pipeline might pass the validator but still trigger an unexpectedly expensive heavy sim that backs up the queue. Complexity tiers: `light` (<5 agents, <10 rounds), `standard` (5–15 agents, 10–20 rounds), `heavy` (>15 agents or >20 rounds, or ≥3 counterfactual branches), `expert` (all three heavy conditions simultaneously). Notes array warns on heavy/expert tier and flags when counterfactual branches inflate estimates.

**How:**
1. `backend/app/services/run_estimator.py` (~120 LoC, stdlib only). `estimate_run(payload: dict) -> dict`: parse `demographic_filters` to estimate agent count (fall back to `Config.DEFAULT_AGENT_COUNT` if absent); parse `polymarket_market_count` (default 1; each market adds ~3 rounds per Config baseline); add `len(counterfactual_branches) * 2` bonus rounds if `counterfactual_branches` present; clamp `estimated_agents` to `[1, Config.MAX_AGENTS]`; clamp `estimated_rounds` to `[Config.MIN_ROUNDS, Config.MAX_ROUNDS]`. Compute `complexity_tier` based on the three conditions above. Compute `estimated_duration_min` from a simple linear model (`Config.BASE_DURATION_PER_ROUND × estimated_rounds × (1 + estimated_agents / Config.AGENTS_PARALLELISM_FACTOR)`, rounded to 1dp). Notes list: append "Heavy tier: queue time may vary" for heavy/expert; append "Counterfactual branches increase round count" if present. Return `{complexity_tier, estimated_agents: int, estimated_rounds: int, estimated_duration_min: float, notes: list}`. No disk reads/writes. Add `POST /api/simulation/estimate` to `simulation.py` on `simulation_bp`. No auth. `Cache-Control: no-store`. Rate-limit via the same sliding-window middleware as `/api/simulation/batch-status`. 10 offline unit tests in `test_unit_run_estimator.py`: minimal payload → light tier, max `polymarket_market_count=5` → rounds increase, large demographic filter → agent count increases, counterfactual branches list → round bonus, missing payload → 400, `complexity_tier` ∈ {"light","standard","heavy","expert"}, `estimated_duration_min` > 0 for non-trivial input, JSON-serialisable, notes is always a list, estimator does not write to disk (sim_root unchanged after call). Zero new deps.
2. Add `estimateSimulation(payload)` to `frontend/src/api/simulation.js`. Add `SimulationEstimate` schema to `openapi.yaml`. Add to `docs/API.md` under Simulation Management with an explicit note: "This is a heuristic estimate — actual duration depends on LLM API latency and queue depth. Distinct from `POST /api/simulation/validate` (correctness) — this estimates complexity." Add `run_estimator` to `surfaces_catalog.py` (38th entry, type: `integration`). Zero new deps.

---

### 5. Chinese README (README.zh-CN.md)

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** All 12 docs files have zh-CN counterparts (`docs/API.zh-CN.md`, `docs/FEATURES.zh-CN.md`, `docs/INSTALL.zh-CN.md`, `docs/ARCHITECTURE.zh-CN.md`, `docs/CLI.zh-CN.md`, `docs/CONFIGURATION.zh-CN.md`, `docs/DEMOGRAPHICS.zh-CN.md`, `docs/MCP.zh-CN.md`, `docs/MODELS.zh-CN.md`, `docs/NOTIFICATIONS.zh-CN.md`, `docs/OBSERVABILITY.zh-CN.md`, `docs/WEBHOOKS.zh-CN.md`) but the repository root has only `README.md` and `README_DEPLOYMENT.md` — no Chinese equivalent. A `README.zh-CN.md` at the root is the standard GitHub internationalization convention (used by Vue.js, Electron, pandas, and most major open-source projects with CJK audiences). Chinese-speaking developers landing on the repo have no native-language entry point. The active hyperstition (deadline 2026-06-15 — 7 days away) targets "MiroShark PR from Chinese-locale contributor OR Chinese-language coverage." A native-language README is the surface that converts Chinese-locale traffic into Chinese-locale contributors. Contributor `666ghj` (219 commits — most active external contributor by a wide margin) suggests an active Chinese developer community that already uses the project; there's just no front door for them.

**How:**
1. Write `README.zh-CN.md` at the repository root. Structure mirrors `README.md` layout: hero tagline translation ("模拟任何事物，$1 内，10 分钟以内 — 通用集群智能引擎"), description section (adapt from `docs/ARCHITECTURE.zh-CN.md` intro), quick-start (same CLI commands from `docs/CLI.zh-CN.md` and `docs/INSTALL.zh-CN.md`, condensed to install + first run), API reference table (from `docs/API.zh-CN.md`, condensed to the 8 most-used surfaces with a link to the full docs), ecosystem section (mention the 14+ integrators, link to `ECOSYSTEM.md`), documentation index (list all 12 `docs/*.zh-CN.md` files with one-line descriptions so Chinese readers can navigate directly to what they need). Total: ~250–350 lines. No new API surfaces. No new dependencies. Content is a synthesis of existing zh-CN docs — no new translation work required.
2. Add a language badge row to the bottom of `README.md` (or top, after the logo): `[中文](README.zh-CN.md)` link alongside existing language/badge row. Standard pattern: one line, no disruption to the English README layout. The badge links to `README.zh-CN.md` so GitHub renders it inline.

---

## Selection Rationale

Today's catalog audit (surfaces_catalog.py full read) confirmed 12 additional surfaces beyond what the pre-existing registry tracked — all added to `memory/topics/pre-existing-features.md`. The discovery category (2 entries: feed_atom, feed_rss) and integration category (3 entries: polymarket_json, batch_status, signed_result) are underserved despite the 14+ integrators. Two of today's five ideas add to those categories.

- **Activity Feed** (#1) — The discovery category has two RSS/Atom feeds for subscription-style consumers. The gap is the "what just happened?" polling primitive. 30s cache, lightweight per-entry payload, ?limit param. Aeon's push-recap uses this tomorrow. Distinct from everything in the catalog.
- **Trending Topics** (#2) — The analytics category covers per-sim outcome characteristics well (volatility, peak_round, distribution). The gap is platform-level topic coverage — *what* people simulate, not *how* the results look. No existing surface comes close.
- **MCP Tool Catalog JSON** (#3) — The MCP layer is real (mcp.py, mcp_server.py) but not catalogued. As MCP becomes the standard for AI agent tool discovery, a clean `/api/mcp/tools.json` lets frameworks auto-register MiroShark without parsing `/api/mcp/status`. Adds the first `discovery`-type surface for the agent/tool-use consumer segment.
- **Cost Estimator** (#4) — Jun-06's Payload Validator validates correctness; this estimates complexity. Different question. Pipeline operators need both: "is this payload valid?" and "how expensive is this sim?" before submitting. $1/sim and 10-minute ceiling make preflight estimation genuinely valuable for batch pipelines.
- **Chinese README** (#5) — All 12 docs files have zh-CN versions. The root README doesn't. 666ghj (219 commits) and btcbabycow's CN tweet suggest real Chinese community interest. The hyperstition deadline is Jun 15 — 7 days. This is the one action in this batch that directly advances a time-sensitive hyperstition goal.

Excluded (blocked): **Operator Profile** — re-verified today via `memory/topics/blocked-features.md`. `SimulationState` has no `operator`/`created_by` field. Block holds.

Excluded (7-day window): **Payload Validator** (Jun-06 #2, re-eligible Jun 13), **Monthly Time-Series** (Jun-06 #4, re-eligible Jun 13), **Agent Behavior Census** (Jun-06 #5, re-eligible Jun 13), **All-Time Leaderboard** (Jun-04 #4, re-eligible Jun 11), **Scenario Clone Button** (Jun-02 #2, re-eligible Jun 9), **Japanese README** (Jun-02 #3, re-eligible Jun 9), **Simulation Batch Create** (Jun-02 #4, re-eligible Jun 9).

Excluded (pre-existing, discovered this run): **Platform Stats Badge** (lives at `/api/stats/badge.svg`), **Per-Sim Badge** (`/badge.svg`), **Simulation Clone JSON** (`/clone.json`), **Polymarket Integration** (`/polymarket.json`), **Volatility** (`/volatility`), **Agent Sparklines** (`/agents/sparklines`), **Live Watch Page** (`/watch/<id>`), **oEmbed Endpoint** (`/oembed`), **Peak Round** (`/peak-round`), **Share Card** (`/share-card.png`), **Replay GIF** (`/replay.gif`), **Chart SVG** (`/chart.svg`). All added to `memory/topics/pre-existing-features.md` this run.
