# Repo Action Ideas — 2026-06-02

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,223 stars · 262 forks · 1 open issue (#95 French locale) · 4 open PRs (all ecosystem additions: #138 HivemindOS, #139 Echo Oracle, #140 Capacitr, #141 SyntheticsAI)
**Recent activity:** PR #137 (agents.json, 26th publish-gated per-sim surface) merged June 2. PRs #132 (private share-link), #133 (UI fix), #134 (README diagrams) all merged June 1–2. Four ecosystem addition PRs opened today — HivemindOS, Echo Oracle, Capacitr, SyntheticsAI — bringing the named integrator count to 16+.

## Ecosystem Context

Four separate teams opened PRs today to add themselves to ECOSYSTEM.md. That single observation frames this batch.

The last two weeks built out MiroShark's machine-readable surface layer: signals, trajectories, agents, surface catalog, clone endpoint, private share-link. Those surfaces were built for integrators. The four PRs today are evidence the integrators arrived. But the ecosystem still exists only as a Markdown file — there's no machine-readable discovery path, no batch tooling for integrators running benchmark suites, and no per-project visibility layer for operators managing multiple published projects.

After 29 surfaces, the API can answer "what are the surfaces" (`/api/surfaces.json`) and "what is this sim" (any of 26 per-sim surfaces), but not "who is building on MiroShark" (`/api/ecosystem.json`) or "how are my simulations performing across projects" (`/api/project/<id>/stats`). The clone flow has a backend (PR #131) but no UI entry point. The JP community has been watching (`@m000_crypto` coverage since May 17) but there are zero Japanese-language docs.

Each of the five ideas below closes one of these gaps. Three are re-eligible from May-26. Two are net-new.

---

### 1. Ecosystem JSON Registry

**Type:** Integration
**Effort:** Small (hours)
**Impact:** Four ecosystem PRs opened today alone. The ecosystem now has 16+ named integrators with no machine-readable discovery path. `GET /api/ecosystem.json` turns ECOSYSTEM.md into a structured API surface: `[{name, url, description, category, github?, added_in_pr}]`. Any integrator can programmatically discover what else is built on MiroShark, cross-reference with `/api/surfaces.json`, and build tooling over the combined list without parsing Markdown. Follows the identical design pattern as `/api/surfaces.json` (PR #130) — static-and-hardcoded, not auto-derived from parsing ECOSYSTEM.md. Re-eligible from May-26 #5.

**How:**
1. Add `backend/app/services/ecosystem_catalog.py` (~100 LoC, pure stdlib). Static hardcoded `ECOSYSTEM_ENTRIES` list (same principle as `surfaces_catalog.py` — explicitly NOT auto-parsed from ECOSYSTEM.md; Markdown parsing is fragile and would silently drift). Each entry: `{name: str, url: str, description: str, category: str ("product" | "tool" | "integration" | "agent" | "benchmark"), github: str | null, added_in_pr: int | null}`. Include all 12 named integrators from ECOSYSTEM.md plus the 4 pending PRs (#138–#141). Add `GET /api/ecosystem.json` to `backend/app/api/surfaces.py` (alongside the existing surfaces catalog route). Response envelope: `{schema_version: "v1", count: int, updated_at_pr: int (highest added_in_pr value), ecosystem: list[dict]}`. `Cache-Control: public, max-age=3600`. `ETag: ecosystem-v1-<count>`. Add 6 offline unit tests in `test_unit_ecosystem_catalog.py`: response has all required envelope fields, `count` matches list length, all entries have required keys (name/url/description/category), `category` is one of the five allowed values, ETag header present, `updated_at_pr` is a positive int. Add `GET /api/ecosystem.json` to `docs/API.md` under Gallery & Discovery. Add `EcosystemRegistry` + `EcosystemEntry` schemas to `openapi.yaml`. Add "Ecosystem JSON Registry" to `docs/FEATURES.md`. Zero new deps.
2. Update `ECOSYSTEM.md` to add a machine-readable note near the top: `> Machine-readable: \`GET /api/ecosystem.json\`` (one line, inline with the existing intro). Update `backend/app/api/surfaces.py` to register `ecosystem_json` as a platform-level surface key alongside `stats` and `surfaces_catalog`. Add `getEcosystem()` to `frontend/src/api/simulation.js`. No frontend view needed.

---

### 2. Scenario Clone Button

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** `GET /api/simulation/<id>/clone.json` (PR #131) shipped June 1 — it returns the exact inputs a sim was built with, wire-compatible with `POST /api/simulation/create`. But there's no UI entry point to use it. An operator or researcher viewing a published share page has no one-click way to launch a new simulation with the same configuration. This closes that loop: a "🔀 Clone this scenario" button in `EmbedDialog.vue` fetches clone.json, constructs a `/?clone=<id>` URL, copies it to the clipboard, and shows a toast ("Clone link copied — open to pre-fill a new simulation"). The create/home view reads `?clone=<sim_id>` on mount, fetches clone.json, and pre-fills the form fields (scenario, URL list, rounds, agent count). The API is built; this is the last 10% — the UX layer that makes it discoverable. Re-eligible from May-26 #3.

**How:**
1. Add `?clone=<sim_id>` param handling to the home/create Vue component (likely `Home.vue` or `NewSimulation.vue`). On mount: if `route.query.clone` is present, fetch `GET /api/simulation/{clone}/clone.json`. On success: pre-fill the Simulation Prompt textarea with `scenario_title` (and `simulation_prompt` if present), add URLs from `simulation_urls` to the URL import list, set rounds + agent_count sliders to cloned values. Show a dismissible info banner: "Cloned from simulation [clone_id] — edit and launch your own run." Same banner pattern as the existing Shareable Scenario Link pre-fill (orange-edged, dismissible). After pre-fill, strip `?clone=` from the URL via `router.replace` so a refresh doesn't re-fetch. 404 or fetch error → show error toast and continue silently. Add `getCloneJson(simId)` to `frontend/src/api/simulation.js`.
2. In `EmbedDialog.vue`, add a "🔀 Clone this scenario" button to the bottom of the Share & Embed section (alongside the Copy URL / Copy embed code buttons). Clicking it constructs `window.location.origin + '/?clone=' + simId`, copies to clipboard via the Clipboard API, shows a `success` toast. Publish-gated: visible only when `is_public` is true (clone.json is itself publish-gated). No new API calls in the button itself — the URL construction is client-side; the clone.json fetch happens on the receiving end.
3. Add `?clone=<sim_id>` to `docs/API.md` under "Shareable Scenario Links" as a fifth query parameter (alongside `scenario`, `url`, `ask`, `template`). Add a note: "Pre-fetches `clone.json` and fills the scenario, URLs, and config fields; strips the param after pre-fill." Update `docs/FEATURES.md` Shareable Scenario Links section with the clone variant. No backend changes needed. No new deps.

---

### 3. Japanese README & Features Guide

**Type:** Community
**Effort:** Medium (1–2 days)
**Impact:** `@m000_crypto` coverage on May 17 was MiroShark's first Japanese-language mention; the JP crypto and AI research communities are among the most active multilingual GitHub audiences globally. The docs tree has comprehensive Chinese translations (FEATURES.zh-CN.md, API.zh-CN.md, ARCHITECTURE.zh-CN.md, and 10 more) but zero Japanese files. A `README.ja.md` + `docs/FEATURES.ja.md` gives the JP audience a native-language entry point, signals community commitment, and adds `日本語` to the FEATURES.md language toggle (currently `English · 中文`). Re-eligible from May-26 #2 (CN half delivered; JP half still unbuilt).

**How:**
1. Create `docs/FEATURES.ja.md` — a full Japanese translation of `docs/FEATURES.md`. Translate all section headings, the feature table (column headers + all ~55 feature name/description rows), and the detailed per-feature narrative sections. Preserve all English code examples, endpoint paths, query param names, field names, and curl snippets verbatim — these are developer-facing identifiers and must not be translated. Add the language toggle at the top: `<sup>[English](FEATURES.md) · [中文](FEATURES.zh-CN.md) · 日本語</sup>`. Update `docs/FEATURES.md` and `docs/FEATURES.zh-CN.md` to add `· [日本語](FEATURES.ja.md)` to their respective language toggles.
2. Create `README.ja.md` at root — a Japanese translation of the key README.md sections: project description, core capabilities (5–7 bullet points), Quick Start steps, and Links section. Not a full clone — scope to what a JP developer needs to understand the project and begin. Add `[日本語](README.ja.md)` to the README.md language strip at the top. Match `README.md` section structure for easy diff maintenance.
3. Create `docs/WEBHOOKS.ja.md` and `docs/NOTIFICATIONS.ja.md` — the two docs most accessed by integrators and most relevant to JP teams building webhook-driven pipelines on MiroShark. These are shorter than FEATURES.ja.md and complete the integration-path docs in Japanese. No backend changes; no new deps.

---

### 4. Simulation Batch Create API

**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** Integrators running benchmark suites — AntFleet's `miroshark-bench`, SyntheticsAI's test pipeline, and at least 14 other named integrators — currently need N sequential API calls to create N simulations. `POST /api/simulation/batch` accepts an array of sim configs (same shape as `POST /api/simulation/create`, up to 10 per request) and creates each in sequence, returning `{created: N, failed: N, results: [{index, sim_id, status, error?}]}`. Reduces benchmark setup from N round-trips to 1; enables the standard pattern "create 10 sims → receive completion webhooks → pull signal.json from each" without scripting a loop around the single-create endpoint. Net-new.

**How:**
1. Add `POST /api/simulation/batch` to `backend/app/api/simulation.py`. Request body: `{simulations: list[SimCreateBody]}` where `SimCreateBody` is the same shape accepted by the single-create endpoint. Validation: `len(simulations) == 0` → 400 `{"error": "batch must contain at least one simulation"}`; `len(simulations) > 10` → 400 `{"error": "batch size limit is 10"}`. For each config in order: call the existing `create_simulation(...)` service function, collect result. On individual failure, record `{index: i, sim_id: null, status: "failed", error: str}` and continue — never abort the whole batch. Response: `{created: int, failed: int, total: int, results: list[{index: int, sim_id: str | null, status: "created" | "failed", error: str | null}]}`. Admin-gated via `require_admin_token` (same as single `/create`). Reuses all existing validation from `create_simulation()` — no new validation logic. Add 8 offline unit tests in `test_unit_batch_create.py`: empty array → 400, array of 11 → 400, single valid config → created=1 failed=0, 3 valid → created=3 failed=0, partial failure (mock one create to raise) → failed count correct, `results` array length equals input length, `index` field matches input position, unauthenticated request → 401.
2. Add `batchCreateSimulations(configs)` to `frontend/src/api/simulation.js`. No frontend UI — this is a pure API-consumer surface for integrators. Add a note in `EmbedDialog.vue` under the existing API endpoints list pointing to the batch endpoint.
3. Add `POST /api/simulation/batch` to `docs/API.md` under Simulation Lifecycle with `BatchCreateRequest` + `BatchCreateResponse` + `BatchResultEntry` schemas and an integrator example (jq pipeline extracting sim_ids → polling run-status → pulling signal.json). Add to `openapi.yaml`. Add "Simulation Batch Create" to `docs/FEATURES.md` under Integrations. Zero new deps.

---

### 5. Per-Project Simulation Statistics

**Type:** Feature / DX
**Effort:** Small (hours)
**Impact:** `/api/stats` returns platform-aggregate numbers (total sims, avg confidence, total surface views across all projects). No per-project slice exists. An operator who has published 20 sims across 3 projects has no API call to ask "how are project X's sims performing specifically — consensus distribution, average quality, total views for just that project?". `GET /api/project/<project_id>/stats` answers this: same aggregate metrics as `/api/stats` but filtered to one project. Operators building dashboards over their published sims get a single-call summary. AntFleet can track benchmark quality metrics per named project run. The `project_id` field is already tracked per sim in `platform_stats.py:42-49`; this is a ~150 LoC read path over existing data. Net-new.

**How:**
1. In `backend/app/services/platform_stats.py`, add `get_project_stats(project_id: str, sim_root: str) -> dict`. Scan all sim dirs where `state.get("project_id") == project_id` (case-sensitive match, consistent with how `project_id` is used as a routing identifier). Per matched sim: count `total_sims`; count `published_sims` if `is_public=True`; count `completed_sims` / `failed_sims` by `status`; compute consensus direction + quality_health from completed sims. Build response: `{project_id: str, total_sims: int, published_sims: int, completed_sims: int, failed_sims: int, consensus_distribution: {bullish_count: int, neutral_count: int, bearish_count: int}, avg_confidence_pct: float | null (null if no completed sims), quality_distribution: {excellent: int, good: int, fair: int, poor: int}, total_surface_views: int}`. Sanitize `project_id` param: regex `[a-zA-Z0-9_.\-]{1,120}`, 400 on invalid. Unknown project_id → return all counts 0 (not 404 — absence is not an error). Add `GET /api/project/<project_id>/stats` to `backend/app/api/stats.py`. No auth (same as `/api/stats`). `Cache-Control: public, max-age=60`. `ETag: project-stats-<project_id>-<total_sims>`. Add 8 offline unit tests in `test_unit_project_stats.py`: unknown project_id → all counts 0, 3 matching sims → `total_sims=3`, non-matching excluded, `published_sims` counts only is_public=True, `avg_confidence_pct` averages correctly across completed, `quality_distribution` counts correct, invalid project_id chars → 400, `total_surface_views` sums per-sim surface_views.
2. Add `getProjectStats(projectId)` to `frontend/src/api/simulation.js`. No frontend view needed — this is an operator/integrator-facing API surface. Add a note to `docs/OBSERVABILITY.md` pointing operators toward this endpoint for per-project monitoring.
3. Add `GET /api/project/<project_id>/stats` to `docs/API.md` under Observability with a `ProjectStats` schema. Document the `project_id` sanitization rule, 0-returns-not-404 behavior, and `avg_confidence_pct: null` case. Add to `openapi.yaml`. Add "Per-Project Simulation Statistics" to `docs/FEATURES.md` under Observability. Zero new deps.

---

## Selection Rationale

Four ecosystem PRs opened today in the same window this batch was generated — HivemindOS, Echo Oracle, Capacitr, SyntheticsAI. The signal is clear: the ecosystem is growing faster than the tooling that serves it.

- **Ecosystem JSON Registry** (#1) — Re-eligible May-26. 16+ integrators and no machine-readable discovery path. The machine-readable ecosystem surface was the obvious pairing for `/api/surfaces.json` but deferred until the ecosystem had enough mass to justify it. Four PRs in one day is that mass. ~100 LoC, identical pattern to the surfaces catalog.
- **Scenario Clone Button** (#2) — Re-eligible May-26. clone.json shipped June 1. The frontend gap has existed for exactly one day. The API is built; this is the UX layer to make it discoverable — a button and a `?clone=` query param.
- **Japanese README & Features** (#3) — Re-eligible May-26 (CN half delivered; JP half still unbuilt). `@m000_crypto` JP coverage since May 17. Comprehensive CN docs exist; zero JP files do. Medium effort but high community signal.
- **Simulation Batch Create API** (#4) — Net-new. AntFleet, SyntheticsAI, and 14 other named integrators need this. Benchmark pipelines involve creating N sims. N round-trips is the current friction. Medium effort, high integration leverage as the ecosystem grows.
- **Per-Project Simulation Statistics** (#5) — Net-new. `platform_stats.py` already tracks `project_id`; this is a 150 LoC read path over data already being written. Operators managing multiple projects currently have no per-project aggregate view.

Excluded (blocked): **Operator Profile** — requires an `operator` field on `SimulationState`; `platform_stats.py:42-49` documents `project_id` as the closest stable identifier. Building this surface requires a data-model change outside autonomous scope.
