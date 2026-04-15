---
name: Vibecoding Digest
description: Monitor r/vibecoding for trending posts, interesting discussions, and notable projects shipped
var: ""
tags: [content]
---
> **${var}** — Time window: "day" (default), "week", or "month". Controls the Reddit top sort period.

Read `memory/MEMORY.md` for context.
Read the last 2 days of `memory/logs/` to avoid repeating posts already covered.

## Data Source

Reddit JSON API (no auth required). Append `.json` to any Reddit URL.

Key endpoints:
- `https://www.reddit.com/r/vibecoding/top.json?t=day&limit=25` — top posts by score in time window
- `https://www.reddit.com/r/vibecoding/hot.json?limit=25` — currently hot (trending) posts
- `https://www.reddit.com/r/vibecoding/comments/{post_id}.json` — post detail + comments

**Important:** Always include header `User-Agent: aeon-bot/1.0` or Reddit will 429 you.

Each post object (at `data.children[].data`) contains:
- `title` — post title
- `selftext` — post body (markdown)
- `score` — net upvotes
- `num_comments` — comment count
- `upvote_ratio` — 0.0–1.0 (below 0.70 = controversial)
- `author` — username
- `created_utc` — unix timestamp
- `permalink` — relative URL (prepend `https://reddit.com`)
- `link_flair_text` — post flair/category
- `url` — linked URL if it's a link post

## Steps

### 1. Fetch trending posts

Pull both top and hot to get full picture:

```bash
TIME_WINDOW="${var:-day}"

# Top posts by score
curl -s -H "User-Agent: aeon-bot/1.0" \
  "https://www.reddit.com/r/vibecoding/top.json?t=$TIME_WINDOW&limit=25" > /tmp/vc_top.json

# Currently hot posts (may surface rising posts not yet in top)
curl -s -H "User-Agent: aeon-bot/1.0" \
  "https://www.reddit.com/r/vibecoding/hot.json?limit=25" > /tmp/vc_hot.json
```

### 2. Merge and dedupe

Combine top + hot results. Dedupe by post ID. Skip pinned/stickied posts (`stickied: true`).

### 3. Categorize and pick the best

Sort posts into buckets:

**Ship posts** — someone built and shipped something ("I built", "I shipped", "my app", "launched")
- These are the pulse of the sub. Note what they built, what stack, user count if mentioned.

**Discussion / hot takes** — opinion posts, debates, meta-commentary
- Low upvote_ratio (<0.70) = controversial = interesting
- High comment count relative to score = heated debate

**Memes / culture** — humor, screenshots, relatable content
- High score + high upvote_ratio = the sub's vibe distilled

**Resource / tutorial** — guides, tools, workflows shared
- Look for links, Claude Code setups, prompt strategies, tool recommendations

**Select 5-8 most notable posts** across categories. Prioritize:
1. Highest score (the sub voted — respect that)
2. Most comments (active discussion = signal)
3. Controversial (low ratio + many comments = spicy)
4. Anything directly relevant to AI coding, Claude, agents, shipping fast

### 4. For top 3 posts, fetch comments

For the 3 most interesting posts (highest comments or most controversial), fetch the comment thread:

```bash
# post_id is the alphanumeric ID from the permalink
curl -s -H "User-Agent: aeon-bot/1.0" \
  "https://www.reddit.com/r/vibecoding/comments/$POST_ID.json?sort=top&limit=10"
```

Response is an array of two listings:
- Index 0: the post itself
- Index 1: comments (`data.children[].data` — each has `body`, `author`, `score`, `replies`)

Pick the **2-3 best comments** per post: sharpest take, funniest reply, most useful advice.

### 5. Build the digest

```
## Vibecoding Digest — ${today}

### Top Posts

1. **[title]** — u/author (score pts, N comments, ratio%)
   [one-line summary of what it's about and why it matters]
   https://reddit.com/r/vibecoding/...

2. **[title]** — u/author (score pts, N comments)
   [summary]

... (5-8 posts)

### Spicy Threads

**"[post title]"** (N comments, ratio%)
- u/commenter: "[interesting comment excerpt]"
- u/commenter: "[interesting comment excerpt]"

**"[post title]"** (N comments)
- u/commenter: "[comment excerpt]"

### Vibes
[2-3 sentences on the overall mood of the sub today. What are vibecoding people excited about? Worried about? Shipping? Arguing about?]
```

### 6. Notify

Send via `./notify`:
```
r/vibecoding — ${today}

top posts:
1. "[title]" — X pts, N comments
2. "[title]" — X pts, N comments
3. "[title]" — X pts, N comments

spicy: "[controversial post title]" (ratio% upvoted, N comments)
best comment: "[excerpt]" — u/author

vibes: [one-line mood summary]
```

### 7. Log

Append to `memory/logs/${today}.md`:
```
## Vibecoding Digest
- **Posts scanned:** N
- **Top post:** "[title]" — X score, N comments
- **Most controversial:** "[title]" — ratio% upvoted
- **Themes:** theme1, theme2, theme3
- **Vibes:** [one-line]
- **Notification sent:** yes
```

If any post contains a strong take or insight relevant to topics tracked in MEMORY.md, note it there.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
