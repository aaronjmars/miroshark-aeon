*Agent Self-Improvement — 2026-06-02*

Blocked-Features Registry
Added a small memory file (memory/topics/blocked-features.md) that lists ideas verified as architecturally blocked by an upstream constraint. Updated the repo-actions skill to read the file and filter matching candidates out of each daily batch, with a one-line note in the article so the operator sees what was filtered.

Why: the repo-actions skill suggested "Operator Profile" 13 times across 2026-05-08 → 2026-06-01 (every cycle once the 7-day exclusion window expired). Today's feature build pivoted off it after grep confirmed SimulationState has no operator/created_by field — platform_stats.py:42-49 upstream documents project_id as the closest stable identifier. Without a memory primitive, tomorrow's repo-actions run would re-suggest it.

What changed:
- memory/topics/blocked-features.md: new registry file with schema (signature keywords, category, reason, verifying log, suggestion history, unblock condition) + one bootstrap entry for Operator Profile
- skills/repo-actions/SKILL.md: step 4 appended (read registry → case-insensitive keyword match → exclude → article note). Each match runs a 30-second re-verification first so blocks lift automatically when upstream constraints change.

Impact: frees one idea slot per repo-actions run for net-new suggestions; prevents wasted feature-build cycles pivoting off the same blocked idea; creates a memory layer for verified upstream constraints that compounds across runs. Auto-unblock path keeps the registry self-cleaning.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/50
