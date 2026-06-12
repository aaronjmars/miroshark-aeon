# MiroShark Gave Simulated Agents a Real Brain

**Apr 08, 2026** | [https://aaronjmars.substack.com/p/miroshark-gave-simulated-agents-a](https://aaronjmars.substack.com/p/miroshark-gave-simulated-agents-a)

---

Most multi-agent simulations are chatbots with character sheets.

System prompt. Persona blurb. LLM call. Repeat. The agent doesn’t remember round 3 when it’s in round 8. It doesn’t know what it said last week. It doesn’t update when someone it trusts changes their mind. It’s stateless theater - impressive from a distance, meaningless under the hood.

MiroShark is a different thing entirely.[

![](https://substackcdn.com/image/fetch/$s_!SY2g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74729f6d-28ed-4ed3-8f23-59de53bcd69d_2752x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!SY2g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74729f6d-28ed-4ed3-8f23-59de53bcd69d_2752x1536.jpeg)

---

**Where it came from**

[MiroFish](https://github.com/666ghj/MiroFish) launched in early March 2026. 20-year-old Beijing student Guo Hangjiang shipped a multi-agent social simulator that topped GitHub’s global trending list and secured $4.1M from Shanda Group in under 24 hours. The concept worked. The execution had gaps: UI and codebase entirely in Chinese, storage locked to Zep Cloud, platforms running in sequence instead of parallel.

[MiroShark](https://github.com/aaronjmars/MiroShark) started as a clean English fork - local Neo4j, local Ollama, nothing proprietary. That was week one. By week two, it had become something the original never attempted: a cross-platform simulation engine where agents trade prediction markets, argue on Twitter, and post Reddit threads simultaneously - with memory that actually persists.

289 commits in 2 weeks. 582 GitHub stars from a standing start. One developer.

This isn’t a fork that survived. It’s a rebuild with a thesis.

---

**The graph-first architecture**

Here’s what separates MiroShark from every weekend agent project: the knowledge graph isn’t decoration. It’s the ground truth everything else runs on.

Feed MiroShark a document - a corporate press release, a merger announcement, a policy paper - and the GraphBuilderService doesn’t summarize it. It chunks the text, runs named entity recognition with few-shot examples and rejection rules to filter noise, then writes entities and relationships into Neo4j using batched UNWIND transactions. “Acme Corp,” “CEO Jane Doe,” “rival firm Widget Inc.” become nodes. leads, acquires, competes_with become typed edges.

That graph becomes every agent’s epistemological substrate.

Each entity extracted gets a persona built from five distinct layers: graph attributes (the entity’s own properties), relationships (who they’re connected to and how), semantic search (embedding-based retrieval of relevant context), related nodes (multi-hop traversal for indirect connections), and web enrichment. That last one is clever - when graph context for an entity is thin (<150 characters), MiroShark auto-triggers a perplexity/sonar-pro call through OpenRouter. A simulated CEO will know their actual public positions, not just what the uploaded document says.

Structured knowledge, not vibes.

---

**Belief states that actually evolve**

Traditional agents are stateless between turns. Every response is a fresh inference. No memory of opinion shifts. No accumulated trust. No actual dynamics.

MiroShark tracks three explicit dimensions per agent across every round:

- **Stance** — position on each topic, -1.0 to +1.0
- **Confidence** — certainty per topic, 0.0 to 1.0
- **Trust** — per-agent trust scores that shift based on interactions

These update heuristically each round based on what agents see and do. When a high-trust agent posts a compelling argument, other agents’ stances and confidence values shift. When a Polymarket price moves, traders and social media agents alike adjust their positions. Polarization, consensus formation, cascade effects - emergent, not scripted.

This is the Soros reflexivity problem applied to simulation: the map changes the territory. Agents aren’t just modeling a system. They’re inside it.

---

**The memory loop**

The knowledge graph doesn’t stay static. The GraphMemoryManager processes agent activities in real time — posts, likes, reposts, comments, trades — converts each into natural language descriptions, and feeds them back into Neo4j as new episodes. The graph grows as the simulation runs.

An agent who posted a viral tweet criticizing a merger now exists as a node with new relationships: authored, criticized, influenced. Other agents’ subsequent actions generate with this updated graph context. Feedback loop between structured knowledge and emergent behavior — exactly the “agentic knowledge graph” pattern researchers at DeepLearning.AI and IBM have been theorizing about. Except running live, not in a whitepaper.

A sliding-window round memory compacts old rounds via background LLM calls. Agents reference earlier conversations, change their minds based on accumulated evidence, call each other out on contradictions. The context window stays manageable. The history doesn’t disappear.

---

**Cross-platform in parallel**

The headline feature that shipped in week two: Twitter, Reddit, and Polymarket running simultaneously via asyncio.gather(). Before: platforms ran in sequence. Now: all three fire at once, connected by a Market-Media Bridge that feeds social sentiment into trader prompts and market prices back into social media posts.

A Polymarket trader in round 8 sees compressed summaries of rounds 1-5, full detail from round 7, and live Twitter and Reddit posts from the current round. Traders read social media before placing bets. Social media agents watch market prices before posting. A bearish Reddit thread can tank a prediction market. A market crash can trigger a Twitter panic.

This is the cross-platform feedback loop that makes real social systems unpredictable. MiroShark is the first open tool that models it.

The Polymarket layer was rebuilt from scratch. The old system let agents create random markets at 50/50 odds. The new version generates a single LLM-designed market with non-50/50 initial pricing via constant-product AMM. Agents can buy, sell, or do nothing. In testing, 18 trades on one market moved the price from $0.35 to $0.27. Best contrarian trader cleared $558 in profit.

Real dynamics, fake money, actual emergent behavior.

---

**The performance overhaul**

Underneath the new features, everything got faster:

Neo4j writes moved from one-transaction-per-entity to batched UNWIND queries - 10x faster. Graph chunk processing went parallel via ThreadPoolExecutor - 3x faster. Config generation runs three concurrent batches — 3x faster. Memory compaction happens in background threads with zero blocking. Full simulation round runs ~40% faster than before.

The prompt engineering layer matters too. Every platform got rewritten prompts with behavioral heuristics. Twitter agents: “DO_NOTHING is your default — you must have a specific reason to do anything else.” Pushed inaction rate from 0% to 36%. Reddit agents write in paragraph form and cite sources. Polymarket traders see position-sizing heuristics and contrarian psychology nudges.

Behavior engineering, not just prompt stuffing.

---

**Why it matters now**

In 2026, “agentic knowledge graphs” are the hot enterprise AI topic. Beam AI, ZBrain, IBM - everyone’s pushing the idea that agents need structured reasoning substrates, not just vector databases. MiroShark is the open-source proof that this architecture works for simulation at scale: 100+ agents, 40+ rounds, three platforms, all grounded in a single evolving knowledge graph.

The multi-agent simulation market is heating up. Gartner reported a 1,445% surge in multi-agent system inquiries from Q1 2024 to Q2 2025. Prediction market AI agents like Polystrat have already executed 4,200+ trades on Polymarket. Population-scale simulators are attracting policymakers.

MiroShark sits at a unique intersection: the only open-source project that simulates social media and prediction markets together in one coherent loop. Four open PRs. Simulation replay. Agent network visualization. JSON/CSV export. 28 commits in seven days.

MiroFish proved the concept.

[MiroShark is building the thing that actually runs.](https://github.com/aaronjmars/MiroShark)

→ [GitHub](https://github.com/aaronjmars/MiroShark)
