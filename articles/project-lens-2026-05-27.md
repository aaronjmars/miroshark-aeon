# The 2026 Agent Map Has Two Continents. Almost Nothing Lives in the Strait Between Them.

If you tried to orient yourself in the AI-agent landscape this spring, you'd find two giant landmasses and a confusing amount of empty water between them. On one continent: orchestration frameworks for agents that *do things* — book the flight, file the ticket, run the workflow. On the other: research simulators for agents that *believe things* — populations of synthetic people whose opinions drift, polarize, and cascade. The two continents barely trade with each other. They use different tools, publish in different venues, and optimize for different proofs. Most people building in 2026 only know one of them exists.

This is a map of both — and of a small, odd project that has quietly set up shop in the strait between them.

## The First Continent: Frameworks for Doing

The orchestration side consolidated hard this year. LangGraph became the production default — its graph-based architecture, with checkpointing and durable execution, now powers agents at Klarna, Uber, and LinkedIn, and it overtook CrewAI in GitHub stars in early 2026. CrewAI still claims adoption at roughly 60% of the Fortune 500 on the back of 44,600-plus stars. The biggest move was structural: Microsoft folded AutoGen and Semantic Kernel into a unified Microsoft Agent Framework that hit v1.0 general availability in April 2026, pushing AutoGen — past 54,000 stars in its prime — into maintenance mode. Add OpenAI's Agents SDK, Google's ADK, and Hugging Face's Smolagents, and the patterns have stabilized into four coordination styles: graph-based, role-based, handoff-based, and hierarchical.

Everything here answers one question: *how do I get a team of agents to reliably accomplish a task?* The proof of success is a completed action — a passing test, a closed ticket, a shipped order.

## The Second Continent: Simulators for Believing

The other landmass is older and stranger. Agent-based modeling has simulated belief dynamics for thirty years; LLMs just made the agents articulate. The 2026 flagship is AgentSociety, which generates lives for over 10,000 LLM-driven agents and simulates roughly 5 million interactions, explicitly as a testbed for social questions — polarization, the spread of inflammatory messages, the effect of universal basic income, the impact of external shocks like hurricanes. Smaller projects like `discourse_simulator` model how public attitudes toward immigration shift in response to protests and policy debates.

The proof of success here is different: not a completed action, but an *explained phenomenon*. And the continent has a structural problem its own researchers name plainly. A 2026 review in *Artificial Intelligence Review* puts it in its title: "Validation is the central challenge for generative social simulation." These models are powerful and almost impossible to ground. Worse, their outputs are locked inside PDFs. You cannot `GET` a result from AgentSociety. The science is real; the surface is a paper.

## The Strait: A Belief Simulator You Can Query for a Dollar

[MiroShark](https://github.com/aaronjmars/MiroShark) — 1,205 stars, 255 forks, tagline "Simulate anything, for $1 & less than 10 min" — belongs to neither continent, which is exactly what makes it interesting to locate. It runs multi-agent LLM debates: agents start with priors, exchange arguments, update their beliefs, and settle into a final distribution. That is unmistakably the *second* continent's kind of work — belief dynamics, not task completion.

But it ships like something from the *first* continent. A simulation isn't a paper; it's an endpoint. As of this week the engine exposes its twenty-third consumable surface. `signal.json` (PR [#91](https://github.com/aaronjmars/MiroShark/pull/91), merged May 19) emits `direction` and `confidence_pct` for quant tools. `peak-round` (PR [#108](https://github.com/aaronjmars/MiroShark/pull/108), merged May 26) collapses a full belief trajectory into the round each stance peaks at and its biggest swing. Per-agent belief sparklines (PR [#115](https://github.com/aaronjmars/MiroShark/pull/115), merged May 27) hand back each individual agent's round-by-round opinion series. The whole thing is a Flask backend of small stdlib services and a Vue frontend — not a research cluster.

That combination is the empty cell on both maps. The orchestration frameworks don't simulate populations; they coordinate task-doers. The academic simulators model populations beautifully but can't be queried, integrated, or — per their own literature — easily validated. MiroShark sits in the strait: population-scale belief simulation with a price tag, a latency budget, and a REST surface.

## What Makes the Strait Habitable

A location between two continents is only useful if you can build there. Two design choices make MiroShark's seam load-bearing.

The first is reproducibility, which is precisely the academic continent's open wound. PR [#84](https://github.com/aaronjmars/MiroShark/pull/84) (merged May 15) anchors each finished simulation's `reproduce.json` SHA-256 hash to the OriginTrail Decentralized Knowledge Graph. Given the citation you recover the config; given the config and the same weights you can re-run the simulation; given the run, every surface is determined. It's a partial, engineering-grade answer to the validation problem the *AI Review* paper says nobody has solved — not ground truth, but at least *re-runnability*.

The second is the tell that a project has stopped being a tool and started being a substrate. On May 26 an outside contributor merged PR [#109](https://github.com/aaronjmars/MiroShark/pull/109), adding `ECOSYSTEM.md` — a curated roster of ten products built *on top of* MiroShark, including AntFleet, Crucible, Signa, and Supercompact, with guidelines that explicitly exclude stock forks. This is the "built-with directory" pattern that signals maturity across the first continent — LangGraph has its production roster, MCP its server registry — but inverted. MiroShark isn't asking to be listed in someone else's catalog of frameworks. It published the catalog of what was built on it, and the maintainer didn't write it.

## What the Map Shows

Two forces are reshaping the whole landscape. The protocol layer went open — Model Context Protocol and Agent-to-Agent moved to Linux Foundation stewardship, and every major framework now speaks MCP. And maturity is increasingly measured not by what a project does but by what accretes on top of it; the "built-with" directory is the new milestone.

The strait between doing and believing is narrow and mostly empty, and it may stay that way — task agents and belief simulators may have good reasons not to mix. But the one project parked there suggests the gap is structural, not permanent: somebody wanted population-level belief dynamics with the ergonomics of an API and the provenance of a hash, and the two big continents each had exactly half of it. Whether the strait becomes a trade route is an open question. This week, at least, it stopped being empty.

---
*Sources: [10 AI Agent Frameworks for 2026 (Medium)](https://medium.com/@atnoforgenai/10-ai-agent-frameworks-you-should-know-in-2026-langgraph-crewai-autogen-more-2e0be4055556); [Best Multi-Agent Frameworks in 2026 (Gurusup)](https://gurusup.com/blog/best-multi-agent-frameworks-2026); [AgentSociety (arXiv 2502.08691)](https://arxiv.org/abs/2502.08691); [Validation is the central challenge for generative social simulation (Springer)](https://link.springer.com/article/10.1007/s10462-025-11412-6); [LLM in agent-based social simulation (arXiv 2507.19364)](https://arxiv.org/pdf/2507.19364); [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark); [ECOSYSTEM.md (PR #109, merged)](https://github.com/aaronjmars/MiroShark/pull/109); [Per-agent sparklines (PR #115, merged)](https://github.com/aaronjmars/MiroShark/pull/115); [Peak-round analytics (PR #108, merged)](https://github.com/aaronjmars/MiroShark/pull/108); [Trading signal JSON (PR #91, merged)](https://github.com/aaronjmars/MiroShark/pull/91); [OriginTrail DKG anchor (PR #84, merged)](https://github.com/aaronjmars/MiroShark/pull/84)*
