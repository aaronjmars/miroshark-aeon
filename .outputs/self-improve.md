*Agent Self-Improvement — 2026-06-06*

feature skill — decide auth posture upfront

The `feature` skill now explicitly decides whether a new endpoint should be public or auth-guarded *before* writing any code, rather than letting the route default-inherit the auth posture of its sibling endpoints. A new step 7 (between pre-existence grep and implementation) walks through three questions about consumer audience, anonymous-state inference risk, and what the openapi sibling spec says — then locks the wiring decision into the same commit as the route handler.

Why: PR #149 (`/api/status.json`, merged 2026-06-05) shipped with default-inherited `internal_auth_guard`, the drift test caught the docs/code disagreement on CI, and the third squash review-commit had to actively *remove* the auth guard to deliver the documented public-status-probe contract. Yesterday's push-recap flagged this as a self-improve target if the pattern recurred. Today's PR #150 got auth posture right on the first commit only because the operator remembered yesterday's flag — the lesson wasn't yet in the skill prompt, so the next fresh-context run would default-inherit again.

What changed:
- `skills/feature/SKILL.md`: new step 7 with three-question framework (public-by-design consumer? anonymous-callable private inference? openapi siblings?) and a public/private/mixed wiring matrix. Requires a one-line "Auth posture: …" comment near the handler + same line in PR body's Design notes. Subsequent steps renumbered 8→Implement, 9→Branch/Push, 10→PR, 11→Update memory, 12→Notification.
- `memory/logs/2026-06-06.md`: self-improve entry covering rationale + the alternatives considered (separate skill — too granular; `repo-actions` pre-classification — wrong layer; rename step 6 — concept-mixing).
- `memory/MEMORY.md`: Skills Built table row noting the sibling pattern with PR #50 (blocked-features) and PR #52 (pre-existing-features) — same "encode each near-miss into the skill prompt" approach.

Impact: future `feature` runs make the auth-posture call deliberately. Saves one CI cycle + one review-commit per public-by-design endpoint going forward. The existing drift test stays in place as a safety net; the prompt change prevents the disagreement from being introduced upstream of CI.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/53
