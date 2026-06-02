*Repo Action Ideas — 2026-06-02*
Four ecosystem PRs opened today (HivemindOS, Echo Oracle, Capacitr, SyntheticsAI). 16+ named integrators and no machine-readable discovery path. Today's batch addresses that gap and three others.

1. Ecosystem JSON Registry (Integration, Small)
   GET /api/ecosystem.json — structured surface for the 16+ integrators; static-hardcoded pattern of /api/surfaces.json; all 4 new PRs included

2. Scenario Clone Button (DX, Small)
   ?clone=<id> URL param + EmbedDialog button — closes the frontend gap opened when clone.json shipped June 1

3. Japanese README & Features Guide (Community, Medium)
   README.ja.md + docs/FEATURES.ja.md — zero JP docs exist; @m000_crypto JP coverage since May 17

4. Simulation Batch Create API (Integration, Medium)
   POST /api/simulation/batch — up to 10 sim configs per call; cuts N round-trips to 1 for benchmark pipelines like AntFleet

5. Per-Project Simulation Statistics (Feature/DX, Small)
   GET /api/project/<project_id>/stats — per-project aggregates over existing project_id tracking in platform_stats.py

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-02.md
