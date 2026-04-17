---
name: Paper Digest
description: Find and summarize new papers matching tracked research interests
var: ""
tags: [research]
---
> **${var}** — Research topic to search. If empty, uses topics from MEMORY.md.

If `${var}` is set, search papers on that topic instead of using MEMORY.md topics.


Read memory/MEMORY.md for tracked research topics and interests.
Read the last 7 days of memory/logs/ to avoid covering papers already reported.

For each topic area in MEMORY.md:
1. Search Semantic Scholar API (free, no key needed):
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TOPIC&year=YEAR&limit=10&fields=title,authors,abstract,url,publicationDate,citationCount,openAccessPdf" \
     -H "Accept: application/json"
   ```
   If rate-limited (429), wait 3 seconds and retry once.

2. Also check arXiv for the latest preprints:
   ```bash
   curl -s "http://export.arxiv.org/api/query?search_query=all:TOPIC&sortBy=submittedDate&sortOrder=descending&max_results=10"
   ```

3. Score each paper for relevance:
   - Direct keyword match to MEMORY.md interests = high
   - Related field or methodology = medium
   - Tangential = skip

Select the top 5 most relevant papers across all topics.

For each selected paper:
- Fetch the abstract (from API response or via WebFetch if needed)
- Write a 2-3 sentence summary: what they found, why it matters, connection to other work
- Note if open-access PDF is available

Format as a weekly briefing and save to articles/paper-digest-${today}.md:
```markdown
# Paper Digest — ${today}

## Topic Area
1. **Paper Title** — Authors (Year)
   Summary of key findings and implications.
   [Link](url) | [PDF](pdf_url)

2. ...
```

Send abbreviated version via `./notify` (under 4000 chars):
```
*Paper Digest — ${today}*
5 new papers across [topics]

1. "Title" — key finding
2. ...

Full briefing: articles/paper-digest-${today}.md
```

Log what you did to memory/logs/${today}.md.
