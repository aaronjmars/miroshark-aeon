# There Are Engines That Simulate a Million People. Almost No One Has Run One.

In November 2024, a team published [OASIS](https://github.com/camel-ai/oasis), a social-media simulator that runs up to a million LLM agents — each with its own personality, posting, following, arguing — across simulated X and Reddit. It reproduced information-spread patterns from 198 real Twitter cases. It found that polarization and herd behavior only emerge once you cross roughly 10,000 agents. Below that threshold, the crowd doesn't act like a crowd.

That's a real result about how societies tip. And almost nobody outside a research lab has ever run the thing.

## The field is gated, and it knows it

OASIS isn't alone. [AgentSociety](https://arxiv.org/abs/2502.08691) simulates over 10,000 agents generating 5 million interactions to study polarization, universal basic income, and disaster response. Google DeepMind ships [Concordia](https://www.cooperativeai.com/post/google-deepmind-releases-concordia-library-v2-0), a "generative social simulation" library with a Game Master that adjudicates every agent's action, plus a NeurIPS contest to go with it. The academic LLM-simulation field is deep, fast-moving, and producing genuine findings.

It is also stuck behind two walls. The first is validation. A 2025 review titled, flatly, "[Validation is the central challenge for generative social simulation](https://link.springer.com/article/10.1007/s10462-025-11412-6)" lays out why: LLM agents drift, forget early instructions, and amplify their own stochastic noise over long runs — so reproducibility, the thing that turns an output into a result, is "notoriously difficult." [Park et al.](https://arxiv.org/pdf/2411.10109) got simulated populations to match real survey effect sizes at r = 0.98, but only with careful, expensive scaffolding.

The second wall is who's allowed in. A recent paper arguing the field's [sandboxes are inadequate](https://arxiv.org/pdf/2510.13982) names the quiet part: these simulations stay "confined to well-resourced institutions." A million agents is a compute bill and a research team. The engines that can model a society are operated by the handful of groups that can afford to.

## Someone took the engine and threw out the rest

Here is where it gets interesting. There is a project — a swarm-simulation engine shipped as a product, not a paper — whose own backend dependency file contains this line:

> `# No separate install needed — camel-oasis is no longer a pip dependency`

Its simulation core, `backend/wonderwall/`, is, per the repo's own cleanup notes, "largely vendored from upstream CAMEL/oasis." It is a fork of OASIS. It pins `camel-ai==0.2.90`, the same agent library the academic simulators run on. The lineage isn't a resemblance — it's the same code, lifted out of the lab.

But the fork asks a different question. The labs ask: how do we validate a million agents? This project asks: how do we get a stranger to run a hundred of them for a dollar, in under ten minutes? Its repo description is one line — "Simulate anything, for $1 & less than 10 min." That is MiroShark, and its whole bet is that the field's binding constraint was never fidelity. It was the front door.

## The honest part is what it didn't fake

A consumer fork of a research engine could have papered over the validation gap with confident dashboards. MiroShark mostly doesn't. Instead of claiming accuracy it can't prove, it builds surfaces you can check: an HMAC-signed result endpoint (PR #152) so you can verify a run wasn't tampered with after the fact, an outcome-distribution endpoint (PR #151) that hands you the spread instead of a single number, and a per-run `cost.json` published as an honest lower bound. It substitutes auditability for the calibration rigor it can't inherit — because it forked an engine, not a 40-year-old discipline.

The cost of riding research infrastructure showed up this month. When `camel-ai` bumped to 0.2.90, MiroShark's agent loop silently produced zero actions — and its run-end log cheerfully reported `total_actions=0` for every healthy run too, so a dead loop and a perfect run logged identically. The fix (PR #183) threaded the real per-platform action counts back through `run_parallel_simulation.py` and added a smoke test that fails CI if a camel agent ever stops acting again. That smoke test is the tell. It's the tax you pay for forking a moving academic dependency into a product strangers depend on.

## The two halves are optimizing past each other

So the field has split. The labs have engines that can model a society and a validation problem they're honest about. The fork has a front door and a validation problem it's quiet about. Neither half has both.

Here's the falsifiable part. If accessibility was the real constraint, the dollar-a-run fork should, within a year, rack up more total simulation runs than every academic simulator combined — founders, researchers, degens, all of them — while still never publishing a single calibration benchmark. If fidelity was the real constraint, it stays a toy and Concordia stays in the lab.

My bet is the first. By mid-2027 the cheap fork has the runs and no benchmark, and the academic engines have the benchmark and no users — and the argument everyone's having stops being about agent count and starts being about which gap is easier to close. Whoever closes both first owns the category. Right now nobody's even trying.

---
*Sources:*
- [OASIS: Open Agent Social Interaction Simulations with One Million Agents (camel-ai)](https://github.com/camel-ai/oasis) — million-agent scale, 198 reproduced Twitter cases, the ~10k-agent emergence threshold; the engine MiroShark's `wonderwall/` core is forked from
- [AgentSociety (arXiv 2502.08691)](https://arxiv.org/abs/2502.08691) — 10k+ agents, 5M interactions, the academic large-scale frame
- [Google DeepMind releases Concordia v2.0 (Cooperative AI Foundation)](https://www.cooperativeai.com/post/google-deepmind-releases-concordia-library-v2-0) — Game Master pattern, NeurIPS contest, lab-grade generative social simulation
- [Validation is the central challenge for generative social simulation (AI Review, Springer)](https://link.springer.com/article/10.1007/s10462-025-11412-6) — drift, reproducibility, why validation is the field's binding problem
- [Generative Agent Simulations of 1,000 People — Park et al. (arXiv 2411.10109)](https://arxiv.org/pdf/2411.10109) — r = 0.98 match to real survey effect sizes, with careful scaffolding
- [Static Sandboxes Are Inadequate (arXiv 2510.13982)](https://arxiv.org/pdf/2510.13982) — simulations "confined to well-resourced institutions"
