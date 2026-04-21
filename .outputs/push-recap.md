*Push Recap — 2026-04-21*
MiroShark: 11 commits (4 substantive + 7 badge cosmetic); miroshark-aeon: 3 substantive PRs + ~30 auto chores. 2 authors (Aeon, Aaron Mars).

*Graph Memory Stack (direct push, 17 files, +2,690/-93)*: Aaron landed 11 capabilities in one commit — BGE cross-encoder reranker, graph-traversal BFS alongside vector+BM25, bi-temporal edges with `as_of` + `invalidate_edge()`, LLM-reflection entity resolution, fact/belief/observation edge labels, contradiction detection (invalidate-don't-delete), Leiden community clustering + `:Community` subgraph, ReACT reasoning persisted as traversable graph, MCP server exposing 8 tools to Claude Desktop. The graph substrate is now bi-temporal with first-class reasoning provenance.

*PR #41 — Sibling-Repo Siphon (43 files, +4,005/-29)*: Aeon-authored 14-feature bundle from MiroJiang/MiroWhale/OpenMiro/oracle-seeds, all gated behind env flags. Highlights: `POST /api/simulation/ask` (question-only pipeline), counterfactual branching via director-event piggyback, `MCP_AGENT_TOOLS_ENABLED` (agents call MCP tools mid-sim — first epistemic leak outward), `analyze_equilibrium` Nash-game report tool, Anthropic prompt caching, embed publish-gate, `miroshark-cli` entry point, and MiroShark's first standing CI test suite (62 unit tests).

*PR #40 — Trending Topics (6 files, +864)*: Stdlib-only RSS/Atom + SSRF-hardened `?feeds=` override (IPv4-encoding normalization blocks `2130706433`/`0x7f000001`/`0177.0.0.1` loopback bypasses). Closes the blank-canvas onboarding gap left by Scenario Auto-Suggest.

*miroshark-aeon XAI cache pipeline (#19/#20/#21)*: Three-round postmortem of yesterday's fetch-tweets triple-run. #19 adds cache query sidecar validation (mismatch falls through to live API instead of serving stale `$AEON`-era content). #20 harvests tweet URLs from Grok's `output_text.annotations[]` when `.text` gets truncated (yesterday: 2 visible / 40 cited). #21 strips the stale "XAI_API_KEY not set" flag that heartbeat kept re-emitting.

Key changes:
- Graph memory: ReACT reasoning now a traversable `(:Report)-[:HAS_SECTION]->(:ReportSection)-[:HAS_STEP]` subgraph — you can query *why* a conclusion was reached
- PR #41: `run_parallel_simulation.py` no longer silently falls back to `gpt-4o-mini` when no model is configured — raises loudly (breaking for deployments relying on the implicit default)
- PR #40: Reuters RSS default swapped for TechCrunch (Reuters shut their public feed years ago — default ship was one-feed-silently-empty)

Stats: ~82 files, +7,953/-184 across 13 substantive commits
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-21.md
