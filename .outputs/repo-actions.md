*Repo Action Ideas — 2026-05-08*
Generated from analysis of MiroShark (1,117 stars / 222 forks / 0 open PRs / PR #75 merged today).

1. Trending Simulations Sort (Feature, Small)
   Extends gallery sort with 'trending' option — ranks public sims by surface-stats total, turning observability data into a discovery signal.

2. oEmbed Endpoint (Integration, Small)
   `GET /api/oembed?url=...` makes every share card URL auto-embed in Substack, Notion, Ghost, and WordPress — zero new deps, pure stdlib.

3. Simulation Lineage Navigator (Feature, Small)
   `GET /api/simulation/<id>/lineage` exposes the fork/counterfactual tree from reproduce.json metadata — turns parent_simulation_id into a navigable graph in SimulationView.

4. Peak-Round Belief Snapshot (Feature, Small)
   `GET /api/simulation/<id>/peak-round` identifies the highest-divergence round and exports a 1200×630 share card of that moment — the inflection, not just the verdict.

5. Operator Profile + Attribution (DX, Small)
   `GET /api/operator/profile` from env vars (OPERATOR_NAME / BIO / URL) — adds authorship byline to share pages and gallery cards; relevant as MiroShark results circulate on Umia and in Grok citations.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-08.md
