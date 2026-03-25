# MiroShark: How a Five-Day Fork Turned a Viral Chinese AI Project Into a Global Simulation Engine

MiroFish exploded onto GitHub in March 2026 — 33,000 stars, $4 million in funding within 24 hours, and the top trending spot worldwide. It promised something genuinely new: feed it a document, and hundreds of AI agents with distinct personalities would simulate how the public would react on social media, hour by hour. The catch? The entire codebase was in Chinese, it depended on cloud-only APIs, and getting it running locally required significant effort. Enter MiroShark — a ground-up English fork that launched five days later and is quietly becoming the version the global developer community actually runs.

## What MiroShark Does

MiroShark is a multi-agent simulation engine. You upload a document — a press release, a policy draft, a financial report — and the system generates hundreds of AI agents, each with a unique personality, opinion bias, reaction speed, and influence level. These agents then interact on simulated social platforms: posting, arguing, shifting opinions, forming coalitions. After the simulation runs its course, a dedicated ReportAgent analyzes everything and produces a structured prediction report.

The underlying simulation engine is OASIS, built by the CAMEL-AI team, which can scale to one million agents across 23 different social actions — following, commenting, reposting, liking, muting, and more. MiroShark inherits this power but wraps it in an English-native, local-first architecture built on Neo4j for knowledge graphs and Ollama for local inference.

At 269 stars and 43 forks in its first five days, MiroShark is gaining traction fast — not through hype, but through usability.

## A Week of Relentless Shipping

The commit history tells the story. Creator Aaron Mars forked MiroFish on March 20th and immediately translated the entire codebase from Chinese to English. By March 21st, he had ripped out the Zep Cloud dependency and replaced it with a local Neo4j + Ollama stack — a fundamental architectural shift that lets MiroShark run entirely offline.

Then came a burst of feature work on March 23rd: OpenRouter cloud API support for users without GPUs, simulation pause/resume/restart controls, a UX overhaul, dead code cleanup, token-saving text filters for the preprocessor, and a "Smart Model" tier that routes intelligence-sensitive workflows (reports, ontology extraction) through a stronger model while keeping high-volume simulation rounds on cheaper inference.

The most interesting addition? Claude Code as a first-class LLM provider. Set `LLM_PROVIDER=claude-code` in your `.env` and MiroShark routes graph building, agent generation, report writing, and persona chat through your Claude Pro or Max subscription — no API key needed. It is one of the first open-source projects to treat the Claude Code CLI as a local inference backend, a pattern likely to spread as more developers realize they already have access to frontier models through their subscriptions.

## Architecture: Knowledge Graphs Meet Swarm Intelligence

MiroShark's architecture is built around a pipeline that converts unstructured documents into structured social simulations:

1. **Graph Build** extracts entities and relationships into a Neo4j knowledge graph with per-agent memory — not just a flat embedding store, but a relational structure that agents can reason over.
2. **Agent Setup** generates personas programmatically, each with tunable parameters for personality, bias, reaction speed, and social influence.
3. **Simulation** runs CAMEL-AI's OASIS engine, where agents interact across simulated platforms. Sentiment evolution and influence dynamics are tracked in real time.
4. **Report Generation** uses a ReACT-loop ReportAgent that interviews a focus group drawn from the simulation, then synthesizes a structured analysis.

The Smart Model feature adds a practical optimization: expensive reasoning (reports, ontology) routes to a stronger model, while the hundreds of per-agent inference calls during simulation stay on fast, cheap models like Qwen 3.5 running locally on Ollama. A typical simulation runs 40 turns across 100+ agents — that volume matters.

## Why It Matters Now

The prediction market boom, the rise of AI-native PR tools, and growing demand for scenario planning have created a moment for swarm simulation. One MiroFish user reportedly plugged it into a Polymarket trading bot, simulating 2,847 digital humans before every trade, and reported over $4,000 in profit across 338 trades. Whether those numbers hold up to scrutiny, the use case is real: PR crisis testing, policy analysis, market sentiment forecasting, and even creative applications like generating narratively consistent endings for unfinished fiction.

MiroShark's contribution is making this accessible. The four deployment options — cloud API, Docker with local Ollama, manual local setup, and Claude Code mode — cover everything from a laptop with no GPU to a production server. The recommended cloud configuration (Qwen3 235B on OpenRouter) runs a full simulation for roughly $0.30. Local users with an RTX 3090 or M2 Pro can run entirely offline.

In a landscape where most AI tools ask you to send your data to someone else's server, MiroShark offers a genuinely local-first alternative for simulating how the world might react — before it actually does.

---

*Sources: [MiroShark on GitHub](https://github.com/aaronjmars/MiroShark), [MiroFish: Swarm-Intelligence with 1M Agents (Medium)](https://agentnativedev.medium.com/mirofish-swarm-intelligence-with-1m-agents-that-can-predict-everything-114296323663), [MiroFish: The AI Swarm Engine That Got $4M in 24 Hours (Emelia)](https://emelia.io/hub/mirofish-ai-swarm-prediction), [MiroFish Overview (DEV Community)](https://dev.to/therealmrmumba/everything-you-need-to-know-about-mirofish-the-ai-swarm-engine-predicting-everything-5fp3), [MiroFish Multi-Agent Prediction (Judy AI Lab)](https://judyailab.com/en/posts/mirofish-multi-agent-prediction/)*
