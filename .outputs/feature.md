*Feature Built — 2026-05-30*

Surface Catalog API
MiroShark now publishes a machine-readable list of every feature its backend exposes. Hit GET /api/surfaces.json and you get back a JSON catalog of all 27 surfaces — share cards, trajectory exports, badges, Polymarket signals, volatility analytics, the lot — each with its endpoint path, HTTP method, type category, one-line description, and a copy-pasteable curl example. The catalog the platform was missing: an API that describes the rest of the API.

Why this matters:
Every integrator hitting MiroShark on day one has had to answer the same question by reading docs/FEATURES.md or grepping routes — *what's actually available on this deployment?* With 12+ named integrators now wiring MiroShark into their pipelines (AntFleet, RevaultDrops, Noelclaw, plus the 10 NurstarK-catalogued products), that discovery loop runs every onboarding. PRs #118 and #119 refined first-touch discoverability for human readers; this PR adds the same for machine readers. Aeon's own daily surface-count check no longer needs to parse FEATURES.md to know what shipped.

What was built:
- backend/app/services/surfaces_catalog.py: Hardcoded 27-entry catalog as a literal Python list — 24 publish-gated per-sim surfaces (signal.json, share-card.png, polymarket.json, volatility, peak-round, badge.svg, etc.) + 2 platform-level (/api/stats and its badge) + 1 self-referential entry. Seven type categories: analytics, visualization, export, embed, integration, platform, discovery.
- backend/app/api/surfaces.py: GET /api/surfaces.json route. ETag is surfaces-v1-<count>, short-circuits to 304 on If-None-Match. Cache-Control max-age 3600. Always returns 200 or 304 — no input can produce a 404.
- backend/tests/test_unit_surfaces_catalog.py: 18 offline tests — schema invariants (key uniqueness, valid types/methods, description ≤120 chars, example_curl references its endpoint verbatim), drift guards (per-sim catalog subset cross-checks against SURFACE_KEYS), ETag determinism, immutability of returned objects, OpenAPI spec presence.
- backend/openapi.yaml + frontend/src/api/simulation.js + docs/API.md + docs/FEATURES.md: full spec + helpers + documentation.

How it works:
The catalog is static and hardcoded by design — NOT auto-derived from SURFACE_KEYS (which only tracks the publish-gated per-sim counters), and NOT scanned off Flask's URL map (which would leak the private mutation routes the catalog must not advertise). A new surface ships in three files: the route handler, SURFACE_KEYS if it's per-sim and publish-gated, and this catalog. A drift-guard unit test cross-checks the per-sim subset against SURFACE_KEYS so neither side can drift silently. The response envelope is schema-versioned ({schema_version: "1", count, surfaces}); appending entries is non-breaking, reordering is breaking. Every example_curl uses literal placeholders (https://your-host and <simulation_id>) — no entry leaks a real host or token.

What's next:
The catalog is the foundation a future deployment-fingerprint surface can build on — version, feature-flag matrix, capability-discovery handshake. Aeon's daily surface-count check can now poll one endpoint instead of parsing docs.

PR: https://github.com/aaronjmars/MiroShark/pull/130
