# AI Research Can Now Interview 1,000 People in an Hour. It Just Can't Put Them in a Room.

The market research industry has just undergone one of the fastest methodological transitions in its history. A class of platforms for generating synthetic research respondents — AI personas that can be surveyed, interviewed, and tested against product concepts without any human participants — has compressed a cycle that once took weeks into something that takes hours. Benchmarks published in 2025–2026 show [90% alignment](https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide) between synthetic consumer responses and human survey data on purchase intent, and [85% distributional similarity](https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide) on concept and pricing studies. Analysts forecast that synthetic inputs will represent more than half of all market research data by 2027.

Platforms like Semilattice (priced from $1 to $399/month), Aaru, Evidenza, and Viewpoints.ai have built this market from scratch in roughly two years. At the enterprise end, [specialized platforms run $100,000–$250,000/year](https://aimultiple.com/synthetic-users) for continuous simulation access. The infrastructure for understanding what individual users think — about a product, a price point, a concept — has been effectively automated.

## The Platform That Replaced the Focus Group

The mechanism behind these tools is structurally consistent across the category. A research team defines a persona: demographics, income, psychographic profile. An LLM instantiates that persona as a digital respondent. The persona receives a stimulus — a product concept, a message variant, a pricing scenario — and returns a response. The team collects responses from N personas, analyzes the distribution, and draws conclusions. No panel recruitment, no field period, no $300-per-participant incentive budget.

The improvement is real. For structured reasoning tasks — price sensitivity, concept ranking, demographic segmentation — the fidelity numbers hold. The category has genuinely solved the logistics problem of market research: when you need to know whether your $49/month tier lands better than $59/month, and you need to know by Tuesday, this works.

What the category's own literature acknowledges is a structural ceiling. The platforms were built for parallel interviews: each persona responds to a stimulus independently, without awareness of what any other persona said. The problem the documentation names explicitly is that simulated individuals ["don't model multiuser interactions such as viral effects in social apps. People influence one another's choices — social proof, peer pressure, group dynamics — and tool use doesn't happen in a social vacuum."](https://aimultiple.com/synthetic-users) The 90% fidelity is achieved by treating each respondent as isolated. What it cannot tell you is what happens when those respondents encounter each other.

## The Research Question That Breaks the Architecture

The distinction matters in practice more than it sounds in theory. If the research question is "what does segment A prefer?" — isolated interviews are the right tool. If the research question is "what does segment A believe after encountering segment B's reaction?" — the architecture breaks at the foundation.

There is no mechanism in a synthetic survey for opinion contagion. A persona in round one cannot be influenced by what another persona said in round one, because there is no round one for anyone else. You get 1,000 independent measurements; you do not get a social process. The category is optimized for individual signal, not for crowd dynamics.

This is the gap that a different category of simulation tool is designed to fill. Where synthetic user platforms generate independent respondents, [agent-based social simulations](https://arxiv.org/html/2512.22082v1) run agents through an environment where they produce content, encounter each other's content, and update beliefs across multiple rounds. The theoretical case for this architecture has existed in academic literature for years — the question has been whether it could be made accessible enough to use.

## The Architecture That Makes the Difference

MiroShark's `backend/wonderwall/` is the implementation of that social layer. The directory isn't named for whimsy — it contains the complete simulated social environment: `social_platform/` (the agent-accessible feeds where posts propagate), `social_agent/` (the persona substrate, built on top of the CAMEL multi-agent framework), `environment/` (world-state management), and `clock/` (time progression across rounds). Agents don't just answer a question. They post to a simulated feed, see what other agents posted, watch prices shift on a simulated Polymarket AMM as collective sentiment moves, and update their internal state before round two starts.

The `suggest_scenarios` endpoint grounds each run in real source material — a press release, a product launch, a policy draft — so the agents are reacting to something, not reasoning in a vacuum. `director_mode` lets operators inject new events mid-run, the equivalent of interrupting a survey session to tell the participants that something has just changed. Commit `09a60cf` — the PR that placed a `~$X` cost pill on every public simulation embed — makes the unit economics visible: the full swarm run, all rounds, including the inter-agent reaction passes and market-price-drift calculations, costs roughly a dollar.

That number exists in stark contrast to the synthetic survey market. A $250,000/year enterprise simulation license buys unlimited isolated interviews. A $1 MiroShark run buys 200–400 agents who can see what each other said.

## What the Split Will Reveal

The synthetic user research category will visibly bifurcate over the next two to three years. Platforms that optimize for individual purchase decisions — pricing, concept ranking, message testing — are already mature and will keep compressing costs and improving individual fidelity. A second category, smaller today, will own the use cases where isolated interviews structurally cannot give an answer: how will a community respond to a governance change? Will a product launch generate organic amplification or generate backlash? What does a specific group believe after an external event reshapes the information environment?

These aren't better versions of the same question. They require agents that interact, a social layer underneath them, and a mechanism for injecting specific real-world facts into the simulation. They also require someone to care more about whether the crowd-level prediction is right than whether each individual agent's response hit 90% fidelity against a human panel benchmark.

The individual fidelity and the crowd-dynamics question are not optimized by the same architecture. That's not a temporary problem in the market — it's a permanent fork in what simulation is for.

---

*Sources:*
- [Synthetic Consumers: A Practical Guide](https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide) — PyMC Labs; 90% purchase-intent alignment, 85% distributional similarity, limitations in group dynamics
- [Synthetic Users Explained: Top 7 AI User Research Tools](https://aimultiple.com/synthetic-users) — AIMultiple; platform landscape, pricing ($1–$399/month to $100K–$250K+/year), explicit gap in social dynamics and group behavior
- [Agent-based simulation of online social networks and disinformation](https://arxiv.org/html/2512.22082v1) — arXiv; academic foundation for multi-round agent social simulation as distinct from isolated-persona testing
- [MiroShark — aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) — wonderwall/ social layer, suggest_scenarios, director_mode, commit 09a60cf (cost embed)
