*Feature Built — 2026-06-16 — aaronjmars/MiroShark*

cost.json — the "$1 to simulate anything" number, made queryable per run 🦈

new endpoint: `GET /api/simulation/<id>/cost.json`. it returns what a specific simulation actually cost — a headline `estimated_cost_usd` plus token/latency totals and a per-model + per-phase breakdown. the one number behind the whole pitch, served as machine-readable JSON instead of buried in a file.

Why this matters:
the cost figure is the proof. but until now it wasn't queryable — MiroShark already prices every LLM call at run completion and writes a `run_summary.md` to disk, and `/observability/stats` gives you tokens but no dollars. so a stranger who runs a sim couldn't programmatically answer the first question they ask: what did this cost? that gap between the "~$1" promise and a verifiable per-run number is exactly the thing that converts to trust. this closes it.

What was built:
- `cost_service.py` (new): reshapes the run aggregate into a stable public envelope — headline cost + totals + by_model/by_phase rows.
- `run_summary.py`: extracted a shared event reader and added a pure `collect_cost_summary()` (no file writes), so the JSON surface and the on-disk report price calls off the *same* table and can never disagree.
- `simulation.py`: the `/cost.json` route — same publish gate as every share surface (403 private / 404 no-calls-yet), 60s cache, usage counter.
- catalog + openapi + docs + offline unit tests wired in.

How it works:
pure read of the sim's event log — no network, no engine state touched, modelled byte-for-byte on the existing `volatility` surface. it reuses the existing OpenRouter price table as the single source of truth. honest by construction: flagged `is_estimate`, carries a `pricing_basis` note, and calls on models not in the table count as $0 — so the figure is an explicit lower bound, never an estimate dressed up as a billed invoice.

What's next:
this is the per-run metric the growth story needs — every worked example can now cite a real, queryable cost. natural follow-on: surface it on the share page + share card so the "$1" lands without a curl.

PR: https://github.com/aaronjmars/MiroShark/pull/179
