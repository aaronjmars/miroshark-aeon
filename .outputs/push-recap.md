*Push Recap — 2026-05-09*
aaronjmars/MiroShark — 1 substantive commit (PR #76, open) · aaronjmars/miroshark-aeon — chore commits only

*Simulation Lineage Navigator (PR #76):* Direct sequel to yesterday's PR #75 reproducibility config. PR #75 wrote `parent_simulation_id` + counterfactual trigger metadata into every reproduce.json — the data was on disk, but the lineage was one-directional (a child knew its parent, the parent had no view into its children). PR #76 adds the reverse pointer: new `GET /api/simulation/<id>/lineage` endpoint returning the parent + every public child with kind (fork / counterfactual) + inline trigger metadata, plus an EmbedDialog 🌳 panel that auto-shows only when there's something to navigate to. A researcher running 3 counterfactual branches off a base scenario can finally walk from parent → all branches without remembering each child sim id.

*aeon steady-state:* No feature/fix work today; ~28 routine cron auto-commits from the day's scheduled skill runs (token-report, fetch-tweets, tweet-allocator, repo-pulse, hyperstitions-ideas, feature, push-recap). PR #32 (MEMORY.md row caps) still open + unchanged from yesterday.

Key changes:
- New `backend/app/services/lineage_service.py` (+390, pure stdlib): MAX_CHILDREN=50 cap with honest total_children, public-children-only privacy primitive, corrupt state.json silently skipped, self-pointer doesn't recurse, oldest-first sort
- 501-line offline test pin (`test_unit_lineage.py`, ~16 tests) covering every shape promise + degradation path; OpenAPI drift guard + route-decorator + module-import guards all pass
- EmbedDialog gains 🌳 Lineage panel between repro config + verified-prediction sections; counterfactual rows render trigger round + label inline ("At round 12 (ceo_resigns)") so each branch reads as the narrative event, not a slightly different scenario

Stats: 11 files, +1,778 / -0 lines (MiroShark) · zero new deps · 16 consecutive zero-new-deps PRs (#57 → #76 assuming merge)
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-09.md
