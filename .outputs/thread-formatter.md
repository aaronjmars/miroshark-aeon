*Thread Draft — 2026-06-19*
Topic: embed cost pill — PR #190

1/ MiroShark has been printing a $1 cost per sim since launch. nobody outside the API could see it. PR #190 puts the cost pill on the public embed.

2/ cost.json shipped 3 days ago — full breakdown at /api/simulation/<id>/cost.json, is_estimate flag, pricing_basis. it worked. the problem: it was behind an auth wall. the embed is public. cost.json wasn't.

3/ PR #190 wires cost.json into EmbedView — the public view anyone hits without an account. getSimulationCost() fetches on complete, costLabel computed, ~$X pill in the meta row. build: clean.

4/ the $1 claim was always real. the engine prices every LLM call, totals it, writes it to cost.json. a number behind an API isn't a claim — it's a promise. now any stranger landing on a public embed sees the bill.

5/ PR #190 — cost pill on the public embed. https://github.com/aaronjmars/MiroShark/pull/190 🦈

(article: articles/thread-2026-06-19.md)
