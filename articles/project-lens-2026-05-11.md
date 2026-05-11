# The AI Forecasting Stack Has Four Neighborhoods. Most Tools Pick One.

When someone says they're building "AI prediction tooling" in 2026, the first useful question is *which stack* they mean. There are four of them, and they do not share a city.

The first stack is **prediction markets**. Polymarket clears [more than $500M of monthly volume](https://www.alphascope.app/blog/polymarket-alternatives-2026). Kalshi is the CFTC-regulated U.S. venue with ~900 live contracts. They are settlement engines. Their job is to take a binary question with a real-world resolver and price it.

The second stack is **forecasting platforms**. Metaculus is the canonical one — a reputation-and-calibration system where humans submit probabilities on long-horizon questions and get scored against ground truth. The platform discipline is *calibration*, not liquidity.

The third stack is **multi-agent frameworks**. [LangGraph, AutoGen, CrewAI, MetaGPT, CAMEL](https://www.intuz.com/blog/top-5-ai-agent-frameworks-2025). These are developer SDKs. AutoGen lets you orchestrate "a dynamic conversation" between agents; MetaGPT spins up a simulated software company with role assignment; CAMEL is "the first and the best multi-agent framework" by its own catchphrase. They are scaffolding. They do not run scenarios for you — they let you build one.

The fourth stack is **reproducibility and citation infrastructure**. Papers with Code, OpenReview, the DOI system, the Inspect framework for evals. The job is to make a result *durable* — bytewise stable, addressable, and re-runnable by someone who wasn't there.

These four stacks have surprisingly little overlap. They were built by different communities, at different times, for different users. And the gap between them is where one specific kind of tool is starting to live.

## What sits in the gap

Imagine a question like: *what happens to a lending protocol's TVL if its largest collateral asset depegs 13% in an hour?*

A prediction market can't price it — there's no public outcome to settle on, and the time window is too short to attract liquidity. A forecasting platform can crowdsource a probability, but it can't show you *what the path looks like*. An agent framework can let an engineer build something, but it won't ship a finished product. A reproducibility system can preserve a result, but only after someone produced one.

What's missing is a thing that *runs* the scenario, *records* the run as a citable artifact, and *publishes* it through enough surfaces that the result can travel. That's a different category. Call it the **simulation substrate** layer.

MiroShark is one project in that category. Stanford's Smallville-style generative-agent experiments are upstream of it conceptually but live on the research side. There is no settled name for the layer yet, which is part of why it confuses people — the most common opening question MiroShark gets is "is this a prediction market?" The answer is no, and the answer also reveals why the question is the wrong one.

## What's complementary, what's competing, what's adjacent

Three columns on the same map.

**Complementary.** Prediction markets and simulators want different things from the same questions. Polymarket needs a clear resolver and short clock; MiroShark wants a messy question and a path. A user-facing app that pairs them looks obvious in hindsight — "here's the market price, here's the simulated path" — but neither side has reached for it yet. Same for citation infrastructure: MiroShark's [reproduce.json schema](https://github.com/aaronjmars/MiroShark/pull/75) shipped May 8 and is functionally a DOI for a sim run. Bytewise-stable JSON, SHA-256 as the citation key. It plugs into the citation column rather than competing with it.

**Adjacent.** Multi-agent frameworks like AutoGen and CrewAI overlap in primitives — agents, rounds, message passing — but diverge in goals. Frameworks ship a toolkit; MiroShark ships an opinionated product on top of a toolkit-like substrate. The two coexist the way a database engine coexists with a finished SaaS app built on it.

**Competing.** Two things actually compete with simulators in this layer. The first is "just ask GPT what would happen" — the zero-effort baseline. It loses on reproducibility (no stable output), provenance (no lineage), and depth (no rounds of disagreement). The second is closed prediction APIs from large labs, which are still mostly internal. Both define the floor the substrate layer has to clear.

## Why the surface layer is the real moat

The interesting design choice in this category is not the agents — every project has agents — it's what gets *recorded*. MiroShark's `sim_dir/` substrate now exposes 11 surfaces over the same run: a public viewer, a thread export, a webhook log, [surface-usage stats](https://github.com/aaronjmars/MiroShark/pull/74), reproduce.json, a [lineage graph](https://github.com/aaronjmars/MiroShark/pull/76), trending sort, an OpenAPI surface, an MCP server, a shareable scenario pre-fill link, and a webhook with HMAC signing (PR #79, opened today). Each is a way for the run to be cited, embedded, or re-derived.

Each individual surface is unremarkable. The compounding only shows when they wire into each other — surface-stats counts events from the viewer, the lineage graph, and reproduce.json; the trending sort ranks by that counter; the citation hash points back to the substrate that the surfaces all read from. The moat is not the simulator. The moat is the surface network.

## Where to look from here

If you're orienting yourself in this space, the useful map is not "AI startups vs. crypto startups vs. forecasting startups." It's *which stack do they belong to* — settlement, calibration, framework, reproducibility, or substrate. Most tools live in one. The interesting tools sit at a seam between two.

Substrate-layer projects are easy to misread as either prediction markets without liquidity or frameworks without flexibility. They are neither. They are the thing the other four neighborhoods were going to need eventually, and which only one of them — citation infrastructure — was already paying attention to.

---
*Sources: [Polymarket Alternatives 2026 — Alphascope](https://www.alphascope.app/blog/polymarket-alternatives-2026), [Top 5 AI Agent Frameworks 2026 — Intuz](https://www.intuz.com/blog/top-5-ai-agent-frameworks-2025), [MiroShark PR #74 (surface analytics)](https://github.com/aaronjmars/MiroShark/pull/74), [MiroShark PR #75 (reproduce.json)](https://github.com/aaronjmars/MiroShark/pull/75), [MiroShark PR #76 (lineage navigator)](https://github.com/aaronjmars/MiroShark/pull/76)*
