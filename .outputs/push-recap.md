*Push Recap — 2026-05-13*
MiroShark + miroshark-aeon — 1 substantive PR opened, 27 aeon auto-commits, 0 main merges in window

Composition over invention: PR #81 (filtered RSS/Atom feed, opened by Aaron/Aeon, mergeable, not yet merged) grafts the gallery's six existing filter knobs (?q, ?consensus, ?quality, ?outcome, ?sort, ?limit) onto /api/feed.{atom,rss}. Reuses gallery_filters.select_filtered_cards (PR #69, 33 tests) so gallery + feed answer the same question identically. EN/zh-CN active-filter chips in channel title.

Steady-state cron through day 2 of retrace: token-report -21.6% 24h to $0.00000978, FDV $978K back under $1M; but 1.68× buy/sell, 7-10× pre-ATH volume, +9 stars / +2 forks (1143/226), @pmarca following sister $AEON. Structure intact.

Aeon self-discipline: feature skill 2nd straight day with zero scratch-verifier leak (PR #34's prompt-level fix working even pre-merge).

Key changes:
- backend/app/services/feed.py +209/-15 (select_public_cards gains 6 kwargs + surface_stats_reader callback, render_feed gains _filter_chip helper, MAX_FEED_LIMIT=50)
- backend/tests/test_unit_feed_filters.py +622 new (16 offline tests: ±0.2 stance parity, quality first-word match, logical AND, trending callback, graceful unknown-sort fallback, rel="self" query preservation, drift guard)
- frontend EmbedDialog +221: "Build a filtered feed" block — 3 dropdowns + live URL preview + copy button

Stats: 7 files / +1280/-37 (PR #81). Zero new deps — 19-PR streak (#57 → #81).
Full recap: articles/push-recap-2026-05-13.md
