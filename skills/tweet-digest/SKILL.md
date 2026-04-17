---
name: Tweet Digest
description: Aggregate and summarize tweets from tracked accounts
var: ""
tags: [social]
---
> **${var}** — Account or topic to filter by. If empty, checks all tracked accounts.

If `${var}` is set, filter tweets by that account or topic.


Read memory/MEMORY.md for context and tracked Twitter/X accounts.
Read the last 2 days of memory/logs/ to avoid repeating items.

Steps:
1. For each account listed under "Tracked X Accounts" in MEMORY.md, fetch recent tweets:
   ```bash
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for the latest tweets from:USERNAME in the last 3 days. Return the 5 most interesting or substantive tweets. For each: full text, date, direct link (https://x.com/USERNAME/status/ID). Skip retweets of others."}],
       "tools": [{"type": "x_search"}]
     }'
   ```
   If `XAI_API_KEY` is not set, skip and log that the skill requires it.

2. Group tweets by theme or topic, not by account.
3. Write a 1-sentence take on each notable tweet.
4. Format and send via `./notify` (under 4000 chars):
   ```
   *Tweet Digest — ${today}*

   *Theme: topic*
   @handle: summary — [link](url)
   @handle: summary — [link](url)
   ```
5. Log the digest to memory/logs/${today}.md.
If no notable tweets found, log "TWEET_DIGEST_OK" and end.

## Environment Variables Required
- `XAI_API_KEY` — X.AI API key for Grok x_search
