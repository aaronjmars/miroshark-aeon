# Repo Action Ideas — 2026-06-06

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,236 stars · 263 forks · 2 open issues · 1 open PR (#150 Multi-Sim Batch Status Lookup, Aeon-built)
**Recent activity:** PR #150 (batch-status, Aeon-built, feat/batch-status-lookup) open as of today. PR #149 (platform status probe) merged Jun 5. PR #147 (per-project stats) merged Jun 4. Jun-04 batch addressed 3/5: #2→PR#149 merged, #3→PR#150 open, #4 (All-Time Leaderboard) still unbuilt; #1+#5 confirmed pre-existing Jun 5. 14+ named integrators in ECOSYSTEM.md.

## Ecosystem Context

Deep API audit today surfaced a substantially larger surface area than the 32-entry catalog reflects. The simulation API alone is ~10,800 lines with 50+ routes per sim. Key surfaces discovered that do NOT appear in the catalog and were not in the pre-existing registry: `/<id>/timeline`, `/<id>/quality`, `/<id>/belief-drift`, `/<id>/interaction-network`, `/<id>/transcript.json`, `/<id>/transcript.md`, `/<id>/thread.txt`, `/<id>/thread.json`, `/<id>/cite.bib`, `/<id>/notebook.ipynb`, `/<id>/lineage`, `/<id>/reproduce.json`, `/<id>/counterfactual`, `/<id>/demographics`, `/<id>/frame/<round>`, `/<id>/agent-stats`, `/interview`, `/trending`, `/templates/list`. All registered in `memory/topics/pre-existing-features.md` this run to prevent future idea-slot waste.

Today's batch focuses on **platform-level analytics gaps**. The stats family (`/api/stats`, `/api/project/<id>/stats`, `/api/status.json`) gives totals and health but no distribution, trend, or behavioral breakdown. Five ideas fill those gaps without touching the per-sim surface layer.

Pre-existence checks confirmed in this run:
- Consensus timeline per round — already at `GET /api/simulation/<id>/timeline` (frontend progress bar / round summary)
- Quality breakdown — already at `GET /api/simulation/<id>/quality`
- Belief drift — already at `GET /api/simulation/<id>/belief-drift`
- Interaction/influence network — already at `GET /api/simulation/<id>/interaction-network`
- Transcript export (Markdown + JSON) — already at `GET /api/simulation/<id>/transcript.{md,json}`
- Thread export — already at `GET /api/simulation/<id>/thread.{txt,json}`
- BibTeX citation — already at `GET /api/simulation/<id>/cite.bib`
- Jupyter Notebook export — already at `GET /api/simulation/<id>/notebook.ipynb`
- Templates list — already at `GET /api/templates/list` + `/templates/capabilities`
- Agent stats (per-sim activity ranking) — already at `GET /api/simulation/<id>/agent-stats`

7-day exclusion window (May 30–Jun 5) excluded: Jun-04 batch (All-Time Leaderboard within window), Jun-02 batch (Scenario Clone Button, Japanese README, Simulation Batch Create API), Jun-01 batch (Operator Profile/pre-existing ideas), May-30 batch (Private Share Link merged / French Locale / pre-existing ideas). All 5 ideas below are net-new and confirmed not pre-existing.

---

### 1. Platform Outcome Distribution

**Type:** Analytics / Integration
**Effort:** Small (hours)
**Impact:** `/api/stats` returns aggregate sim totals: total_sims, unique_projects, surface_view counts. It does not answer "what do MiroShark results look like in aggregate?" — what fraction go bullish vs bearish, what confidence tier is most common, how quality distributes. `GET /api/stats/distribution.json` (no auth; 5-minute cache) fills this. Returns bucketed breakdowns of all public completed sims across four dimensions: direction (bullish/bearish/neutral count and pct), confidence tier (high ≥70%, medium 40-70%, low <40%), quality tier (excellent/good/fair/poor), and round-count bucket (short <10, medium 10–20, long >20), plus `avg_confidence_pct` and `avg_total_rounds`. Enables: researchers citing "X% of MiroShark simulations on financial topics go bullish," Aeon's digest reporting distribution shifts month-over-month, directory builders characterizing the platform, integrators calibrating their confidence thresholds against the platform baseline.

**How:**
1. `backend/app/services/outcome_distribution.py` (~100 LoC, stdlib `json` + `os`). `build_distribution(sim_root) -> dict`: scan `WONDERWALL_SIMULATION_DATA_DIR`; filter `is_public=True` + `status="completed"`; bucket each sim by direction (from `signal_service.compute_signal`), confidence_pct into high/medium/low, quality_health into the four tiers, and total_rounds into short/medium/long. Return `{generated_at, total_analyzed, by_direction, by_confidence, by_quality, by_round_count, avg_confidence_pct, avg_total_rounds}`. Empty platform → all-zero envelope with `total_analyzed=0`, never 500. Add `GET /api/stats/distribution.json` to `stats.py` on `stats_bp`. ETag `distribution-{total_analyzed}-{most_recent_completed_at[:7]}` for 304 short-circuit. `Cache-Control: public, max-age=300`. 12 offline tests in `test_unit_outcome_distribution.py`: direction buckets correct, confidence tier boundaries enforced (70/40 thresholds), quality tiers from quality_health field, round-count buckets correct, private/incomplete sims excluded, empty sim_root → all-zero valid response, avg fields are floats, JSON-serialisable, ETag changes when a new sim completes, pct fields sum to 100, total_analyzed accurate, response has generated_at ISO string.
2. Add `getOutcomeDistribution()` to `frontend/src/api/simulation.js`. No UI required — this is a researcher/integrator surface.
3. Add `GET /api/stats/distribution.json` to `docs/API.md` under Platform alongside `/api/stats`. Distinguish clearly: `/api/stats` is totals (how many sims, views, projects), `/api/stats/distribution.json` is shape (what the results look like in aggregate). Add `OutcomeDistribution` schema to `openapi.yaml`. Add to `surfaces_catalog.py` (33rd catalogued surface). Zero new deps.

---

### 2. Simulation Payload Validator

**Type:** DX
**Effort:** Small (hours)
**Impact:** Every time an integrator sends a malformed `POST /api/simulation/create` payload, the platform either silently ignores unknown fields or returns a vague 400. There is no way to preflight a sim config before spending $1 and waiting up to 10 minutes. `POST /api/simulation/validate` (no auth) takes the same body shape as `/create` and returns `{valid: bool, errors: [{field, message}], warnings: [{field, message}]}` without writing anything to disk. Reuses the same validation rules applied at the create boundary — one source of truth, no drift. Integrators building sim generation pipelines (Capacitr's config-to-run loop, AntFleet's benchmark harness) can validate hundreds of configs programmatically before submitting any. Closes the "why did my sim fail at config time?" debugging loop.

**How:**
1. `backend/app/services/payload_validator.py` (~120 LoC, stdlib only). `validate_sim_payload(payload: dict) -> dict`: check required fields present and non-empty (`scenario_title`, `topic`, `market_question`); validate field types and lengths (scenario_title ≤200 chars, topic ≤100 chars, market_question ≤500 chars); validate `polymarket_market_count` ∈ [1,5] if present; validate `demographic_filters` is a dict if present; validate `counterfactual_branches` is a list of ≤5 strings if present. Return `{valid: bool, errors: list, warnings: list}`. Warnings (not errors) for: scenario_title > 150 chars (may truncate in UI), missing optional but recommended fields (`description`), `polymarket_market_count=5` (max, longer sim). Add `POST /api/simulation/validate` to `simulation.py` on `simulation_bp`. No auth — same allow-list as `/batch-status`. Rate-limit using the same sliding-window as `/suggest-scenarios` (prevents validation-as-oracle abuse). 14 offline tests in `test_unit_payload_validator.py`: missing required field → error, valid minimal payload → valid=true, polymarket_count=6 → error (out of range), polymarket_count=0 → error, counterfactual_branches too many → error, scenario_title too long → warning not error, extra unknown fields → no error (pass-through), demographic_filters wrong type → error, empty payload → errors on all required fields, valid maximal payload → valid=true, response JSON-serialisable, validator doesn't write to disk (test reads sim_root after call to verify unchanged), response has errors+warnings lists always, warnings-only case → valid=true.
2. Add `validateSimPayload(payload)` to `frontend/src/api/simulation.js`. No UI required (programmatic endpoint). Add `PayloadValidation` + `ValidationIssue` schemas to `openapi.yaml`. Note rate limiting and that valid=true does not guarantee sim creation succeeds (runtime checks may still fail). Zero new deps.

---

### 3. Signed Simulation Result

**Type:** Security / Integration
**Effort:** Small (hours)
**Impact:** `GET /api/simulation/<id>/signal.json` returns the direction/confidence/quality result for a public sim. The response is served over HTTPS (transport-layer auth) but once downloaded and stored — in an integrator's database, a prediction market's ledger, a research archive — there is no way to prove the stored value matches what MiroShark actually returned without making a live API call. `GET /api/simulation/<id>/signed-result.json` returns the signal payload plus an HMAC-SHA256 signature over the canonical JSON. Integrators who store results for later verification (Capacitr's settlement flow, financial audit trails, ML result provenance) can prove authenticity offline using their copy of `WEBHOOK_SECRET`. Same key as webhook delivery — no new secret to configure. First provenance mechanism that works without internet access or blockchain. Pairs with the DKG citation (`/<id>/dkg-citation` — on-chain hash) for integrators who want both coverage: on-chain for decentralized verification, HMAC for synchronous lightweight verification.

**How:**
1. `backend/app/services/signed_result.py` (~80 LoC, stdlib `json + os + hmac + hashlib`). `build_signed_result(sim_dir, sim_id, webhook_secret) -> dict`: compute signal using the same `signal_service.compute_signal` call as `signal.json`; serialize `result` dict with `json.dumps(result, sort_keys=True, separators=(',', ':'))` (deterministic canonical form); compute `signature = hmac.new(key=webhook_secret.encode(), msg=canonical.encode(), digestmod=hashlib.sha256).hexdigest()`. Return `{sim_id, signed_at: ISO, algorithm: "hmac-sha256", result: {...signal fields...}, signature: str, signing_key_hint: webhook_secret[:8] + "..."}`. If `WEBHOOK_SECRET` not set or empty → `{sim_id, signed: false, result: {...signal fields...}, error: "signing_unavailable: WEBHOOK_SECRET not configured"}` — never 500. Publish gate: private or non-completed sims return the same 404 as `signal.json`. `Cache-Control: public, max-age=300` for completed sims (result is stable once computed). Add `GET /api/simulation/<id>/signed-result.json` to `simulation.py` — publish-gated, no auth. Add to `internal_auth_guard` allow-list. Add to `surfaces_catalog.py` (33rd or 34th entry, type: `integration`). 10 offline tests in `test_unit_signed_result.py`: signature verifiable with HMAC-SHA256, no WEBHOOK_SECRET → signed=false not 500, private sim → 404, running sim → 404 (same as signal.json), signature changes if result changes (determinism), canonical JSON is sort_keys stable, signing_key_hint is first 8 chars, result fields match signal.json exactly, JSON-serialisable, openapi drift test.
2. Add `getSignedResult(simId)` to `frontend/src/api/simulation.js`. Add `SignedResult` schema to `openapi.yaml` with an `x-verification-note` description explaining HMAC-SHA256 verification steps. Add to `docs/API.md` under Simulation Data with a verification code example (`hmac.compare_digest` in Python / `crypto.timingSafeEqual` in Node.js). Zero new deps.

---

### 4. Monthly Statistics Time-Series

**Type:** Analytics / Growth
**Effort:** Small (hours)
**Impact:** `/api/stats` gives all-time platform totals: how many sims exist, how many surfaces have been viewed. It doesn't tell you whether the platform is growing. `GET /api/stats/timeseries.json` returns month-by-month activity for the last 12 months (or all months if the deployment is newer). Each entry: `{month: "2026-05", completed: 42, published: 28, avg_confidence_pct: 63.2, distinct_projects: 7}`. Enables: Aeon's weekly digest to report "platform completions up 40% MoM," directory builders displaying growth sparklines on the MiroShark listing, integrators gauging platform load before scaling their automated runs, researchers studying platform adoption curves. Today this data can only be computed by downloading the full gallery and parsing timestamps locally — a time series endpoint makes it first-class.

**How:**
1. `backend/app/services/timeseries_stats.py` (~120 LoC, stdlib `json + os + datetime`). `build_timeseries(sim_root, months: int = 12) -> list`: scan `WONDERWALL_SIMULATION_DATA_DIR`; filter public+completed sims; bucket by `completed_at[:7]` (YYYY-MM key); for each bucket: count completed, count published (is_public=True), avg confidence_pct, distinct project_ids. Return entries sorted newest-first, covering the last `months` calendar months (zero-fill months with no completions so the series is contiguous). Empty platform → empty list `[]`. Add `GET /api/stats/timeseries.json` to `stats.py` on `stats_bp`. ETag `timeseries-{most_recent_month}-{total_eligible}`. `Cache-Control: public, max-age=300`. Query param `?months=N` (1–24, default 12; clamp silently). 10 offline tests in `test_unit_timeseries_stats.py`: sims bucket by completed_at month, zero-fill for empty months, months clamped to [1,24], distinct_projects accurate, avg_confidence_pct float, private sims excluded (completed count includes private; published count excludes — clarify in test), JSON-serialisable, newest-first ordering, ETag changes month boundary, empty platform → empty list.
2. Add `getStatsTimeseries(months)` to `frontend/src/api/simulation.js`. Add `StatsTimeseries` + `StatsTimeseriesEntry` schemas to `openapi.yaml`. Add to `docs/API.md` under Platform alongside `/api/stats` and `/api/stats/distribution.json`. Note the months param. Add to `surfaces_catalog.py`. Zero new deps.

---

### 5. Platform Agent Behavior Census

**Type:** Analytics / Research
**Effort:** Small (hours)
**Impact:** Fourteen-plus integrators now use MiroShark as an AI simulation substrate. Researchers and platform architects ask: "how do agents on MiroShark typically behave in aggregate?" — not for one sim, but across all of them. What fraction start bullish and end bearish? How often does the swarm flip consensus between rounds? What's the average belief shift per round? `GET /api/stats/agents.json` answers these questions at the platform level by scanning all public completed sims and aggregating agent trajectory data. Returns: `{total_sims_analyzed, total_agents_counted, avg_agents_per_sim, stance_at_start: {bullish_pct, bearish_pct, neutral_pct}, stance_at_end: {bullish_pct, bearish_pct, neutral_pct}, opinion_flip_rate, avg_belief_change_per_round, generated_at}`. The per-sim `agents.json` surface answers *who was in this debate*; this answers *how agents on MiroShark behave as a population*. Distinct from `/api/stats` (sim-level aggregates) and platform stats (view counts, surface usage). Relevant for: ML researchers citing swarm properties, journalists characterizing the model, integrators understanding the baseline behavior of the swarm before running custom sims.

**How:**
1. `backend/app/services/agent_census.py` (~150 LoC, stdlib `json + os + math`). `build_agent_census(sim_root) -> dict`: scan public+completed sims; for each, read `trajectory.json` to extract per-agent start position (round 0 belief) and end position (final round belief); apply `±0.2` stance threshold (same as transcript.py / signal_service); compute per-agent opinion_flip (sign(start) != sign(end)); aggregate across all agents. Fields: `total_sims_analyzed`, `total_agents_counted`, `avg_agents_per_sim` (float), `stance_at_start` (pct of all agent starts per stance), `stance_at_end` (pct of all agent ends per stance), `opinion_flip_rate` (fraction of agents who changed stance from start to end), `avg_belief_change_per_round` (mean |delta| per round per agent, across all sims/agents). Missing trajectory.json → skip sim (log warning). Empty platform → all-zero safe envelope. Add `GET /api/stats/agents.json` to `stats.py` on `stats_bp`. ETag `agent-census-{total_sims_analyzed}`. `Cache-Control: public, max-age=300`. 10 offline tests in `test_unit_agent_census.py`: stance buckets sum to 100 pct, flip_rate ∈ [0,1], avg_agents_per_sim ≥ 1 when sims present, private sims excluded, sims with missing trajectory → skipped not errored, JSON-serialisable, ±0.2 threshold consistent with transcript service (test with known trajectory), empty platform → all-zero valid response, ETag string present, generated_at is ISO string.
2. Add `getAgentCensus()` to `frontend/src/api/simulation.js`. Add `AgentCensus` schema to `openapi.yaml`. Add to `docs/API.md` under Platform with a note that the ±0.2 threshold matches the transcript and chart surfaces. Add to `surfaces_catalog.py`. Zero new deps.

---

## Selection Rationale

Today's audit of `backend/app/api/simulation.py` (~10,800 lines, 50+ routes) revealed the platform is far larger than the 32-entry catalog suggests. Seventeen surfaces discovered and registered in the pre-existing registry this run — preventing future idea-slot waste on already-shipped work. The catalog covers the curated public integration layer; the full API is substantially broader.

Given that depth, today's batch avoids the per-sim analytics layer (well-covered) and focuses on **platform-level analytics gaps** — the `/api/stats` family has totals and health but no distribution, trend, or behavioral breakdown:

- **Outcome Distribution** (#1) — "what do MiroShark results look like in aggregate?" is unanswered. Researchers citing the platform need this. Journalists covering it need this. Currently only computable by downloading the full gallery.
- **Payload Validator** (#2) — $1/sim and up to 10 minutes per run means malformed config is expensive to debug. A dry-run validate endpoint saves money and time for the 14+ integrators running automated sim pipelines.
- **Signed Result** (#3) — HTTPS covers in-transit authenticity. Once a result is stored in a database or ledger, there's no way to prove it matches what the server returned without a live API call. HMAC signature over the canonical result JSON gives integrators offline verifiability — same key as webhook delivery, zero new config.
- **Monthly Time-Series** (#4) — `/api/stats` is static. Platform growth is invisible from the API today. Month-by-month completions enable trend reporting, growth dashboards, and load planning for high-volume integrators.
- **Agent Behavior Census** (#5) — "how do agents on MiroShark behave as a population?" is a research-grade question no existing surface answers. The 14+ integrators and any ML researcher citing MiroShark need platform-level behavioral baselines, not just per-sim agent rosters.

Excluded (blocked): **Operator Profile** — re-verified today. `platform_stats.py:42-43` still documents `project_id` as the closest stable identifier; no `operator`/`created_by` field present. Block holds.

Excluded (7-day window): **All-Time Leaderboard** (Jun-04 #4) — still unbuilt, re-eligible Jun 11. **Scenario Clone Button** (Jun-02 #2) — re-eligible Jun 9. **Japanese README** (Jun-02 #3) — re-eligible Jun 9. **Simulation Batch Create** (Jun-02 #4) — re-eligible Jun 9.

Pre-existing entries added this run to `memory/topics/pre-existing-features.md`: consensus timeline (`/<id>/timeline`), quality breakdown (`/<id>/quality`), belief drift (`/<id>/belief-drift`), interaction network (`/<id>/interaction-network`), transcript JSON/MD, thread text/JSON, BibTeX citation (`/<id>/cite.bib`), Jupyter notebook, templates list (`/templates/list`), agent stats (`/<id>/agent-stats`), per-round frame, demographics, lineage, counterfactual, reproduce JSON, archive zip, per-agent interviews.
