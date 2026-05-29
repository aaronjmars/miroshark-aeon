*Thread Draft — 2026-05-29*
Topic: Belief Volatility Score — MiroShark PR #124

1/ MiroShark has 25 API surfaces. The 25th — merged today as PR #124 — describes how contested a simulation was. Not just which direction it ended. Not just when it peaked. The full distribution of belief swings.

2/ Every prior MiroShark surface answers what a simulation concluded or when it moved. signal.json returns direction and confidence. peak-round returns the single most volatile round. Nothing described whether the consensus formed smoothly or under sustained pressure.

3/ GET /api/simulation/<id>/volatility returns mean and standard deviation of round-over-round swings, a volatility_index from 0 to 100, and a trend label — stable, converging, or contested. A 404 enforces minimum two rounds. No new dependencies. 200 lines of stdlib.

4/ Peak-round already showed you the single most volatile round. Volatility shows you the shape behind it — whether momentum compressed into one inflection or stayed contested across the whole simulation. Direction plus peak plus distribution: that's the full analytical answer.

5/ volatility_service.py — 200 lines of stdlib. Reuses load_trajectory_rounds from peak-round; max_delta_round matches by construction. The distribution is the new information. PR #124: https://github.com/aaronjmars/MiroShark/pull/124

(article: articles/thread-2026-05-29.md)
