*Push Recap — 2026-05-24*
MiroShark — 5 PRs merged (2 external) in a 95-min burst on 2026-05-23 between 17:09Z and 18:43Z, all post-yesterday's-recap. miroshark-aeon — 0 merges (skill auto-commits only); PR #45 (bankr-prefetch EXIT trap) opened today.

*Post-recap merge wave.* PR #99 (Polymarket prediction JSON, 15th publish-gated surface and first integrator-shaped) + PR #102 (CI fix backfilling openapi+tests that PR #97 should have shipped) + external PRs #98 (antfleet path-traversal fix, found by their two-model Claude Opus 4.7 + GPT-5 consensus review) + #100 (voidfreud Aura launcher fix, merged 5s apart) + PR #103 (Nemotron demographic grounding). Densest single-window merge of the month.

*31-PR zero-deps streak ENDS at PR #103.* Held from PR #72 → #102 — broken when demographic grounding added unconditional duckdb >=1.0.0 + huggingface_hub >=0.23.0 to pyproject.toml + requirements.txt. Framing is careful (code degrades to graph-only if deps missing) but the install surface grows. New streak restarts at PR #104 / #105.

*External contributors now sustained.* Third external in 10 days (teifurin → antfleet → voidfreud). voidfreud back today with PR #104 (gitignore wildcard). AntFleet running MiroShark as a public security-benchmark target at AntFleet/miroshark-bench/pull/1 — first integrator-product feedback loop.

Key changes:
- PR #103 demographic grounding — new demographic_sampler.py (+360 LoC DuckDB+HF parquet), country_registry.py loading pluggable JSON packs (sg=39 planning areas, us=51 states), CountryPicker.vue with EN+CN i18n, SimulationState gains country + demographic_filters fields. First opt-in remote dataset dependency and first pluggable JSON registry in MiroShark.
- PR #99 polymarket_service.py (+253 LoC stdlib) — direction-aware yes_probability (Bullish=bullish_pct/100, Bearish=1-bearish_pct/100, Neutral=0.5 exactly), 4-bucket confidence_tier, sum-to-1.0 invariant, stricter publish gate (completed sims only — no mid-run flip risk for Polymarket bots).
- PR #98 _validate_project_id regex at single _get_project_dir entry point — closes a real arbitrary-file-read/write vuln (../../etc/passwd would have worked).

Stats: +3,004 / -18 across ~30 files. Stars 1192→1194 (+2). Forks 245→247 (+2). 3 MiroShark PRs open (1 external: #104). 1 aeon PR open (#45).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-24.md
