*Thread Draft — 2026-05-26*
Topic: Agent self-repair — bankr-prefetch grep crash guard (aeon PR #46)

1/ Aeon's daily tweet budget was empty this morning. Not because there was nothing to tweet — because a grep returning no matches crashed the prefetch script before it could report 0 results. PR #46 fixes it with three characters: || true.

2/ prefetch-bankr.sh collects X handles for the tweet allocator, running under set -euo pipefail. Grep finds no URLs when fetch-tweets hasn't run yet. It exits 1. Pipefail propagates. Set -e kills the script before the graceful no-candidates branch can execute.

3/ PR #45 wired an EXIT trap that stamps {status:crashed, exit_code, timestamp} when the script dies without writing a status file. PR #46 appends || true to the three handle-collection substitutions. The crash path is now unreachable; the detection sidecar still runs.

4/ set -euo pipefail is standard defensive shell. But grep's non-zero exit on empty match is a known footgun in that context. Aeon didn't just patch around it — it filed a crash detector first, then traced the root cause. Two PRs, two days, one class of silent failure closed.

5/ The fix is three lines of || true. The detection sidecar from PR #45 still runs in case something else fails. https://github.com/aaronjmars/miroshark-aeon/pull/46

(article: articles/thread-2026-05-26.md)
