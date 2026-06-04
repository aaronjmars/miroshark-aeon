# Repo Action Ideas — 2026-06-04

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,231 stars · 265 forks · 1 open issue (#95 French locale) · 1 open PR (#147 Per-Project Simulation Statistics, open)
**Recent activity:** PR #147 (per-project stats, Aeon-built, feat/project-stats-api) open as of today. PRs #145 (ecosystem.json) and #146 (drift fix) merged Jun 3. 14 named integrators in ECOSYSTEM.md. Token: $0.00000550 (-21.0% 24h), FDV $550.1K, -87.4% from ATH.

## Ecosystem Context

Codebase audit ran deeper than usual today. The platform is larger than the surfaces catalog suggests: `docs.py` already serves `GET /api/openapi.json` + `GET /api/docs` (Swagger UI); `templates.py` exposes preset simulation templates; `observability.py` streams LLM events and stats; `trajectory_export.py` has had CSV + JSONL export since before the catalog tracked it; `fork` and `branch-counterfactual` endpoints exist for sim reproduction; `watch.py` serves a live broadcast page for in-progress sims. The surface catalog (31 entries) is a curated public list — the underlying API is substantially broader.

Given that gap, today's batch focuses on the operator and integrator experience rather than adding more surfaces: the 14+ named integrators need better visibility into their webhook pipelines, a way to health-check the platform before batch runs, and a single endpoint to poll multiple sims at once. One platform-level discoverability surface rounds out the batch.

Pre-existence checks confirmed in this run:
- `/api/openapi.json`, `/api/openapi.yaml`, `/api/docs` (Swagger UI) — already in `docs.py`
- Preset simulation templates — already in `templates.py`
- Trajectory CSV export — already in `trajectory_export.py` / `/api/simulation/<id>/trajectory.csv`
- Webhook test ping — already at `POST /api/settings/test-webhook` + UI button
- Gallery trending (7-day window, by views) — already as `?sort=trending` on gallery endpoint
- Per-sim influence leaderboard — already at `GET /api/simulation/<id>/influence` (per-sim agent ranking)
- Simulation fork / branch-counterfactual — already in `simulation.py`

7-day exclusion window (May 28–Jun 4) excluded: May-28 batch (all), May-30 batch (all), Jun-01 batch (Operator Profile/Agent Persona Export/Search JSON/Gallery Trending/Per-Sim Surface Engagement), Jun-02 batch (Ecosystem JSON Registry/Scenario Clone Button/Japanese README/Simulation Batch Create/Per-Project Stats). All 5 ideas below are net-new and confirmed not pre-existing.

---

### 1. Webhook Delivery Log API

**Type:** DX
**Effort:** Small (hours)
**Impact:** The `webhook-log.jsonl` file has been written by `webhook_service.py` on every delivery attempt since before PR #120. It tracks attempt number, timestamp, status code, event type, payload hash, latency, and success/failure. There is no read endpoint — operators verify delivery by checking their own server logs or asking for help. `GET /api/simulation/<id>/webhook-log.json` (admin-gated, same `X-Admin-Token` pattern as other admin routes) exposes this history as structured JSON. 14+ integrators debug webhook issues today without any platform-side visibility. One endpoint changes that.

**How:**
1. In `backend/app/api/settings.py` (or a new `backend/app/api/webhook_log.py` mounted on `simulation_bp`), add `GET /api/simulation/<id>/webhook-log.json` (admin-auth via `require_admin_token`). Calls `webhook_service._read_log_lines(sim_dir)` and `webhook_service._parse_log_entries(lines)` — both already exist in `webhook_service.py`. Response: `{sim_id, delivery_count: int, last_success_at: ISO-8601 | null, last_failure_at: ISO-8601 | null, entries: [{attempt, timestamp, status_code, event_type, success, latency_ms, payload_hash, error: str | null}]}`. Sorted newest-first. Empty log → `{delivery_count: 0, entries: []}` (not 404). Cap at 100 entries. `Cache-Control: no-store` (admin endpoint, always fresh). Add 6 offline unit tests in `test_unit_webhook_log_api.py`: valid log → returns parsed entries, empty log → `delivery_count: 0`, non-existent sim → 200 with empty (same as empty log), missing admin token → 401, `last_success_at` derives correctly, response JSON-serialisable.
2. In `frontend/src/api/simulation.js`, add `getWebhookLog(simId, adminToken)`. In the EmbedDialog or Settings UI (wherever the webhook test button lives), add a "Delivery History" section showing the last 10 entries as a compact table: attempt # | timestamp | status code | ✅/❌ chip | latency. "View full log" link opens the raw JSON URL.
3. Document `GET /api/simulation/<id>/webhook-log.json` in `docs/API.md` under Notifications. Note admin-gating and the `delivery_count`/`last_success_at` envelope. Add to `openapi.yaml` with `WebhookLogResponse` + `WebhookLogEntry` schemas. Zero new deps.

---

### 2. Platform Status API

**Type:** DX / Integration
**Effort:** Small (hours)
**Impact:** `/api/stats` returns aggregate sim statistics — consensus distribution, surface view counts, unique project count. It does not answer "is the platform healthy?" — queue depth, recent completion rate, or uptime status. `GET /api/status.json` (no auth) fills this. Returns: pending sim count (dirs with `status: "running"`), completed count in the last 24h, last-completed sim timestamp, total platform sims, surface count (from surfaces catalog), `ok: true`. Enables external status pages (Upptime, BetterUptime, Statuspage.io) to monitor the deployment, integrators to pre-flight-check before batch runs, and Aeon's heartbeat skill to check platform health without parsing `/api/stats`. This is the "is MiroShark up and working?" endpoint that `/api/stats` deliberately is not.

**How:**
1. Add `backend/app/services/platform_status.py` (~100 LoC, stdlib `json` + `os` + `time`). `build_status(sim_root, catalog_count) -> dict`: scan all sim dirs — count `status: "running"` (queue depth), count `status: "completed"` with `completed_at` within the last 24h (recent completions), find `max(completed_at)` for last-completed timestamp, count total dirs. Response: `{ok: true, queue_depth: int, completed_24h: int, last_completed_at: ISO-8601 | null, total_sims: int, surface_count: int, check_at: ISO-8601}`. Add `GET /api/status.json` (no auth, `Cache-Control: public, max-age=30` — 30s TTL; this is a health probe, not static data). Register on `stats_bp` or a new `status_bp`. Add 6 offline unit tests in `test_unit_platform_status.py`: running sims increment `queue_depth`, completed-in-24h count excludes older sims, empty sim_root → all-zero valid response, `ok: true` always present, `check_at` is ISO-8601 string, response JSON-serialisable.
2. Add `getPlatformStatus()` to `frontend/src/api/simulation.js`. No UI changes required — this endpoint is primarily for external consumers.
3. Add `GET /api/status.json` to `docs/API.md` under Platform. Distinguish from `GET /api/stats` (aggregate stats) vs `GET /api/status.json` (health check). Add `PlatformStatus` schema to `openapi.yaml`. Add "Platform Status" to `docs/FEATURES.md` under Platform. Zero new deps.

---

### 3. Multi-Sim Status Lookup

**Type:** Integration
**Effort:** Small (hours)
**Impact:** AntFleet's benchmark pipeline, Capacitr's polling loop, and other integrators running parallel sims currently poll each simulation ID separately — N sims = N API calls. `POST /api/simulation/batch-status` (body `{sim_ids: ["abc", "def", ...]}`, up to 20 IDs) returns status/direction/confidence/quality for all in one response. Publish-gate applied per sim: private sims in the batch return `{sim_id, found: false}` rather than exposing data. Reduces polling overhead for any workflow that tracks more than one sim at a time. Capacitr's spec describes polling `/x402/run` status — this endpoint makes that pattern N-to-1.

**How:**
1. Add `POST /api/simulation/batch-status` to `backend/app/api/simulation.py` (no auth). Validates: body is JSON with `sim_ids` array, each ID is `[A-Za-z0-9_\-]{1,64}`, count 1–20 (400 if > 20). For each ID: reads `simulation_state.json` from `WONDERWALL_SIMULATION_DATA_DIR`; if `is_public: false` → `{sim_id, found: false}`; if not completed → `{sim_id, found: true, status: state.get("status"), direction: null, confidence_pct: null, quality_health: null, completed_at: null}`; if completed+public → `{sim_id, found: true, status: "completed", direction, confidence_pct, quality_health, total_rounds, completed_at}`. Response: `{count: int, results: list[dict]}`. `Cache-Control: no-store` (result depends on per-sim state, not worth caching). Add 8 offline unit tests in `test_unit_batch_status.py`: single published sim → `found: true` with all fields, private sim → `found: false`, unknown sim → `found: false`, > 20 IDs → 400, running sim → `status: "running"` + null analytics fields, mixed batch (published + private + running) → correct per-entry shape, `count` matches `len(sim_ids)`, non-string ID in array → 400.
2. Add `batchSimulationStatus(simIds)` to `frontend/src/api/simulation.js`. No UI view needed — this is an operator/integrator-facing endpoint.
3. Add `POST /api/simulation/batch-status` to `docs/API.md` under Simulation Management with a `BatchStatusResponse` + `SimStatusEntry` schema and a polling example (`jq '[.results[] | select(.status == "completed")]'`). Add to `openapi.yaml`. Note the 20-ID cap and publish-gate behavior. Zero new deps.

---

### 4. All-Time Simulation Leaderboard API

**Type:** Integration
**Effort:** Small (hours)
**Impact:** The gallery's `?sort=trending` surfaces the most-viewed public sims in a rolling time window. There is no all-time multi-dimensional ranking. `GET /api/leaderboard.json` returns four ranked lists of top-10 public completed sims: `highest_confidence` (by confidence_pct desc), `best_quality` (quality tier rank: excellent > good > fair > poor, then confidence_pct as tiebreak), `most_viewed` (all-time total_surface_views desc), `longest_debate` (total_rounds desc). One endpoint for directory builders, Aeon's weekly digest, and showcase pages — replaces the pattern of downloading the full gallery and sorting locally. The existing per-sim `GET /api/simulation/<id>/influence` endpoint ranks agents *within* a sim; this ranks *sims* at the platform level — genuinely distinct.

**How:**
1. Add `backend/app/services/leaderboard_service.py` (~100 LoC, stdlib `json` + `os`). `build_leaderboard(sim_root) -> dict`: scan `WONDERWALL_SIMULATION_DATA_DIR`; filter `is_public=True` + `status="completed"`; build four sorted lists of top-10. `_quality_rank(q) -> int`: `{"excellent": 4, "good": 3, "fair": 2, "poor": 1}.get(q, 0)`. Per sim entry in each list: `{sim_id, scenario_title: str[:100], direction, confidence_pct, quality_health, total_rounds, total_surface_views, created_at}`. Response envelope: `{generated_at: ISO-8601, total_eligible: int, highest_confidence: list, best_quality: list, most_viewed: list, longest_debate: list}`. Add `GET /api/leaderboard.json` (no auth; `Cache-Control: public, max-age=300`; `ETag: leaderboard-{total_eligible}-{newest_created_at[:10]}`). Register on a new `leaderboard_bp` or `stats_bp`. Add 8 offline unit tests in `test_unit_leaderboard.py`: `highest_confidence` sorted desc by `confidence_pct`, `best_quality` puts excellent before good, unpublished/incomplete excluded, `total_eligible` accurate, at most 10 entries per list, `most_viewed` sorted desc by `total_surface_views`, `longest_debate` sorted desc by `total_rounds`, ETag header present.
2. Add `getLeaderboard()` to `frontend/src/api/simulation.js`. Add `leaderboard` entry to `surfaces_catalog.py` under platform-level surfaces (32nd catalogued surface).
3. Add `GET /api/leaderboard.json` to `docs/API.md` under Gallery & Discovery with a `LeaderboardResponse` schema. Note the four dimensions and all-time (not windowed) framing. Add to `openapi.yaml`. Add "All-Time Simulation Leaderboard" to `docs/FEATURES.md`. Zero new deps.

---

### 5. Webhook Manual Retry

**Type:** DX
**Effort:** Small (hours)
**Impact:** When an integrator's endpoint has a transient outage — Cloudflare blip, brief downtime — the webhook was sent and failed. The operator has three options today: re-run the full sim (expensive), call `/api/simulation/<id>/signal.json` and parse it themselves (manual work), or ask Aaron. `POST /api/simulation/<id>/webhook/retry` (admin-auth) re-fires the completion webhook for a finished sim using the real payload from `simulation_state.json`, re-signed with HMAC, delivered to the configured `WEBHOOK_URL`. Distinct from `POST /api/settings/test-webhook` (synthetic payload, any URL) — this sends the actual completion payload for a specific finished sim to the currently configured URL. The delivery is logged to the existing `webhook-log.jsonl` as a new attempt. Closes the operator recovery loop for the 14+ integrators who already have webhooks wired.

**How:**
1. Add `POST /api/simulation/<id>/webhook/retry` to `backend/app/api/simulation.py` (or `backend/app/api/settings.py`) behind `require_admin_token`. Validate: sim must be `status: "completed"` (400 "simulation not complete" otherwise). Build the real webhook payload the same way as the original delivery: read `simulation_state.json`, call the same payload-builder used in `webhook_service.py`'s normal dispatch path. Call `webhook_service.dispatch_webhook(payload, sim_id, sim_dir)` — or the equivalent send function — to re-fire with HMAC signing and delivery logging. Response: `{sim_id, delivered: bool, status_code: int, latency_ms: float, attempt: int, webhook_url_suffix: last 12 chars masked, timestamp: ISO-8601}`. Return 503 `{"error": "WEBHOOK_URL not configured"}` if blank. Add 6 offline unit tests in `test_unit_webhook_retry.py`: completed sim + configured URL → `delivered` key in response, non-completed sim → 400, no WEBHOOK_URL → 503, missing admin token → 401, `attempt` number increments from existing log, delivery appended to webhook-log.jsonl.
2. In the EmbedDialog (or wherever the delivery log UI from idea #1 lands), add a "Retry delivery" button next to failed log entries. On click: `POST /api/simulation/<id>/webhook/retry` → show result toast: "✅ Delivered (HTTP 200, {ms}ms)" or "❌ Failed (HTTP {code})". Add `retryWebhook(simId, adminToken)` to `frontend/src/api/simulation.js`.
3. Add `POST /api/simulation/<id>/webhook/retry` to `docs/API.md` under Notifications. Distinguish clearly from `POST /api/settings/test-webhook` (synthetic) — this sends the real payload. Note HMAC re-signing and log-append behavior. Add to `openapi.yaml`. Zero new deps.

---

## Selection Rationale

Today's batch comes after a thorough codebase audit that found the API substantially broader than the surfaces catalog reflects. Many ideas that seemed novel are already built (CSV export, openapi.json endpoint, templates, trending sort, test webhook). The remaining gap is in **operator visibility and pipeline ergonomics** — the 14+ integrators who are shipping PRs against the ecosystem have no webhook delivery history, no platform health endpoint, and no batch polling primitive.

- **Webhook Delivery Log** (#1) — The `webhook-log.jsonl` has been tracking every delivery since before PR #120. The file exists; the read endpoint doesn't. 14 integrators debugging webhook issues need this more than another new surface.
- **Platform Status API** (#2) — `/api/stats` is not a health check. External status monitors (Upptime, BetterUptime, StatusPage) need an unambiguous "is the platform up and completing sims?" endpoint. 30-second cache, no auth, minimal scan. The endpoint that makes MiroShark monitorable.
- **Multi-Sim Status Lookup** (#3) — Capacitr's spec describes a polling loop; AntFleet runs parallel benchmark sims. Both need to check N sims at once. One endpoint vs N reduces poll overhead from linear to constant. The payload shape is a strict subset of what `/api/simulation/public` already returns — the only new logic is the batch wrapper and per-sim publish gate.
- **All-Time Leaderboard** (#4) — "What are the best simulations on MiroShark?" is an unanswered question for directories, journalists, and showcase builders. `?sort=trending` answers "what's popular this week". The leaderboard answers "what's the best, ever, across four dimensions." The existing per-sim `/api/simulation/<id>/influence` ranks agents inside a sim; this ranks sims across the platform.
- **Webhook Manual Retry** (#5) — Pairs with #1. Seeing delivery history is useful; being able to re-fire without re-running the sim is what converts that visibility into action. Admin-gated, logs to the same JSONL, re-signs with HMAC. The operator's escape hatch when their endpoint was temporarily unreachable.

Excluded (blocked): **Operator Profile** — re-verified today. `platform_stats.py:42-43` still reads: "SimulationState has no operator / created_by field — the closest stable identifier is project_id." Block holds. Entry remains in `memory/topics/blocked-features.md`.
