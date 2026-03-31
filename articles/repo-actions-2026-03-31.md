# Repo Action Ideas — 2026-03-31

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 362 stars · 60 forks · 3 contributors · 0 open issues · 0 open PRs
**Recent activity:** All 4 feature PRs merged (export, templates, replay, network viz) — clean slate for new work. MCP server PR #5 closed. Repo momentum: +16 stars in 24h, +4 forks.

## Ecosystem Context

MiroShark enters week three with zero open PRs — a rare clean slate and an opportunity to ship the next wave of features. Key ecosystem signals for 2026-03-31:

- **URL-first content workflows:** The dominant way users discover shareable content in 2026 is via links — Slack messages, X posts, newsletter links. Requiring users to copy-paste article text is the single highest-friction step in MiroShark's onboarding funnel. Every major research/AI tool (NotebookLM, Perplexity, Elicit) accepts URLs natively.
- **Multi-market prediction complexity:** Real-world news events generate multiple simultaneous prediction markets (election + policy + market reaction). MiroShark's single auto-generated market understates the complexity users want to model. Polymarket regularly runs 50+ correlated markets on a single event.
- **Template ecosystems as growth drivers:** Notion, Figma, and Raycast all built significant growth flywheels around user-created and community-shared templates. MiroShark has 6 hardcoded preset templates but no mechanism for users to save their own configs or share them with others.
- **Influence propagation as research output:** Academic simulation research (OASIS, Artificial Societies) consistently reports on influence propagation — which agents drive cascades, who shifts opinion first, what network position predicts influence. MiroShark generates this data but surfaces none of it.
- **Zero-config cloud deploy as star driver:** Repos with "Deploy to Railway" or "Deploy to Render" buttons get 2-3× more forks from non-technical audiences. MiroShark currently requires Docker, Neo4j, Node, and Python to be configured manually — the deploy button collapses this to one click and directly drives the star growth toward the 500 target.

These 5 ideas are distinct from all 20 previously generated (webhooks, A/B testing, embeddable widget, replay ✓, gallery, WebSocket streaming, snapshot sharing, prompt scoring, doc preprocessing, benchmarking, network viz ✓, REST API, multi-document comparison, Discord bot, belief analytics, MCP server, demographic calibration, CLI runner, agent memory inspector, simulation cost estimator) and from the 0 open PRs.

---

### 1. URL Document Ingestion

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** The most common MiroShark workflow is "I just read a news article and want to simulate reactions to it." Requiring users to manually copy-paste the article text creates unnecessary friction. URL ingestion — paste a link, system fetches and cleans the article — removes the single biggest onboarding barrier and makes MiroShark directly composable with news feeds, RSS readers, and research pipelines. Estimated 30-40% reduction in setup time for the most common use case.
**How:**
1. Add a `fetch_url` utility in `backend/app/utils/` using `httpx` for fetching and `trafilatura` (already common in Python NLP stacks) for clean text extraction from HTML — strips ads, nav, footers, leaving just article body. Fall back to `readability-lxml` if `trafilatura` yields <200 chars.
2. Add a "Paste URL" input tab to the document upload step in `frontend/src/` — user pastes a URL, system fetches it, shows a preview of the extracted text, and lets them confirm before proceeding. Wire to a new `/api/fetch-url` FastAPI endpoint.
3. Support the 5 most common URL types: news articles, GitHub README pages, Reddit threads, HN posts, and Medium articles. Document the supported formats in the README with examples.

---

### 2. Multi-Prediction Market Mode

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** A single auto-generated prediction market captures only one dimension of a simulation's uncertainty. Real events generate correlated questions: "Will the bill pass?" AND "Will approval ratings drop?" AND "Will markets react negatively?" Multi-market mode lets researchers model these dependencies — agents can trade across multiple markets with correlated positions. This is the feature that makes MiroShark useful for serious policy simulation and financial scenario analysis, directly differentiating from OASIS and CAMEL which have no prediction market layer at all.
**How:**
1. Update the config generation step to optionally generate 2–5 prediction markets instead of 1. Each market gets its own question, initial probability, and topic focus. Store them as an array in the simulation config JSON.
2. Update the Wonderwall AMM in `backend/wonderwall/` to support multiple simultaneous markets — each with independent constant-product pricing, order books, and P&L tracking. Agents are assigned a "primary market focus" but can trade in any market.
3. Update the UI report view to render a multi-market dashboard — price curves, volume bars, and final odds for each market side by side. Add a "Markets" tab to the simulation results view.

