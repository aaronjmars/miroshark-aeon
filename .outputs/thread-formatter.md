*Thread Draft — 2026-06-16*
Topic: cost.json endpoint — PR #179 on aaronjmars/MiroShark

1/ MiroShark's $1-per-sim number just became checkable. PR #179 ships /api/simulation/<id>/cost.json — query any run, get a full cost breakdown. the number was always computed. now it's an API.

2/ the engine already priced every LLM call. run_summary.py walks the full call log, totals it, writes a markdown file. but that number lived in /tmp. there was no API path. you couldn't query it, pipe it, or display it. the $1 claim was real — just unverifiable from the outside.

3/ PR #179 uses the same MODEL_PRICING table run_summary.py already had. no new pricing logic. read-only route at /api/simulation/<id>/cost.json, 60s cache, is_estimate=true. a pricing_basis field makes the lower bound explicit. one real sim: $0.93.

4/ 1,290 stars. three production integrators running it as infrastructure. the cost number was always real — now it's auditable. you don't take an agent infra stack seriously until you can pull the bill.

5/ PR #179 — the $1 cost endpoint. https://github.com/aaronjmars/MiroShark/pull/179 🦈

(article: articles/thread-2026-06-16.md)
