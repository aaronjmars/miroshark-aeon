# Repo Action Ideas — 2026-05-28

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,207 stars · 257 forks · 2 open issues (#95 French locale) · 1 open PR (#106 Railway deployment, external/Devin)
**Recent activity:** PR #120 (WEBHOOK_EVENTS dispatch filter, 24th surface) merged today; PR #119 (README: Use Cases above Features), PR #118 (README: condensed feature table + diagram images), PR #117 (Noelclaw = 11th ecosystem integrator) all merged this window. Token: $0.00000742 (-47% 24h, -83% from ATH $0.0000436 May 18); FDV $742K.

## Ecosystem Context

The merge log since yesterday tells two stories at once: the product is accelerating (24th surface shipped in 24 hours) and the documentation layer is catching up to it (PRs #118 and #119 both refined README discoverability on the same day). The maintainer is actively closing the gap between what MiroShark can do and what an arriving developer can immediately see it can do.

Three analytical gaps are now the clearest bottlenecks for the integrator cohort:

**The integrator data access gap.** Eleven integrators are named in ECOSYSTEM.md. None of them have a machine-readable index of what's been published on the platform — they either scrape the HTML gallery at `/explore` or call specific sim endpoints by ID. `GET /api/gallery.json` is the paginated JSON index of all public, completed simulations that every directory builder, Aeon skill, and external data consumer needs as a starting point. The filtered search endpoint (still unbuilt) comes after the full index exists; you can't filter what you can't list. Re-eligible from May-20 (unbuilt).

**The turbulence measurement gap.** `signal.json` gives direction + confidence. `peak-round` gives inflection points. Neither answers "how contested was the path to consensus?" — whether the swarm converged quickly and quietly (stable) or swung violently before settling (contested). `GET /api/simulation/<id>/volatility` computes per-round belief delta standard deviation and returns a 0–100 volatility index. A high-volatility Bullish signal is a different investment input than a low-volatility one. The analytical surface that makes signal.json and peak-round useful together. Re-eligible from May-20 (unbuilt).

**The webhook verification gap.** With 11+ named integrators each wiring MiroShark's webhook into their own pipeline, every new integration starts with the same painful loop: configure `WEBHOOK_URL`, wait for a real sim to complete, hope the payload arrives. `POST /api/webhook/test` sends a synthetic test payload — same shape as a real completion, including HMAC signature — to the configured endpoint, and returns delivery status immediately. Eliminates the "wait for a sim to test your endpoint" loop entirely. Re-eligible from May-20 (unbuilt).

Two net-new ideas close the picture:

**The comparative analysis gap.** AntFleet is using MiroShark as a benchmark target for multi-model consensus review — comparing sim outputs across model configurations. Researchers running variant sims (same scenario, 5 vs 20 agents; neutral vs charged phrasing) currently need to download two JSON files and diff them manually. `GET /api/compare?a=<simId>&b=<simId>` returns a structured comparison: delta in belief distributions, consensus agreement (do they agree on direction?), confidence delta, quality comparison. One curl command replaces a two-step manual process. Pairs naturally with the clone button (still unbuilt) to close the full variant-analysis loop.

**The capability discovery gap.** MiroShark has 24 publish-gated surfaces. No API endpoint lists them programmatically — operators discover surfaces by reading docs, not by querying the platform. `GET /api/surfaces.json` returns the full surface catalog: key, endpoint, description, type, example curl. Integrators can query this to know exactly what's available on a given deployment. Enables Aeon to detect the live surface count without parsing FEATURES.md. Completely static — a hardcoded catalog — so ~30 LoC with no file scanning.

Previously suggested ideas excluded from this batch (7-day window May 22–28): Private Share Link (May-22 #1, unbuilt); French Locale (May-22 #2, unbuilt); Operator Profile (May-24 #3, unbuilt); Agent Persona Export JSON (May-24 #4, unbuilt); Simulation Search JSON API (May-24 #5, unbuilt); CN+JP README (May-26 #2, unbuilt); Scenario Clone Button (May-26 #3, unbuilt); Ecosystem JSON Registry API (May-26 #5, unbuilt). All 5 ideas below are net-new or re-eligible.

---

### 1. Gallery Public JSON

**Type:** Integration
**Effort:** Small (hours)
**Impact:** The gallery HTML at `/explore` is human-facing; no machine-readable equivalent exists. `GET /api/gallery.json` returns a paginated JSON index of all published, completed simulations — each with `{sim_id, title, direction, confidence_pct, quality_health, total_rounds, created_at, surface_views}`. External directories, Aeon's integrator-discovery skills, and dashboard builders can consume this without scraping HTML. Distinct from the planned search.json (query-filtered, still unbuilt) — gallery.json is the unconditional full index, the foundation every derived query starts from. Re-eligible from May-20 (unbuilt).

**How:**
1. Add `backend/app/api/gallery_json.py` (new blueprint, ~100 LoC, stdlib `json` + `os`). `GET /api/gallery.json` — query params: `page` (int ≥ 1, default 1), `per_page` (int 1–100, default 20), `sort` (`recent` default / `confidence_desc` / `views_desc`). Reads from the same sim_root scan as the existing gallery service. Filter: `is_public=True` + `status="completed"`. Per sim: `{sim_id, title: str[:120], direction: str, confidence_pct: float, quality_health: str, total_rounds: int, created_at: str (ISO-8601), surface_views: int}`. Response: `{page, per_page, total, sims: list[dict]}`. `Cache-Control: public, max-age=60`. `ETag: f"{total}-{newest_created_at}"[:16]`; 304 on match. Register blueprint in `backend/app/__init__.py`. Add 8 offline unit tests in `test_unit_gallery_json.py`: returns valid structure, `total` accurate, `page`+`per_page` math correct, sort orders work, unpublished/incomplete excluded, `confidence_pct` is float, ETag header present, `per_page=1` returns exactly 1 result.
2. Add `<link rel="alternate" type="application/json" href="/api/gallery.json" title="MiroShark Simulation Gallery">` in the `/explore` page `<head>` for auto-discoverability (same injection pattern as OG tags). In the `/explore` HTML gallery, add an unobtrusive `[JSON ↗]` badge link near the filter bar pointing to `/api/gallery.json`. Add `getGalleryJson(page, perPage, sort)` to `frontend/src/api/simulation.js`.
3. Add `GET /api/gallery.json` to `docs/API.md` under Gallery & Discovery with a `GalleryPage` schema and pagination pattern note. Add `GalleryPage` + `GallerySimEntry` schemas to `openapi.yaml`. Add "Gallery JSON API" to `docs/FEATURES.md` under Gallery & Discovery. Zero new deps.

---

### 2. Simulation Comparison API

**Type:** Feature / Integration
**Effort:** Small (hours)
**Impact:** AntFleet is benchmarking MiroShark across model configurations — comparing sim outputs is their core workflow. Researchers running variant analysis (same scenario, different agent counts or phrasing) currently need to download two sim JSON files and diff them manually. `GET /api/compare?a=<simId>&b=<simId>` returns a structured comparison: delta in bullish/neutral/bearish pct, delta in confidence, consensus agreement (same direction?), quality tier comparison, rounds delta. One curl command replaces a two-step manual process. The natural partner to the clone button (still unbuilt) — clone creates the variant, compare measures the difference. Net-new.

**How:**
1. Add `backend/app/services/comparison_service.py` (~120 LoC, stdlib `json` + `os`). `load_sim_summary(sim_id, sim_root) -> dict | None`: reads `simulation_state.json` for the given sim; returns `{sim_id, scenario_title, direction, bullish_pct, neutral_pct, bearish_pct, confidence_pct, quality_health, total_rounds, created_at}` for published/completed sims; `None` for missing/unpublished/incomplete. `build_comparison(a, b) -> dict`: `{sim_a: dict, sim_b: dict, agreement: {same_direction: bool, direction_a: str, direction_b: str}, deltas: {bullish_pct: float (b-a), neutral_pct: float, bearish_pct: float, confidence_pct: float, rounds: int}, quality_comparison: "a_wins"|"b_wins"|"tied"}` (quality tier rank: excellent > good > fair > poor). Add `GET /api/compare` (no auth; both sims must be published/completed; 404 `{"error": "sim_a not found or not published"}` / `{"error": "sim_b not found or not published"}`; 400 `{"error": "cannot compare a simulation to itself"}` when a==b). `Cache-Control: public, max-age=60`. Add 10 offline unit tests in `test_unit_comparison.py`: two bullish sims → `same_direction: true`, bullish vs bearish → `same_direction: false`, `confidence_pct` delta = b-a, unpublished sim → 404, unknown sim → 404, a==b → 400, quality tiers rank correctly (excellent > good), `rounds` delta correct, `quality_comparison: "tied"` when same tier, response includes full `sim_a` + `sim_b` summary blocks.
2. Add `compareSimulations(simIdA, simIdB)` to `frontend/src/api/simulation.js`. In the simulation detail view (wherever Share/Embed actions appear), add a "Compare" action button. On click: a minimal search-by-ID input modal where the user enters the second sim ID, then navigates to `/compare?a=<id1>&b=<id2>`. Add `CompareView.vue` in `frontend/src/views/` — route `/compare` (add to router). Layout: two summary cards side-by-side, delta row below each belief pct field (↑ green / ↓ red / — gray), consensus agreement chip (Agree/Disagree), quality winner chip.
3. Add `GET /api/compare` to `docs/API.md` under Analytics with a `ComparisonResult` + `SimSummary` schema and a variant-analysis curl example. Add to `openapi.yaml`. Add "Simulation Comparison" to `docs/FEATURES.md` under Data Export & Analysis. Zero new deps.

---

### 3. Belief Volatility Score

**Type:** Feature
**Effort:** Small (hours)
**Impact:** `signal.json` gives direction + confidence. `peak-round` gives inflection points. Neither answers "how contested was the path to consensus?" A high-volatility Bullish result — where agents swung repeatedly before aligning — is a different signal from a low-volatility one where consensus formed in the first three rounds. `GET /api/simulation/<id>/volatility` computes per-round belief delta standard deviation and a 0–100 volatility index, plus a `trend` label (Converging/Stable/Contested). The 25th publish-gated surface; completes the analytical quadrant alongside signal.json, peak-round, and sparklines. Pure O(n) pass over trajectory data; stdlib only. Re-eligible from May-20 (unbuilt).

**How:**
1. Add `backend/app/services/volatility_service.py` (~130 LoC, stdlib `json` + `os` + `math`). Reads `trajectory.json` rounds. Per consecutive round pair: compute `bullish_delta = |bullish_pct_n - bullish_pct_{n-1}|` (and same for neutral, bearish). Aggregates: `mean_delta: float`, `std_dev_delta: float` (population std dev of per-round bullish deltas), `max_delta: float` (largest single-round bullish swing), `max_delta_round: int`, `volatility_index: float` (normalized 0–100: `min(std_dev_delta * 5, 100)` — calibrated so a std_dev of 20pp maps to index 100), `trend: str` ("converging" if std dev of second-half deltas < std dev of first-half deltas, "stable" if `std_dev_delta < 3`, "contested" otherwise), `total_rounds: int`. Returns `None` for single-round or empty trajectory. Add `GET /api/simulation/<id>/volatility` (publish-gated; 404 `{"error": "no trajectory data"}` when None). Extend `SURFACE_KEYS` + `surface_stats` with `volatility`. Add 12 offline unit tests in `test_unit_volatility.py`: single-round → None/404, monotone trajectory → `std_dev_delta=0, trend="stable"`, high-swing trajectory → `volatility_index` elevated, `max_delta_round` at correct index, `mean_delta` arithmetic check, `volatility_index` capped at 100, published → 200, unpublished → 403, `total_rounds` matches input, `trend="converging"` when second half calmer, `trend="contested"` when std_dev ≥ 3, `surface_stats` increment called.
2. Add `getVolatility(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "📈 Belief Volatility" section (publish-gated; positioned after the "📊 Peak Beliefs" section). Layout: `Volatility index: {n}/100` with a horizontal bar (gradient: green ≤33 / amber 34–66 / red ≥67), `Max swing: ±{pct}% at round {n}`, `Path: {trend}` chip (Converging = green / Stable = gray / Contested = amber). "Copy volatility JSON URL" button.
3. Add `GET /api/simulation/<id>/volatility` to `docs/API.md` under Analytics with a `VolatilityResponse` schema defining `volatility_index` normalization. Add `VolatilityResponse` to `openapi.yaml`. Add "Belief Volatility Score" to `docs/FEATURES.md` under Data Export & Analysis. Zero new deps.

---

### 4. Webhook Test Ping

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Every operator integrating webhooks hits the same loop: configure `WEBHOOK_URL`, wait for a real sim to complete, hope the payload arrived. With 11+ named integrators each wiring MiroShark's webhook into their own pipeline, this debugging wait happens at least once per integration setup. `POST /api/webhook/test` sends a synthetic test payload — same JSON shape as a real completion, including HMAC signature — to the configured `WEBHOOK_URL`, and returns `{delivered, status_code, latency_ms}` immediately. Integrators know within seconds whether their endpoint is reachable and signature-verified, before running a single real sim. Reuses the existing HMAC dispatch infrastructure; ~60 new LoC. Re-eligible from May-20 (unbuilt).

**How:**
1. Add `POST /api/webhook/test` route (~60 LoC, reuses the HTTP dispatch logic from `webhook_service.py`). The test payload is a hardcoded struct matching the production payload schema exactly: `{sim_id: "test-ping-{unix_timestamp}", status: "completed", is_test: true, scenario_title: "Webhook Test Ping — ignore this delivery", final_beliefs: {direction: "Bullish", bullish_pct: 65.0, neutral_pct: 22.0, bearish_pct: 13.0}, confidence_pct: 65.0, quality_health: "good", total_rounds: 5}`. Compute HMAC signature with `WEBHOOK_SECRET` (same function as prod dispatch). POST to `WEBHOOK_URL`; capture HTTP status code + latency. Return: `{delivered: bool (status_code < 400), status_code: int, latency_ms: float, webhook_url_suffix: last 12 chars of URL (masked), timestamp: ISO-8601}`. Return 503 `{"error": "WEBHOOK_URL not configured"}` if blank. Auth-gate via `X-Admin-Token` (same pattern as existing config-sensitive routes). Add 6 offline unit tests in `test_unit_webhook_test.py`: no WEBHOOK_URL → 503, successful HTTP 200 from mock target → `delivered: true`, HTTP 422 from target → `delivered: false`, `status_code` reflects actual target response, HMAC `X-MiroShark-Signature` header present in outbound payload, `is_test: true` in payload body.
2. In `EmbedDialog.vue` or the configuration admin view (wherever WEBHOOK_URL config is referenced), add a "🔔 Test Webhook" button (visible only when WEBHOOK_URL is configured). On click: `POST /api/webhook/test` → show result toast: "✅ Delivered ({ms}ms, HTTP {code})" or "❌ Failed (HTTP {code})". No new view required. Add `testWebhook()` to `frontend/src/api/simulation.js`.
3. Add `POST /api/webhook/test` to `docs/API.md` under Notifications with a `WebhookTestResult` schema. Add "Webhook Test Ping" to `docs/FEATURES.md` under Notifications with a one-line integrator onboarding note. Add to `openapi.yaml`. Zero new deps.

---

### 5. Surface Catalog API

**Type:** Integration / DX
**Effort:** Small (hours)
**Impact:** MiroShark has 24 publish-gated surfaces. No API endpoint lists them programmatically — integrators discover surfaces by reading docs, not by querying the platform. `GET /api/surfaces.json` returns the full surface catalog: each surface's key, endpoint, HTTP method, description (≤100 chars), type category, and example curl. Integrators can query this once on startup to discover what's available on the deployment they're connecting to. Enables Aeon to check the live surface count without parsing FEATURES.md. Completely static (hardcoded catalog, not auto-generated from SURFACE_KEYS counters) — ~60 LoC, no file scanning. Net-new.

**How:**
1. Add `backend/app/api/surfaces.py` (~80 LoC, stdlib `json`). The catalog is a hardcoded list — all 24 current surfaces documented as a list of dicts. Each entry: `{key: str, endpoint: str, method: "GET"|"POST", description: str (≤100 chars), type: "analytics"|"visualization"|"export"|"embed"|"integration"|"platform"|"notification", added_in_pr: int, example_curl: str}`. Cover all 24: signal.json, share-card.png, badge.svg, chart.svg, archive.zip, reproduce.json, notebook.ipynb, cite.bib, waybackclaw, polymarket.json, peak-round, agents/sparklines, oembed, platform-stats, platform-badge, platform-stats-badge, webhook, webhook-test, ecosystem (when built), volatility (if built today), gallery-json (if built today), compare (if built today), surfaces (self-referential). Add `GET /api/surfaces.json` (no auth; `Cache-Control: public, max-age=3600` — only changes when new surfaces ship; `ETag: str(len(catalog))[:8]`). Response: `{count: int, surfaces: list[dict]}`. Add 4 offline unit tests in `test_unit_surfaces.py`: returns valid JSON, `count` matches list length, each entry has `key`/`endpoint`/`method`/`description`/`type` fields, ETag header present. Register blueprint in `backend/app/__init__.py`.
2. Add `<link rel="alternate" type="application/json" href="/api/surfaces.json" title="MiroShark Surface Catalog">` in the app `<head>`. In `README.md`, add one line in the API overview section: "Full surface catalog: [`GET /api/surfaces.json`](docs/API.md#surface-catalog)". Add `getSurfaceCatalog()` to `frontend/src/api/simulation.js`.
3. Add `GET /api/surfaces.json` to `docs/API.md` under Platform with a `SurfaceCatalogEntry` schema and a note on the `type` enum values. Add to `openapi.yaml` under Platform. Add "Surface Catalog API" to `docs/FEATURES.md` under Platform. Zero new deps.

---

## Selection Rationale

Today's batch responds to where MiroShark is on May 28: 24 surfaces live, 11+ integrators named, documentation actively catching up to capability, and the analytical layer maturing.

- **Gallery Public JSON** (#1) — Re-eligible from May-20. The index every downstream consumer needs before anything else. No machine-readable full-sim listing exists; without it, integrators scrape HTML or query by known IDs. Every subsequent query-driven surface (search.json, comparison queries, directory listings) is built on top of this. Foundation first.
- **Simulation Comparison API** (#2) — Net-new. AntFleet is already doing comparative benchmark work. Clone button + compare API is the full variant-analysis loop; the compare half is more automatable (no frontend clone flow needed). `GET /api/compare?a=&b=` is a 120-LoC stdlib service that turns a two-file manual diff into one curl command.
- **Belief Volatility Score** (#3) — Re-eligible from May-20. The last analytical gap in the quant layer. Signal gives direction, peak-round gives inflection, volatility gives turbulence — the three-factor view that makes the signal interpretable. High-volatility Bullish ≠ low-volatility Bullish; both consumers and integrators need to know the difference. 25th surface.
- **Webhook Test Ping** (#4) — Re-eligible from May-20. Every one of the 11+ integrators has to survive this setup loop once. A 60-LoC endpoint collapses "wait for a real sim" into a 200ms API call. The DX improvement with the highest integrator reach per line of code.
- **Surface Catalog API** (#5) — Net-new. MiroShark's surface count is itself becoming a capability signal. A machine-readable catalog lets integrators check what's available on a deployment, lets Aeon track live surface count without parsing docs, and closes the loop on the discoverability work the maintainer started with PRs #118 and #119. Static catalog, ~60 LoC, no file scanning — the lowest-effort surface in the history of this project.
