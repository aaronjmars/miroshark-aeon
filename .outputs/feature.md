*Feature Built — 2026-05-27*

Per-Agent Belief Sparklines
MiroShark simulations already show the *swarm's* belief curve — the aggregate read of where all the agents collectively landed each round. This adds the layer underneath: a tiny line chart for *every individual agent*, tracing how that one agent's conviction moved round by round, colored green/gray/red by where they ended up (bullish/neutral/bearish). A new API endpoint serves the raw data; the Embed dialog draws the little charts.

Why this matters:
Until now, the only way to study how individual agents converged — which agent anchored the consensus, whether one cohort (say, financial-analyst personas) aligned before another — was to read the full transcript by hand. There was no surface for the per-agent view. This was the #1 idea in the 2026-05-26 repo-actions batch and the last remaining agent-level visualization gap: aggregate curves and inflection-point summaries existed, but the individual-agent trajectory did not.

What was built:
- agent_sparklines_service.py: New stdlib-only service that reads trajectory.json, computes each agent's scalar belief position per round, and groups it into per-agent series. Returns None (→ 404) when a sim has no per-agent data yet.
- simulation.py: New GET /api/simulation/<id>/agents/sparklines route — publish-gated, 5-minute cache, increments a new agent_sparklines surface counter (the 23rd share surface).
- EmbedDialog.vue + api/simulation.js: A "🤖 Agent trajectories" section — a scrollable list of agents, each rendered as a name + an inline SVG sparkline stroked in the agent's stance color + the final-stance label, plus copyable URL and curl snippet.
- openapi.yaml / docs/API.md / docs/FEATURES.md: Full documentation of the surface and its JSON schema.

How it works:
It's a pure derivation, transposed. Every other surface buckets all agents into one per-round percentage (the aggregate view); this one instead tracks one scalar per agent per round — the same per-topic mean and ±0.2 stance threshold every surface uses, so an agent tagged "bullish" here is "bullish" in the transcript too. Agent names resolve from reddit_profiles.json with an "Agent <id>" fallback. The frontend maps each agent's belief position (clamped to -1..1) onto a 60×16px SVG polyline. Agents are ordered most-bullish-first so the list reads top-to-bottom from strongest bull to strongest bear. A has_per_agent_data flag is false for single-round sims, where a sparkline would just be a dot. 18 offline unit tests cover it; zero new dependencies.

What's next:
Natural follow-ons: a sortable/filterable agent table, or grouping sparklines by demographic archetype to make cohort-level convergence patterns visible at a glance.

PR: https://github.com/aaronjmars/MiroShark/pull/115
