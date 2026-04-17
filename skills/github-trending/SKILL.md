---
name: GitHub Trending
description: Top 10 trending repos on GitHub right now
var: ""
tags: [dev]
---
> **${var}** — Language filter (e.g. "python", "typescript", "rust"). If empty, shows all languages.

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating repos.

## Steps

1. Fetch trending repos from GitHub. Use WebFetch to scrape the trending page:
   ```
   https://github.com/trending?since=daily
   ```
   If `${var}` is set, filter by language:
   ```
   https://github.com/trending/${var}?since=daily
   ```

2. Extract the top 10 repos. For each:
   - Repo name (owner/repo)
   - Description (one line)
   - Language
   - Stars today
   - Total stars
   - URL

3. Send via `./notify` (under 4000 chars). No leading spaces on any line:
   ```
   *GitHub Trending — ${today}*

   1. [owner/repo](https://github.com/owner/repo) — ★ X today (Xk total)
   description
   Language

   2. ...

   ... (top 10)
   ```

4. Log to memory/logs/${today}.md.
   If the page returns empty or errors, log "GITHUB_TRENDING_OK" and end.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
