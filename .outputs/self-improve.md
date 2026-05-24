*Agent Self-Improvement — 2026-05-24*

bankr-prefetch EXIT-trap crash sidecar — scripts/prefetch-bankr.sh now stamps a 'crashed' status to .bankr-cache/prefetch-status.json whenever the script exits non-zero before reaching a normal write_status call, and skills/tweet-allocator/SKILL.md has a new 'crashed' branch in its status switch that surfaces the exit code in its alert message.

Why: today's tweet-allocator run logged TWEET_ALLOCATOR_ERROR — prefetch-bankr.sh did not run; .bankr-cache/prefetch-status.json is missing and fired a workflow-misconfiguration alert. The workflow does invoke the script — but set -euo pipefail can exit silently if any early jq/grep pipeline bails before reaching write_status. With no sidecar written, the skill couldn't tell 'workflow misconfigured' (file truly absent) from 'script crashed mid-run' (silent failure) — so the alert pointed at the wrong root cause.

What changed:
- scripts/prefetch-bankr.sh: trap ... EXIT registered after mkdir -p .bankr-cache; fires only when $? != 0 AND prefetch-status.json is absent. Writes {status: 'crashed', exit_code: N, note, timestamp} via jq. Normal exits (which always call write_status) untouched. Non-tweet-allocator early exit happens before the trap registers, so unrelated skills still skip cleanly.
- skills/tweet-allocator/SKILL.md: new 'crashed' branch in the status switch with its own alert message (exit code surfaced via the note field); Status flags section updated.

Impact: next silent prefetch crash produces an actionable diagnostic (exit code + timestamp) instead of a misleading 'workflow misconfigured' alert. The truly-absent-file case still falls through to the original missing-file branch.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/45
