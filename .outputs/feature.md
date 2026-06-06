*Feature Built — 2026-06-06*

Multi-Sim Batch Status Lookup
MiroShark now exposes a single endpoint that polls up to 20 simulations in one HTTP request: `POST /api/simulation/batch-status` with a body like `{"sim_ids": ["sim_aaa", "sim_bbb", ...]}` returns one entry per id, in input order. Until today, an integrator running a parallel benchmark batch had to fire N separate requests to check on N sims — this collapses that to one.

Why this matters:
The ECOSYSTEM.md table grew past 14 named integrators last week, and the public ones (AntFleet's miroshark-bench, Capacitr's polling loop spec) all run parallel sims and poll status. Yesterday's PR #149 gave them a platform health probe (*is MiroShark up?*); today's PR closes the natural follow-up (*and what's the state of my 20 sims right now?*). It's the third pre-flight / observability primitive in three days — the cluster of surfaces an integrator hits before they touch the sim engine itself.

What was built:
- backend/app/services/batch_status.py: New service (~350 LoC stdlib) — `build_batch_status(sim_root, sim_ids)` walks the input list in order, applies the publish gate per id, derives signal fields for the completed subset via `signal_service.compute_signal`. Helpers (`_final_belief_from_trajectory`, `_signal_for_sim`) duplicate the trajectory-walk pattern from `platform_stats` / `project_stats` byte-for-byte so a sim's batch entry matches its platform contribution exactly.
- backend/app/api/simulation.py: New `@simulation_bp.route('/batch-status', POST)` handler — validates body shape (sim_ids array, non-empty, ≤20, each id passing `^[A-Za-z0-9_\-.]{1,128}$`), 400s before the disk read, returns the envelope with `Cache-Control: no-store`.
- backend/app/__init__.py: `/api/simulation/batch-status` added to the `internal_auth_guard` allow-list alongside `/api/status.json` (same posture — a polling endpoint integrators hit on every batch tick cannot require the internal key).
- backend/app/services/surfaces_catalog.py: New `batch_status` catalog entry (type: integration). Catalog grows 31 → 32.
- backend/openapi.yaml: New `POST /api/simulation/batch-status` path + `BatchStatusResponse` + `BatchStatusEntry` schemas.
- frontend/src/api/simulation.js: New `batchSimulationStatus(simIds)` + `getBatchStatusUrl()` helpers.
- docs/API.md + docs/API.zh-CN.md + docs/FEATURES.md: Endpoint row added (English + Simplified Chinese) and a dedicated FEATURES section explaining the three semantic guarantees.
- backend/tests/test_unit_batch_status.py: 26 offline unit tests — cap drift, ordering, completed/running/failed envelopes, private indistinguishability from unknown, duplicate handling, id validation, empty/missing sim_root, mixed-case status, quality N/A fallback, catalog + auth-guard + openapi drift guards, corrupt state.json tolerance.

How it works:
The endpoint enforces three semantic guarantees that make it safe to expose without auth. First, the per-id publish gate: private sims and unknown sim ids both return a byte-identical `{found: false, status: null, direction: null, ...}` envelope — a caller cannot probe for the existence of a private sim by reading the response. (One of the unit tests deletes the `sim_id` field from a private entry and an unknown entry and asserts the remainders are equal.) Second, analytics fields are emitted only on completed sims: running / failed / cancelled return the bare `status` + null analytics, so a consumer can render the right badge without the response pretending an in-flight sim produced a signal. Third, order is preserved and duplicates are honored — `results[i]` corresponds to `sim_ids[i]`, and a duplicate id emits a duplicate entry, so a polling loop that batches the same id twice gets the same answer twice without having to dedupe itself. Signal derivation uses the same `signal_service.compute_signal` the per-sim `/signal.json` surface calls, so a sim labelled "Bullish 64.5%" here matches its signal.json byte-for-byte. Zero new dependencies (41-PR streak); pure stdlib.

What's next:
The Jun-04 batch is now 4/5 addressed — only #4 All-Time Simulation Leaderboard remains net-new and unbuilt (a `GET /api/leaderboard.json` returning top-10 sims across four dimensions: highest_confidence, best_quality, most_viewed, longest_debate). The natural follow-up to today's PR is an MCP tool wrapper around batch-status so the ecosystem's MCP-connected integrators can poll batches from inside Claude / Cursor / any LLM workflow with one tool call.

PR: https://github.com/aaronjmars/MiroShark/pull/150
