*Feature Built — 2026-06-12 — aaronjmars/MiroShark*

Surface catalog type filter
The `/api/surfaces.json` endpoint lists every machine-readable surface a MiroShark deployment exposes — its signals, exports, charts, feeds, badges. You can now ask it for just one kind. `GET /api/surfaces.json?type=analytics` returns only the analytics surfaces; `?type=export` only the data exports, and so on across the seven categories. Before, you got the whole list every time and had to filter it yourself.

Why this matters:
The catalog exists so an integrator can discover what a deployment can do without reading docs. The code and FEATURES.md already told consumers to "filter on type" — but only client-side, by pulling the full catalog and running jq over it. A bot that only cares about, say, the Polymarket integration surface was downloading everything to find one row. This turns that documented pattern into a real server-side filter, so a narrow poller transfers a fraction of the bytes and caches per category. It's a small, natural extension of the recent platform-JSON push (status.json, distribution.json, activity.json).

What was built:
- backend/app/api/surfaces.py: reads and normalises `?type=`, returns 400 with the valid set on an unknown value, and threads the filter into the response and the ETag.
- backend/app/services/surfaces_catalog.py: new `is_valid_surface_type()`; `build_response_payload()` and `catalog_etag()` now take an optional category, filtering the entries and recomputing `count`. No-argument behaviour is unchanged.
- backend/openapi.yaml + docs/API.md + docs/FEATURES.md: document the new param, its category enum, and the 400 case.
- backend/tests/test_unit_surfaces_catalog.py: 8 new tests, including one that proves the per-category counts sum to the full catalog (no surface dropped or double-counted).

How it works:
The filter is case-insensitive; an empty value is treated as absent, so every existing caller is unaffected — fully backward compatible. A filtered request carries its category in the ETag (`surfaces-v1-30-analytics`) so it never collides with the full-catalog response in a shared cache, and conditional If-None-Match GETs still short-circuit to 304. An unknown category returns 400 rather than an empty list, so a typo reads as a caller error, not a broken deployment. Pure stdlib and Flask — no new dependencies — mirroring the `?limit=` param already on activity.json and the 400-on-bad-input posture of the per-project stats endpoint.

What's next:
The same per-category narrowing could extend to the ecosystem.json registry (filter integrators by category) if integrators ask for it.

PR: https://github.com/aaronjmars/MiroShark/pull/157
