*Repo Action Ideas — 2026-06-01*
Generated from analysis of aaronjmars/MiroShark (1,222⭐ · 259 forks · 0 open PRs · 28 surfaces). Three re-eligible from May-24 + two net-new.

1. Operator Profile (Community, Medium)
   Per-operator gallery at /profile/<name> + API — every share page gains a backlink to the operator's full body of work.

2. Agent Persona Export JSON (Feature, Small)
   GET /api/simulation/<id>/agents.json — 29th surface, exports the full agent roster (name, role, initial belief, final stance) so researchers don't parse transcript.md.

3. Simulation Search JSON API (Integration, Small)
   GET /api/search.json?q=&consensus=&min_confidence= — query-filtered companion to the full gallery index; lets LLM agents and benchmark pipelines find sims without downloading everything.

4. Gallery Trending JSON (Integration, Small)
   GET /api/gallery/trending.json — top-10 most-viewed public sims in a rolling 7-day window; exposes the existing surface_stats counters as a ranked discovery feed.

5. Per-Sim Surface Engagement JSON (Feature/DX, Small)
   GET /api/simulation/<id>/surfaces/stats.json — per-surface view counts for a published sim; operators see which surfaces are being consumed (AntFleet benchmark vs. organic share); no new tracking needed.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-01.md
