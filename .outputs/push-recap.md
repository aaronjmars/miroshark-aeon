*Push Recap — 2026-06-09*
MiroShark + miroshark-aeon — 2 substantive merges, both Aeon-authored

Theme 1 (MiroShark): `/api/activity.json` lands as the 35th surface — the "what just completed?" polling primitive integrators have been asking the gallery and feed endpoints to be. Third entry in the platform-shaped/keyless cluster alongside `/api/status.json` and `/api/simulation/batch-status`; reuses signal-pipeline byte-for-byte so direction/confidence/quality/total_rounds line up across activity.json + batch-status + signal.json.

Theme 2 (miroshark-aeon): The 7-day re-derivation is retired. PR #55 encodes the May-31 noise-exclusion convention as explicit step 5 of the push-recap skill — `aeonframework` commits prefixed `chore(scheduler):` / `chore(cron):` / `chore(<skill>): auto-commit` are dropped on the agent repo before diff-reading. This recap is the first to run with the rule baked in; it filtered 30 cron commits, saved ~30 `gh api` calls. Second prompt-level self-improvement in 4 days.

Key changes:
- PR #153 (+1615/-1, 10 files): new `activity_bp` blueprint with `Cache-Control: public, max-age=30` + ETag, 439-LoC service module reusing `signal_service.compute_signal` and `batch_status` trajectory walker for byte-for-byte equivalence, 39 unit tests across 18 properties, OpenAPI schemas locked
- PR #153 follow-up fix: `test_documented_paths_exist_in_flask` had a quiet failure mode — blueprints missing from `_BLUEPRINT_PREFIXES` silently skipped; fixed for `activity_bp`, latent for any future blueprint
- PR #55 (+163/-16, 6 files): step 5 inserted into `skills/push-recap/SKILL.md`, steps 5–10 renumbered to 6–11; filter scoped to agent repo (or any repo ending `-aeon`), never to watched project repos

Stats: 16 files changed, +1,778 / -17 lines. 43-PR zero-deps streak intact on MiroShark. Catalog 34 → 35. Both repos closed at 0 open Aeon PRs (third consecutive recap).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-09.md
