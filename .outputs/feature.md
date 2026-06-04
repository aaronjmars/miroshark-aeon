*Feature Built — 2026-06-04*

Per-Project Simulation Statistics
MiroShark just got a per-project view of its aggregate stats. Until now, operators publishing simulations across multiple projects could see the platform total (every public sim, all projects, in one number) but had no API call to scope those numbers to a single workspace. The new `GET /api/project/<project_id>/stats` returns the same shape of envelope — sim count, consensus distribution, average confidence, surface views, newest sim — filtered to one `project_id`, plus a per-bucket quality distribution (excellent / good / fair / poor) that's only meaningful at the per-project granularity.

Why this matters:
Sixteen-plus named integrators are now building on MiroShark and the ecosystem PRs keep landing. An operator running several published projects — AntFleet's miroshark-bench security suite, SyntheticsAI's pipeline, or any of the 14 other named teams — has had to fetch `/api/stats` plus the public gallery and filter client-side just to answer *"how is **this** project performing?"*. One call now returns those numbers directly. This was Jun-02 #5 from repo-actions and pairs with the Ecosystem JSON Registry that shipped yesterday (PR #145) — both close gaps between MiroShark's machine-readable surface area and the integrators consuming it.

What was built:
- `backend/app/services/project_stats.py` — new ~470-LoC stdlib service. Scans `WONDERWALL_SIMULATION_DATA_DIR` for sims matching the requested `project_id` exactly, applies the same publish-gate (`is_public` + `completed`) as the platform aggregate, and returns the envelope. Module-level cache keyed on `(sim_root, project_id)` with a 60-second TTL matching `/api/stats`.
- `backend/app/api/stats.py` — second blueprint (`project_stats_bp`) mounted at `/api/project`. `project_id` validated against `[A-Za-z0-9_.\-]{1,120}` at the boundary; malformed returns 400, unknown returns an all-zero envelope (not 404 — absence is a valid state). ETag `"project-<total>-<newest_id_prefix>"` distinct from the platform ETag so a polling consumer doesn't confuse the two caches.
- `backend/app/services/surfaces_catalog.py` — added `project_stats` entry so the new endpoint is discoverable via `/api/surfaces.json` alongside `platform_stats` and `platform_stats_badge`.
- `backend/openapi.yaml` — full path + `ProjectStats` schema component (envelope shape, four-bucket `quality_distribution`, ETag header, 304/400 responses).
- `backend/tests/test_unit_project_stats.py` — 28 offline unit tests covering empty/missing sim_root, unknown/non-matching/case-sensitive `project_id` filter, unpublished/incomplete exclusion, mixed-direction counts, quality bucketing (including unknown-value exclusion), surface-views per-project boundary, newest-sim selection, avg confidence rounding, 60s cache + force_refresh + per-project cache isolation, ETag derivation + distinctness from platform ETag, route/blueprint/openapi/drift-test wiring guards.
- `frontend/src/api/simulation.js` — `getProjectStats(projectId)` + `getProjectStatsUrl(projectId, origin)` helpers, same shape as the existing `getPlatformStats` / `getEcosystem` consumers (no Vue view; this is an operator/integrator-facing API).
- `docs/{API,FEATURES,OBSERVABILITY}.md` — table row, full feature section between Ecosystem JSON Registry and BibTeX Academic Citation, new Aggregate Metrics section in OBSERVABILITY listing all three platform-level endpoints.

How it works:
The endpoint walks the sim directory tree once and counts every directory whose `state.json` has `project_id == <requested>` AND `is_public == true` AND `status == "completed"`. Stance derivation reuses `signal_service.compute_signal` over each sim's trajectory — same plurality + `bullish > bearish > neutral` tie-break rules the per-sim `signal.json` uses, so a sim counted Bullish in its signal lands in the project's bullish bucket. Surface views sum over the same `surface_stats.SURFACE_KEYS` whitelist the platform aggregate uses, so unknown surface keys can't pollute the counter. The 60-second per-`(sim_root, project_id)` cache absorbs polling-dashboard load; an `If-None-Match` GET short-circuits to 304 without re-serialising the body.

What's next:
The Jun-02 batch is now half-built: Ecosystem JSON Registry (#1) shipped yesterday, this is #5. Three remain — Scenario Clone Button (#2, UI for the existing `/clone.json` API), Japanese README (#3, JP community signal active since @m000_crypto May-17 coverage), Simulation Batch Create API (#4, integrator pain point as benchmark suites scale). PR #147 is open and pending CI.

PR: https://github.com/aaronjmars/MiroShark/pull/147
