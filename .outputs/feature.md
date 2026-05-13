*Feature Built — 2026-05-13*

Filtered RSS / Atom Feed
The MiroShark public-gallery RSS and Atom feeds used to return every published simulation in date order with no way to slice. They now accept the same filter parameters as the gallery API: `?consensus=bullish`, `?quality=excellent`, `?outcome=correct`, `?q=etf`, `?sort=trending`, and `?limit=N`. A subscriber can bookmark "bullish + excellent + trending" in Feedly, pipe "correct outcomes only" into an n8n workflow, or tail a structured slice in Zapier — without any new schemas or new endpoints.

Why this matters:
Revault and CancerHawk are live integrations consuming MiroShark surfaces today. A trading-signal operator who wanted *bullish-only* simulations in their pipeline had to fetch the full feed and filter client-side. With filters in the URL, the feed becomes a structured signal source instead of a firehose. This was idea #3 in the 2026-05-12 repo-actions batch — the underlying filter logic has been tested and shipped since PR #69 (the gallery filter rollout), so this PR is composition, not new algorithm work. It also pulls `?sort=trending` (PR #78's discovery primitive) onto the syndication channel — the most-served sims float to the top of an RSS reader's river view.

What was built:
- backend/app/services/feed.py: `select_public_cards` gains `q`, `consensus`, `quality`, `outcome`, `sort`, and `surface_stats_reader` kwargs. Reuses `gallery_filters.select_filtered_cards` so the feed and `GET /api/simulation/public` answer the same question identically. `render_feed` gains a `_filter_chip` helper that builds an EN / zh-CN summary of active filters and splices it into the feed channel title + subtitle. New `MAX_FEED_LIMIT = 50` shared with the route.
- backend/app/api/feed.py: parses + normalises the new query params via existing `gallery_filters.normalise_*` helpers, plumbs them through to the renderer. Trending sort lazily injects a surface-stats reader; every other sort key keeps the route read-free.
- backend/openapi.yaml: both `/api/feed.atom` and `/api/feed.rss` document every new param with its enum + default. Drift-detection test passes.
- backend/tests/test_unit_feed_filters.py: 16 new offline tests — ±0.2 stance threshold parity, near-tie exclusion, quality first-word match on "Good with caveats", logical AND between filters, surface-stats callback wiring, graceful fallback on unknown sort, case-insensitive q substring, limit clamping at MAX_FEED_LIMIT, default limit unchanged for legacy callers, verified_only still uses the on-disk outcome_reader (PR #60 regression guard), title reflects active filters, rel="self" preserves query string, source-side drift guard.
- frontend/src/api/simulation.js: `getFeedUrl(...)` now accepts the full filter set; default / empty params are omitted from the query string.
- frontend/src/components/EmbedDialog.vue: new "Build a filtered feed" block with three dropdowns (consensus / quality / sort) + a live URL preview + a one-click copy button. Reactive `feedFilters` map drives the URL as the operator picks. EN / zh-CN strings included.
- docs/FEATURES.md: extends the "Public Gallery Feeds (RSS / Atom)" section with the filtered-feed bullet, the title-reflection contract, and a pointer to the dialog's filter builder.

How it works:
The route handler normalises every query param through the same `gallery_filters.normalise_*` helpers the public-gallery API uses, then passes them into the refactored `select_public_cards` helper. That helper builds gallery cards for every public sim, then defers all filtering, sorting, and truncation to `gallery_filters.select_filtered_cards` — already exercised by 33 tests since PR #69. One source of truth, reused on both surfaces. The `verified_only` gate stays on the feed side rather than going through gallery_filters' embedded-outcome path, because the live card builder doesn't always inline `outcome.json` into the card payload; trusting the embedded field alone would silently drop legit verified sims. `sort=trending` reads `surface-stats.json` only when the operator opts in — every other sort key keeps the path read-free, same as the gallery API.

What's next:
The remaining 2026-05-12 batch ideas — granular simulation lifecycle webhooks (#1), interactive iframe embed widget (#2), per-round belief snapshot API (#4), sitemap.xml for SEO (#5). All four extend the same arc this PR sits in: turning each MiroShark surface into a structured, addressable, subscribable primitive that integrators can plug into without scraping HTML or filtering client-side.

PR: https://github.com/aaronjmars/MiroShark/pull/81
