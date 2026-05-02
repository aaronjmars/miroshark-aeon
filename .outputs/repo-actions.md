*Repo Action Ideas — 2026-05-02*
Generated from analysis of MiroShark (976 stars · 195 forks · 1 open PR) — five ideas the feature skill can autonomously build next.

1. 1-Click Cloud Deploy (DX/Growth, Small)
   Deploy to Railway button + fly.toml + docker-compose.prod.yml — cuts install from ~20 min to ~3 min; 976 stars, 4 contributors, the star-to-deploy gap is the bottleneck before 1K.

2. Gallery Full-Text Search & Consensus Filter (Feature, Small)
   `?q=<keyword>&consensus=bullish&quality=excellent` query params on /api/simulation/public + search bar + filter chips in /explore — turns the gallery from a reverse-chron scroll into a searchable research corpus.

3. Pre-Run Cost & Time Estimator Widget (DX/Feature, Small)
   '~$0.40 · ~7 min' line next to the Run button, computed from pricing_constants.json + existing Langfuse cost data — renders the '$1 & under 10 min' promise at the moment of decision, zero new API calls.

4. Per-Agent Stance Sparklines / Character Arc View (Feature/Research, Small)
   GET /api/simulation/:id/agent-arcs returns per-agent stance time-series; SimulationView 'Agent Arcs' tab renders 120×24px SVG sparklines per agent — the per-agent cut of the trajectory CSV, makes results citable in research.

5. Pre-filled Scenario URL (Growth/DX, Small)
   /new?scenario=...&preset=Cheap&rounds=30 pre-fills the New Sim form; 'Copy link' button in the form and on template cards — turns any tweet or blog post CTA into a one-click 'run this sim yourself' flow.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-02.md
