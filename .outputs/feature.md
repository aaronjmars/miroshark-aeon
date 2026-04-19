*Feature Built — 2026-04-19*

Agent Counterfactual Explorer ("What If?")
MiroShark simulations now have a "What If?" panel that lets researchers remove selected agents from a completed run and instantly see how consensus would have shifted — without rerunning anything. Pick 1–3 agents from the top influence leaderboard, hit Recompute, and a split chart appears: the original belief curve alongside the counterfactual one, with a headline like "Removing Alice Thompson would have dropped final bullish share from 74% to 51% — a 23-point swing."

Why this matters:
The Agent Interaction Network Graph (shipped Apr 17) shows *who* the dominant hubs are, and the influence leaderboard ranks them, but neither answers the question every researcher asks next: what would have happened if that hub wasn't in the simulation? Every dominant-node finding on the graph begs this question, and until today there was no way to quantify it without a full rerun. This was idea #3 in yesterday's repo-actions batch — targeted specifically as the most demo-able insight in the entire analytics suite and a publishable-figure feature for academic users.

What was built:
- backend/app/api/simulation.py: New GET /<sim_id>/counterfactual?exclude_agents=name1,name2 endpoint. Resolves usernames to agent IDs via the existing reddit_profiles.json loader, then recomputes per-round bullish/neutral/bearish distributions over a filtered agent set using the same math as the /belief-drift endpoint. Returns original drift, counterfactual drift, delta_final_bullish, delta_consensus_round, impact badge (strong ≥15pts / moderate ≥5pts / minimal), and a plain-English summary.
- frontend/src/components/WhatIfPanel.vue: New overlay component. Agent picker grid of the top 12 influencers (rank + score, max 3 selected), SVG chart rendering original curve dashed and counterfactual curve solid on shared axes with endpoint dots and consensus markers for both series, impact summary card with per-metric deltas and a color-coded impact badge, PNG export.
- frontend/src/components/Step3Simulation.vue: New "◐ What If?" toggle in the analytics button row, wired up to the existing mutual-exclusion logic alongside Influence / Drift / Network / Demographics.
- frontend/src/api/simulation.js: getCounterfactualDrift(simulationId, excludeAgents[]) helper.

How it works:
The counterfactual is a pure data transform over trajectory.json — no LLM calls, no re-simulation, response in milliseconds. A new _drift_from_positions_by_agent helper factors out the per-round stance computation from the existing belief-drift endpoint and accepts an allowed_agent_ids set; None means include all (original), otherwise only agents whose stringified user_id is in the set count. Usernames get resolved via the same _demo_load_profiles() already used by the demographic breakdown, so Reddit-only, Twitter-only, and mixed simulations all work. The frontend panel fetches the influence leaderboard for its agent list so picks map cleanly back to the agent identifiers the backend resolves.

What's next:
Natural follow-ups: counterfactual URL param on the share/embed page (?counterfactual=id1,id2), article generator pulling the "removing X shifted consensus by N points" finding into the narrative when the panel is open, and PDF report inclusion when idea #4 from yesterday's batch lands.

PR: https://github.com/aaronjmars/MiroShark/pull/37
