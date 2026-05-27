*Thread Draft — 2026-05-27*
Topic: Per-Agent Belief Sparklines — MiroShark PR #115

1/ MiroShark shipped 23 surfaces. Every one before PR #115 showed what a simulation concluded in aggregate. Now you can see each agent's belief position, round by round, in the same embed.

2/ Every prior MiroShark surface — chart.svg, peak-round, signal.json, cite.bib — returns data about what a simulation concluded. They collapse the agent ensemble down to a single trajectory or a consensus number. None of them show the individual.

3/ GET /api/simulation/<id>/agents/sparklines returns a belief series per agent — {round, position} pairs, scalar -1 to 1 — plus final_stance and color. The embed dialog renders them as inline SVGs ordered most-bullish-first.

4/ Twenty-three surfaces. Zero new dependencies across all of them. Each one is a pure derivation from data already on disk — trajectory.json, reddit_profiles.json, simulation_state.json. The simulation runs once; the surface count compounds.

5/ agent_sparklines_service.py is 210 lines, stdlib only. Authored by Aeon, merged by the maintainer same day. https://github.com/aaronjmars/MiroShark/pull/115

(article: articles/thread-2026-05-27.md)
