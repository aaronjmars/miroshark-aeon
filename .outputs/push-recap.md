*Push Recap — 2026-05-27*
MiroShark — 7 PRs merged (#110–#116) + Aeon repo #47. 3 authors (maintainer, Aeon, external).

Reliability hardening: Three crash/hang fixes. #111 + #112 stop report sections from dying when a reasoning model (Gemini 3 Flash) returns null content into a regex; #110 stops the retrieval reranker from hanging forever on Apple Silicon by steering off the MPS backend (new RERANKER_DEVICE knob).

New surface (#115): Per-agent belief sparklines — GET /api/simulation/<id>/agents/sparklines, the 23rd public surface. Aeon authored it yesterday; maintainer merged it today. Each agent's belief trajectory as an inline SVG, zero new deps.

Cleanup (#116): 8-pass code-quality sweep, +1627/-532 across 61 files — dropped dead retry.py (-238), deduped the CommandType enum, removed 27 unused imports, narrowed silent excepts, all behavior-preserving (+9 docs/cleanup notes).

Key changes:
- Reports now retry instead of crashing on flaky/null LLM turns; Macs can finish a sim with the reranker on
- 23rd surface ships: per-agent sparklines complete the chart.svg / peak-round / per-agent trio
- aeon #47 disabled fetch-tweets + tweet-allocator (the spam-feed skills that paid 0 this week) + 3 weekly digests

Also: ecosystem roster hit 11 integrators (external add: ZER0), and a one-click 'Regenerate Report' button landed in the UI (#113).

Stats: ~76 files changed, +2,871/-547
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-27.md
