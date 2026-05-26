*Feature Built — 2026-05-26*

Peak-Round Analytics
MiroShark simulations now expose a one-call summary of *when* belief shifted, not just *what* the final belief was. The new GET /api/simulation/<id>/peak-round endpoint reports the exact round each stance (bullish / neutral / bearish) hit its high point, which round saw the biggest swing, and how big that swing was — the answers a researcher used to get only by reading 100 rows of the trajectory CSV by hand.

Why this matters:
The project already ships the raw per-round data (trajectory.csv) and the visual (chart.svg), but neither answers "which round did bullish peak?" or "which round was the most volatile?" without parsing. Quant tools and research scripts needed that inflection summary as a single machine-readable call. This was the #2 idea in the 2026-05-24 repo-actions batch (and re-eligible from May-16) — it completes the analytical quadrant alongside signal.json.

What was built:
- backend/app/services/peak_round.py: load_trajectory_rounds() + compute_peak_rounds() — a pure O(n) pass over trajectory.json that finds each stance's earliest peak round, the most-volatile round (largest summed round-over-round swing), and total rounds. ~190 LoC, pure stdlib.
- backend/app/api/simulation.py: the publish-gated /peak-round route, mirroring the signal.json handler (404 = no trajectory yet, 403 = unpublished) and incrementing a new surface counter.
- backend/openapi.yaml + surface_stats: new PeakRoundResponse/StancePeak schemas and a peak_round surface key.
- frontend EmbedDialog.vue: a "📊 Peak beliefs" panel showing the bullish/bearish peaks, most-volatile round, and total rounds, with copyable URL + curl snippet.
- 19 offline unit tests + docs (API.md, FEATURES.md).

How it works:
It reuses trajectory_export.compute_stance_split — the exact ±0.2-threshold function trajectory.csv uses — so "bullish peaked at 71% on round 4" matches row 4 of the CSV byte-for-byte. Nothing is re-computed; the endpoint only changes the *shape* of existing data into an inflection summary. Peak ties resolve to the earliest round so the output is deterministic. Zero new dependencies, consistent with the project's surface pattern.

What's next:
Still unbuilt from the May-24 batch: Operator Profile pages, Agent Persona Export JSON (the first per-agent data surface), and a query-driven Simulation Search API.

PR: https://github.com/aaronjmars/MiroShark/pull/108
