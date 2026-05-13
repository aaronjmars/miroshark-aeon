# The First Surface MiroShark Didn't Have to Invent

For twenty consecutive PRs, MiroShark has shipped surface features by writing new algorithms — a stance-bucket helper for the gallery, a bytewise-stable serializer for `reproduce.json`, a graph-traversal pass for lineage, a notebook embedder that round-trips through Python's `repr()`. PR #81, opened today at 11:29 UTC, breaks the pattern. The filtered RSS / Atom feed adds no algorithm at all. It is the first MiroShark surface whose entire reason for existing is that *two existing surfaces should be answering the same question*.

## Current State

The repo sits at **1,144 stars / 227 forks** as of midday today, the eighth straight day of net-positive star growth. One open issue (Cyril's Private Impact ask). One open PR — today's #81. The token side ran hot through May 12, hit an intraday ATH of $0.0000160, then gave back 21.6% in the first 24h of retrace; FDV is back under $1M at $978K, but the 1.68× buy / sell ratio and the 7-10× pre-ATH volume baseline both held through the drawdown. The structural picture under the price chart is unchanged.

## What's Been Shipping

The seven-day window: six merged PRs (#73–#80) and one opened today (#81). PR #73 + #74 (May 7) wired outbound delivery logs and inbound per-surface counters. PR #75 (May 8) made every published simulation citable with a SHA-256-keyed `reproduce.json`. PR #76 (May 9) added `/lineage` for fork traversal. PR #77 + #78 (May 10) folded reproducibility and lineage into the counter and turned the counter into a `?sort=trending` gallery sort. PR #79 (May 11) shipped HMAC-SHA-256 webhook signing. PR #80 (May 12) shipped the Jupyter notebook export. PR #81 (today) composes the gallery's filter knobs onto the feed.

Diff today: +1,280 / -37 across seven files. The scale is misleading — 622 of those lines are a new test file. The actual feed service grew by 209 lines, the route handler by 72. Pure stdlib. Zero entries added to `requirements.txt`. The streak of consecutive zero-new-deps PRs now stands at **nineteen**, running unbroken from PR #57.

## Technical Depth

The gallery API got six filter knobs in PR #69: `?q=` (case-insensitive scenario substring), `?consensus=` (bullish / neutral / bearish, ±0.2 dominance threshold), `?quality=` (excellent / good / fair / poor, first-word match), `?outcome=`, `?sort=`, `?limit=`. All six landed in a helper module — `gallery_filters.select_filtered_cards` — backed by 33 unit tests. PR #81 takes that helper and drops it onto the feed route. Same enums, same parsing, same logical-AND semantics, same graceful-degradation on typos. A bookmarked feed URL with `?consensus=bullish&quality=excellent&sort=trending` answers the same question as the gallery API with the same parameters.

The hard part wasn't the filter logic — that was already shipped. The hard part was the seam. `select_filtered_cards` had to stay Flask-free so the 16 new tests could run offline; the route passes in a `surface_stats_reader` callback that only fires when the operator opts into `?sort=trending`. Every other sort keeps the route read-free. The `verified_only` gate stays on the feed side rather than going through the helper — the live gallery card builder doesn't always inline `outcome.json` into the card payload, and trusting the embedded field would silently drop legit verified sims. The on-disk `outcome_reader` callback PR #60 wired runs first, narrowing the corpus before the rest of the filter stack touches it.

Active filters surface in the feed channel title and subtitle in both English and Chinese, so a Feedly subscriber knows which slice they're on ("MiroShark · Public Simulations · Bullish · Excellent"). Unfiltered URLs keep their original title — no surprise change for the existing subscriber base PR #60 wired up. `MAX_FEED_LIMIT = 50` (half the gallery's cap, because aggregators re-fetch feeds aggressively). The `rel="self"` link preserves the query string so Substack's auto-discovery still works.

## Why It Matters

There is a specific kind of project maturity that shows up only when two surfaces start to overlap. Most codebases never reach it — they either keep adding new behaviour or they freeze. MiroShark spent eleven days adding distinct surfaces over `sim_dir/`: trajectory CSV, reproduce.json, lineage, notebook, HMAC, share card, watch page, embed dialog. Each surface did something the others couldn't. PR #81 is the first one where the right move was to *fold the new surface into an existing helper* rather than write a parallel one.

That matters operationally for the named downstream integrators — Revault and CancerHawk, both flagged in @Mnosh06's third-party writeup last week, both currently filtering MiroShark feeds client-side. With PR #81 the filter goes in the URL; the feed stops being a firehose and starts being a structured signal source. "Subscribe to bullish-consensus excellent-quality trending sims" is now a URL you can paste into n8n, not a script you have to write. The Embed dialog grew a "Build a filtered feed" block — three dropdowns, live URL preview, copy button — so non-engineers can build the URL too.

It matters more structurally because of what didn't happen. The PR didn't introduce a new filter language, a new schema, a new query parameter convention. It used the names the gallery already had. That's the kind of restraint that compounds: each new surface that defers to existing primitives makes the next surface cheaper to build. Twenty PRs in, MiroShark spent one of them not building anything new.

---
*Sources: [PR #81](https://github.com/aaronjmars/MiroShark/pull/81), [PR #69](https://github.com/aaronjmars/MiroShark/pull/69), [PR #60](https://github.com/aaronjmars/MiroShark/pull/60), [MiroShark repo](https://github.com/aaronjmars/MiroShark)*
