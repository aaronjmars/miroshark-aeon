---
name: fetch-tweets
description: Search X/Twitter for tweets about a token, keyword, username, or topic
var: ""
---
> **${var}** — Search query for X/Twitter. **Required** — set your query in aeon.yml.

Today is ${today}. Search X for tweets matching **${var}**.

## Steps

1. **Build the search prompt for Grok.** The prompt sent to Grok must be specific enough to get relevant results:
   - If the query mentions a token/cashtag/crypto: include "crypto token", the chain name, and the contract address from `memory/MEMORY.md` in the Grok prompt. This eliminates false matches.
   - Example: instead of searching "aeon", search "the $AEON crypto token on Base chain (contract 0xbf8e...) in the last 7 days. Only return tweets about the cryptocurrency."

2. **Load previously-reported tweet URLs** from the last 3 days of `memory/logs/`. Grep each log file for lines that match `https://x.com/` — collect all tweet URLs already reported. You'll use these to filter duplicates in step 4.

3. **Search tweets.** Use whichever path is available:

   **Path A — X.AI API** (preferred, use when `XAI_API_KEY` is set):
   ```bash
   FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "YOUR_SEARCH_PROMPT_HERE. Date range: '"$FROM_DATE"' to '"$TO_DATE"'. Return 10 tweets — prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."}],
       "tools": [{"type": "x_search"}]
     }'
   ```
   Parse the response JSON to extract the text from the output array:
   ```bash
   echo "$RESPONSE" | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

   **Path B — WebSearch fallback** (use when `XAI_API_KEY` is NOT set):
   Use the built-in WebSearch tool to search for recent tweets. Construct a query like:
   `site:x.com "${query_terms}" after:${FROM_DATE}`
   Note at the top of the log entry: "XAI_API_KEY not available; results compiled via WebSearch". WebSearch rankings favour high-engagement older tweets — **prioritise results that mention a date within the last 48 hours** when possible.

4. **Deduplicate against previously-reported tweets** (from step 2):
   - Compare each candidate tweet URL against the collected set of already-reported URLs.
   - Remove any tweet that was already reported in the last 3 days.
   - If ALL tweets found are already in the recent logs: log "FETCH_TWEETS_NO_NEW: all results already reported" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

5. **If no relevant tweets found** (no results, API error, or empty after dedup): log "FETCH_TWEETS_EMPTY" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

6. **Save the results** (new tweets only) to `memory/logs/${today}.md`.

7. **Send a notification via `./notify`** with the top NEW tweets. Each tweet MUST include a clickable link. Use Telegram Markdown link format: `[link text](url)`.

   Format the notification like this:
   ```
   *Top Tweets — ${var} (${today})*

   1. x.com/handle — [brief summary of tweet content]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   2. x.com/handle — [brief summary]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   3. x.com/handle — [brief summary]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   ... (up to 5 tweets)
   ```

   IMPORTANT: Do NOT use @handle format — it tags/pings users on Telegram. Use x.com/handle instead (shows the profile URL without tagging anyone). The `[View tweet](URL)` link is required so users can tap to open each tweet.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (optional; skill falls back to WebSearch when not set, but quality is lower)
