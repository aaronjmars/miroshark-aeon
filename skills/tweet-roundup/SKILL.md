---
name: Tweet Roundup
description: Gist of the latest tweets on configurable topics
var: ""
tags: [social]
---
> **${var}** — Topic or search query to focus on (e.g. "solana", "brain-computer interfaces", "@elonmusk"). If empty, uses default topics (configurable in MEMORY.md).

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating items.

## Steps

1. Search X for the latest chatter. If `${var}` is set, search for that specific topic instead of the defaults.

   **Default topics** (used when `${var}` is empty and no topics configured in MEMORY.md under a "Tweet Roundup Topics" section):
   - `artificial intelligence OR AI agents OR LLM`
   - `crypto OR bitcoin OR DeFi`
   - `technology OR startups OR open source`

   Users can customize default topics in MEMORY.md under a "Tweet Roundup Topics" section.

   **First, check for pre-fetched data** (the workflow pre-fetches XAI results outside the sandbox):
   - If `${var}` is set: read `.xai-cache/roundup-var.json`
   - Otherwise: read `.xai-cache/roundup-*.json` files matching your configured topics
   - If cache files exist and contain results, use that data. Extract the tweet lists from each response.

   **If no cache files exist**, try the direct API call:
   ```bash
   FROM_DATE=$(date -u -d "yesterday" +%Y-%m-%d 2>/dev/null || date -u -v-1d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)

   # If ${var} is set, use: TOPICS=("${var}")
   # Otherwise use the default topics listed above
   for TOPIC in \
     "artificial intelligence OR AI agents OR LLM" \
     "crypto OR bitcoin OR DeFi" \
     "technology OR startups OR open source"; do
     curl -s -X POST "https://api.x.ai/v1/responses" \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer $XAI_API_KEY" \
       -d '{
         "model": "grok-4-1-fast",
         "input": [{"role": "user", "content": "Search X for the latest popular tweets about: '"$TOPIC"' from '"$FROM_DATE"' to '"$TO_DATE"'. Return the 3-5 most interesting or viral tweets. IMPORTANT: For each tweet you MUST include: 1) the @handle of the person who tweeted, 2) a one-line summary of what they said, 3) the actual tweet permalink in the format https://x.com/username/status/ID — NOT the URL of any article they linked to. I want the tweet URL itself, not news article URLs. If you cannot find the exact tweet URL, still include the @handle and note the tweet link is unavailable."}],
         "tools": [{"type": "x_search", "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
       }'
   done
   ```
   If neither cache nor direct API works, fall back to WebSearch for each topic. **IMPORTANT:** Always include "today" or "past 24 hours" and the current date in your search query to force fresh results — e.g. `"crypto twitter today ${today}"`. Discard any results older than 48 hours. Summarize the top 3-5 results per topic.

2. For each topic, write 2-3 bullet points capturing the gist — what people are talking about, any big news, notable takes. Every bullet MUST attribute to a specific @handle and link to the actual tweet (x.com/user/status/ID). Do NOT link to news articles — link to the tweet discussing them. If a tweet URL is unavailable, still include the @handle.

3. Send via `./notify` (under 4000 chars):
   ```
   *Tweet Roundup — ${today}*

   *[Topic 1]*
   - @handle: gist (https://x.com/handle/status/ID)
   - ...

   *[Topic 2]*
   - @handle: gist (https://x.com/handle/status/ID)
   - ...

   *[Topic 3]*
   - @handle: gist (https://x.com/handle/status/ID)
   - ...
   ```

4. Log to memory/logs/${today}.md.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
