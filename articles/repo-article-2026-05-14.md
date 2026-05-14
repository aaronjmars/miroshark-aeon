# From Browse to Subscribe to Crawl

For the last eighteen days, finding a MiroShark simulation has been a problem with exactly two answers. Either you knew the share-link URL someone had handed you, or you opened the gallery and scrolled. PR #82 merged at 12:49 UTC today and added the third answer: a search engine can now discover every public simulation by itself. With it, an arc that started with PR #69's gallery filter helper and continued through yesterday's filtered RSS / Atom feed (PR #81) is structurally complete. MiroShark has shipped its external discovery layer.

## Current State

The repo crossed **1,147 stars / 227 forks** at midday today — net +4 stars / +1 fork in 24 hours, the ninth straight day of positive star growth. Zero open issues, zero open PRs. The May-12 repo-actions idea batch is now resolved 5 / 5 (two ideas turned out to already exist as SPA routes, one was deferred for runner-hook-point risk, two shipped as PRs #81 and #82). The token side is recovering from May 13's drawdown: $0.000011578 (+20.42% 24h), FDV $1.16M back above the seven-figure threshold, 30-day return +363.7%, May 12 ATH still standing at $0.0000160.

## What's Been Shipping

The seven-day window: eight merged PRs (#73 → #82), one per substantive day, no overlap. PR #73 + #74 (May 7) wired observability over `sim_dir/`. PR #75 (May 8) made every public simulation citable with a bytewise-stable `reproduce.json`. PR #76 (May 9) added `/lineage` graph traversal. PR #77 + #78 (May 10) folded the citation and lineage surfaces into the counter and turned the counter into a `?sort=trending` discovery primitive. PR #79 (May 11) shipped HMAC-SHA-256 webhook signing. PR #80 (May 12) shipped the Jupyter notebook export. PR #81 (May 13) composed the gallery filter knobs onto the feed. PR #82 (today) ships `GET /sitemap.xml` plus a companion `GET /robots.txt` plus `GET /api/config/sitemap` for the SPA flag.

PR #82 diff: +1,273 / -2 across 15 files. 22 new offline tests covering pinned invariants, public/private filtering, the `<lastmod>` fallback chain, `<changefreq>` semantics, byte determinism, the 50,000-URL cap (sitemaps.org spec ceiling), robots.txt directives, and XML round-trip via `xml.etree.ElementTree.fromstring`. Pure stdlib: `xml.etree.ElementTree` + `os` + `datetime`. Zero entries added to `requirements.txt`. The streak of consecutive zero-new-deps PRs now stands at **twenty**, running unbroken from PR #57.

## Technical Depth

The three layers compose. Layer one is PR #69's `gallery_filters.select_filtered_cards` — six filter knobs (`q`, `consensus`, `quality`, `outcome`, `sort`, `limit`), 33 tests, Flask-free so it runs offline. Layer two is PR #81: that helper, plus the existing PR #60 feed surface, plus a `surface_stats_reader` callback that only fires when the operator opts into `?sort=trending`. Layer three is PR #82: a deterministic sweep over the same public-simulation corpus, one `<url>` block per `/share/<id>` (priority 0.8) and per `/watch/<id>` (priority 0.7), sorted by `simulation_id` ascending. Two consecutive renders against the same on-disk corpus produce byte-identical XML — the same discipline that made `reproduce.json` a SHA-256 citation key in PR #75.

The `<lastmod>` field falls through `updated_at` → `created_at` → `state.json` mtime, so a long-lived in-progress simulation whose `created_at` is days old still tells the crawler "the artifact changed today." `<changefreq>always</changefreq>` for in-progress sims (belief bars genuinely change every round), `weekly` for completed share entries, `daily` for completed watch entries. The `ENABLE_SITEMAP=false` switch makes `/sitemap.xml` 404 *and* drops the `Sitemap:` directive from `robots.txt` — no leak through robots either, in case a private deployment forgets to harden both. `Disallow: /api/` is always served regardless of the flag; even a private gallery wants its JSON namespace out of public indices.

## Why It Matters

Discovery isn't a feature. It's a stack of audience tiers, and most projects ship one and ignore the others. The human-browsing tier is the gallery — that's the default a project gets for free. The aggregator tier is a feed URL you paste into Feedly or n8n; ship that and analysts can subscribe to a slice. The crawler tier is a sitemap; ship that and Google can index 50,000 simulation pages by itself, and the "have you heard of MiroShark" problem stops being a referral problem and starts being a search problem. PR #82 takes a Tuesday-morning analyst Googling "swarm intelligence financial forecasting reproducible" from zero MiroShark surfaces in her results to fifty.

Two days, three PRs, one discovery layer — and only PR #82 was genuinely new code. PR #81 composed PR #60 and PR #69. PR #82 composed the same public-corpus selection logic with a different output format. The arc demonstrates the architectural idiom the streak has been quietly building toward: portable algorithm, boundary I/O. Once the corpus selector exists, every external-facing surface that wants to enumerate it (RSS, Atom, sitemap, oEmbed, an archive bundle) becomes a serializer instead of a feature.

---
*Sources: [PR #82](https://github.com/aaronjmars/MiroShark/pull/82), [PR #81](https://github.com/aaronjmars/MiroShark/pull/81), [PR #69](https://github.com/aaronjmars/MiroShark/pull/69), [PR #75](https://github.com/aaronjmars/MiroShark/pull/75), [PR #60](https://github.com/aaronjmars/MiroShark/pull/60), [MiroShark repo](https://github.com/aaronjmars/MiroShark)*
