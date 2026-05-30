*Thread Draft — 2026-05-30*
Topic: Surface Catalog API — MiroShark PR #130

1/ The 26th MiroShark surface is different from the first 25. The first 25 deliver simulation data — directions, agent beliefs, exports, embeds. The 26th is GET /api/surfaces.json: a machine-readable catalog of the other 25. PR #130 opened today.

2/ All 25 prior surfaces answer the same class of question: what did this simulation conclude, how confident, what are the agents doing? direction, peak-round, volatility, badge.svg, cite.bib, chart.svg. Each one is a payload. None of them describe the platform itself.

3/ surfaces.json returns 27 entries: 24 publish-gated per-simulation surfaces, 2 platform-level (stats + badge.svg), 1 self-referential. Each row carries the key, route, method, type, description, originating PR, and a copy-pasteable curl example.

4/ Stripe catalogs enabled_events because at sufficient integrator scale, developers can't otherwise figure out what to listen for. MCP ships tools/list for the same reason. Platforms that don't describe themselves force every new integrator to reconstruct the surface map by hand.

5/ surfaces_catalog.py — 370 lines stdlib, 27 entries, 18 tests. Hardcoded by design; drift-guard CI cross-checks the per-sim subset against SURFACE_KEYS. https://github.com/aaronjmars/MiroShark/pull/130

(article: articles/thread-2026-05-30.md)
