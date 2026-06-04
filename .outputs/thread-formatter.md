*Thread Draft — 2026-06-04*
Topic: Per-Project Simulation Statistics — /api/project/<id>/stats (PR #147)

1/ MiroShark's API had per-platform stats and per-simulation stats. It had nothing in between. PR #147 ships the missing layer: GET /api/project/<id>/stats aggregates across every sim under a single project ID.

2/ The platform exposed two endpoints: /api/stats for the whole instance and 26 per-simulation surfaces for individual runs. Operators running multiple named projects had to fetch the platform aggregate and filter it themselves on the client side.

3/ The new route validates project_id at the boundary, returns an all-zero envelope for unknown IDs (not a 404), caches at 60s, and adds one new field absent from the platform aggregate: quality_distribution — excellent/good/fair/poor buckets, only useful at per-project granularity.

4/ This establishes a third axis the stats API can grow along. Whole-instance / per-project / per-sim is how multi-tenant analytics APIs end up shaped. stats.py now mounts three blueprints where it mounted two yesterday. 39th consecutive PR with zero new dependencies.

5/ PR #147 — 13 files, +1,864 lines, 28 offline tests, zero new dependencies. https://github.com/aaronjmars/MiroShark/pull/147

(article: articles/thread-2026-06-04.md)
