# Economics Built Its Models on a Person Who Has Never Existed

There is a character who appears in nearly every macroeconomic model of the last century. Median wage. Average preferences. Stable risk tolerance. Responds to price signals exactly as theory predicts. Economists call her the representative agent.

She has never been a real person. And this has consequences.

## The Theorem That Broke the Framework

The mathematical case against her was built in the 1970s. Working independently, Sonnenschein, Mantel, and Debreu proved that for any aggregate demand curve you can draw, there exists some collection of individually rational consumers who would produce it. The implication runs the wrong direction: aggregate behavior tells you almost nothing about the individuals behind it. You can't derive the representative agent from the population. You have to assume her at the start and average everyone else away in the process.

What's destroyed in that averaging: distributional information. Who holds the debt. Whose spending changes when rates rise. Which segments absorb a shock first versus which pass it through. A [2025 challenge in the Economic Journal](https://academic.oup.com/ej/advance-article/doi/10.1093/ej/ueaf104/8323145) called distributional dependence "a generic feature of heterogeneous agent models" that representative-agent frameworks cannot replicate — not approximately, but structurally. Heterogeneous models have been outperforming averaged ones since the 1990s. They reproduce crises the representative agent misses: who defaults first, which sector contracts, how a shock propagates through an uneven balance sheet.

The field knew this for decades. The representative agent survived not because she was right but because she was tractable.

## The Lobster Fishery That Runs on Six Officers

Elinor Ostrom won the 2009 Nobel Prize in Economics by running the same argument through fieldwork. Her research on commons — fisheries, irrigation systems, forests — showed that heterogeneous communities with different stakes, knowledge, and time horizons routinely governed shared resources better than any model built around a single representative actor predicted.

The [Maine lobster fishery](https://centerforneweconomics.org/publications/polycentricity-complexity-and-the-commons/) is the example with the cleanest numbers. Harbor gangs manage local territories under informal enforcement; state conservation law protects breeding stock system-wide. The whole system operates with six patrol officers for 6,800 fishermen. It works because lobstermen aren't interchangeable — different boats, territories, seasons, knowledge — and governance adapted to that heterogeneity rather than averaging over it.

Ostrom was direct about why polycentricity beats central control: "If the region were regulated by a single governing agency, one out of ten policy changes would be failures for the entire region. If designing rules were delegated to three genuinely independent authorities, the probability that a failure would simultaneously occur would be reduced from 1/10 to 1/100."

The representative agent doesn't just describe the wrong person. It concentrates failure risk.

## The Same Fork in Simulation

Modern simulation tooling has arrived at the same architectural choice.

The mainstream approach — synthetic user research — runs the representative-agent logic. Define a persona for a demographic segment. Collect N independent responses. Aggregate. Fidelity on individual decisions is [real: 85–90% alignment against human panels](https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide) on purchase intent, concept ranking, price sensitivity. What the averaging removes — the same thing it removed in macroeconomics — is distributional dynamics. N personas answering a question independently isn't a population. It's N parallel measurements of the same representative agent.

MiroShark's `backend/wonderwall/` is the opposing structural bet. Four interacting layers: `social_agent/` (the persona substrate), `social_platform/` (where agents post and encounter each other's content), `environment/` (world-state tracking across rounds), `clock/` (time-progression so round two differs from round one). Agents don't answer a question. They produce content, see what others produced, and update. The distributional dynamics — who shifts first, which subgroups amplify or suppress — become the observable output.

Commit `165118d` (PR #198) shows how seriously the heterogeneity is operationalized. It decoupled each agent's language locale through the `ThreadPoolExecutor` in `graph_tools._fallback_interview`. A single shared language setting — hardcoded English prompts — produces outputs that don't reflect what a DE- or FR-locale community actually generates. Same failure Ostrom named in a different context: one policy for everyone produces the wrong result for almost everyone.

PR #203 added `LLM_REASONING_MAX_TOKENS` alongside the existing response budget in `backend/app/utils/llm_client.py`. Now agent types can receive different reasoning budgets — an informed-expert persona thinks at different depth than a casual-observer persona before outputting. The cognitive asymmetry that defines how information actually propagates through a real community: operationalized at the LLM-call layer.

## What This Predicts

The representative-agent framework held for fifty years not because economists didn't know about heterogeneity. They knew. It held because tracking distributions was expensive. When compute got cheap, heterogeneous models started compounding.

Same pressure. Same dynamic. Different domain.

Synthetic user platforms will keep improving individual-persona fidelity. For questions that reduce to individual behavior under a stimulus — pricing, message testing, concept ranking — they're the right tool. For questions that depend on how a population's distributional structure evolves — what a community believes after half of it encounters a news event, which subgroups amplify a signal, how a governance decision lands differently across segments with different stakes — the individual-persona architecture can't close the gap. The distributional information was removed at design time.

Ostrom's lobstermen and MiroShark's locale-specific agents make the same structural bet: the dynamics that matter live in the heterogeneity, not the average. Fifty years of macroeconomics proved she was right about fisheries.

---

*Sources:*
- [Trouble with Rational Expectations in Heterogeneous Agent Models](https://academic.oup.com/ej/advance-article/doi/10.1093/ej/ueaf104/8323145) — Economic Journal (Oxford), 2025; distributional dependence as a generic feature of heterogeneous agent models; the structural failure of representative-agent macro
- [Polycentricity, Complexity, and the Commons](https://centerforneweconomics.org/publications/polycentricity-complexity-and-the-commons/) — Schumacher Center for a New Economics; Ostrom's polycentric design; Maine lobster fishery (6 officers, 6,800 fishermen); failure-probability reduction from 1/10 to 1/100
- [Synthetic Consumers: A Practical Guide](https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide) — PyMC Labs; 85–90% fidelity on individual purchase decisions; structural ceiling on distributional dynamics
- [MiroShark — aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) — wonderwall/ directory (social_agent/, social_platform/, environment/, clock/); commit 165118d / PR #198 (locale-per-agent decoupling); PR #203 / LLM_REASONING_MAX_TOKENS in llm_client.py
