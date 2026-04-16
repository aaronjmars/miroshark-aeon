# Break It Mid-Run: MiroShark's Director Mode Turns Simulation Into Controlled Experiment

Most multi-agent simulation platforms let you set up a scenario and watch it play out. MiroShark now lets you throw a wrench into the middle.

Director Mode, merged today as [PR #31](https://github.com/aaronjmars/MiroShark/pull/31), introduces mid-simulation event injection — users can type a breaking event like "Central bank raised rates by 100 basis points" or "CEO just resigned" and every agent in the simulation receives it at the next round boundary. The event propagates through Twitter posts, Reddit threads, and Polymarket trades simultaneously, and the belief drift chart marks the injection point with an amber dashed line so you can see exactly when the shock hit and how sentiment shifted.

This is not a cosmetic feature. It is the difference between observation and experimentation.

## What Director Mode Actually Does

The implementation is deceptively simple. A file-based event queue (`director_events.py`) handles atomic writes. The simulation loops in `run_parallel_simulation.py` check for pending events at each round boundary and inject them using a marker-replace pattern into every agent's context. Two new API endpoints — `POST /director/inject` and `GET /director/events` — connect the frontend's Director panel to the backend queue.

The frontend work is where the user experience comes together. A Director button appears during active simulations, opening an injection panel where users can describe any event in natural language. Once injected, timeline banners mark the event in the simulation feed, and the belief drift chart (itself only three days old, from [PR #23](https://github.com/aaronjmars/MiroShark/pull/23)) renders event markers at the exact round of injection.

The total footprint: six files, 724 lines of new code.

## The Experimental Control Stack

Director Mode does not exist in isolation. Over the past week, MiroShark has quietly assembled a full experimental control stack:

- **Fork** ([PR #17](https://github.com/aaronjmars/MiroShark/pull/17)) — clone any completed simulation with the same agent pool and run it again under different conditions.
- **Belief Drift** ([PR #23](https://github.com/aaronjmars/MiroShark/pull/23)) — stacked area chart showing bullish/neutral/bearish stance distribution per round, with consensus detection.
- **Prediction Resolution** ([PR #22](https://github.com/aaronjmars/MiroShark/pull/22)) — record real-world outcomes and compare against what the agents predicted.
- **Trace Interview** ([PR #26](https://github.com/aaronjmars/MiroShark/pull/26)) — interrogate individual agents about their logged behavior after a simulation ends.
- **Director Mode** ([PR #31](https://github.com/aaronjmars/MiroShark/pull/31)) — inject exogenous shocks mid-run.

Combined, these features form a perturbation analysis pipeline. Fork a simulation, inject a different event, compare belief drift charts side by side, check which agents changed their stance, interview the ones that did not. That is a research workflow, not a demo.

## Why This Matters Now

The 27th International Workshop on Multi-Agent-Based Simulation ([MABS 2026](https://mabsworkshop.github.io/)) convenes next month in Paphos, Cyprus. Academic frameworks like OrgForge are publishing structured event buses for verifiable ground truth in organizational simulation. The research community is converging on a shared need: the ability to introduce controlled perturbations and measure their downstream effects across agent populations.

MiroShark is arriving at the same destination from the open-source side. No conference paper, no institutional backing — just a developer shipping features at a pace that has attracted 698 GitHub stars and 132 forks in under four weeks. The project has merged 12 pull requests since April 9, averaging nearly two per day, with contributions split between the maintainer (Aaron Mars) and an autonomous agent (Aeon) running on GitHub Actions.

The broader agentic AI landscape is still obsessed with agents that act. MiroShark's bet is on agents that react — to documents, to each other, and now to events that arrive mid-stream. The distinction matters because simulation-as-experimentation produces falsifiable outputs. You can fork the run, change the input, and check whether the result changes. That is a standard of evidence that most agent frameworks cannot meet.

## What Comes Next

With Director Mode in place, the next natural moves are replay (scrubbing through completed simulations round by round), multi-document comparative runs (same agents, two documents, controlled analysis), and an embeddable simulation widget for sharing results outside the app. All three appeared in today's [repo-actions ideation](https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-04-16.md). The question is no longer whether MiroShark can simulate public reaction — it is whether it can become the standard instrument for studying it.

---
*Sources: [MiroShark GitHub](https://github.com/aaronjmars/MiroShark), [MABS 2026](https://mabsworkshop.github.io/), [OrgForge](https://arxiv.org/html/2603.14997v2), [AgentOS comparison](https://docs.agentos.sh/blog/2026/04/13/mars-genesis-vs-mirofish-multi-agent-simulation)*
