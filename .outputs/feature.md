## Summary

**Built and shipped Simulation Lineage Navigator** — repo-actions 2026-05-08 idea #3 — as PR #76 on aaronjmars/MiroShark. Direct follow-up to PR #75 (Reproducibility Config Export merged yesterday): turns the one-directional `parent_simulation_id` pointer into a navigable graph, so a researcher running counterfactual branches off a base scenario can finally walk from the parent to "the three branches that diverged at round 12".

**Files created/modified:**
- `backend/app/services/lineage_service.py` (new, ~390 LoC, pure stdlib)
- `backend/app/api/simulation.py` — `GET /api/simulation/<id>/lineage` route
- `backend/openapi.yaml` — `SimulationLineage` schema under Analytics
- `backend/tests/test_unit_lineage.py` (new, 16 offline tests)
- `frontend/src/api/simulation.js` — `getSimulationLineage()` helper
- `frontend/src/components/EmbedDialog.vue` — 🌳 Lineage panel
- `README.md` + `docs/FEATURES.md` + `docs/API.md` (en + zh-CN mirrors)
- `memory/MEMORY.md` Skills Built table + `memory/logs/2026-05-09.md` log entry

**Outcomes:**
- PR: https://github.com/aaronjmars/MiroShark/pull/76 (CI pending)
- Frontend builds clean (728 modules, vite v7.2.7); zero new deps; 16-PR zero-new-deps streak
- Notification queued in `.pending-notify/` for post-run delivery (Telegram/Discord/Slack)
- Could not run `pytest` directly (sandbox restrictions on python3 invocations) — CI will validate

**Follow-ups:** Tests run on CI; if they fail, will need a follow-up commit. Counterfactual-branch comparison view (diff belief curves across parent + branches via existing `/api/simulation/compare`) is a natural next step.
