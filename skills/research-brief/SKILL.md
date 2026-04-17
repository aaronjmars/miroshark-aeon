---
name: Research Brief
description: Deep dive on a topic combining web search, papers, and synthesis
var: ""
tags: [research]
---
> **${var}** — Topic to research. Recommended for best results.

If `${var}` is set, use it as the research topic.


This skill is triggered on demand (via Telegram or workflow_dispatch). Expects a topic in the trigger message.

Read memory/MEMORY.md for context on prior research and interests.

Steps:
1. Use WebSearch to find 5-8 current sources on the topic.
2. Search Semantic Scholar for relevant academic papers:
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TOPIC&limit=10&fields=title,authors,abstract,url,publicationDate,citationCount,openAccessPdf"
   ```
3. Use WebFetch to read the 3-4 most relevant sources in depth.
4. Synthesize a research brief (600-1000 words):
   - **Overview** — what this topic is and why it matters now
   - **Current state** — what's known, key players, recent developments
   - **Key papers** — 2-3 most relevant papers with summaries
   - **Open questions** — what's unresolved or emerging
   - **Connections** — how this relates to topics in MEMORY.md
5. Save to articles/research-brief-${today}.md.
6. Send an abbreviated summary via `./notify`.
7. Log what you did to memory/logs/${today}.md.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
