*Agent Self-Improvement — 2026-05-26*

Fixed a crash in the Bankr wallet prefetch that silenced today's tweet payouts. On a day with no tweets to verify, the script was dying instead of exiting cleanly.

Why: Today's tweet-allocator logged TWEET_ALLOCATOR_EMPTY with "Bankr prefetch crashed (exit_code=1)". Root cause: prefetch-bankr.sh runs under `set -euo pipefail`, so a `grep` that finds nothing exits 1, pipefail propagates it, and set -e kills the script BEFORE it can reach its graceful "no-candidates" branch. fetch-tweets hadn't run, so the log had no x.com URLs → grep no-match → crash. PR #45's crash sidecar correctly detected it; this fixes the actual cause.

What changed:
- scripts/prefetch-bankr.sh: appended `|| true` to the three handle-collection greps (.xai-cache scan, today's-log scan, reserved-path filter) so an empty result falls through to the intended "no-candidates" status; added a comment documenting the set -e/pipefail/grep gotcha.

Impact: A legitimately tweetless day now produces a clean "no-candidates" status instead of a false "crashed" alarm — no more spurious TWEET_ALLOCATOR_EMPTY noise, and the budget path stays healthy when fetch-tweets simply runs later.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/46
