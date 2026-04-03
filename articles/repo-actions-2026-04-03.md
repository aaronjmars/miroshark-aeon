# Repo Action Ideas — 2026-04-03

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 411 stars · 66 forks · 3 contributors · 1 open issue · 1 open PR (one-click-cloud-deploy)
**Recent activity:** URL ingestion merged, Agent Influence Leaderboard merged, repo cleanup (images, test artifacts). One-click cloud deploy PR #9 open. Star trajectory: 411 / 500 target by Apr 15 — ~7 stars/day needed, ~18/day recent pace, well on track.

## Ecosystem Context

MiroShark enters April with its core feature set in strong shape — export, replay, templates, network viz, URL ingestion, influence leaderboard, MCP server. The next opportunity is quality and depth: fixing real friction points exposed by actual users, unlocking research-grade outputs, and making configuration feel like a first-class experience.

Key signals driving this batch:

- **Issue #8 (open, 0 replies):** A real user is stuck in the "Generate Simulation Configuration" step with the frontend polling `/api/simulation/config/realtime` forever. No timeout, no error display, no recovery path. This is the most visible UX failure in the repo right now — unanswered issues on a 411-star repo signal rough edges to evaluators. Fixing it with clear diagnostics turns a support failure into a demonstration of project quality.
- **LLM setup is invisible:** OpenRouter model selection requires manually editing `.env`. Experienced users know where to look; new users don't. A settings panel that surfaces model choice and key validation removes the last invisible configuration step. This is especially relevant now that one-click cloud deploy will bring more non-technical users.
- **Multi-run statistical credibility:** Academic simulation tools (OASIS, NetLogo, Mesa) all report results as distributions, not single runs. A single MiroShark run is interesting; 10 runs with confidence intervals is publishable. This is the feature that upgrades MiroShark from "cool demo" to "research tool" in a single PR.
- **Simulation comparison is the natural next step after replay:** Users already have replay. The question they now ask is "what if I changed the agent mix?" or "how does Twitter-heavy vs Reddit-heavy differ?" Side-by-side comparison answers this and creates shareable, tweetable outputs.
- **Bulk persona import for research teams:** Researchers and simulation practitioners have predefined agent cohorts — demographically calibrated, role-defined, sometimes thousands of profiles. Requiring them to regenerate personas from documents every time blocks serious research use. CSV/JSON import unblocks this segment.

These 5 ideas are distinct from all previously suggested ideas: webhooks, A/B testing, embeddable widget, replay ✓, gallery, WebSocket streaming, snapshot sharing, prompt scoring, doc preprocessing, benchmarking, network viz ✓, REST API, multi-document comparison, Discord bot, belief analytics, MCP server, demographic calibration, CLI runner, agent memory inspector, simulation cost estimator, multi-prediction market, custom template saver, URL ingestion ✓, one-click deploy ✓.

---

### 1. Config Generation Timeout & Error Recovery

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** Issue #8 is the only open issue on MiroShark — a user stuck in step 3 (config generation) with the frontend polling forever, no error, no recovery path. This fix adds a configurable client-side timeout (default: 90s) to the config polling loop, surfaces the actual failure reason (LLM error, timeout, empty response) in the UI with a visible error panel, and adds a "Retry" button that restarts the config generation call. A single unanswered issue on a growth-stage repo signals quality problems to evaluators — closing it with a clean fix plus a public reply directly supports the 500-star goal.
**How:**
1. In `frontend/src/views/SimulationRunView.vue` (or whichever view handles step 3), add a polling timeout: if the `/api/simulation/:id/config/realtime` endpoint returns no meaningful progress after 90 seconds, stop polling and render an error state with the last known response body. Add a "Retry Generation" button that calls a new `/api/simulation/:id/config/retry` endpoint.
2. In `backend/app/services/simulation_config_generator.py`, add structured error responses: instead of hanging or returning empty data on LLM failure, return `{"status": "error", "stage": "config_generation", "reason": "llm_timeout|empty_response|invalid_json", "detail": "..."}`. Wrap the LLM call with the existing `retry.py` utility and surface the final exception message.
3. Reply to issue #8 with the fix explanation and a pointer to the error message it would have shown — this closes the issue, demonstrates responsiveness, and makes the project look actively maintained.

---

### 2. Simulation Comparison Mode

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** The natural question after running a simulation is "how would this differ with a different agent mix?" or "does the document framing change the outcome?" Comparison mode lets users run two simulations with different configs (agent demographics, document variants, platform weights) and view the results side by side: prediction market divergence, belief shift vectors, influence ranking deltas. This creates shareable, tweetable outputs ("Twitter-heavy vs Reddit-heavy: 23% divergence in market probability") and directly differentiates MiroShark from single-run tools like OASIS and CAMEL.
**How:**
1. Add a "Compare" button to the results view that opens a second simulation slot. The second simulation can clone the first config (with a "Change parameters" panel) or start from a saved template. Store both simulation IDs in the URL (`/compare/:id1/:id2`) so comparison views are linkable.
2. Build a `ComparisonView.vue` component that renders the two simulation IDs side by side with a diff overlay: prediction market prices (line chart with two colored series), influence leaderboard (left vs right rank badges), belief shift heatmap (two columns). Wire to the existing `/api/simulation/:id/report` and influence scoring endpoints — no new backend logic needed.
3. Add a "Download Comparison" export button that writes a JSON file with both simulation IDs, the diffed metrics, and a `divergence_score` (normalized mean absolute difference across all prediction market outcomes).

