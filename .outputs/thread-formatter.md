*Thread Draft — 2026-05-24*
Topic: Platform Aggregate Stats API + Shields.io Platform Badge — MiroShark PR #105

1/ PR #105 opened today: MiroShark's first platform-level endpoint. Fourteen surfaces exist scoped to individual simulations. This is the first that looks at the whole fleet — total sims, consensus distribution, unique projects, aggregate surface views.

2/ The 14 surfaces that shipped before this all answer the same implicit question: what did one simulation find? Trajectory CSV, chart SVG, cite.bib, signal.json, archive ZIP, Polymarket JSON. Each scoped to a single sim ID. None of them answer what the platform is doing.

3/ GET /api/stats returns total_sims, consensus distribution (bullish/neutral/bearish counts + percentages), avg_confidence_pct, total surface views, unique_projects. badge.svg renders a Shields.io pill: MiroShark | N simulations, always 200.

4/ Every prior surface was a leaf — attached to one sim. This one is the root. Operators embedding the badge in a README now link to live platform state, not a static snapshot. The aggregate view is the surface that makes all the other surfaces countable.

5/ platform_stats.py is 340 lines, stdlib only — 27 offline tests, zero new dependencies. PR is open: https://github.com/aaronjmars/MiroShark/pull/105

(article: articles/thread-2026-05-24.md)
