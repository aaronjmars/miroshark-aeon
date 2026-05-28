*Repo Action Ideas — 2026-05-28*
Generated from analysis of aaronjmars/MiroShark (1,207⭐ · 257 forks · 24 surfaces · 11+ integrators).

1. Gallery Public JSON (Integration, Small)
   Paginated JSON index of all published sims — the machine-readable full index that every integrator, external directory, and Aeon skill needs before any query-driven surface can exist. Re-eligible from May-20.

2. Simulation Comparison API (Feature, Small)
   GET /api/compare?a=<simId>&b=<simId> — structured diff of two sims: belief delta, consensus agreement, confidence delta, quality winner. AntFleet is already doing this manually; one curl replaces two JSON downloads and a manual diff. Net-new.

3. Belief Volatility Score (Feature, Small)
   GET /api/simulation/<id>/volatility — 0–100 turbulence index (std dev of per-round belief deltas) + trend label (Converging/Stable/Contested). High-volatility Bullish ≠ low-volatility Bullish. 25th surface; completes the quant analytical layer. Re-eligible from May-20.

4. Webhook Test Ping (DX, Small)
   POST /api/webhook/test — sends a synthetic completion payload to WEBHOOK_URL and returns delivery status immediately. Eliminates the 'wait for a real sim to test your endpoint' loop that every new integrator hits exactly once. Re-eligible from May-20.

5. Surface Catalog API (Integration, Small)
   GET /api/surfaces.json — machine-readable catalog of all 24 publish-gated surfaces: key, endpoint, type, description, example curl. Integrators check what's available on a deployment; Aeon tracks live surface count without parsing docs. Net-new, ~60 LoC, static catalog.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-28.md
