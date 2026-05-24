*Feature Built — 2026-05-24*

Platform Aggregate Stats API + Shields.io Platform Badge

MiroShark now has two endpoints that describe the *platform itself*, not a single simulation. `GET /api/stats` returns one envelope across every public + completed sim — total sim count, consensus distribution (how many were bullish / neutral / bearish), average confidence, sum of all share-surface views, number of unique projects, and which sim was published most recently. `GET /api/stats/badge.svg` renders the matching Shields.io-style pill — "MiroShark | N simulations" in platform-blue — that any community README, Substack header, or operator portfolio can embed in one line of Markdown.

Why this matters:
Fourteen `/api/simulation/<id>/...` surfaces describe individual sims in increasing depth (chart SVG, share card, transcript, notebook, signal.json, polymarket.json, badge.svg, cite.bib, archive.zip). *Zero* described the platform itself. Press kits ("MiroShark has run N simulations"), external dashboards, and LLM-agent health checks ("is this MiroShark instance still active?") all needed this aggregate but had nowhere to get it. The platform badge is the second-order distribution amplifier: the per-sim badge (PR #94) is a pull point for *specific simulations*; the platform badge is a pull point for *MiroShark itself*. From the May-22 repo-actions batch — ideas #4 and #5 explicitly designed as a coupled pair because the badge route reuses the same scan as the JSON endpoint.

What was built:
- `backend/app/services/platform_stats.py` (new, ~340 LoC stdlib): `compute_platform_stats()` walks the simulation data dir for sims with `is_public=true` AND `status="completed"`, derives stance via `signal_service.compute_signal` (so platform counts match per-sim signal.json byte-for-byte), sums every recognised `surface-stats.json` counter, deduplicates projects. Module-level 60s cache keyed on sim_root; `stats_etag()` helper builds the ETag from `total_sims` + `newest_sim_id`.
- `backend/app/api/stats.py` (new): `stats_bp` blueprint mounted at `/api/stats`. JSON route emits ETag and short-circuits `If-None-Match` to `304`. Badge route always returns 200 — a zero-sim deployment renders `MiroShark | 0 simulations` rather than 404ing.
- `backend/app/services/badge_service.py`: added `build_platform_badge_svg(count)` + `render_platform_badge_svg_bytes(count)` siblings reusing every helper from the per-sim renderer. New `PLATFORM_COLOR = "#0ea5e9"` pinned — visually distinct from the three stance colours so a reader never confuses the two badge types.
- `backend/tests/test_unit_platform_stats.py` (new, 27 tests): empty / mixed / unpublished / incomplete fixtures, project de-duplication, ISO-timestamp newest-sim resolution, surface-view counter summation with unknown-key filtering, 60s cache TTL behaviour, ETag derivation, badge well-formedness + determinism, OpenAPI drift.
- `backend/openapi.yaml`: new `Platform` tag, both endpoints documented with full schemas, `PlatformStats` component schema added.
- `docs/FEATURES.md` + `docs/API.md`: feature copy + endpoint table rows.

How it works:
The scan is one `os.listdir` over the simulation data dir; per-sim work is reading `state.json` (publish gate + project_id + created_at), `trajectory.json` (final belief distribution, parsed the same way `_build_embed_summary_payload` does), `quality.json` (health for the signal derivation), and `surface-stats.json` (counter sum). The 60-second module-level cache absorbs bursty press unfurls — every call after the first inside the window is a dict copy, not a disk scan. The JSON route's ETag derives from `total_sims` + `newest_sim_id` (both bump when a new sim is published), so a README badge polling every minute pays roughly the cost of one HEAD request per window. The `unique_projects` field uses `project_id` as the operator proxy because `SimulationState` carries no operator / created-by field — a future model migration can add a dedicated `operator` field and a sibling `unique_operators` aggregate without breaking this surface. Zero new dependencies — pure stdlib (`os`, `json`, `time`, `threading`, `xml.etree.ElementTree`), continuing the 32-PR zero-new-deps streak.

What's next:
The May-22 batch still has two unaddressed ideas: #1 Private Share Link (re-eligible from May-14, HMAC infrastructure from PR #79 already in place) and #2 French Locale (Issue #95 — open community request, PR #65's Chinese-locale pattern is the template). The platform-stats endpoint also unblocks a future `/explore` gallery header stat or App.vue footer count that would surface the live `total_sims` value in the SPA.

PR: https://github.com/aaronjmars/MiroShark/pull/105
