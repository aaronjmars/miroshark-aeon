*Feature Built — 2026-05-10*

Trending Simulations Sort
The MiroShark gallery at `/explore` now has a "🔥 Trending" sort option that ranks public simulations by how widely they've been distributed. Pick it from the sort dropdown and the most-served sims float to the top — the share cards, replay GIFs, transcripts, watch pages, RSS feeds, and every other share surface get summed into a single popularity score per sim. The first time a viral run becomes findable by merit instead of by recency.

Why this matters:
Until now `/explore` could only sort by date, rounds, or agent count — all structural, none reflecting which sims people actually opened or shared. Surface-stats (PR #74, late April) gave every public sim per-surface serve counters on disk, but those numbers were operator-facing only — visible inside the EmbedDialog Distribution panel, invisible to anyone browsing the gallery. This PR closes that loop: distribution analytics now drives discovery ranking, so a sim that gets shared on Twitter and unfurled 500 times outranks one that's been sitting at offset 0 for a week. The discovery ceiling repo-actions flagged on May 8 — sims that get shared get found more easily, compounding the distribution advantage.

What was built:
- `backend/app/services/gallery_filters.py`: New `_trending_key(card)` reads a transient `_serves_total` field, clamps to ≥0 on missing/negative/garbage input, tie-breaks on `created_at` desc so the most-served-and-most-recent floats above the most-served-and-stale. New `TRENDING_FIELD = "_serves_total"` constant pinned at module level so the route handler and the sort key reader stay in lockstep.
- `backend/app/api/simulation.py`: `list_public_simulations()` does a single sweep over `surface_stats.read_surface_stats(sim_dir)` for every public sim **only when `sort=trending`** — the default `date` path stays read-free. Strips the transient field from `page_items` after sort+paginate so the JSON contract stays untouched.
- `backend/openapi.yaml`: `sort` query enum + response enum extended with `trending`; description points at the surface-stats counter sum and explains the date tie-break.
- `frontend/src/views/ExploreView.vue`: Sort dropdown gains a "🔥 Trending" option (i18n: "🔥 热门"); `ALLOWED_SORT` extended; URL-routable so `/explore?sort=trending` is bookmarkable.
- 8 new offline unit tests in `test_unit_gallery_filters.py` (descending sort, date tie-break, missing-field degradation, garbage clamping, end-to-end filter+sort composition, all-zero corpus stays deterministic) + README/FEATURES/API docs in en+zh.

How it works:
The implementation is a read-and-rank, not a new write path. When a request lands with `?sort=trending`, the route handler iterates every public sim once, calls the existing `surface_stats.read_surface_stats(sim_dir)` reader (which sums every per-surface counter into a `total` field), and stamps that total onto each gallery card as a private `_serves_total` field. The sort key reads it, sorts descending, ties break on date. After sort+paginate the field is stripped before serialisation so the public response shape stays byte-identical to other sort keys. Sims with no surface-stats file yet (predating PR #74) count as zero and sort to the bottom — old data doesn't break the trending list. The endpoint's `Cache-Control: public, max-age=30` amortises the per-sim disk reads across many requests; other sort paths add zero new I/O.

What's next:
Natural follow-ups: a "🔥 N serves this week" badge on each gallery card when trending is active (the data is already injected on the card pre-strip), or windowed trending (last-7-day deltas vs. all-time) once the surface-stats schema gains time bucketing. The Substack/Notion-friendly oEmbed endpoint (idea #2 from the same May 8 batch) is also still open and would extend platform reach the same way trending extends discoverability.

PR: https://github.com/aaronjmars/MiroShark/pull/78
