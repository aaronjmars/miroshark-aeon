---
name: Telegram Digest
description: Digest of recent posts from tracked public Telegram channels
var: ""
tags: [social]
---
> **${var}** — Channel username to check (without @). If empty, checks all channels in `skills/telegram-digest/channels.md`.

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating content.

## Steps

1. **Load channel list.** If `${var}` is set, use only that channel. Otherwise read `skills/telegram-digest/channels.md` (one username per line, skip comments and blanks).

2. **Fetch recent posts for each channel.** Use WebFetch to scrape the public feed. Paginate back to get ~48h of coverage:

   ```
   Page 1: WebFetch https://t.me/s/{channel}
   ```

   From the first page, find the `?before=N` pagination link. If the oldest post on the page is less than 48h old, fetch the next page:

   ```
   Page 2: WebFetch https://t.me/s/{channel}?before=N
   ```

   Continue until you have posts covering the last 48 hours or have fetched 5 pages (whichever comes first). Stop early if posts are older than 48h.

   For each post extract: post number/ID, date, full text, any links, view/reaction counts if visible.

3. **Filter and rank.** From all fetched posts across all channels:
   - Skip low-signal posts (single emoji reactions, forwarded ads, bot messages)
   - Prioritize: posts with high engagement, posts with links to articles/threads, posts with original analysis, breaking news
   - If `${var}` targets a single channel, include more posts (top 10). For multi-channel runs, pick top 5 per channel.
   - Deduplicate against the last 2 days of memory/logs/

4. **Send via `./notify`** (under 4000 chars):
   ```
   *Telegram Digest — ${today}*

   *@channel_name*
   - [post summary or excerpt] (link)
   - [post summary or excerpt] (link)

   *@channel_name_2*
   - [post summary or excerpt] (link)
   ...
   ```

   Link format for individual posts: `https://t.me/channel/POST_NUMBER`

5. **Log to `memory/logs/${today}.md`:**
   ```
   ## Telegram Digest
   - **Channels:** N checked
   - **Posts scanned:** N (last 48h)
   - **Highlights:** N posts surfaced
   - **Notification sent:** yes/no
   ```

   If no interesting posts found, log "TELEGRAM_DIGEST_OK".

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
