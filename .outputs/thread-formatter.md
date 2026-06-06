*Thread Draft — 2026-06-06*
Topic: Multi-Sim Batch Status Lookup — POST /api/simulation/batch-status (PR #150)

1/ MiroShark had 31 API surfaces before today. All 31 ask about one sim or about all sims. PR #150 ships the first that takes a list: POST /api/simulation/batch-status, 1 to 20 IDs per request.

2/ The per-sim surfaces answer questions about one run: signal, agents, sparklines, volatility, transcript. Platform surfaces answer questions about the whole instance: stats, catalog, status probe. Nothing in between for callers tracking a set of sims.

3/ Takes a JSON body of up to 20 sim IDs, returns one entry per ID in input order, duplicates honored. Private and unknown IDs share an identical envelope — callers cannot probe whether a private sim exists. 26 tests, one dedicated to that invariant.

4/ AntFleet's miroshark-bench, Capacitr's polling loop, the integrators in ECOSYSTEM.md — all of them need to monitor a set of sims at once. One batch call replaces N sequential calls. This is the primitive that makes polling on a fleet of sims practical.

5/ PR #150 — 10 files, 26 offline tests, 41st consecutive zero-dependency PR on MiroShark. https://github.com/aaronjmars/MiroShark/pull/150

(article: articles/thread-2026-06-06.md)
