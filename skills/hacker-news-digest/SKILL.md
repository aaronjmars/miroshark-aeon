---
name: Hacker News Digest
description: Top HN stories filtered by keywords relevant to your interests
var: ""
tags: [research]
---
> **${var}** — Topic filter for stories. If empty, uses interests from MEMORY.md.

If `${var}` is set, only include stories matching that topic.


Read memory/MEMORY.md for tracked topics and interests.
Read the last 2 days of memory/logs/ to avoid repeating stories.

Steps:
1. Fetch top stories from the HN API:
   ```bash
   # Get top 30 story IDs
   STORY_IDS=$(curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq '.[0:30][]')
   # Fetch each story's metadata
   for ID in $STORY_IDS; do
     curl -s "https://hacker-news.firebaseio.com/v0/item/${ID}.json"
   done
   ```
2. Filter stories by relevance to topics in MEMORY.md (AI, crypto, neuroscience, programming, etc.).
   Also include anything with 200+ points regardless of topic.
3. For the top 5-7 stories:
   - If the story has a URL, fetch it with WebFetch for more context
   - Write a 1-2 sentence summary
   - Include the HN discussion link: `https://news.ycombinator.com/item?id=ID`
4. Format and send via `./notify` (under 4000 chars):
   ```
   *HN Digest — ${today}*

   1. [Title](url) (250 pts, 89 comments)
      Summary of why it matters.
      [Discussion](https://news.ycombinator.com/item?id=ID)

   2. ...
   ```
5. Log to memory/logs/${today}.md.
If no relevant stories found, log "HN_DIGEST_OK" and end.
