---
name: Search Academic Papers
description: Search for recent academic papers on topics of interest and save a summary
var: ""
tags: [research]
---
> **${var}** — Search query for papers. If empty, picks topics from MEMORY.md.


Read `memory/MEMORY.md` for context on current interests and recent activity.

Steps:
1. Determine search topics:
   - If `${var}` is set, use that as the search topic.
   - Otherwise, pick 1-2 topics from current priorities or recent articles in memory (AI, crypto, consciousness, etc.).
2. For each topic, search Semantic Scholar using curl:
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TOPIC&limit=5&fields=title,authors,year,abstract,url,citationCount,publicationDate,journal,externalIds,openAccessPdf&sort=publicationDate:desc"
   ```
   - Filter to recent papers (last 30 days) by adding `&publicationDateOrYear=YYYY-MM-DD:` with a date 30 days ago.
   - If rate-limited (429), wait 3 seconds and retry once.
3. Format the results as a markdown summary:
   ```
   ## Recent Papers — ${today}

   ### Topic Name
   1. **Paper Title** (YYYY) — Author1, Author2 et al.
      Citations: N | [Semantic Scholar](url) | [DOI](doi_url)
      > First ~200 chars of abstract...

   2. ...
   ```
4. Save the summary to `memory/logs/${today}.md` (append under a `## Papers` heading).
5. Send a notification via `./notify` with the top 2-3 most interesting finds (title + one-line summary + link).
6. Log what you did to `memory/logs/${today}.md`.
