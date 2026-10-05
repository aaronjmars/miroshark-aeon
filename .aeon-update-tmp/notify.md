**aeon-update — 2026-10-05**
Synced 71 upstream commits → PR #194.

`aeonfun/aeon` `531f575..1a7f07e`. 312 files applied cleanly (81 new, 231 updated, 5 removed). Catalogs, AGENTS.md, harnesses.json and the eyebrow lock regenerated from the synced tree — every CI gate this PR triggers passes locally (incl. `eyebrow verify` v0.5.6, 0 critical).

Highlights: dashboard Aeon Connect onboarding, `aeon init` + credential manifest, ~52 skill refreshes, new harness-gateway failover + run-context scripts.

26 paths held for you — the big one: upstream tightened the README skill-count validators, but this fork's docs say 85/79 while the catalog is 82. Reconcile the counts by hand, then adopt. Also held: `fetch-tweets`/`shiplog` edits, dashboard/webhook dep bumps, and new skills `feedback-builder`/`compute-resell`.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/194
