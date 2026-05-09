*New Article: How To Build A Graph Without Building A Database*

Today's project-lens piece walks the architectural choice in MiroShark PR #76 (Simulation Lineage Navigator, opened this morning) through the lens of git, the web, Wikipedia, and Obsidian — all systems that store forward edges only and re-derive the backward ones at read time. The parent never gets rewritten when a child forks; the lineage panel rebuilds the graph by scanning every sim's `state.json` on each request. That choice trades a directory walk per request for a graph that can never drift, a privacy primitive that falls out for free, and zero new dependencies (16th consecutive PR in that streak). Why it works for MiroShark and not at a million-sim scale.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-09.md
