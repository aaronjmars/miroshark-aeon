*Thread Draft — 2026-05-31*
Topic: Simulation Clone JSON — MiroShark PR #131

1/ MiroShark shipped 26 API surfaces before today. All 26 return what a simulation concluded — directions, beliefs, exports, badges, the catalog itself. PR #131, opened this morning, is the first that returns what went in. GET /api/simulation/<id>/clone.json.

2/ Every prior surface answers one question: what did this simulation produce? signal.json delivers direction and confidence. volatility.json delivers the distribution of belief swings. cite.bib delivers the academic citation. None deliver the configuration that produced the result.

3/ GET /api/simulation/<id>/clone.json returns the body that produced the simulation. Wire-compatible with POST /api/simulation/create: same fields, same defaults, same polymarket_market_count clamp [1,5], same country normalisation. 250 lines of stdlib. 1h cache.

4/ It pairs with /api/simulation/compare, which already exists: clone the inputs, modify one field, run a new simulation, diff the outputs. That loop — fork, modify, diff — needed no new UI, no new database schema, just an endpoint returning what went in.

5/ clone_service.py — 250 lines stdlib, 24 offline tests. 35th consecutive zero-dependency PR. https://github.com/aaronjmars/MiroShark/pull/131

(article: articles/thread-2026-05-31.md)
