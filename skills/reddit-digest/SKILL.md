---
name: Reddit Digest
description: Fetch and summarize top Reddit posts from tracked subreddits
var: ""
tags: [news]
---
> **${var}** — Topic filter or subreddit name. If empty, checks all tracked subreddits.

If `${var}` is set, only check that subreddit or filter posts by that topic.


## Config

This skill reads subreddits from `memory/subreddits.yml`. If the file doesn't exist yet, create it or skip this skill.

```yaml
# memory/subreddits.yml
subreddits:
  - name: r/ExampleSub
    subreddit: ExampleSub
  - name: r/AnotherSub
    subreddit: AnotherSub
```

---

Read memory/MEMORY.md for tracked topics and interests.
Read memory/subreddits.yml for the list of subreddits to monitor.
Read the last 2 days of memory/logs/ to avoid repeating posts.

## Steps

1. **Fetch posts from each subreddit.** For each subreddit in subreddits.yml, fetch the top/hot posts using Reddit's public JSON API:
   ```bash
   curl -sL -H "User-Agent: aeon-bot/1.0" "https://www.reddit.com/r/${SUBREDDIT}/hot.json?limit=15&t=day"
   ```
   Parse the JSON response — posts are under `data.children[].data`. Extract:
   - `title`
   - `url` (external link) and `permalink` (Reddit discussion link)
   - `score` (upvotes)
   - `num_comments`
   - `created_utc` (filter to last 24h)
   - `selftext` (for text posts)

2. **Filter for relevance.** From all fetched posts:
   - Keep posts from the last 24h only
   - Prioritize posts matching topics tracked in MEMORY.md (AI, crypto, neuroscience, programming, etc.)
   - Also include any post with 100+ upvotes regardless of topic
   - Deduplicate against recent logs — skip any post title already mentioned

3. **Summarize top posts.** Select the 5-8 most interesting posts across all subreddits:
   - If a post links to an external article, use WebFetch to get more context
   - For text posts (self posts), use the `selftext` field
   - Write a 1-2 sentence summary of why it matters

4. **Format and send via `./notify`** (keep under 4000 chars):
   ```
   *Reddit Digest — ${today}*

   *r/subreddit*
   - [Title](url) (150 pts, 42 comments)
     Summary of the post.
     [Discussion](https://reddit.com${permalink})

   *r/subreddit*
   - [Title](url) (300 pts, 120 comments)
     Summary of the post.
   ```

5. **Log to memory/logs/${today}.md.** Record which posts were included.

If no relevant posts are found across all subreddits, log "REDDIT_DIGEST_OK" and end.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables

No environment variables required — uses Reddit's public JSON API (no authentication needed).
A custom User-Agent header is set to avoid rate limiting.
