*Repo Action Ideas — 2026-06-10*
Generated from analysis of aaronjmars/MiroShark (1,244★, 263 forks, catalog 35, PR #155 Chinese README merged today).

1. Japanese README — README.ja.md (Community/Growth, Small)
   First Japanese-language root entry point; m000_crypto JP coverage since May 17; mirrors the README.zh-CN.md pattern just proved out today.

2. Scenario Clone Button (Feature/DX, Small)
   UI button + ?clone= query param that pre-fills the create form from an existing published sim's clone.json — the API exists, the front door doesn't.

3. Simulation Batch Create API (Integration, Medium)
   POST /api/simulation/batch creates up to 10 sims in one request; pairs with the existing batch-status endpoint to close the create→poll→signal pipeline loop.

4. Simulation Percentile Rank (Analytics, Small)
   GET /api/simulation/<id>/rank.json — where does a specific sim's confidence and quality sit in the platform distribution? The distribution endpoint provides the shape; this applies it per-sim.

5. Platform Performance Metrics (Analytics, Small)
   GET /api/stats/performance.json — p50/p95 completion latency and sims/hour throughput over rolling windows; the number batch pipeline operators need before scheduling a run.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-10.md
