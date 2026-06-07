*Thread Draft — 2026-06-07*
Topic: Platform Outcome Distribution — GET /api/stats/distribution.json (PR #151)

1/ /api/stats tells you how many simulations are in the corpus. /api/stats/distribution.json — merged today as PR #151 — tells you how those simulations are shaped: direction, confidence, quality, and round-count, each split into buckets.

2/ Before today, /api/stats answered size questions only: total sims, total views, projects. It couldn't tell you whether the corpus leaned bullish, what share hit high-confidence, or whether most runs were long. Shape questions had no surface.

3/ Four dimensions: direction (bullish/neutral/bearish, same tie-break as per-sim signal.json), confidence (high ≥70 / medium 40–70 / low <40), quality from quality.json.health, round-count short/medium/long. Plus avg_confidence_pct and avg_total_rounds. 300-second cache.

4/ The cache is 300 seconds — five times /api/stats' 60 — because the consumer is press unfurls and slow dashboards, not per-tick polling. ETag bumps on a new calendar month even when totals are static. PR #150 merged 8 minutes later, closing the open-PR queue to 0.

5/ The 33rd catalogued surface, 41st stdlib-only PR in a row. GET /api/stats/distribution.json — shape companion to /api/stats. https://github.com/aaronjmars/MiroShark/pull/151

(article: articles/thread-2026-06-07.md)
