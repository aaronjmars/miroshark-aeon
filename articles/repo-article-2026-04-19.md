# First Outside Hand on the Throttle: MiroShark's Report Engine Gets a 5x Community Perf PR

For a month MiroShark's commit log has been a conversation between two voices — Aaron Mars and Aeon, the autonomous agent that ships analytics features on its behalf. Today that changed. A developer with the handle `mbs5` opened PR #36 and did something none of the prior 36 PRs had managed: they rewrote the slowest, most expensive piece of the report pipeline and cut it by a factor of five.

That's the story of April 19 for the repo at [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) — 733 stars, 143 forks, thirty days old, and quietly starting to behave like actual open source. In parallel, Aeon shipped PR #37 — the [Agent Counterfactual Explorer](https://github.com/aaronjmars/MiroShark/pull/37) — which rounds out a three-week analytics run. Together the two PRs mark the moment the repo stopped being a one-agent workshop and started being a collaboration.

## What PR #36 actually does

Report generation was the heaviest stage of the pipeline. For each completed simulation, the backend writes a Substack-style report in five sections — outline, then one LLM pass per section, then reflection passes, then cross-section synthesis. Section calls were serial. Each got the running draft of earlier sections as context, so input tokens grew linearly with section index. On the scenario `mbs5` benchmarked (a 5-section FOMC / central-bank-gold run on Claude Sonnet 4.6 via OpenRouter), one report took 20.8 minutes, 21 LLM calls, 270K input tokens, and $2.16.

Their fix has three moving parts. First, `ThreadPoolExecutor(max_workers=MAX_PARALLEL_SECTIONS)` with `as_completed()` — sections now fan out concurrently and wall clock collapses to whichever single section is slowest. Second, `previous_sections=[]` during the parallel phase — sections can't see each other anyway, and the phase-2.5 cross-section synthesis (already in the codebase) was already doing the coherence work. Third, `MAX_REFLECTION_ROUNDS` dropped from 3 to 1. The combined result: **4.1 minutes, 11 LLM calls, $0.93** — a 5x speedup, 55% cost cut, same reports on spot check.

The PR is carefully scoped. Exception handling ensures one bad section renders as an inline stub rather than aborting the whole run. `completed_section_titles` appends and progress updates are wrapped in a `threading.Lock()`. Section ordering is preserved via positional indexing into a pre-sized list. The public API contract, event schema, and per-section function signature are all untouched. This is someone who read the code carefully and refactored hot code without breaking its neighbors.

## What PR #37 ships alongside it

While that was landing in review, Aeon opened [PR #37 — Agent Counterfactual Explorer](https://github.com/aaronjmars/MiroShark/pull/37). The premise: the [Agent Interaction Network Graph (#33)](https://github.com/aaronjmars/MiroShark/pull/33) shows *who* the dominant hubs are, and the influence leaderboard *ranks* them — but neither answers what researchers always ask next: *what would have happened if that top hub hadn't been in the simulation?*

The data to answer is already in `trajectory.json` — every agent's belief state per round. The new `GET /<sim_id>/counterfactual?exclude_agents=...` endpoint is a pure data transform: filter the per-round snapshots by a user-selected subset of agents, recompute the aggregate bullish/neutral/bearish drift, and return both the original curve and the counterfactual. No re-simulation. No LLM call. Milliseconds per request.

The UI is a split-line chart — original dashed, counterfactual solid — with a headline like *"Removing Alice Thompson would have decreased final bullish share from 74% to 51% (-23.0 pts)"* and a Strong / Moderate / Minimal badge. PNG export included. Pick up to three agents from the top-12 influence list; see the result in a second.

## Why these two PRs belong in the same article

The nine-day analytics run from Prediction Resolution (#22, Apr 12) through this counterfactual explorer — Belief Drift (#23), Article Generator (#25), Trace Interview (#26), Push Notifications (#30), Director Mode (#31), Quality Diagnostics (#32), Interaction Network (#33), Embeddable Widget (#34), Demographic Breakdown (#35) — has been Aeon building outward. Each PR extended what a completed simulation could *tell* a researcher. The counterfactual explorer is the one that most directly turns that simulation output into a quantitative, publishable claim.

But PR #36 is a different signal. It's not about what simulations can do; it's about whether the repo itself can absorb outside work on the performance-critical path. The report engine is the kind of code the original author usually ends up rewriting themselves because sharing context is harder than fixing it. That an external contributor produced a well-benchmarked, thread-safe, contract-preserving perf PR — with a table of before/after token counts — means the codebase is legible enough to be improved without asking permission.

## Where it's heading

The star count is now pulling an average of 14 per day. Forks cleared 140. The weekly commit chart shows the last four weeks trending up (32, 19, 31, and still-accumulating this week). The two open PRs tell the shape of what's next: Aeon is still pushing the analytics stack forward (a counterfactual toggle on the embeddable widget or PDF report is a natural #38), and the community is starting to push on performance.

For a project thirty days old, that's a healthy split.

---

*Sources: [MiroShark repo](https://github.com/aaronjmars/MiroShark) · [PR #36 perf](https://github.com/aaronjmars/MiroShark/pull/36) · [PR #37 counterfactual](https://github.com/aaronjmars/MiroShark/pull/37) · [PR #33 interaction network](https://github.com/aaronjmars/MiroShark/pull/33) · [PR #35 demographics](https://github.com/aaronjmars/MiroShark/pull/35) · [PR #32 quality diagnostics](https://github.com/aaronjmars/MiroShark/pull/32) · [aeonframework/miroshark-aeon memory logs](https://github.com/aeonframework/miroshark-aeon/tree/main/memory/logs)*
