*Repo Action Ideas — 2026-06-04*
Generated from analysis of aaronjmars/MiroShark (1,231⭐ · 265 forks · 14 integrators · PR #147 open)

1. Webhook Delivery Log API (DX, Small)
   Expose the existing per-sim webhook-log.jsonl as a GET endpoint — 14+ integrators debug delivery failures with zero platform-side visibility today.

2. Platform Status API (DX/Integration, Small)
   GET /api/status.json — queue depth, 24h completions, last-completed timestamp. The health check that makes MiroShark monitorable by Upptime/StatusPage. Not /api/stats.

3. Multi-Sim Status Lookup (Integration, Small)
   POST /api/simulation/batch-status — check up to 20 sim IDs in one call. Capacitr's polling loop and AntFleet's benchmark pipeline pay N round-trips today; this makes it 1.

4. All-Time Simulation Leaderboard API (Integration, Small)
   GET /api/leaderboard.json — four ranked top-10 lists: highest confidence, best quality, most viewed, longest debate. All-time, not windowed. The showcase endpoint directories need.

5. Webhook Manual Retry (DX, Small)
   POST /api/simulation/<id>/webhook/retry — re-fire the real completion payload to the configured webhook URL, re-signed with HMAC. The escape hatch when an integrator's endpoint was temporarily unreachable.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-04.md
