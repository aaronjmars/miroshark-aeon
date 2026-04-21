*Agent Self-Improvement — 2026-04-20*

XAI Cache Query Validation — fetch-tweets now refuses to consume a pre-fetched cache that was populated for a different `${var}`. The prefetch script writes a `.xai-cache/fetch-tweets.query` sidecar on success, and the skill's Path A checks it matches the current var before using the cache.

Why: today `fetch-tweets` ran three times. First run returned FETCH_TWEETS_NO_NEW against an empty cache; re-run 1 discovered a stale `$AEON OR @miroshark_ OR github.com/aaronjmars/miroshark` cache (while aeon.yml has long been on `$MIROSHARK OR ...`); only re-run 2 — with a manually-refreshed cache — surfaced 11 new tweets. The skill had no way to detect it was consuming wrong-query cache content.

What changed:
- scripts/prefetch-xai.sh: fetch-tweets branch `rm -f`s the existing cache + sidecar before xai_search, then writes the current $VAR to `.xai-cache/fetch-tweets.query` on success. Failed API call → no cache, instead of stale cache.
- skills/fetch-tweets/SKILL.md: Path A now checks the sidecar matches `${var}` before reading the cache. Mismatch or missing sidecar → fall through to Path B (live X.AI call).

Impact: eliminates the "stale-cache silent failure" mode that burned two fetch-tweets invocations today. Any future `aeon.yml` var change (new token, handle rename) self-heals on the next prefetch cycle instead of requiring manual re-runs.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/19
