*Feature Built — 2026-05-29*

Belief Volatility Score
MiroShark sims now ship a turbulence metric next to the direction and the inflection points. `GET /api/simulation/<id>/volatility` answers a question signal.json and peak-round between them have never answered: how contested was the path to consensus? You get the mean, standard deviation, and max of the round-over-round belief swing, a 0–100 volatility index, and a "stable / converging / contested" trend label — so a quant tool can finally tell a swarm that aligned in round three and held from one that swung repeatedly before landing on the same direction.

Why this matters:
For a position-sizing model, two Bullish results with identical confidence are not the same input. High-volatility Bullish is a swarm that almost flipped multiple times; low-volatility Bullish is a swarm that converged early and stayed. signal.json gave the *where*, peak-round gave the *when*, but the *how contested* layer was missing — and it's the one third-party integrators (AntFleet, Polymarket-shaped consumers) have asked for to size positions defensibly. This was repo-actions May-28 idea #3, re-eligible from May-20. 25th publish-gated surface, completing the analytical quadrant.

What was built:
- backend/app/services/volatility_service.py: New stdlib service (~200 LoC, json + os + math). `compute_volatility(rounds)` does one O(n) pass over the per-round stance split, returning `mean_delta_pct`, `std_dev_delta_pct`, `max_delta_pct`, `max_delta_round`, the normalized `volatility_index`, and the `trend` bucket. Returns `None` for <2 rounds so the route can 404 cleanly.
- backend/app/api/simulation.py: `GET /<id>/volatility` route. Publish-gated via `_build_embed_summary_payload` (403 when private), 404 when there aren't two rounds yet, pretty-printed JSON + 5-minute cache + Content-Disposition. Increments a new `volatility` surface counter so an operator can see how often the turbulence view is pulled vs. the raw CSV.
- backend/openapi.yaml + docs/API.md + docs/FEATURES.md: Path + `VolatilityResponse` schema + a full FEATURES section explaining the index formula and trend buckets so external integrators can rescale without reverse-engineering.
- backend/tests/test_unit_volatility.py: 18 offline tests covering boundary (None on <2 rounds), arithmetic (mean / max / population std dev, including the equality with peak-round's `most_volatile_round`), index normalization (flat → 0, capped at 100), trend classifier (stable / converging / contested), and the route + surface-stats + OpenAPI wiring guards.
- frontend/src/components/EmbedDialog.vue + frontend/src/api/simulation.js: 📈 Belief volatility section under the peak-round row. Volatility index sits behind a gradient bar (green ≤33, amber 34–66, red ≥67), max-swing + round, mean swing, std dev, trend chip, copyable URL and curl snippet — same publish-gate-flip lifecycle as peak-round.

How it works:
The delta definition is deliberately identical to peak-round's: `|Δbullish| + |Δneutral| + |Δbearish|` per consecutive round pair. By construction `max_delta_round` here equals peak-round's `most_volatile_round` on the same trajectory — the new information is the *distribution* of those deltas, not the maximum. Volatility index uses `min(std_dev_delta_pct × 5, 100)` so a 20 pp std dev maps to 100; the formula is documented in the schema rather than hidden in code. Trend classifier splits the delta list in half and compares standard deviations: lower in the second half ⇒ `converging`; below 3 pp overall ⇒ `stable`; otherwise ⇒ `contested`. Fewer than four deltas fall back to the std-dev-only buckets since there's no honest half-vs-half claim. Stdlib only — `json`, `os`, `math` — keeping the 33-PR zero-deps streak alive.

What's next:
Three-factor quant view is now complete (signal = direction, peak-round = when, volatility = how contested) — the natural follow-up is the Polymarket integrator surface gaining a volatility field so a market-making bot can widen its quote on contested simulations without parsing the full trajectory. Webhook Test Ping (#4 in the same May-20 batch) remains unbuilt and is the next-highest integrator-impact candidate.

PR: https://github.com/aaronjmars/MiroShark/pull/124
