*Push Recap — 2026-06-03*
aaronjmars/MiroShark — 6 substantive commits by 3 authors. aaronjmars/miroshark-aeon — 1 substantive commit (cron churn excluded).

**Ecosystem-as-a-contract finished its arc.** The ECOSYSTEM.md registry got a logo column (and lost dormant Nookplot+Supercompact rows), got linked from README in en+zh, gained Capacitr and Sparkleware, and — most consequentially — gained a machine-readable JSON twin at `GET /api/ecosystem.json` (PR #145, Aeon-built, +953/-19 across 10 files). `surfaces.json` and `ecosystem.json` now share one blueprint with identical ETag+cache posture — the platform exposes both meta-questions a new integrator hits ('what can I call?' / 'who else is built on this?') as twin JSON catalogs.

**Drift guard saved itself within an hour.** PR #144 (sparkleware adding their own ECOSYSTEM.md row) merged 52 min after PR #145 — immediately breaking the catalog/Markdown sync the new tests guard. PR #146 closed the gap 5 minutes later. First live save of the design choice to hardcode rather than parse Markdown.

**Aeon learned to forget on purpose (PR #50).** `repo-actions` had suggested Operator Profile 13 times across May 8 → Jun 1. New `memory/topics/blocked-features.md` registry + a 30-sec upstream re-verify on each match means the idea is filtered out until `SimulationState` gains an `operator` field — at which point the entry self-deletes and the idea returns to the pool.

Key changes:
- PR #145 `backend/app/services/ecosystem_catalog.py` — 263 lines pure stdlib, literal list of 13 dicts, 5 categories, drift-guarded
- PR #143 ECOSYSTEM.md visual rebuild — logo column added, Nookplot+Supercompact dropped, every row now has a 40px image
- PR #50 `memory/topics/blocked-features.md` — schema + Operator Profile bootstrap entry, signature-keyword matching, auto-unblock condition

Stats: ~12 files changed, +1,003 / -36 across 7 substantive commits
Open PRs at window close: 0/0 (both ledgers cleared)
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-03.md
