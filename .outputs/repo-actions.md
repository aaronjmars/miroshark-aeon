*Repo Action Ideas — 2026-05-18*
Generated from analysis of aaronjmars/MiroShark (1,172⭐ · 236 forks · FDV $3.32M ATH day) — ideas that could be autonomously built by the feature skill tomorrow.

1. Trading Signal JSON (Feature, Small)
   `GET /api/simulation/<id>/signal.json` — direction + confidence_pct + risk_tier derived from final beliefs; machine-readable action primitive for quant tools and Zapier workflows.

2. Simulation Archive Bundle (Feature, Small)
   `GET /api/simulation/<id>/archive.zip` — all published surfaces (share-card, chart, trajectory, reproduce.json, notebook) in one timestamped ZIP with manifest.json; one-command offline copy for researchers.

3. Per-Agent Stance Sparklines (Feature, Medium)
   `GET /api/simulation/<id>/agent-sparklines.svg` — SVG grid of per-agent belief evolution across rounds; shows whether consensus was driven by unanimous drift or a few late-flipping outliers.

4. Scenario Clone Button on Share Page (Growth, Small)
   "Run this scenario →" button on /share/<id> that pre-fills the New Sim form via PR #71's URL params — turns passive share-page viewers into active sim runners; no auth, no new backend.

5. Chinese + Japanese README Translations (Community, Small)
   README.zh.md + README.ja.md + language badges in README.md — timed to CN tweet "米罗莎要来了" (May 16) + first JP coverage (May 17); directly targets the CN-locale contributor hyperstition (deadline 2026-06-15).

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-18.md
