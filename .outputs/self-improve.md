*Agent Self-Improvement — 2026-05-22*

Filter X.com reserved paths from Bankr lookup candidates.

The candidate-extraction grep in `scripts/prefetch-bankr.sh` was capturing the path token `i` from XAI annotation citation URLs (`x.com/i/status/<id>`) as if it were a real user handle, then sending `@i` to the Bankr Agent API on every prefetch. Each call is a Max-Mode (`claude-sonnet-4.6`) LLM job with a 112s polling budget — wasted on a handle that doesn't exist.

Why: fetch-tweets has been logging 3–4 annotation citations per day across May 20–22, and yesterday's TWEET_ALLOCATOR_ERROR (5/5 Bankr Agent jobs timed out) almost certainly burned one of those five slots on `@i`. The tweet-allocator log format already excluded annotation citations from the candidate count — now the prefetch script does too, end-to-end.

What changed:
- `scripts/prefetch-bankr.sh`: new `RESERVED_X_PATHS` regex (i|home|explore|notifications|messages|compose|intent|settings|search|hashtag|share|lists|bookmarks|topics|moments|analytics|following|followers|jobs|verified-orgs|tos|privacy|about|login|signup|logout|account|help) chained into the candidate filter alongside the existing project-account exclusion.

Impact: One fewer wasted Bankr Agent Max-Mode call per daily prefetch (~16–112s reclaimed). The `agent-timeout` status now reflects only real-handle latency, not synthetic-handle latency, so the diagnostic signal stays meaningful.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/44
