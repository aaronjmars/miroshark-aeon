*Feature Built — 2026-05-03*

Gallery Search & Filtering
The /explore gallery just got a query language. Researchers can now type into a search bar to find every simulation about "Aave" or "ETH staking", click chips to filter to bullish / neutral / bearish consensus or excellent / good / fair / poor quality, sort by date / rounds / agents, and bookmark the resulting URL — every filter is encoded as a query string, so "all excellent-quality bearish calls about Aave" is now a single tweetable link. Until today /explore was a reverse-chronological scroll; now it's a research database.

Why this matters:
The seven prior export surfaces — gallery card, share card, replay GIF, transcript Markdown + JSON, RSS / Atom feed, trajectory CSV / JSONL, live watch page — all serialize one simulation. They give you everything you need to share a single result, but until today there was no surface that helped you find the result in the first place. With the corpus past a hundred public sims and growing, the reverse-chronological /explore page had stopped being a tool and started being noise. This is the multiplicative move: the index across the seven existing surfaces, the layer that finally makes them discoverable. From repo-actions May 2 idea #2 — picked over Cloud Deploy / Cost Estimator / Per-Agent Sparklines / Pre-filled Scenario URL because it was the cleanest small-effort autonomous pick that compounds on every previous surface.

What was built:
- backend/app/services/gallery_filters.py: New ~320-LoC pure-stdlib service with dominant_stance() (the same ±0.2 threshold every other surface uses), param normalisers for limit / offset / page / query / consensus / quality / outcome / sort, filter_cards() with logical-AND composition + garbage-card skipping, sort_cards() with deterministic tie-breakers, end-to-end select_filtered_cards() returning (page_items, total_filtered).
- backend/app/api/simulation.py: list_public_simulations() now accepts q / consensus / quality / outcome / sort / page query params, builds gallery cards for every public sim before filtering (the existing 30s Cache-Control amortises the work), and defers to gallery_filters.select_filtered_cards() for the filter → sort → paginate composition. Backward-compatible — verified=1, limit, offset still work exactly as before.
- backend/tests/test_unit_gallery_filters.py: 33 offline unit tests covering param normalisation, ±0.2 threshold parity, every filter alone + combined, sort determinism, and end-to-end pagination including the filtered-total-vs-corpus-total contract.
- frontend/src/views/ExploreView.vue: Debounced 300ms search bar with clear button, Consensus chip group (All / ▲ Bullish / ● Neutral / ▼ Bearish), Quality chip group (All / Excellent / Good / Fair / Poor), sort dropdown (Newest / Most rounds / Most agents), filter-aware empty state with a Reset CTA, all filter state mirrored to URL params via router.replace so the back button doesn't pile up keystrokes.
- backend/openapi.yaml: New query parameters + response envelope fields documented; drift-detection test passes.
- README.md + docs/FEATURES.md + docs/API.md (and zh-CN mirrors): "Gallery Search & Filtering" feature row + complete query parameter reference table.

How it works:
The filter logic is a single in-memory pass over the gallery cards the public endpoint already assembles — pure-stdlib, no whoosh, no sqlite-fts, no rebuilt indexes. At the current corpus size, an in-memory substring + dict-comparison pass is faster than any indexed alternative would be after JSON deserialization. Filters compose with logical AND; empty / unknown values are no-ops (?consensus= returns the unfiltered listing rather than 400-ing, ?sort=popularity falls back to sort=date) so the frontend forwards whatever the user typed without re-validating — single source of truth on the API side. The total in the response envelope is the **filtered** count (Stripe total_count convention), so paginating through ?consensus=bearish doesn't see the load-more button promise more results that don't match. The frontend stores filter state in URL params, not localStorage — /explore?q=aave&consensus=bearish is a tweetable link, and toggling Verified ↔ Explore via the header chip preserves the active query string across the route swap so users don't lose their search.

What's next:
The same filter shape could land on /api/feed.atom / .rss so a Feedly subscriber can follow "every bearish DeFi call" as an RSS feed, not just the global list. Per-agent sparklines (idea #4 from May 2 repo-actions) would add a per-sim quantitative cut alongside the new corpus-level discovery surface, completing the picture between "find the simulation" and "read inside the simulation."

Eight surfaces / one ±0.2 threshold / one folder. Zero-new-deps streak now spans 9 consecutive PRs.

PR: https://github.com/aaronjmars/MiroShark/pull/69
