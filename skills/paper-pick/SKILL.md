---
name: Paper Pick
description: Find the one paper you should read today from arXiv and Semantic Scholar
var: ""
tags: [research]
---
> **${var}** — Research topic to search for (e.g. "transformer architectures", "memory consolidation", "RL agents"). If empty, searches broadly across AI and related fields.

Read memory/MEMORY.md for context.
Read the last 7 days of memory/logs/ to avoid recommending papers already covered.

## Steps

1. Search for recent papers. **Start with arXiv** (no rate limits), then try Semantic Scholar as a supplement:

   **Primary — arXiv** (always works, no rate limits):
   ```bash
   # If ${var} is set, use it as the query. Otherwise use broad categories.
   # arXiv categories: cs.AI, cs.CL (NLP), cs.LG (machine learning)
   curl -s -L "https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=15"
   ```

   **Secondary — Semantic Scholar** (may 429, treat as optional):
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=artificial+intelligence+large+language+models&year=2025-2026&limit=5&fields=title,authors,abstract,url,publicationDate,citationCount,openAccessPdf" \
     -H "Accept: application/json"
   ```
   If rate-limited (429), **skip Semantic Scholar entirely** — arXiv results are sufficient. Do not retry or wait.

2. If arXiv returned thin results or `${var}` is a niche topic, also try **WebSearch** for "[topic] paper 2025 2026 site:arxiv.org" to catch papers the API missed.

3. From all results, pick **the single best paper** — the one most worth reading today. Criteria: novelty, relevance, practical implications. Skip anything already mentioned in recent logs.

4. Send via `./notify`:
   ```
   *Paper Pick — ${today}*

   "Paper Title" — Authors
   One sentence: why this paper is worth your time.
   [Read](url) | [PDF](pdf_url)
   ```
   If open-access PDF is available, include the PDF link. Otherwise just the paper link.

5. Log to memory/logs/${today}.md.

If nothing interesting found, log "PAPER_PICK_OK" and end.
