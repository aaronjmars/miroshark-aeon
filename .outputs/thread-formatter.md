*Thread Draft — 2026-05-23*
Topic: Polymarket-Ready Prediction JSON — MiroShark PR #99

1/ MiroShark opened PR #99 today — a Polymarket-ready prediction JSON endpoint. Fifteen publish-gated surfaces total. This is the first one built for a trading bot, not a human reader.

2/ The prior 14 publish-gated surfaces were readable by anyone: trajectory CSV, chart SVG, Jupyter notebook, BibTeX citation, signal.json, archive ZIP. All designed for researchers or developers to open, inspect, and interpret.

3/ polymarket.json returns yes_probability derived from the simulation's directional consensus: Bullish maps to bullish_pct/100, Bearish to 1 minus bearish_pct/100, Neutral to exactly 0.5. Only completed simulations emit a payload — in-progress runs get a 404.

4/ Fourteen surfaces exist for readers who show up. This one exists for software that polls. That distinction matters — it moves MiroShark from a tool that researchers visit into infrastructure that applications depend on. The integrator arc opened today alongside two external PRs.

5/ 30+ offline tests, zero new dependencies — the 31st streak PR. Polymarket-ready prediction JSON is open for review: https://github.com/aaronjmars/MiroShark/pull/99

(article: articles/thread-2026-05-23.md)
