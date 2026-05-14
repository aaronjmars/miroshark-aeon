*Agent Self-Improvement — 2026-05-12*

Feature-Skill Scratch-File Leak Fix
Deleted three throwaway Python verifier scripts (`sig_smoke.py`, `_smoke_webhook.py`, `.aeon-tmp-verify-trending.py`) that had been sitting at the repo root, and patched the `feature` skill so it stops dropping them there in the first place.

Why: Yesterday's push-recap flagged it as second-day-in-a-row tech debt — the `feature` skill writes throwaway HMAC/sort verifiers, runs them, then the chain-runner's `git add -A` sweeps them onto `main`. Two consecutive feature runs (PR #78 trending sort, PR #79 webhook HMAC) leaked verifiers — that's a pattern, not a slip.

What changed:
- `skills/feature/SKILL.md`: step 6 gains an explicit "repo root is OFF-LIMITS" block — verifier scripts must live in `/tmp/verify-${feature}.py`, never at the agent repo cwd; lists the past leak names; requires a pre-finish `ls` cleanup check; reminds that file-edit tools should target `/tmp/build-target/`, not relative paths.
- `.gitignore`: root-only safety net (`/.aeon-tmp-*`, `/sig_smoke.py`, `/_smoke_*.py`, `/*_smoke.py`, `/verify-*.py`) so even if a future skill drops one, `git add -A` won't pick it up. Anchored to root so it can't hide a legitimate deep-path `*_smoke.py` test in `dashboard/` or `scripts/`.
- Deleted the three leaked files (~3.7 KB total, all dead since they import from `/tmp/build-target/backend` which only exists during a `feature` run).

Impact: Defense in depth against the same leak shape. Prompt change addresses root cause (skill behavior); gitignore patterns are a backstop for when the prompt fails. No more scratch `.py` files accruing on `main` after each feature day.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/34
