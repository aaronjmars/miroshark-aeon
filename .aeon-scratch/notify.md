**aeon-update — 2026-09-21**
Synced 19 upstream commits → PR #181.

Upstream `aeonfun/aeon` was 19 commits ahead (`95142d1..ba01e9f`). Applied **47 files clean** (15 added, 31 updated, 1 auto-merged) + regenerated catalogs. Baseline advances to `ba01e9f` on merge.

Two new skills landed clean: **`sc-audit`** (deep smart-contract audit) and **`create-prove`** — pulled the eyebrow v0.4.2 binary in-run (the version CI actually verifies with, not the v0.4.3 in the action comment), so the lock covers them and CI stays green. Rest of the window is upstream's dev-loop hardening stack (live proof + verified repair + telegram ship route).

**5 need a hand** (in the PR): `aeon.yml` workflow + `ci-tests.yml` (your env/test-list narrowing), `.github/README.md` (I bumped the 80→82 skill count to keep CI green; the upstream rewrite still needs merging), `docs/skill-packs.md`, and `miroshark-matchday` (upstream added a vertical 9:16 render — clean +2 to graft). 14 older conflicts still carried forward.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/181