---

### 3. Custom Simulation Template Saver

**Type:** Feature
**Effort:** Small (hours)
**Impact:** Users run the same simulation archetype repeatedly — same agent count, same platform mix, same document type — but must reconfigure from scratch each time. A "Save as Template" button lets users persist their own configurations as named templates alongside the 6 built-in presets. This removes re-setup friction for power users, enables teams to share standardized configs, and creates the foundation for a future community template gallery. It's the "Save Preset" feature that every parameterized tool eventually needs.
**How:**
1. Add a `POST /api/templates` endpoint that accepts a simulation config JSON and a user-provided name/description, saves it to a `user_templates.json` file in `backend/app/storage/`. Return the saved template with an auto-generated `id`.
2. Update the preset templates UI panel to show user-saved templates alongside the 6 built-in presets, with a "Save current config as template" button at the bottom of the simulation setup form. User templates get a distinct visual indicator (e.g., a star icon).
3. Add a `DELETE /api/templates/:id` endpoint for removing saved templates, and a rename option via `PATCH`. Export/import via JSON download for sharing between instances.

---

### 4. Agent Influence Leaderboard

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** MiroShark generates rich interaction data — who replied to whom, who shifted whose belief, which posts got the most engagement — but buries it in the simulation feed. A leaderboard that surfaces the top influencers (by reply volume, belief-shift causation, and cross-platform reach) turns every simulation into a publishable finding: "Agent 'TechCEO_SF' drove 34% of all opinion shifts in this simulation." This is the kind of output that gets shared in research papers, social posts, and newsletter writeups — directly driving star growth and MiroShark's credibility as a research tool.
**How:**
1. Add an influence scoring pass at simulation end in `backend/app/services/`. For each agent, calculate: (a) reply/engagement received count, (b) belief-shift score (sum of belief deltas in agents who interacted with them), (c) cross-platform reach (appeared in Twitter + Reddit + Polymarket). Combine into a single influence score.
2. Add an `InfluenceLeaderboard.vue` component to the results view — top 10 agents ranked by influence score, each row showing name, platform distribution bar, influence score breakdown, and a "View Agent" button that opens the existing agent detail panel.
3. Add a downloadable "Influence Report" to the existing export functionality — JSON array of agents sorted by influence score, suitable for import into research tools or spreadsheets.

---

### 5. One-Click Cloud Deploy Button

**Type:** Growth
**Effort:** Small (hours)
**Impact:** MiroShark's setup requires Docker, Neo4j, Node 18+, Python 3.11+, and correct `.env` configuration — a 15-minute process that stops non-technical users cold. A "Deploy to Railway" button reduces this to 3 clicks and zero config. Railway natively provisions Neo4j, Python, and Node services from a `railway.json` config. This single change typically drives 2-3× fork increase from non-technical audiences (builders, researchers, product managers) who want to try MiroShark without touching the terminal. Direct path to the 500-star target.
**How:**
1. Create `railway.json` in the repo root defining a multi-service deployment: `neo4j` (Neo4j 5.15 community image), `backend` (Python + FastAPI), `frontend` (Node + Vite build). Map the environment variables from `.env.example` to Railway's secret injection format.
2. Add a `[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/...)` badge to the README's Quick Start section, directly below the existing cloud and Docker options. Create the Railway template in Railway's dashboard and link it.
3. Create a parallel `render.yaml` for Render.com as a fallback (many users prefer Render for its free tier). Document both options under a new "One-Click Deploy" section in the README with screenshots of the expected result.

---

## Selection Rationale

This batch targets MiroShark's current gaps after week two of merged features:

- **Onboarding friction** (#1, #5) — URL ingestion removes the copy-paste step; deploy button removes the install barrier. Both directly drive new user conversion and star growth toward the 500 target by April 15.
- **Research depth** (#2, #4) — Multi-market mode and influence analytics give researchers publishable outputs that differentiate MiroShark from academic competitors (OASIS, CAMEL).
- **Power user retention** (#3) — Template saving prevents re-setup churn for the users who run MiroShark most frequently.

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, no ambiguous design decisions, no external approvals needed.
