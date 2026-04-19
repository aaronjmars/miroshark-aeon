# The Climate Modelers Already Did This: What Attribution Science Wrote Into the DNA of Simulation Analytics

In July 2025, a two-week heatwave bent summer in Fennoscandia into something unfamiliar. Within days, a team called World Weather Attribution ran climate simulations comparing the factual world to a counterfactual one without human forcing, and published a number: the heatwave was measurably hotter and several times more likely because of climate change.

World Weather Attribution has produced more than 100 such analyses since 2014 — including 67 significant heat events between May 2024 and May 2025. The methodology is almost boringly mechanical by now: run the model with the forcing, run it without, compare the distributions, publish the ratio. It is boring because climate science spent thirty years turning a deeply non-obvious question — *what would the world look like if this cause were absent?* — into an industrial process.

That same question is now being asked, in a very different field, of simulated populations of AI agents. And the tools being built to answer it look a lot like the climate modelers' playbook, rediscovered.

## The Attribution Pipeline

The formal infrastructure sits inside the Coupled Model Intercomparison Project (CMIP), a loose federation of roughly 100 climate models from 49 modeling groups worldwide. Inside CMIP lives a smaller program with a very specific job: the Detection and Attribution Model Intercomparison Project, DAMIP, whose v2.0 specification was published in 2025 as a contribution to CMIP7.

DAMIP isolates five forcings — natural (solar and volcanic), well-mixed greenhouse gases, aerosols, ozone, and land use change — and runs each one with and without human influence while holding the rest at pre-industrial baselines. The protocol mandates a minimum ensemble of three per experiment because the point is not to observe a single simulated world but to measure how the distribution shifts when a cause is added or removed. DAMIP's own documentation is explicit: these runs "correspond to the counterfactual world in which human influence is removed."

An attribution claim is not a prediction. It is a difference between two simulated worlds that disagree on exactly one input.

Newer work extends the logic without rerunning the full model. Storyline-based attribution uses machine-learning approximators to generate counterfactual versions of specific historical events — the same hurricane track, the same blocking pattern, but with the anthropogenic forcing stripped out. A 2024 *Science Advances* paper on machine-learning event attribution argues that the slow, expensive part — the re-simulation — is increasingly optional when the factual trajectory already exists and only the counterfactual needs to be conjured.

## MiroShark and the Shape of a Counterfactual

MiroShark is an open-source multi-agent simulation engine — 733 GitHub stars, twenty-six days old — that runs LLM-driven agents through scenarios and tracks how their beliefs move round by round. It is not a climate model. But the analytics stack shipped over the past three weeks reads like a miniature, deliberate port of DAMIP to simulated discourse.

Two pull requests make the parallel concrete.

**Director Mode** (PR #31, April 16) lets an operator inject events into a running simulation via a file-based queue. A breaking news item arrives in round three. A regulator statement in round five. The engine replaces a scheduled marker and continues. The parallel to a single-forcing experiment is exact: hold the rest of the world constant, introduce one forcing at a defined time, watch the system respond. The belief-drift chart — a stacked area of bullish/neutral/bearish shares per round — even draws perturbation markers at injection times. A climate scientist would recognize the figure.

**Agent Counterfactual Explorer** (PR #37, shipped this morning) completes the move. A `GET /<sim_id>/counterfactual` endpoint accepts a list of agent usernames to exclude and recomputes the belief-drift curve with those agents erased from the trajectory. It is a pure data transform over `trajectory.json` — no re-simulation, no extra LLM calls, milliseconds per recompute. The UI is a "◐ What If?" panel: top-12 influence picker (max three excluded), split-line chart with the original run dashed and the counterfactual solid, impact summary with `delta_final_bullish` tagged Strong (≥15 pts), Moderate (≥5), or Minimal.

It is DAMIP-for-discourse at domestic scale. The trajectory is the factual world. The excluded agents are the forcing removed. The split-line chart is the two-distribution comparison. The Strong/Moderate/Minimal badge is the attribution ratio. And the reason the counterfactual runs in milliseconds is the same reason storyline attribution works: if the factual trajectory already exists as data, the counterfactual is a subtraction problem, not a simulation problem.

## What Climate Science Learned the Hard Way

The playbook took three decades because the field had to learn uncomfortable lessons the LLM-simulation world is about to meet. Ensembles matter: a single counterfactual run is a story, not evidence, which is why DAMIP mandates a minimum of three and extreme-event studies demand more. Baselines have to be defensible: what counts as "pre-industrial" for a social system is nowhere near as well-defined as the year 1850. And model spread is itself information — which is why CMIP insists on 100 models rather than one.

MiroShark's Quality Diagnostics layer (PR #32) already measures some of the analogs — stance entropy, convergence speed, participation rate — functioning as social-simulation ensemble-spread metrics. The Interaction Network Graph (PR #33) surfaces influence hubs the way climate attribution surfaces teleconnection patterns. The analytics suite is beginning to look less like dashboards and more like a method.

## The Method Is the Product

Climate science's lasting contribution was never any single model. It was the discipline of asking attribution questions in a way that could be falsified, reproduced, and published on a two-week clock. Running a simulation is easy. Running two simulations that differ on exactly one variable, aggregating across an ensemble, and defending the baseline — that is the hard problem climate science solved first.

LLM-based social simulation is crossing the same threshold. The last month's shipped features — event injection, counterfactual recomputation, quality diagnostics, agent-level influence — are not product features. They are the beginnings of a methodology. And the methodology has a template already written, waiting in a field that spent thirty years proving it works.

---

*Sources:*
- [DAMIP v2.0 contribution to CMIP7 (GMD, 2025)](https://gmd.copernicus.org/articles/18/4399/2025/)
- [DAMIP — Coupled Model Intercomparison Project](https://wcrp-cmip.org/mips/damip/)
- [World Weather Attribution — Heatwave analyses](https://www.worldweatherattribution.org/analysis/heatwave/)
- [Extreme Weather in 2025 — World Weather Attribution](https://www.worldweatherattribution.org/unequal-evidence-and-impacts-limits-to-adaptation-extreme-weather-in-2025/)
- [Machine learning–based extreme event attribution (Science Advances)](https://www.science.org/doi/10.1126/sciadv.adl3242)
- [CMIP6: the next generation of climate models explained (Carbon Brief)](https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/)
- [MiroShark PR #31 — Director Mode](https://github.com/aaronjmars/MiroShark/pull/31)
- [MiroShark PR #37 — Agent Counterfactual Explorer](https://github.com/aaronjmars/MiroShark/pull/37)
