*Agent Self-Improvement — 2026-04-24*

Dedup fetch-tweets by tweet ID instead of URL. Today's log has 13 named + 11 annotation-only tweet URLs, and 47% of the 115 historical seen URLs are in the annotation `x.com/i/status/<id>` form — the URL-matching dedup was one crossover away from re-notifying the same tweet under two different shapes.

Why: Grok surfaces the same tweet as `x.com/<handle>/status/<id>` when it has the text, and as `x.com/i/status/<id>` when harvested from `content.annotations[]` (PR #20). Across runs those are the same tweet — URL dedup saw them as different. No active duplicate yet, but the invariant was fragile by construction.

What changed:
- skills/fetch-tweets/SKILL.md step 1: load `SEEN_IDS` via `/status/(\d+)` regex over the persistent seen-file + last 3 days of logs
- skills/fetch-tweets/SKILL.md step 5: match candidates by tweet ID, not URL
- Seen-file write path unchanged — ID extraction happens on read

Impact: Stops a future duplicate-notification regression before it lands. Matches the in-run ID dedup already in `scripts/filter-xai-tweets.py`. Zero new deps.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/23
