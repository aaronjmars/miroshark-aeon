---
name: Remix Tweets
description: Fetch 10 random past tweets from your account and craft 10 new rephrased versions in your voice
var: ""
tags: [social]
---
> **${var}** — Override time window (e.g. "180d", "1y"). Defaults to 30-180 days ago. Can also be a specific date range like "2025-06-01:2025-09-01".

Read `memory/MEMORY.md` for context on current topics and recent thinking.
Read the last 3 days of `memory/logs/` to avoid remixing tweets that were already remixed recently.

## Voice

If a `soul/` directory exists, read the soul files for voice calibration:
1. `soul/SOUL.md` — identity, worldview, opinions
2. `soul/STYLE.md` — writing style, sentence structure, anti-patterns
3. `soul/examples/tweets.md` — rhythm and tone calibration (if present)

Otherwise, match the tone of recent tweets fetched in step 1.

## Steps

### 1. Fetch older tweets

Pull 10 tweets from your account that are at least 30 days old. Default window is 30-180 days ago — we want forgotten posts worth resurfacing, not recent stuff.

**First, check for pre-fetched data** (the workflow pre-fetches XAI results outside the sandbox):
- Read `.xai-cache/remix-tweets.json` — if it exists and contains results, use that data. Extract the tweet list from the response.

**If no cache file exists**, try the direct API call:
```bash
# Parse time window
TIME_WINDOW="${var:-180d}"

if echo "$TIME_WINDOW" | grep -q ':'; then
  FROM_DATE=$(echo "$TIME_WINDOW" | cut -d: -f1)
  TO_DATE=$(echo "$TIME_WINDOW" | cut -d: -f2)
else
  DAYS=$(echo "$TIME_WINDOW" | sed 's/[^0-9]//g')
  UNIT=$(echo "$TIME_WINDOW" | sed 's/[0-9]//g')
  if [ "$UNIT" = "y" ]; then
    DAYS=$((DAYS * 365))
  fi
  FROM_DATE=$(date -u -d "$DAYS days ago" +%Y-%m-%d 2>/dev/null || date -u -v-${DAYS}d +%Y-%m-%d)
  # End date is 30 days ago — skip recent tweets
  TO_DATE=$(date -u -d "30 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-30d +%Y-%m-%d)
fi

# Replace YOUR_HANDLE with your X handle
curl -s -X POST "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "Search X for original tweets (not replies, not retweets) posted by @YOUR_HANDLE from '"$FROM_DATE"' to '"$TO_DATE"'. I want a diverse sample — mix of topics, tones, and engagement levels. Return exactly 10 tweets. For each: the full tweet text, date posted, engagement stats (likes, retweets, replies), and the direct tweet link (https://x.com/YOUR_HANDLE/status/ID). Return as a numbered list."}],
    "tools": [{"type": "x_search", "allowed_x_handles": ["YOUR_HANDLE"], "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
  }'
```

If neither cache nor direct API works, skip and log that the skill requires XAI data.

### 2. Filter the 10 tweets

From the results, keep only tweets that:
- Are original posts (not replies or RTs)
- Haven't been remixed in recent logs
- Cover a diverse spread of topics

### 3. Remix each tweet

For each of the 10 selected tweets, write a **new tweet** that:
- Captures the same core idea or take
- Uses **different words, different angle, different framing**
- Is NOT a minor paraphrase — it should feel like a fresh tweet about the same insight
- Matches your current voice (from soul files or recent tweets)
- Could stand on its own — someone shouldn't recognize it as a remix
- Stays within 280 characters (standard tweet length)

### Remix strategies (vary across the 10)
- **Sharpen** — the original was good but wordy. Compress the take into a one-liner.
- **Flip the frame** — same insight, but approached from the opposite direction.
- **Update** — the take still holds but the world has changed. Ground it in today's context.
- **Escalate** — the original was mild. Make it spicier.
- **Soften** — the original was a hot take. Restate it as an observation that leads the reader there.
- **Concretize** — the original was abstract. Add a specific example or data point.
- **Abstract** — the original was specific. Zoom out to the general principle.

### Voice rules
- Write in first person.
- Short sentences. Em dashes over commas. No semicolons.
- State the opinion first, reasoning after (if any).
- No hedging. No corporate voice. No hashtags. No emojis.
- Each remix must pass the test: would you actually post this?

## Output & Notify

Send all 10 via `./notify` (under 4000 chars). No indentation on any line:
```
*Remix Tweets — ${today}*

1. *[strategy]*
[original tweet excerpt] → [remix]

2. *[strategy]*
[original tweet excerpt] → [remix]

... (all 10)
```

## Log

Append to `memory/logs/${today}.md`:
```
## Remix Tweets
- **Source window:** FROM_DATE to TO_DATE
- **Remixes generated:** N
- **Original tweets fetched:**
  1. "tweet text excerpt" — @HANDLE, DATE (URL)
  2. ...
  (all 10)
```

Save the fetched original tweets to memory so other skills (article, write-tweet) can reference them as source material.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables Required
- `XAI_API_KEY` — X.AI API key for Grok x_search
