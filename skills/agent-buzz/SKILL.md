---
name: Agent Buzz
description: Top 10 tweets by influence mentioning AI agents
var: ""
tags: [social]
---
> **${var}** — Specific project or topic to prioritize in the search (e.g. "MyProject", "MCP protocol"). If empty, searches AI agents broadly.

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating tweets.

## Steps

1. Search X for high-engagement tweets about AI agents using the X.AI API:
   ```bash
   FROM_DATE=$(date -u -d "2 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-2d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)

   # Search AI agents broadly
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for the most viral and influential tweets from '"$FROM_DATE"' to '"$TO_DATE"' mentioning AI agents, autonomous agents, agent frameworks, agent protocols, or agentic AI. Rank by influence — prioritize accounts with large followings, high engagement (likes, retweets, quote tweets), and people who are builders/founders/researchers in the space. Return the top 15 tweets. For each: @handle, follower count if visible, a one-line summary of what they said, engagement stats if available, and the direct link (https://x.com/username/status/ID)."}],
       "tools": [{"type": "x_search", "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
     }'
   ```

   If `${var}` is set, also search for that specific project/topic and prioritize those results:
   ```bash
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for all tweets from '"$FROM_DATE"' to '"$TO_DATE"' mentioning '"${var}"'. Return every tweet you find with @handle, summary, engagement, and direct link (https://x.com/username/status/ID)."}],
       "tools": [{"type": "x_search", "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
     }'
   ```

   If `XAI_API_KEY` is not set or the curl command fails (sandbox blocking, network errors), fall back to WebSearch. **IMPORTANT:** Always include "today" or "past 24 hours" and the current date in your search query to force fresh results — e.g. `"AI agents twitter today ${today}"`. Discard any results older than 48 hours. Summarize what you find.

2. Merge both result sets (if `${var}` was searched). Deduplicate against recent logs. Rank by influence:
   - Follower count / account credibility (builders > commentators > anons)
   - Engagement (likes, RTs, quote tweets)
   - Substance (actual insight > hype > shilling)

3. Pick the top 10 tweets.

4. Send via `./notify` (under 4000 chars):
   ```
   *Agent Buzz — ${today}*

   1. @handle — one-line summary
      [link](https://x.com/...)

   2. @handle — one-line summary
      [link](https://x.com/...)

   ...
   ```

5. Log to memory/logs/${today}.md.
   If nothing found, log "AGENT_BUZZ_OK" and end.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables Required
- `XAI_API_KEY` — X.AI API key for Grok x_search
