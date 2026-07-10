---
type: Reference
---
# Blocked Features

Ideas that the `repo-actions` skill should NOT regenerate because they have been verified as architecturally blocked by an upstream constraint (missing data-model field, third-party API limit, etc.). Each entry records signature keywords (for exclusion matching), the verifying log, and an "Unblock when" condition so the block can be lifted once upstream changes.

## How this list is used

- **`repo-actions` step 4** reads this file. If a candidate idea matches any entry's signature keywords (case-insensitive substring on the idea title or implementation path), it is excluded from the 5-idea batch and a one-line `Excluded (blocked): <title>` note is added to the article's Selection Rationale section.
- **`feature` step 6** also reads this file. If the picked idea matches a blocked entry, the feature skill skips it and falls through to the next candidate (same path as a pre-existence grep hit).
- **Lifecycle:** when the "Unblock when" condition becomes true (verifiable via grep on the cloned watched repo), remove the entry in the same self-improve / repo-actions run that re-eligibilises the idea.

Each entry: signature keywords, category, reason, verifying log, suggestion history, unblock condition.

## Entries

### Operator Profile
- **Signature keywords:** `operator profile`, `/api/operator`, `/profile/<operator`, `per-operator gallery`, `operator identity layer`
- **Category:** Community / Identity
- **Reason:** `SimulationState` has no `operator` / `created_by` field. `platform_stats.py:42-49` (aaronjmars/MiroShark) explicitly documents that `project_id` is the closest stable identifier — adding `operator` requires an upstream data-model migration threaded through sim creation, persistence, and export. Outside autonomous scope.
- **Verified:** 2026-06-02 by `feature` skill (memory/logs/2026-06-02.md — pivoted from Operator Profile to Agent Persona Export after grep confirmed the missing field).
- **Suggestion history:** appeared in 13 `articles/repo-actions-*.md` files between 2026-05-08 and 2026-06-01 (May 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, Jun 1). Re-eligible from May-16 #5 / May-22 #1-equivalent / May-24 #3.
- **Unblock when:** upstream `SimulationState` (or equivalent persisted sim record) gains an `operator` / `created_by` field. Verify via `gh api repos/aaronjmars/MiroShark/contents/backend/app/models/simulation_state.py` (or the current state file path) and grep for `operator` / `created_by` as a top-level field. Once the field lands, delete this entry — the idea returns to the eligible pool.
