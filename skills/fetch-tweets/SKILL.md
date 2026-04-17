---
name: Fetch Tweets
description: Search X/Twitter for tweets about a token, keyword, username, or topic
var: ""
tags: [social]
---
> **${var}** — Search query for X/Twitter. **Required** — set your query in aeon.yml.

Today is ${today}. Search X for tweets matching **${var}**.

## Steps

1. **Load previously-reported tweet URLs** from two sources, then union them into `SEEN_TWEETS`:
   - **Persistent seen-file** (`memory/fetch-tweets-seen.txt`) — if it exists, read all URLs. This file contains every tweet URL ever reported, preventing stale tweets from cycling back into notifications once log entries age out of the 3-day window.
   - **Last 3 days of `memory/logs/`** — grep each log file for lines matching `https://x.com/` (catches URLs not yet in the seen-file).
   
   You'll use `SEEN_TWEETS` in step 5 to filter duplicates.

2. **Build the search prompt for Grok.** Pass `${var}` to Grok **verbatim** as the search query. Do NOT narrow it to a single angle (e.g. don't force "crypto token only", don't inject a contract address, don't filter by chain). Let Grok interpret OR/AND operators in the var as-is. The goal is broad coverage — token mentions, repo mentions, handle mentions, general chatter, all of it.

3. **Search tweets.** Use whichever path is available:

   **Path A — pre-fetched cache** (preferred, when the workflow ran `scripts/prefetch-xai.sh`):
   ```bash
   cat .xai-cache/fetch-tweets.json 2>/dev/null | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

   **Path B — X.AI API** (fallback, use when `XAI_API_KEY` is set and cache is empty):
   ```bash
   FROM_DATE=$(date -u -d "yesterday" +%Y-%m-%d 2>/dev/null || date -u -v-1d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for ALL tweets about: ${var}. Date range: '"$FROM_DATE"' to '"$TO_DATE"'. Return at least 10 tweets (more if available) — prioritize the most interesting, insightful, or highly-engaged posts but also include smaller accounts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."}],
       "tools": [{"type": "x_search"}]
     }'
   ```
   Parse the response JSON to extract the text from the output array:
   ```bash
   echo "$RESPONSE" | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

   **Path C — WebSearch fallback** (use when both cache and XAI_API_KEY are unavailable):
   Use the built-in WebSearch tool to search for recent tweets. Construct a query like:
   `site:x.com "${query_terms}" after:${FROM_DATE}`
   Note at the top of the log entry: "XAI_API_KEY not available; results compiled via WebSearch". WebSearch rankings favour high-engagement older tweets — **prioritise results that mention a date within the last 48 hours** when possible.

4. **If no relevant tweets found** (no results, API error, or empty): log "FETCH_TWEETS_EMPTY" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

5. **Deduplicate against `SEEN_TWEETS` from step 1.** Compare each candidate tweet URL against the collected set of already-reported URLs. Remove any tweet that was already reported in the last 3 days. If ALL tweets found are already in the recent logs: log "FETCH_TWEETS_NO_NEW: all results already reported" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

6. **Save the results** (new tweets only) to `memory/logs/${today}.md`. Include the tweet URLs, handles, and engagement so future runs can deduplicate and so downstream skills (like `tweet-allocator`) can consume them.

6b. **Update the persistent seen-file** — append each new tweet URL (one per line) to `memory/fetch-tweets-seen.txt`. Create the file if it doesn't exist. This ensures these URLs are excluded from all future runs, regardless of log rotation.

7. **Send a notification via `./notify`** with up to 10 NEW tweets (those that survived dedup). Each tweet MUST include a clickable link. Use Telegram Markdown link format: `[link text](url)`.

   Format the notification like this:
   ```
   *Top Tweets — ${var} (${today})*

   1. x.com/handle — [brief summary of tweet content]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   2. x.com/handle — [brief summary]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   ... (up to 10 tweets)
   ```

   IMPORTANT: Do NOT use @handle format — it tags/pings users on Telegram. Use x.com/handle instead (shows the profile URL without tagging anyone). The `[View tweet](URL)` link is required so users can tap to open each tweet.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (optional; skill falls back to WebSearch when not set, but quality is lower)
