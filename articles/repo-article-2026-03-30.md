# The Knowledge Graph Inside MiroShark: How Structured Memory Makes Simulated Agents Think

Most multi-agent simulations treat their agents like chatbots with character sheets — a system prompt, a persona blurb, and an LLM call. MiroShark takes a fundamentally different approach. At its core sits a Neo4j knowledge graph that extracts entities and relationships from any document you upload, then uses that structured knowledge to generate agents who don't just roleplay — they *reason* from interconnected context. Ten days after launch, with 344 stars and a growing ecosystem of community forks, MiroShark's graph-first architecture is quietly proving that the "agentic knowledge graph" trend reshaping enterprise AI in 2026 has legs in simulation too.

## From Documents to Knowledge

When you feed MiroShark a document — say, a corporate press release about a merger — the system doesn't just summarize it. The `GraphBuilderService` chunks the text, runs named entity recognition with few-shot examples and rejection rules to filter noise, then writes entities and relationships into Neo4j using batched `UNWIND` transactions. The result is a structured graph where "Acme Corp," "CEO Jane Doe," and "rival firm Widget Inc." are nodes connected by typed edges: *leads*, *acquires*, *competes_with*.

This isn't decorative. The graph becomes the ground truth that every simulated agent is built from.

## Five Layers of Persona Context

Here's where MiroShark diverges from the prompt-and-pray school of agent design. Each entity extracted from the graph gets a persona constructed from five distinct layers:

1. **Graph attributes** — the entity's own properties (role, type, metadata)
2. **Relationships** — who they're connected to and how
3. **Semantic search** — embedding-based retrieval of relevant graph context
4. **Related nodes** — multi-hop traversal to discover indirect connections
5. **Web enrichment** — for public figures or entities with thin graph context (<150 characters), an LLM research call pulls in real-world data

The web enrichment layer is particularly clever. MiroShark detects whether an entity is a public figure via keyword matching and auto-triggers a `perplexity/sonar-pro` call through OpenRouter when the graph alone doesn't provide enough context. The result: an agent representing a real CEO will know about their actual public positions, not just what the uploaded document says.

## Belief States That Actually Evolve

Traditional chatbot agents are stateless between turns — each response is a fresh inference with no memory of opinion shifts. MiroShark tracks three explicit dimensions per agent across every simulation round:

- **Stance** — position on each topic, ranging from -1.0 (strongly opposed) to +1.0 (strongly supportive)
- **Confidence** — certainty level per topic, 0.0 to 1.0
- **Trust** — per-agent trust scores that shift based on interactions

These aren't just stored; they're updated heuristically each round based on what agents see and do. When a high-trust agent posts a compelling argument on Twitter, other agents' stances and confidence values shift. When a Polymarket price moves, traders and social media agents alike adjust their positions. The belief system creates emergent opinion dynamics — polarization, consensus formation, cascade effects — without any of it being scripted.

## The Graph Memory Loop

What makes MiroShark's architecture genuinely novel is that the knowledge graph isn't static. The `GraphMemoryManager` processes agent activities in real time, converting each action — posts, likes, reposts, comments, trades — into natural language descriptions that get fed back into Neo4j as new episodes. The graph grows as the simulation runs.

An agent who posted a viral tweet criticizing the merger now exists as a node with new relationships: *authored*, *criticized*, *influenced*. Other agents' subsequent actions are generated with this updated graph context. It's a feedback loop between structured knowledge and emergent behavior — exactly the "agentic knowledge graph" pattern that researchers at DeepLearning.AI and IBM have been theorizing about, but running in a live simulation rather than an enterprise RAG pipeline.

## Cross-Platform Context as Connective Tissue

The graph doesn't just power individual agents — it bridges MiroShark's three simultaneous platforms. Twitter posts, Reddit threads, and Polymarket trades all run in parallel via `asyncio.gather`, but agents see cross-platform context: traders read social media sentiment before placing bets, social media agents watch market prices before posting. A sliding-window round memory compacts old rounds via background LLM calls, keeping the context window manageable while preserving the most salient information.

The `SimulationConfigGenerator` even models realistic activity patterns — time-of-day multipliers, response delays, influence weights — so the emergent dynamics feel organic rather than uniformly distributed.

## Why This Matters Now

In 2026, "agentic knowledge graphs" are the hot topic in enterprise AI: Beam AI, ZBrain, and IBM are all pushing the idea that agents need structured reasoning substrates, not just vector databases. MiroShark is the open-source proof that this architecture works for simulation at scale — 100+ agents, 40+ rounds, three platforms, all grounded in a single evolving knowledge graph.

With 28 commits in the last seven days, four open PRs adding features like simulation replay and agent network visualization, and 344 GitHub stars from a standing start, MiroShark isn't just a fork that survived. It's becoming the reference implementation for what happens when you give simulated agents a real memory — not a prompt, but a graph.

---

*Sources:*
- [MiroShark on GitHub](https://github.com/aaronjmars/MiroShark)
- [Agentic Knowledge Graphs with A2UI (2026)](https://medium.com/@visrow/agentic-knowledge-graphs-with-a2ui-why-ai-reasoning-looks-different-in-2026-8e51f3d26cec)
- [5 Ways Knowledge Graphs Are Reshaping AI Workflows](https://beam.ai/agentic-insights/5-ways-knowledge-graphs-are-quietly-reshaping-ai-workflows-in-2026)
- [Agentic Knowledge Graph Construction — DeepLearning.AI](https://learn.deeplearning.ai/courses/agentic-knowledge-graph-construction/information)
- [Graphs Meet AI Agents: Taxonomy, Progress, and Future Opportunities](https://arxiv.org/html/2506.18019v1)
- [MiroShark on Microlaunch](https://microlaunch.net/p/miroshark)
