# Repo Action Ideas — 2026-03-30

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 347 stars · 56 forks · 3 contributors · 0 open issues · 4 open PRs
**Recent activity:** 34 commits in 14 days — cross-platform engine, Polymarket integration, graph reasoning tools, Hyperstitions Design System v2.0, Claude Code provider, smart model tiers

## Ecosystem Context

The multi-agent simulation space continues accelerating. Key signals this week:

- **MCP as agent standard:** Gartner and industry consensus now position MCP as "the standard for tool and data access in agent-style LLM systems." Every major agent framework is shipping MCP support. MiroShark has no MCP integration yet — this is the single biggest interoperability gap.
- **TradingAgents framework:** A new multi-agent LLM financial trading framework assigns specialized roles (fundamental analyst, sentiment analyst, technical analyst, risk manager) to different agents. MiroShark's Polymarket agents currently share identical decision logic — role specialization would produce more realistic market dynamics.
- **MiroFish ecosystem expansion:** The Italian fork added an Institutional Calibration Framework (ICF) for generating synthetic populations at regional granularity using census data. Another fork ships 484 MCP tools as real-time data sources. MiroShark risks falling behind forks that are adding research credibility.
- **Cost collapse:** GPT-4-level performance now costs 1/100th of two years ago. Users are running bigger simulations but have no visibility into costs before hitting "Start."
- **Polymarket AI volume:** 122 active LLM-related markets with $26.5M+ in volume on Polymarket. AI agents represent 30%+ of wallets. The demand for simulation-before-trading tools is real and growing.

These 5 ideas are distinct from all 15 previously generated (webhooks, A/B testing, embeddable widget, replay, gallery, WebSocket streaming, snapshot sharing, prompt scoring, doc preprocessing, benchmarking, network visualization, REST API, multi-document comparison, Discord bot, belief analytics) and from the 4 open PRs (export, preset templates, replay, network viz).

---

### 1. MCP Server for Simulation Access

**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** MCP is rapidly becoming the universal agent-tool protocol. An MCP server would let Claude Code, Cursor, Windsurf, and any MCP-compatible agent trigger simulations, query results, and inspect agent states without custom API integration. This is the single highest-leverage interoperability play — it connects MiroShark to the entire agent ecosystem in one move. The Italian MiroFish fork already ships 484 MCP tools; MiroShark should lead, not follow.
**How:**
1. Create a `mcp_server.py` module using the MCP Python SDK (`mcp` package) that exposes 4 tools: `create_simulation` (accepts document text + config), `get_simulation_status` (returns progress and current round), `get_simulation_results` (returns structured JSON with agent actions, beliefs, market data), and `list_simulations` (returns recent runs).
2. Wire each tool to the existing FastAPI backend logic — the MCP server is a thin adapter over the same simulation engine the frontend uses.
3. Add a `--mcp` flag to the startup command that launches the MCP server alongside the web UI, and document the connection string in the README.

---

### 2. Demographic Calibration Profiles for Agent Generation

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** MiroShark currently generates agents with LLM-randomized personas. For research credibility, simulations need to reflect real population distributions — age brackets, political lean, education levels, urban/rural split. The Italian MiroFish fork's Institutional Calibration Framework proves there's demand for this. Calibrated agents make MiroShark viable for policy simulation, market research, and academic papers where "random AI personas" isn't a credible methodology.
**How:**
1. Create a `calibration/` directory with 3 built-in demographic profiles as JSON: `us_general.json` (based on US Census ACS data — age, education, income, urban/rural, political affiliation distributions), `us_tech_workers.json` (Stack Overflow developer survey demographics), and `global_twitter.json` (Pew Research Twitter user demographics).
2. Update the agent generation pipeline in the config generator to accept an optional `calibration_profile` parameter. When set, sample agent attributes from the profile's distributions instead of letting the LLM freestyle.
3. Add a "Population Profile" dropdown to the simulation setup UI with the 3 built-in options plus "Custom JSON" upload.

---

### 3. CLI Runner for Headless Simulations

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** MiroShark is UI-only — there's no way to run a simulation from the command line. A CLI runner (`python -m miroshark run config.json`) unlocks batch processing, CI/CD integration, research pipelines, and scripted experiments. Researchers need to run 50 variations of a simulation overnight; the UI can't do that. This also makes MiroShark composable — Aeon's `feature` skill could trigger simulations programmatically for testing.
**How:**
1. Create a `cli.py` entry point using `argparse` with subcommands: `run` (accepts a config JSON file, runs the simulation headlessly, outputs results to stdout or a file), `status` (checks a running simulation), and `export` (dumps results as JSON/CSV).
2. Reuse the existing backend simulation logic — the CLI calls the same functions the FastAPI endpoints call, just without the web server.
3. Add a `Makefile` target (`make simulate CONFIG=config.json`) and document the CLI in the README's "Advanced Usage" section.

---

### 4. Agent Memory Inspector Panel

**Type:** DX Improvement
**Effort:** Medium (1–2 days)
**Impact:** MiroShark's Neo4j knowledge graph is its core architectural innovation — agents build persistent memory through graph relationships, belief states, and cross-platform context. But this graph is completely invisible in the UI. An inspector panel that lets users browse what each agent "knows" and "remembers" would make the graph architecture tangible, help researchers debug agent behavior, and create compelling screenshots for articles and demos. This turns MiroShark's hidden differentiator into a visible one.
**How:**
1. Add a `MemoryInspector.vue` component that queries the Neo4j graph for a selected agent and renders: the agent's persona node with all attributes, connected memory nodes (posts they've seen, interactions they've had), belief state history as a timeline, and trust relationships with other agents.
2. Visualize the agent's local subgraph using a small D3 force layout — the agent at center, connected to memory nodes, belief nodes, and other agents they've interacted with. Color-code by node type (persona, memory, belief, interaction).
3. Wire the inspector into the simulation results view — clicking any agent name in the timeline feed opens their memory inspector in a slide-out panel.

---

### 5. Simulation Cost Estimator

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** Users configure simulations with agent counts, round numbers, and model tiers but have zero visibility into what it will cost before hitting "Start." With GPT-4-level models now 100x cheaper than 2024, users are running bigger simulations — but a 500-agent, 40-round simulation on GPT-4o still costs real money. A cost estimator that shows projected token usage and dollar cost before launch prevents bill shock, helps users pick the right model tier, and builds trust with new users who are hesitant to try expensive configurations.
**How:**
1. Create a `cost_estimator.py` module that calculates estimated tokens per simulation based on: agent count × rounds × average prompt size (from the existing prompt templates) × platform count. Apply per-model pricing from a `model_pricing.json` config file covering OpenRouter, OpenAI, and local (free) options.
2. Surface the estimate in the simulation setup UI — after the user configures agents and rounds, display a card showing: estimated total tokens, estimated cost by model tier (with the selected model highlighted), and estimated runtime based on historical round durations.
3. After simulation completes, show actual vs. estimated cost in the results summary so users can calibrate their expectations for future runs.

---

## Selection Rationale

This batch targets MiroShark's three biggest gaps heading into week three:

- **Interoperability** (#1) — MCP is the protocol of the agent era; MiroShark needs to speak it before competitors make it table stakes
- **Research credibility** (#2, #4) — Demographic calibration and graph memory inspection transform MiroShark from "cool demo" to "publishable research tool"
- **Developer workflow** (#3, #5) — CLI access and cost transparency remove the two biggest friction points for power users and researchers running repeated simulations

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, no ambiguous design decisions, no external approvals needed.
