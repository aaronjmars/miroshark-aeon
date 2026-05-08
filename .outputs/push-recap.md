*Push Recap — 2026-05-08*
2 substantive commits across both watched repos.

*MiroShark — PR #75 merged (Reproducibility Config Export):* New `GET /api/simulation/<id>/reproduce.json` returns a v1-schema JSON blob with scenario, agents, rounds, platforms, time_config, director events, and lineage (original/fork/counterfactual). Pretty-printed + sort_keys=True so identical exports are bytewise-identical — the file hash becomes a stable citation key. Closes the reproducibility gap behind the six citation surfaces (transcript/trajectory/thread/watch/GIF/share card). Pure stdlib; 22 offline tests; new EmbedDialog "🔬 Reproducibility config" panel with curl snippet + Download button + lineage badge. Zero-new-deps streak now 15 consecutive PRs.

*aeon — PR #32 opened (MEMORY.md row caps):* The index had grown to 76KB / 31K+ tokens — over the Read tool's 25K limit, so every skill loading MEMORY.md was failing the Read call. Condensed each row to a one-sentence summary (file now 9.4KB / 79 lines, 8x smaller); `memory-flush` skill now enforces per-row caps (Skills Built ≤280, Recent Articles ≤220, Recent Digests ≤180) with a `wc -c` sanity check after every flush.

Key changes:
- New `backend/app/services/repro_export.py` (487 lines, pure stdlib): SCHEMA_VERSION=1, REQUIRED_KEYS frozenset, `build_repro_config()`, `_build_lineage()` (3 cases), `_read_director_events()` (handles JSONL + legacy formats), `render_json_bytes()` for citation-hash stability, `validate_blob()` helper
- `frontend/src/components/EmbedDialog.vue` (+484 lines): collapsed-by-default panel between Distribution and Mark-outcome, lineage badge (🪐 Forked / 🔀 Counterfactual) with parent-id tooltip, copy-ready curl snippet, Download `reproduce.json` button
- `memory/MEMORY.md` shrunk 8x (76KB → 9.4KB) + new top-of-file callout banner explaining the index contract

Stats: 13 files changed, +1,961 / -42 lines across 2 substantive commits (~35 commits total counting the day's routine cron auto-commits — token-report / fetch-tweets / tweet-allocator / repo-pulse / feature / self-improve / repo-actions all OK).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-08.md
