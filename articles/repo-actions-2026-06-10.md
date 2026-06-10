# Repo Action Ideas — 2026-06-10

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,244 stars · 263 forks · 1 open issue (#95 French locale) · 0 open PRs (PR #155 Chinese README merged today, PR #153 Activity Feed merged Jun 09)
**Recent activity:** PR #155 (README.zh-CN.md, Aeon-built) merged today — Jun-15 Chinese-locale hyperstition front-door coverage in place. Catalog at 35 entries. batch-status (PR #150) and batch-create are now mirror endpoints (status exists; create doesn't yet). Zero-deps streak 43 intact.

## Ecosystem Context

Two things happened today that frame this batch.

First: `README.zh-CN.md` merged (PR #155). MiroShark now has the same Chinese front door that Vue.js, Electron, and pandas have. Twelve docs files already had zh-CN counterparts; the root README was the only holdout. The Japanese community has been watching since `@m000_crypto` coverage on May 17 — same gap exists for Japanese, no `README.ja.md` at root. The README.zh-CN.md was 154 lines; a Japanese equivalent is the same scope and the same effort.

Second: the platform's batch-pattern is now established. `POST /api/simulation/batch-status` (PR #150) proved the shape — array of IDs in, array of results out, 20-item cap, per-item privacy envelope. The batch-*create* side is still a sequential N-round-trip loop. AntFleet's benchmark harness, SyntheticsAI's test pipeline, and Capacitr's config-to-run loop all create multiple sims before polling their results. One endpoint closes that.

The other gap that emerged from today's catalog review: the platform now tells you *what results look like in aggregate* (`/api/stats/distribution.json`) but not *where a specific sim sits in that distribution*. A confidence of 71.4% is meaningless without a platform baseline. Is that the 60th percentile or the 97th? The distribution endpoint provides the shape; a per-sim rank endpoint applies it.

And the status family (`/api/status.json`, `/api/stats`, `/api/stats/distribution.json`) describes *what results exist* and *what the platform's current state is* — but not *how fast the platform runs*. Completion latency (p50/p95) and throughput (sims/hour) are the two numbers batch pipeline operators need before scheduling a run. Neither surfaces anywhere today.

---

### 1. Japanese README (`README.ja.md`)

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** The root README.md has one language: English. Today `README.zh-CN.md` merged — the first non-English root README. The Japanese community is next: `@m000_crypto` (`@m000_crypto` on X) covered MiroShark on May 17 with Japanese-language commentary; the JP crypto and AI research communities are among the most active GitHub audiences globally. Twelve docs files have `zh-CN` counterparts; zero have `ja` equivalents. A `README.ja.md` at repo root gives JP developers a native-language landing page, signals community investment, and follows the same convention just proved out with `README.zh-CN.md`. Smaller scope than the Jun-02 #3 suggestion (which included FEATURES.ja.md, WEBHOOKS.ja.md, NOTIFICATIONS.ja.md) — scoped today to root README only, matching the README.zh-CN.md pattern (154 lines, mirrors English structure). README.ja.md can be the anchor file; docs/*.ja.md can follow in future batches.

**How:**
1. Create `README.ja.md` at the repository root. Structure mirrors `README.zh-CN.md` layout: badges row (reuse identical badge URLs from English), hero tagline in Japanese ("任意のシナリオをシミュレート、1ドル以下・10分以内"), project description (adapt from the English README's lead), Quick Start (same CLI commands verbatim; terminal commands and code blocks are not translated), Key Features (translate the 5–7 bullets), Documentation section (list `docs/API.md` and key siblings with Japanese headings), Star History chart, license badge. Total: ~150–160 lines. All image paths, code blocks, endpoint paths, and field names remain in English. All 7 image paths and all internal doc/link paths verified against English README. Zero backend changes. Zero new deps.
2. Add `[日本語](README.ja.md)` to the language switcher strip at the top of `README.md` and `README.zh-CN.md` (alongside the existing `[中文](README.zh-CN.md)` / `[English](README.md)` links). One line edit per file — no disruption to existing layout. No backend changes. No openapi/catalog changes.

---

### 2. Scenario Clone Button

**Type:** Feature / DX
**Effort:** Small (hours)
**Impact:** `GET /api/simulation/<id>/clone.json` (PR #131, June 1) returns the exact parameter set used to build a sim — wire-compatible with `POST /api/simulation/create`. The API is built; the UI entry point isn't. An operator or researcher viewing any published simulation share page has no one-click way to launch a new run with the same configuration. This closes that loop: a "Clone this scenario" button in `EmbedDialog.vue` constructs a `/?clone=<id>` URL and copies it to clipboard (toast: "Clone link copied"); the create/home view reads `?clone=<sim_id>` on mount, fetches clone.json, and pre-fills scenario, URL list, rounds, and agent count. Strip `?clone=` via `router.replace` after pre-fill so refresh doesn't re-fetch. 404 or fetch error → silent fallback, blank form. Distinct from the Simulation Templates surface (`/api/templates/list`) — templates are curated presets; this clones a specific live published run. `clone.json` is publish-gated; the button only renders when `is_public` is true.

**How:**
1. Add `?clone=<sim_id>` handling to the home/create Vue component (likely `Home.vue` or `NewSimulation.vue`). On mount: if `route.query.clone` is present, fetch `GET /api/simulation/{clone}/clone.json`. On success: pre-fill the Simulation Prompt textarea with `scenario_title` (and `simulation_prompt` if present), add URLs from `simulation_urls` to the URL import list, set rounds + agent_count sliders to cloned values. Show a dismissible info banner: "Cloned from simulation [clone_id] — edit and launch your own run." After pre-fill, strip `?clone=` from the URL via `router.replace`. Add `getCloneJson(simId)` to `frontend/src/api/simulation.js`. No backend changes. No new deps.
2. In `EmbedDialog.vue`, add a "Clone this scenario" button to the Share & Embed section (alongside the existing Copy URL / Copy embed code buttons). Clicking it constructs `window.location.origin + '/?clone=' + simId`, copies to clipboard via the Clipboard API, and shows a success toast. Publish-gated: visible only when `is_public` is true. No backend changes — the clone.json fetch happens on the receiving end when the URL is opened.
3. Add `?clone=<sim_id>` to `docs/API.md` under "Shareable Scenario Links" as a query parameter. Note: "Fetches `clone.json` and pre-fills scenario, URLs, and config fields; strips the param after pre-fill." Update `docs/FEATURES.md` Shareable Scenario Links section with the clone variant. Zero new deps.

---

### 3. Simulation Batch Create API

**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** `POST /api/simulation/batch-status` (PR #150) established the batch-pattern: array of IDs in, array of results out, per-item privacy envelope, 20-item cap. The *creation* side has no equivalent. Integrators running benchmark pipelines — AntFleet's `miroshark-bench`, SyntheticsAI's test suite, Capacitr's config-to-run loop — currently issue N sequential calls to `POST /api/simulation/create`. `POST /api/simulation/batch` accepts up to 10 sim configs (same body shape as single create) and creates each in sequence, returning `{created: N, failed: N, total: N, results: [{index, sim_id, status, error?}]}`. Individual failure → `status: "failed"` in that slot, batch continues. Reduces N round-trips to 1; enables the standard pattern "batch-create → poll batch-status → pull signal.json per completed sim" without scripting a creation loop. Admin-gated (same token as single create).

**How:**
1. Add `POST /api/simulation/batch` to `backend/app/api/simulation.py`. Request body: `{simulations: list[SimCreateBody]}` where `SimCreateBody` is the same shape as the single-create endpoint. Validation: empty array → 400; array > 10 → 400 ("batch size limit is 10"). For each config in order: call the existing `create_simulation()` service function, collect result. Individual exception → `{index: i, sim_id: null, status: "failed", error: str}` and continue — never abort the full batch. Response: `{created: int, failed: int, total: int, results: [{index: int, sim_id: str | null, status: "created" | "failed", error: str | null}]}`. Reuses all existing validation from `create_simulation()` — no new validation logic. 8 offline unit tests in `test_unit_batch_create.py`: empty array → 400, array of 11 → 400, single valid config → created=1 failed=0, 3 valid → created=3 failed=0, partial failure (mock one create to raise) → failed count increments, `results` array length equals input length, `index` field matches input position, unauthenticated → 401. Zero new deps.
2. Add `batchCreateSimulations(configs)` to `frontend/src/api/simulation.js`. No frontend UI — pure API-consumer surface. Add `POST /api/simulation/batch` to `docs/API.md` under Simulation Lifecycle with `BatchCreateRequest` + `BatchCreateResponse` + `BatchResultEntry` schemas and an example pipeline (`batch-create → poll batch-status → pull signal.json per completed sim`). Distinguish from `POST /api/simulation/batch-status` (checking status of existing sims) vs this (creating new ones). Add to `openapi.yaml`. Zero new deps.

---

### 4. Simulation Percentile Rank

**Type:** Analytics / Integration
**Effort:** Small (hours)
**Impact:** `GET /api/stats/distribution.json` (PR #151) tells you the platform-wide result shape: 40% bullish, top quartile confidence ≥ 70%, etc. But there's no per-sim equivalent. A confidence of 71.4% has no context until you know whether that's the median or the top 5%. `GET /api/simulation/<id>/rank.json` answers the comparative question: where does this sim sit in the platform distribution? Returns `{sim_id, confidence_pct_rank: int, quality_rank: int, total_ranked: int, confidence_pct_percentile: float, quality_percentile: float, generated_at: ISO-8601}`. Integrators (Capacitr settlement logic, AntFleet leaderboard) can now frame results in relative terms without downloading the full gallery and sorting locally. Publish-gated: only completed public sims are ranked. Unknown sim or incomplete/private sim → same 404 envelope as signal.json. Distinct from distribution.json (platform-level aggregate) and from the proposed All-Time Leaderboard (top-N lists) — this ranks a single specific sim.

**How:**
1. `backend/app/services/rank_service.py` (~100 LoC, stdlib `json` + `os`). `build_rank(sim_root, sim_id) -> dict`: scan all public+completed sims to build a sorted list of `confidence_pct` values and a scored `quality_health` list (`excellent=4, good=3, fair=2, poor=1`). Compute `confidence_pct_rank` (1-indexed position in descending confidence sort, 1 = highest), `quality_rank` (1-indexed position in descending quality sort), `total_ranked` (count of public completed sims). Derive `confidence_pct_percentile = 100 * (1 - (rank - 1) / total_ranked)` (100th percentile = top; round to 1dp). Empty platform → 404 (not enough data to rank). Add `GET /api/simulation/<id>/rank.json` to `simulation.py` on `simulation_bp`. Publish gate: private/incomplete → same 404 as signal.json. `Cache-Control: public, max-age=60`. 10 offline unit tests in `test_unit_rank.py`: highest-confidence sim → rank=1, lowest → rank=total_ranked, percentile formula correct, private sim → 404, running sim → 404, total_ranked accurate, ties broken by sim_id desc for determinism, JSON-serialisable, `quality_rank` uses the quality scoring function, rank changes after new completed sim. Zero new deps.
2. Add `getSimulationRank(simId)` to `frontend/src/api/simulation.js`. Add `SimulationRank` schema to `openapi.yaml`. Add `GET /api/simulation/<id>/rank.json` to `docs/API.md` under Simulation Data. Note: "Percentile reflects platform state at time of request — may change as new sims complete." Add `simulation_rank` to `surfaces_catalog.py` (36th entry, type: `analytics`). Zero new deps.

---

### 5. Platform Performance Metrics

**Type:** Analytics / Integration
**Effort:** Small (hours)
**Impact:** The status family answers "what exists" and "is it healthy" — `status.json` (queue depth / recent completions / last completed), `stats` (totals), `distribution.json` (result shape). None of them answer "how fast does the platform run?" Batch pipeline operators (AntFleet benchmark scheduler, Capacitr's automated config-to-run loop) need completion latency and throughput to schedule runs: "if I submit 10 sims now, when will they be done?" `GET /api/stats/performance.json` returns `{p50_completion_min: float, p95_completion_min: float, throughput_24h: float, throughput_7d: float, sample_count: int, generated_at: ISO-8601}` where `p50_completion_min` and `p95_completion_min` are the median and 95th-percentile completion latency in minutes (time from `created_at` to `completed_at`) across the last 30 days of public completed sims; `throughput_24h` and `throughput_7d` are completions per hour over rolling 24h and 7d windows. Distinct from `status.json` (current point-in-time queue snapshot) — this is historical performance data for capacity planning. Requires no auth (same as status.json and stats). Platform with no completed sims → safe all-null envelope (`{p50_completion_min: null, p95_completion_min: null, ...}`), never 500. Zero new deps.

**How:**
1. `backend/app/services/performance_stats.py` (~130 LoC, stdlib `json + os + datetime`). `build_performance(sim_root) -> dict`: scan public+completed sims; for each, compute `latency_min = (completed_at - created_at).total_seconds() / 60`; collect latencies for sims completed in the last 30 days (60-day cap on sample window). Sort latency list and compute p50 and p95 via index arithmetic (`p50 = sorted[len//2]`, `p95 = sorted[int(len * 0.95)]`; integer division, handles 0 and 1 sample gracefully). Compute `throughput_24h` (sims with `completed_at` in last 24h divided by 24) and `throughput_7d` (sims completed in last 7d divided by 168). If fewer than 3 samples → return `null` for percentiles (too few to be meaningful), still return throughput. Add `GET /api/stats/performance.json` to `stats.py` on `stats_bp`. `Cache-Control: public, max-age=60`. `ETag: perf-{sample_count}-{latest_completed_at[:10]}`. 10 offline unit tests in `test_unit_performance_stats.py`: p50/p95 correct for simple known latency list, fewer than 3 sims → p50/p95 null, throughput_24h = count_in_window / 24, private sims excluded, incomplete sims excluded, sims outside 30d window excluded from percentile sample, JSON-serialisable, ETag format present, safe null envelope for empty platform, throughput_7d vs throughput_24h computed from distinct windows. Zero new deps.
2. Add `getPlatformPerformance()` to `frontend/src/api/simulation.js`. Add `PlatformPerformance` schema to `openapi.yaml`. Add `GET /api/stats/performance.json` to `docs/API.md` under Platform alongside `status.json` and `stats`. Note: "Latency samples cover the last 30 days of public completed sims. Fewer than 3 samples → `null` percentiles." Add `platform_performance` to `surfaces_catalog.py` (37th entry, type: `platform`). Zero new deps.

---

## Selection Rationale

**Excluded (blocked):** **Operator Profile** — re-verified today via `memory/topics/blocked-features.md`. `SimulationState` still has no `operator` / `created_by` field. Block holds.

**Excluded (7-day window, Jun 03–09):** Trending Topics (Jun-08 #2, re-eligible Jun 15), MCP Tool Catalog JSON (Jun-08 #3, re-eligible Jun 15), Pre-Run Cost Estimator (Jun-08 #4, re-eligible Jun 15), Payload Validator (Jun-06 #2, re-eligible Jun 13), Monthly Stats Time-Series (Jun-06 #4, re-eligible Jun 13), Agent Behavior Census (Jun-06 #5, re-eligible Jun 13), All-Time Leaderboard (Jun-04 #4, re-eligible Jun 11 — tomorrow).

**Re-eligible from Jun-02 (#2/#3/#4, past 7-day window as of Jun 09):**

- **Japanese README** (#1 in this batch) — Same gap as when suggested Jun 02, now with a concrete pattern to follow: `README.zh-CN.md` (154 lines) merged today and immediately validates the approach. Scoped to root README only (vs. Jun-02's fuller 4-file scope) to match what the feature skill can ship in one PR.
- **Scenario Clone Button** (#2) — `clone.json` API has been live since PR #131 (Jun 01). The UI gap is 9 days old. Standalone `EmbedDialog.vue` addition + `?clone=` query param; no backend changes.
- **Simulation Batch Create** (#3) — Was medium effort in Jun-02 context; PR #150 (batch-status, Jun 07) now proves the batch-shape convention on this codebase. Implementation path is cleaner with that precedent. Still medium effort but the pattern is now documented in the codebase.

**Net-new ideas:**

- **Simulation Percentile Rank** (#4) — `distribution.json` was not built yet on Jun-02 (merged Jun 07 via PR #151). Its existence is what makes rank.json a natural next step. Without platform-level distribution data, per-sim ranking was premature; now it's the logical complement.
- **Platform Performance Metrics** (#5) — Closes the last gap in the platform monitoring family: status.json (current health), stats (totals), distribution.json (result shape), and now performance.json (latency + throughput). Batch pipeline operators have needed this since at least PR #150 landed and made multi-sim orchestration practical.
