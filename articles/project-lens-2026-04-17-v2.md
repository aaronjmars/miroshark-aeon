# A Crowd Is Not a Swarm: What Honeybees Knew Before the Wisdom of Crowds Got Famous

In 2011, a team at ETH Zürich ran a clean little experiment that should have killed a popular theory and didn't. They sat 144 people down and asked them to estimate factual answers — geographical facts, crime statistics — across six rounds. Some participants got no feedback between rounds. Others saw the group average. Others saw every individual estimate. The thinking, borrowed from James Surowiecki's bestseller *The Wisdom of Crowds*, was that pooling and sharing would sharpen the group's collective accuracy.

It didn't. Diversity collapsed. Confidence rose. Accuracy stayed flat or got worse. The researchers identified three distinct failure modes — the *social influence effect* (diversity narrows without accuracy improving), the *range reduction effect* (the truth gets pushed to the edges of the surviving estimates), and the *confidence effect* (people get more sure of answers that are no better than before). The subjects, in their own minds, became *more confident in a worse answer* the moment they could see what their neighbors thought.

This is the dirty secret of collective intelligence research: the conditions Surowiecki specified — diversity, independence, decentralization — almost never survive contact with a real social network. As soon as people can see each other, the magic goes away.

## The Bees Already Solved This

Tom Seeley spent four decades at Cornell studying how honeybee swarms decide where to build a new home. The problem is hard: a swarm of ten thousand bees has hours, maybe days, to evaluate dozens of potential cavities — each varying in volume, exposure, and entrance size — and pick one without splitting the colony. Get it wrong and the colony dies in winter.

What Seeley documented in *Honeybee Democracy* (2010) is essentially a biological architecture for *avoiding* the failures the ETH Zürich team measured. Scout bees evaluate sites independently. They report findings through waggle dances whose vigor encodes their personal assessment. Crucially, they do not pile on. A scout that has danced for one site does not switch to another simply because its neighbor's dance looks more popular. Quorum sensing — not majority voting — closes the decision: when a critical number of scouts have independently endorsed a single site, the swarm commits. Seeley distilled the conditions for true swarm intelligence: diversity of evaluation, honest signaling, independent assessment, unbiased aggregation, and leadership that organizes without dominating.

Those five conditions sound suspiciously like the ones the 2011 PNAS paper found humans systematically violate. The bees evolved an architecture that protects independence. Humans, given the chance, abandon it within five rounds.

## The Project That Treats This as an Engineering Problem

MiroShark — an open-source simulation engine at 709 GitHub stars and 135 forks, twenty-five days after launch — describes itself as a "Universal Swarm Intelligence Engine." That phrase was a marketing flourish until last week. With the analytics layer that landed on April 17, it became something more like a measurement instrument for the exact problem the bees solved and humans don't.

Upload a document — a policy draft, an earnings call, a research paper — and MiroShark generates hundreds of LLM-driven agents with distinct personas. They post, argue, and trade across simulated Twitter, Reddit, and Polymarket platforms. None of this is novel. What is novel is what the system records about itself as it runs.

The Agent Interaction Network (PR #33) builds a force-directed graph of every agent-to-agent interaction, computes degree centrality, identifies bridge agents, and outputs an *echo chamber score*. The Quality Diagnostics layer (PR #32) computes stance entropy across the population — a direct measure of opinion diversity — and tracks how fast that entropy collapses. Convergence speed is reported as a metric, not assumed as a virtue.

Read those features against the 2011 findings and they are almost on the nose. The social influence effect shows up as falling stance entropy. The range reduction effect shows up as shrinking opinion clusters. The confidence effect — well, that's still hard to measure, but the trace interview feature, where any agent on the influence leaderboard can be interrogated about why it shifted stance, gets at the same question from a different direction.

## What This Buys You

The interesting thing is not that MiroShark simulates what crowds do. Many tools simulate crowds. The interesting thing is that it instruments the conditions under which the simulation is reliable. An echo chamber score above some threshold means the agent population has converged prematurely — the result is a feedback loop, not a forecast. A participation rate below threshold means too few agents engaged for the result to mean anything. A health badge of "Excellent" or "Low" tells the user whether the simulated swarm is behaving like Seeley's bees or like the ETH undergraduates.

That distinction is not academic. Iain Couzin, Director of the Max Planck Institute of Animal Behavior and a 2025 Royal Society Fellow, has spent the last decade tracking thousands of fish, locusts, and birds with sub-millimeter precision to understand exactly when collective behavior produces intelligence and when it produces stampede. Recent work in *Nature Communications* (2025) on collective intelligence in animals and robots makes the case explicitly: the architecture of interaction determines whether a group computes or whether it cascades. There is no general "wisdom of crowds." There is wisdom *of certain interaction structures* — and a need for tools that can tell them apart.

## The Architecture Is the Argument

In a research field where most LLM multi-agent work is racing to *increase* coordination — better consensus, faster convergence, lower disagreement — MiroShark's analytics suite quietly does the opposite. It treats premature consensus as a defect, diversity as a measurable asset, and convergence speed as something to be diagnosed rather than celebrated.

That framing comes naturally to anyone who has read *Honeybee Democracy* and then watched a Twitter discourse cycle. The bees figured out, over millions of years of evolution, that the swarm only works when each scout's report is independent. The humans built a software stack that breaks independence by design. The question for the agentic AI era is whether we'll build the same software stack again, only faster — or whether we'll build something closer to the hive.

The 700-star milestone is not the headline. The headline is that the open-source side of multi-agent simulation is starting to ship the diagnostic layer the field has been missing. Without it, every multi-agent forecast is a crowd. With it, you can finally tell whether you've got a swarm.

---
*Sources: [Honeybee Democracy — Princeton University Press](https://press.princeton.edu/books/hardcover/9780691147215/honeybee-democracy) · [How social influence can undermine the wisdom of crowd effect — PNAS (2011)](https://www.pnas.org/doi/abs/10.1073/pnas.1008636108) · [Collective intelligence in animals and robots — Nature Communications (2025)](https://www.nature.com/articles/s41467-025-65814-9) · [Iain Couzin — Max Planck Institute of Animal Behavior](https://www.ab.mpg.de/couzin) · [Multi-agent systems powered by large language models: applications in swarm intelligence — Frontiers in AI (2025)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1593017/full) · [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) (709 stars)*
