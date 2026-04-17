# A Map of Who's Simulating What — And the Gap Nobody's Filling

If you wanted to simulate how a population would react to a piece of news last year, your options were scattered across four different software categories, none of which talked to each other. In April 2026, the landscape hasn't consolidated. It's gotten more crowded. And the most interesting thing about the map isn't who's on it — it's the gap in the middle.

## The Four Quadrants

The first quadrant is the oldest. **Classical agent-based modeling** tools like Mesa (3,600 GitHub stars, first commit in 2014), NetLogo, and MASON have been the standard for simulating complex systems for decades. Mesa 4 is in active development; researchers use these tools to model everything from epidemics to traffic flow to urban sprawl. The agents follow mathematical rules. They don't use language models. They're excellent for studying emergent behavior in systems where the rules are known — but they can't simulate a Twitter argument, because a Twitter argument is conducted in natural language with no fixed ruleset.

The second quadrant arrived in late 2024. **Academic LLM social simulation** is led by OASIS, a research platform from CAMEL-AI that now has 4,300 stars on GitHub. OASIS was designed to scale: its paper title promises "One Million Agents," and it delivers infrastructure for running LLM-driven agents on simulated versions of X and Reddit. It replicates group polarization, information cascades, and herd effects. What it doesn't include is a way to verify whether those simulated effects predicted anything real. OASIS is infrastructure — a research telescope, not an observatory with a logbook.

The third quadrant is commercial. **Artificial Societies**, a London-based startup that launched in mid-2025, sells social simulation as market research. Their platform generates 20 to 300 AI personas per run, tests ad campaigns and product messaging against simulated audience reactions, and claims over 80% accuracy in predicting social media performance — compared to 67% for Claude Sonnet and 60% for GPT-4o in their internal benchmarks. At $40/month for unlimited simulations, it has a clear business model. But the scope is narrow: it answers "will this LinkedIn post perform?" not "what happens to public sentiment if this policy drops?"

The fourth quadrant is the loudest. **AI agent orchestration frameworks** — CrewAI, LangGraph, AutoGen, MetaGPT — dominate the multi-agent conversation in 2026. These tools build agents that *do things*: execute tasks, manage workflows, write code, process documents. CrewAI has the lowest barrier to entry (20 lines to start). LangGraph is the most production-ready for stateful systems. Microsoft has shifted AutoGen to maintenance mode in favor of its broader Agent Framework. None of them simulate social dynamics. They orchestrate labor, not opinion.

## The Gap

Draw a two-axis chart. One axis runs from "mathematical rules" to "language-model reasoning." The other runs from "infrastructure" to "complete analytical product." Mesa sits at mathematical-rules-plus-infrastructure. OASIS sits at LLM-reasoning-plus-infrastructure. Artificial Societies sits at LLM-reasoning-plus-product, but narrowed to marketing. The orchestration frameworks are off the chart entirely — they're not simulating anything, they're executing.

The gap is in the LLM-reasoning-plus-analytical-product quadrant, scoped to open-ended questions rather than marketing tests.

That's where MiroShark landed.

## What Fills the Gap

MiroShark is an open-source simulation engine — 708 GitHub stars and 135 forks in its first 25 days — that generates hundreds of LLM-powered agents reacting across simulated Twitter, Reddit, and Polymarket simultaneously. Upload a document (an earnings call, a policy draft, a news article) and the agents post, argue, shift stances, and trade. That much is structurally similar to OASIS, though at a different scale.

What separates it from the infrastructure layer is the analytical stack built on top. In the past ten days, MiroShark has shipped:

- **Quality Diagnostics** — a health badge computed from participation rate, stance entropy, convergence speed, and cross-platform interaction rate. It tells you whether a simulation's output is trustworthy before you act on it.
- **Agent Interaction Network** — a force-directed graph of who influenced whom, with echo chamber scoring, bridge agent detection, and platform filters. It reveals the emergent social structure that the raw simulation output buries.
- **Prediction Resolution** — record what actually happened after a simulation, compute accuracy against real Polymarket prices, and build a track record across runs.
- **Trace Interview** — select any agent from the influence leaderboard and interrogate it about its logged behavior. The responses are grounded in the agent's actual posts and actions, not hallucinated after the fact.
- **Director Mode** — inject breaking events mid-simulation and watch how the agent population responds. Fork the simulation, inject a different event, compare the belief drift charts.

No tool in any of the four quadrants offers this combination. Mesa can't reason in language. OASIS doesn't verify predictions. Artificial Societies doesn't let you inject events or interrogate agents. The orchestration frameworks aren't simulating at all.

## What the Map Tells Us

The fragmentation in this landscape isn't accidental. It reflects a genuine architectural tension: simulation tools optimized for scale (OASIS) tend to sacrifice analytical depth, while tools optimized for insight (Artificial Societies) tend to sacrifice scope. Classical ABM tools are rigorous but can't handle the unstructured nature of social discourse. Orchestration frameworks are powerful but pointed in the wrong direction for understanding collective behavior.

The bet MiroShark is making — whether deliberately or by momentum — is that the right entry point is neither scale nor scope but *accountability*. A simulation that can't tell you whether it was right is a toy. A simulation that tracks its own accuracy, lets you stress-test its outputs, and shows you why its agents did what they did is an instrument.

The ecosystem map will keep shifting. OASIS could add an analytics layer. Artificial Societies could open up beyond marketing. Mesa could integrate LLM agents. But right now, the gap between infrastructure and instrument is where the most interesting engineering is happening — and it's being filled from the open-source side, one pull request at a time.

---
*Sources: [Mesa — GitHub](https://github.com/mesa/mesa) (3,597 stars) · [OASIS: Open Agent Social Interaction Simulations](https://arxiv.org/abs/2411.11581) (4,314 stars) · [Artificial Societies — SiliconANGLE](https://siliconangle.com/2025/07/30/ai-startup-artificial-societies-simulates-behavior-target-audiences-speed-market-research/) · [Multi-Agent Frameworks Explained for Enterprise AI Systems](https://www.adopt.ai/blog/multi-agent-frameworks) · [CrewAI vs LangGraph vs AutoGen — DataCamp](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen) · [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) (708 stars)*
