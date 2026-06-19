# AI Simulation's Validity Problem Is a Price Problem in Disguise

In March 2026, two researchers published a position paper in the ICML track titled "AI Agents Are Not (Yet) a Panacea for Social Simulation." [Yiming Li and Dacheng Tao](https://arxiv.org/html/2603.00113v1) documented a genuine problem: LLM-agent simulations built as role-playing pipelines are optimized for conversational plausibility, not behavioral validity. They identified three fundamental mismatches between current practice and simulation science, plus five specific technical gaps — evaluation protocols, interaction dynamics, state-update mechanisms, initialization procedures, and information priors. The argument has circulated widely in discussions about whether AI simulations can be trusted for anything important.

The argument is correct. It is also, if you follow its logic carefully, not an argument against simulation. It is an argument against calibrating simulation without iteration. And iteration requires a price you can actually afford to pay.

## The case against agents

The position paper's core objection is that "role-playing plausibility does not imply faithful human behavioral validity." An agent that writes convincingly in the voice of a 30-year-old swing voter does not necessarily behave the way one would in a real information environment. The paper is right about this. But it is right for a reason the paper treats as a footnote: the field hasn't built calibration benchmarks because the field hasn't been able to afford the runs required to build them.

The paper cites [OASIS](https://arxiv.org/abs/2411.11581) — the camel-ai simulator capable of 1 million LLM agents, reproducing 198 real Twitter information-spread cases — as an example of what the field can produce. What it doesn't dwell on is what that scale costs. A HuggingFace analysis this year [named LLM evaluation itself](https://huggingface.co/blog/evaleval/eval-costs-bottleneck) a "new compute bottleneck" — the costs of systematic, multi-run calibration have risen fast enough that even well-funded labs are constraining the number of evaluation passes they run. The same structural ceiling appeared in a different context in June: [Meta conscripted 6,500 engineers as data labelers](https://www.techtimes.com/articles/318586/20260617/meta-conscripts-6500-engineers-data-labelers-revolt-exposes-ai-training-ceiling.htm) when synthetic data hit its training ceiling, forcing human labor back into the pipeline. Cost is the recurring character across AI's current quality problems — not just in simulation.

The five technical gaps Li and Tao identify are not exotic research problems. They are the kind of problems you solve empirically — by running many experiments, varying parameters, and observing what changes. You cannot solve them by theorizing harder. You solve them by being able to afford the next run. A meaningful calibration suite for social simulation would need to vary agent count, initialization conditions, question framing, and persona definition across hundreds of runs. At current research compute pricing, that's a funded-lab problem. Most researchers and practitioners aren't running funded labs.

## The infrastructure that makes the critique answerable

There is a simulation engine that chose, at every architectural decision point, to build the primitives you need to run calibration cheaply rather than claim accuracy it couldn't prove.

MiroShark's backend runs on the same agent core as the academic systems — its `backend/wonderwall/` directory is documented in the repo's own cleanup notes as "largely vendored from upstream CAMEL/oasis," the same camel-ai library the million-agent simulations run on. The difference is what the project built around the engine.

[PR #151](https://github.com/aaronjmars/MiroShark/pull/151) added an outcome-distribution endpoint: instead of returning a single directional result, the API returns the spread — how many agent-runs converged on each outcome. That spread is the raw material for calibration. Run the same simulation fifty times with different random seeds and a consistent distribution tells you something; an unstable one tells you something different. Neither fact is discoverable from a single run.

[PR #152](https://github.com/aaronjmars/MiroShark/pull/152) built an HMAC-SHA256-signed result envelope: every simulation's output is cryptographically signed so an integrator can verify, offline, that a result wasn't modified after the fact. This is not accuracy — it is reproducibility, the prerequisite for calibration, because calibration requires being able to trust that the result you're comparing is the result that was actually returned.

[PR #179](https://github.com/aaronjmars/MiroShark/pull/179) surfaced a per-sim cost in a queryable `cost.json`, documented explicitly as a lower bound. If you're building calibration runs and need to know whether you can afford 500 of them, you need to know what each one costs. That endpoint answers the operational question the field avoids asking.

None of these features constitute a validity proof. Together, they constitute a toolkit for building one cheaply — which is precisely what the five technical gaps require.

## What this predicts

The academic field's response to Li and Tao's position paper will not arrive as a theoretical breakthrough. It will arrive as a series of empirical papers — probably 2027 onward — that characterize how LLM-agent simulation results vary by agent count, initialization, persona definition, and question framing, with enough runs to make the claims statistically meaningful.

Those papers will have been enabled by researchers who ran thousands of simulations for a few hundred dollars while working on something else, noticed patterns in the distribution data, and realized they had calibration observations by accident. The five technical gaps will close the way every empirical gap in science has closed: someone ran enough cheap experiments to see what was actually happening, rather than what theory predicted.

Here is the falsifiable version: by 2028, the first peer-reviewed calibration benchmark for LLM social simulation will cite run counts above 1,000 — and the infrastructure enabling those runs will be priced below $5 per simulation. The critique that agents can't be trusted for social simulation is correct about today's validation gap. It is wrong to treat that gap as evidence that agents can't produce the runs needed to close it. The ceiling is a price ceiling. It will move.

---
*Sources:*
- [Position: AI Agents Are Not (Yet) a Panacea for Social Simulation — Yiming Li, Dacheng Tao (arXiv 2603.00113)](https://arxiv.org/html/2603.00113v1) — the position paper argument: three mismatches, five technical gaps, "role-playing plausibility doesn't imply faithful human behavioral validity"
- [OASIS: Open Agent Social Interaction Simulations with One Million Agents (arXiv 2411.11581)](https://arxiv.org/abs/2411.11581) — million-agent scale; the upstream simulator MiroShark's `backend/wonderwall/` core is forked from
- [AI evals are becoming the new compute bottleneck — HuggingFace](https://huggingface.co/blog/evaleval/eval-costs-bottleneck) — calibration itself is a compute cost problem the field is actively grappling with
- [Meta Conscripts 6,500 Engineers as Data Labelers — TechTimes, June 17 2026](https://www.techtimes.com/articles/318586/20260617/meta-conscripts-6500-engineers-data-labelers-revolt-exposes-ai-training-ceiling.htm) — cost constraints forcing human labor back into AI development pipelines; structural evidence that quality problems and cost problems are the same problem
- [MiroShark — feat: outcome-distribution endpoint (PR #151)](https://github.com/aaronjmars/MiroShark/pull/151) — raw spread data as the primitive for calibration runs
- [MiroShark — feat: signed-result.json HMAC-SHA256 (PR #152)](https://github.com/aaronjmars/MiroShark/pull/152) — reproducibility infrastructure: the prerequisite for cross-run comparison
- [MiroShark — feat: cost.json per-sim USD cost surface (PR #179)](https://github.com/aaronjmars/MiroShark/pull/179) — per-run cost surfaced as a queryable lower bound, answering "can I afford 500 calibration runs?"
