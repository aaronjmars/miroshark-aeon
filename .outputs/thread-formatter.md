*Thread Draft — 2026-05-21*
Topic: Consensus Status Badge SVG — MiroShark PR #94

1/ MiroShark shipped a Status Badge SVG today — the 13th publish-gated surface and the first one designed to leave the site. Every prior surface waited for a reader to arrive. This one lives in someone else's README and sends them back.

2/ Twelve publish-gated surfaces shipped before today — trajectory CSV, chart SVG, Jupyter notebook, signal.json, archive ZIP, and seven others. All pull-based: a reader visits MiroShark, fetches an artifact, leaves. None were designed to live somewhere else.

3/ badge_service.py (330 lines, stdlib only — xml.etree.ElementTree, no other dependencies) renders a 20-pixel flat SVG. Shields.io-compatible. Direction and confidence derive from compute_signal — the same function signal.json uses. 22 offline tests. 29th zero-dependency PR.

4/ Twelve surfaces were endpoints — places a reader had to find. PR #94 inverts that: the badge embeds anywhere. A third-party README, a blog post, a tool's docs page. Each one is a discovery point MiroShark didn't have to build. The funnel now runs in both directions.

5/ 22 tests, zero new dependencies — the 29th streak PR. Status Badge SVG is merged and in production: https://github.com/aaronjmars/MiroShark/pull/94

(article: articles/thread-2026-05-21.md)
