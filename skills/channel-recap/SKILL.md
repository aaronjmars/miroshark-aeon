---
name: Channel Recap
description: Weekly recap article from a public Telegram channel — expand on the best posts
var: ""
tags: [content]
---
> **${var}** — Telegram channel username (without @). Required — set in aeon.yml var field.

Read memory/MEMORY.md for context.

## Steps

### 1. Fetch 7 days of posts

Paginate through `https://t.me/s/${var}` using WebFetch. Each page has ~17 posts.

```
Page 1: WebFetch https://t.me/s/${var}
```

From each page, extract the `?before=N` link. Fetch the next page and continue until:
- Posts are older than 7 days, OR
- You've fetched 15 pages (whichever comes first)

For each post extract: full text, any shared links/URLs, timestamp, post number.

### 2. Select the best posts

From all fetched posts, pick the **8-12 most interesting**. Prioritize:
- Original takes (not just a link with no comment)
- Posts that sparked discussion or share a strong opinion
- Posts linking to substantial content (articles, threads, papers — not memes)
- Posts that connect to broader narratives (crypto, AI, tech, culture)
- Recurring themes across multiple posts (these become article sections)

Skip: single-word reactions, emoji-only posts, low-context forwards.

### 3. Research and expand

For each selected post:
- If it links to a tweet, use WebFetch to get the full tweet/thread context
- If it links to an article, use WebFetch to read it
- Use WebSearch to get additional context on the topic if needed
- Note connections between posts — what themes keep coming up?

### 4. Write the article

Write a **750-1500 word article** that weaves the best posts into a coherent narrative. Structure:

```markdown
# [Channel] Week in Review — ${today}

[Opening — 2-3 sentences setting up what the channel was buzzing about this week]

## [Theme 1 title]

[Expand on 2-3 related posts. Don't just quote them — add context, explain why they matter,
connect to the bigger picture. Link to the original posts: https://t.me/${var}/POST_NUMBER]

## [Theme 2 title]

[Same treatment — expand, contextualize, connect]

## [Theme 3 title]

[...]

## Quick hits

[Bullet list of 3-5 smaller posts worth noting but not worth a full section]

---
*Sourced from [@${var}](https://t.me/${var}) — ${date_range}*
```

Rules:
- Write in a direct, opinionated style — no hedging, no filler
- Don't just summarize posts — add value. Explain why something matters, what the implications are, what people are missing.
- Use the channel posts as jumping-off points, not the whole story
- Link to original posts and sources
- Group by theme, not chronologically

### 5. Save the article

Write to `output/articles/channel-recap-${var}-${today}.md`.

### 6. Notify

Send via `./notify` (under 4000 chars) — a condensed version:
```
*${var} — week recap*

[3-4 sentence summary of the biggest themes]

top posts:
- [one-liner] (link)
- [one-liner] (link)
- [one-liner] (link)

full article: output/articles/channel-recap-${var}-${today}.md
```

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

### 7. Log

Append to `memory/logs/${today}.md`:
```
## Channel Recap — ${var}
- **Posts scanned:** N (7-day window)
- **Posts featured:** N
- **Themes:** [list]
- **Article:** output/articles/channel-recap-${var}-${today}.md
- **Notification sent:** yes
```