---

### 3. Multi-Round Statistical Aggregation

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** A single simulation run is stochastic — agent responses vary with LLM temperature, turn order, and sampling. Running the same config N times and aggregating results into confidence intervals ("65% ± 8% probability the bill passes across 10 runs") transforms MiroShark from a demo tool into a credible research instrument. Academic simulation papers (OASIS, Park et al. 2023) all report distributions. This is the feature that earns MiroShark citations and gets it shared by simulation researchers, a segment with high social reach in the target audience.
**How:**
1. Add a "Run N times" option to the simulation launch form — a number input (default 1, max 10 for cost/time reasons) that creates N simulation runs with identical configs but different random seeds. Store the batch under a `batch_id` in the existing simulation storage. Add a `POST /api/simulation/batch` endpoint that queues N runs sequentially (to avoid LLM rate limits).
2. Add a `GET /api/simulation/batch/:batch_id/aggregate` endpoint in `backend/app/services/` that reads all N completed simulations in the batch and computes: mean ± std for each prediction market final probability, top-5 most consistently influential agents (appeared in top-5 across ≥70% of runs), belief shift confidence bands (percentile ranges across runs).
3. Build a `BatchResultView.vue` component that renders the aggregated output: market probability distribution (box plot or range band overlay on the price chart), stable influencer list, and a run-by-run breakdown table. Add a "Download Statistical Report" export to CSV.

---

### 4. Agent Persona Bulk Import (CSV/JSON)

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** Researchers and simulation practitioners — MiroShark's highest-value users — have predefined agent cohorts: demographically calibrated profiles from survey data, fictional character sets for media research, or role-based archetypes from organizational models. Requiring them to regenerate personas from a document every time blocks serious research use and forces artificial document construction. Bulk import via CSV or JSON lets these users bring their own agent definitions directly, making MiroShark compatible with existing research pipelines and academic datasets.
**How:**
1. Add an `agent_import` tab to the simulation setup form alongside the existing document upload and preset template options. Accept CSV (columns: `name`, `persona`, `platform`, `age`, `political_leaning`, `occupation`) or JSON (array of agent objects with the same fields). Show a preview table of parsed agents before the user proceeds.
2. Add a `POST /api/simulation/agents/import` FastAPI endpoint that validates the uploaded file, normalizes the agent fields to match the existing agent schema in `backend/app/models/`, and returns a preview payload. On confirmation, write the agents to the simulation config in place of the LLM-generated persona set.
3. Provide a downloadable CSV template with the correct column headers and 3 example rows linked from the import UI. Also add a "Export agents as CSV" button to the results view so users can save and re-import agent cohorts from completed simulations.

---

### 5. LLM Provider & Model Selector UI

**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** MiroShark's LLM configuration lives entirely in `.env` — users must know to edit `OPENROUTER_MODEL` manually, have no visibility into which model is active during a run, and get no feedback if the model name is invalid. Now that one-click cloud deploy (PR #9) brings non-technical users, invisible configuration becomes a support burden. A settings panel that shows the active model, lets users switch from a dropdown of OpenRouter's supported models (organized by cost/capability tier), and validates the API key on save reduces setup friction and eliminates the most common "why isn't this working?" question.
**How:**
1. Add a settings gear icon to the main nav in `frontend/src/App.vue` that opens a `SettingsPanel.vue` modal. The panel has two sections: "LLM Configuration" (model selector dropdown, API key field with a "Test Connection" button) and "Graph Database" (Neo4j URI/credentials with a "Test Connection" button).
2. Add a `GET /api/settings` endpoint that returns the current active config (model name, masked API key, Neo4j URI) and a `POST /api/settings` endpoint that updates `backend/app/config.py` at runtime (without restart, using a mutable config object). Add a `POST /api/settings/test-llm` endpoint that makes a minimal test call to OpenRouter and returns the model's response time and name.
3. Populate the model dropdown by calling `GET https://openrouter.ai/api/v1/models` (OpenRouter's public model list endpoint) on settings panel open — group by tier (Fast <$0.5/M, Standard $0.5–5/M, Capable >$5/M). Cache the list for 24h. Default selection highlights the model currently set in `config.py`.

---

## Selection Rationale

This batch targets MiroShark's next layer of maturity — from "working demo" to "reliable research tool":

- **Issue resolution** (#1) — Config error recovery closes the only open issue and signals active maintenance to evaluators.
- **Research credibility** (#2, #3) — Comparison mode and statistical aggregation produce publishable outputs that differentiate MiroShark from single-run competitors and drive sharing among the academic/research audience.
- **User segment expansion** (#4) — Bulk persona import unblocks researchers with existing agent cohorts, a high-value segment that will cite and share the tool.
- **Onboarding polish** (#5) — LLM provider UI removes the last invisible configuration step, especially critical now that one-click deploy brings non-technical users who won't read the `.env.example`.

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, no ambiguous design decisions, no external approvals needed.
