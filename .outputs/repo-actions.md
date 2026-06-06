*Repo Action Ideas — 2026-06-06*
Generated from deep API audit of aaronjmars/MiroShark — 5 net-new ideas for the platform-level analytics layer, confirmed not pre-existing.

1. Platform Outcome Distribution (Analytics, Small)
   GET /api/stats/distribution.json — bucketed breakdown of all public sims by direction/confidence/quality/round-count. Answers "what do MiroShark results look like in aggregate?" for researchers and journalists.

2. Simulation Payload Validator (DX, Small)
   POST /api/simulation/validate — dry-run validation of a sim creation payload without spending $1 or waiting 10 minutes. Returns {valid, errors, warnings}. Reuses create's validation logic.

3. Signed Simulation Result (Security/Integration, Small)
   GET /api/simulation/<id>/signed-result.json — HMAC-SHA256 over the canonical signal payload using WEBHOOK_SECRET. Integrators who store results for audit trails or prediction market settlement can verify authenticity offline without a live API call.

4. Monthly Statistics Time-Series (Analytics/Growth, Small)
   GET /api/stats/timeseries.json — month-by-month completion counts, published sims, avg confidence, distinct projects. Platform growth is invisible from the API today; this closes that gap.

5. Platform Agent Behavior Census (Analytics/Research, Small)
   GET /api/stats/agents.json — aggregate behavioral stats across all public completed sims: stance distribution at start vs end, opinion flip rate, avg belief change per round. First platform-level answer to "how do agents on MiroShark behave as a population?".

Note: deep audit today discovered 17 additional pre-existing surfaces (timeline, quality, belief-drift, interaction-network, transcript, thread, cite.bib, notebook.ipynb, templates/list, and more) — all registered in pre-existing-features.md to prevent future idea-slot waste.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-06.md
