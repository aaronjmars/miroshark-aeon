*Agent Self-Improvement — 2026-04-16*

Persistent tweet dedup for fetch-tweets — stale tweets no longer cycle back into notifications.

The fetch-tweets skill was using a 3-day log window for deduplication, but WebSearch (the fallback when XAI_API_KEY is unavailable) favors high-engagement older tweets. Once a log entry aged past 3 days, the same launch-era tweets would resurface. The Apr 16 run showed this clearly: all but one surfaced URL were stale content already reported weeks ago.

Why: Apr 16 fetch-tweets log showed 7+ stale tweet URLs being re-evaluated because they fell outside the 3-day dedup window despite being reported in Apr 11-12 logs.

What changed:
- skills/fetch-tweets/SKILL.md: Added persistent seen-file (memory/fetch-tweets-seen.txt) as primary dedup source. New step 6b appends URLs after each run. 3-day log scan kept as fallback.
- memory/fetch-tweets-seen.txt (new): Seeded with all 24 unique tweet URLs from existing logs — takes effect immediately.

Impact: Eliminates redundant stale-tweet notifications entirely. The skill will only report genuinely new tweets, improving signal quality especially in WebSearch-fallback mode.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/15
