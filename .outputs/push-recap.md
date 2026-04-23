*Push Recap — 2026-04-23*
aaronjmars/MiroShark — 1 commit by 2 authors (Aaron + Aeon co-author); aaronjmars/miroshark-aeon — 0 substantive, ~28 auto-chore commits.

Public Simulation Gallery (PR #43): /explore is live. Every simulation toggled public via /publish now has a discoverable home — a card grid pulling the share-card PNG as thumbnail, quality + stance pills, belief-split mini-bar, and paired "Open →" + "Fork this →" actions. Closes the discovery gap left by PR #41 (is_public) and PR #42 (share card).

Backend pattern compounds: new `_build_gallery_card_payload()` is the sibling of PR #42's `_build_embed_summary_payload()` — cheap reads over the per-simulation on-disk layout (state/config/quality/trajectory/resolution JSON), graceful per-sim degradation, no DB joins. GET /api/simulation/public is paginated, sorted created_at desc, with a 30s public cache.

Key changes:
- New ExploreView.vue (+957 lines) — responsive card grid, loading skeleton, empty + error states, Load more pagination
- New /api/simulation/public endpoint (+215 lines in simulation.py) with scenario truncation to 180 chars
- EmbedDialog callout flips to "Live on the public gallery" + Open gallery ↗ once operator toggles public; 5 offline unit tests in test_unit_public_gallery.py; ◎ Explore nav link added to Home.vue

Distribution lever for the 1K-stars-by-Apr-30 target (773 → 1,000, 7 days left, ~30/day pace). Zero new deps, zero DB schema change.

Stats: 8 files changed, +1,536 / -0 lines
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-23.md
