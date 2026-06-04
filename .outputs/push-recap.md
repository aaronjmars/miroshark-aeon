*Push Recap — 2026-06-04*
aaronjmars/MiroShark — 1 substantive commit by Aeon (39th zero-deps streak)
aaronjmars/miroshark-aeon — 2 substantive commits by Aeon

*Per-project aggregate stats:* PR #147 shipped `GET /api/project/<id>/stats` — the missing middle between platform-wide `/api/stats` and per-sim `signal.json`. Same envelope shape filtered to one workspace, plus a new `quality_distribution` (excellent/good/fair/poor) that's only useful at per-project granularity. Two blueprints (`stats_bp` + `project_stats_bp`) on one file; module docstring rewritten 'Two surfaces' → 'Three surfaces.' Unknown project_id returns all-zero, not 404 — absence is a valid dashboard state. Surfaces catalog 30→31.

*Aeon learns to forget — part 2:* PR #52 added `memory/topics/pre-existing-features.md` — sibling to yesterday's blocked-features registry. Same shape, opposite half: 'already shipped, don't suggest' vs 'architecturally blocked, don't suggest.' `repo-actions` now reads both with distinct exclusion notes (`Excluded (pre-existing)` vs `Excluded (blocked)`); `feature` skill checks pre-existing before its grep and writes back new entries on discovery. Bootstrapped with 8 entries (Gallery JSON, Compare API, RSS Feed, Webhook Test Ping, etc.) — motivated by May-28/Jun-01 batches where 3 of 5 ideas were pre-existing.

Key changes:
- backend/app/services/project_stats.py (+522, stdlib-only, 60s per-(root,project_id) cache, 28 offline tests in test_unit_project_stats.py +843)
- backend/app/api/stats.py (+109/-9, second blueprint mounted at /api/project, ETag "project-<total>-<newest_id_prefix>" distinct from platform)
- memory/topics/pre-existing-features.md (new +71, 8 bootstrapped entries with signature-keywords + lives-at path + verifying log + suggestion history)

Stats: ~22 files changed, +2,218 / -20 across 3 commits. Window: 24h since 2026-06-03T15:46:09Z.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-04.md
