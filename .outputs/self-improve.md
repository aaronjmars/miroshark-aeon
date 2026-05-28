*Agent Self-Improvement — 2026-05-28*

Tightened the token-report Grok query so zero-engagement contract-drop spam stops landing in the daily Social Pulse section. The prompt now applies three explicit pre-filters before Grok picks results, and tells it to return zero results rather than fall back to spam on quiet days — the skill's existing Path B already handles the empty case cleanly.

Why: Today's token-report log captured the recurring issue — "All 5 Grok results are spam/bot accounts, 0 engagement. No organic signal. Pattern continues from prior days." Same spam pattern that drove aeon PR #47 (disable fetch-tweets + tweet-allocator) on 2026-05-27. token-report kept consuming the cache and citing scam contract drops as if they were sentiment.

What changed:
- scripts/prefetch-xai.sh (1 line, line 187): replaced the token-report Grok prompt with a version that explicitly drops (1) zero-likes-AND-zero-RT tweets, (2) contract-drop / "vote for" / "fam drop" templates and known clone domains (arbihunter.live, toknsite.live, toknsite.club, coinmarkettcap.fun, *.live/*.club farms), (3) duplicate-template spam across handles. No skill-side change needed — token-report/SKILL.md Path A still parses the same JSON shape.

Impact: Higher signal-to-spam ratio in the daily Social Pulse section; on quiet days the section now degrades cleanly to "X/Grok data unavailable" instead of citing scam links. Tomorrow's 06:00 UTC token-report run validates end-to-end.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/48
