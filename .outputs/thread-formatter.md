*Thread Draft — 2026-05-18*
Topic: Farcaster Frame v2 — MiroShark PR #90

1/ Until today, sharing a MiroShark simulation on Farcaster produced a blank link card. PR #90 injects fc:frame:* meta tags into every public share page — the cast becomes an interactive belief-chart with a View Simulation button. 26th consecutive zero-dependency PR.

2/ $MIROSHARK lives on Base. Base-native social is Farcaster. Before PR #90, sharing a simulation as a Farcaster cast was identical to sharing a plain URL — the platform knew nothing about the content, so it rendered nothing. An audience-fit gap open since day one.

3/ frame_metadata.py (~210 lines, stdlib only) builds two helpers: build_frame_metadata() and warpcast_compose_url(). The Frame image is the chart SVG from PR #85 at 2:1 — if the simulation has no trajectory yet, it falls back to the share-card PNG. 13 offline tests.

4/ The project's audience is on Base. Base's social layer is Farcaster. That gap existed since launch. PR #85 (chart SVG) merged two days ago. PR #90 (Frame injector) opens today using it. The same trajectory now has a native entry point on the network where the token trades.

5/ 13 tests, zero new dependencies, the 26th consecutive. Base-chain audience now has a native entry point. PR #90 is open on MiroShark: https://github.com/aaronjmars/MiroShark/pull/90

(article: articles/thread-2026-05-18.md)
