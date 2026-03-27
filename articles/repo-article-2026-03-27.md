# MiroShark Just Built the Simulation Engine That MiroFish Promised

One week ago, MiroShark was a clean English fork of MiroFish with a local-first Neo4j stack. Today it's a cross-platform simulation engine where AI agents trade prediction markets while arguing on Twitter and Reddit — simultaneously, in real time, with memory that stretches across rounds. The fork has officially diverged.

## The Numbers So Far

MiroShark hit 285 stars and 47 forks in its first seven days on GitHub — modest next to MiroFish's 33,000-star juggernaut, but the velocity tells a different story. Developer Aaron Mars has pushed 31 commits since March 20, averaging more than four per day. The most recent push alone touched 22 files with over 4,400 lines of new code. This isn't maintenance. This is a rebuild.

The original MiroFish project, created by 20-year-old Beijing student Guo Hangjiang, took the AI world by storm in early March 2026. It topped GitHub's global trending list, secured $4.1 million in funding from Shanda Group in under 24 hours, and demonstrated that thousands of AI agents could simulate realistic social dynamics. But MiroFish shipped with its UI and codebase entirely in Chinese, its storage locked to Zep Cloud, and its simulation platforms running in sequence rather than in parallel.

MiroShark started by solving the first two problems — full English translation and a local Neo4j + Ollama stack. This week, it solved the third and went further than anyone expected.

## What Shipped This Week

The headline feature is a cross-platform simulation engine that runs Twitter, Reddit, and Polymarket simultaneously using `asyncio.gather()`. Before this change, platforms executed in sequence — social media first, then prediction markets. Now all three fire at once, with a "Market-Media Bridge" that feeds social sentiment into trader prompts and market prices back into social media posts. A Polymarket trader in round 8 sees compressed summaries of rounds 1-5, full detail from round 7, and live Twitter and Reddit posts from round 8.

The Polymarket integration itself was rebuilt from scratch. The old system let agents create random markets at 50/50 odds and post comments instead of trading. The new version generates a single LLM-designed prediction market with non-50/50 initial pricing via a constant-product AMM. Agents can only buy, sell, or do nothing. In testing, 18 trades on one market moved the price from $0.35 to $0.27, with the best contrarian trader clearing $558 in profit.

A sliding-window round memory system now gives every agent persistent context. Old rounds get LLM-compacted into summaries via background threads. Recent rounds are shown in full. The result: agents reference earlier conversations, change their minds based on accumulated evidence, and occasionally call each other out on contradictions.

Performance got a serious overhaul too. Neo4j writes moved from one-transaction-per-entity to batched UNWIND queries (10x faster). Graph chunk processing went parallel via ThreadPoolExecutor (3x faster). Config generation runs three concurrent batches (3x faster). Memory compaction happens in background threads with zero blocking. Combined with the parallel platform execution, a full simulation round runs roughly 40% faster than before.

## The Technical Depth That Matters

What separates MiroShark from a weekend fork is the prompt engineering layer. Every platform got rewritten prompts with behavioral heuristics. Twitter agents are told "DO_NOTHING is your default — you must have a specific reason to do anything else," which pushed the inaction rate from 0% to 36%. Reddit agents write in paragraph form and cite sources. Polymarket traders see position-sizing heuristics and contrarian psychology nudges.

The report agent — previously limited to searching the knowledge graph from the original PDF — now has direct access to simulation data through two new tools: `simulation_feed` (actual posts, comments, and trades filtered by platform, keyword, or round) and `market_state` (prices, trade history, P&L). Reports now quote what agents actually said and cite specific trades with dollar amounts.

Web enrichment automatically researches public figures during persona generation. When the knowledge graph context for an entity is thin — say, a CEO or politician mentioned in passing — the system makes an LLM research call to flesh out the profile. Set `WEB_SEARCH_MODEL=perplexity/sonar-pro` and it uses grounded web search via OpenRouter.

Perhaps most notably, MiroShark added Claude Code as a first-class LLM provider. Set `LLM_PROVIDER=claude-code` and your Claude Pro or Max subscription handles graph building, profile generation, config creation, reports, and persona chat — no API key needed. Only the CAMEL-AI simulation rounds and embeddings still require Ollama or a cloud API.

## Why It Matters Now

The multi-agent simulation market is heating up fast. Gartner reported a 1,445% surge in multi-agent system inquiries from Q1 2024 to Q2 2025, and the sector is projected to reach $52.6 billion by 2030. Prediction market AI agents like Polystrat have already executed over 4,200 trades on Polymarket with returns as high as 376% on individual positions. Population-scale simulators like Aaru are attracting attention from policymakers.

MiroShark sits at a unique intersection: it's the only open-source project that simulates social media and prediction markets together in a single coherent loop, where traders read Twitter posts and social media users watch market prices. That cross-platform feedback loop — where a bearish Reddit thread can tank a prediction market, and a market crash can trigger a Twitter panic — is what makes real social systems unpredictable. MiroShark is the first open tool that models it.

The project's roadmap includes scheduled mid-simulation events (injecting breaking news at specific rounds), longer stress tests, and report visualizations. An open PR adds JSON/CSV export for simulation data. For a seven-day-old fork with one developer, the shipping pace is remarkable.

MiroFish proved the concept. MiroShark is building the product.

---
*Sources: [aaronjmars/MiroShark on GitHub](https://github.com/aaronjmars/MiroShark), [MiroFish by 666ghj](https://github.com/666ghj/MiroFish), [MiroFish: Swarm-Intelligence with 1M Agents (Medium)](https://agentnativedev.medium.com/mirofish-swarm-intelligence-with-1m-agents-that-can-predict-everything-114296323663), [AI agents are quietly rewriting prediction market trading (CoinDesk)](https://www.coindesk.com/tech/2026/03/15/ai-agents-are-quietly-rewriting-prediction-market-trading), [Multi-Agent Systems: The Top AI Trend to Watch in 2026 (Medium)](https://medium.com/@keplers-team/multi-agent-systems-the-top-ai-trend-to-watch-in-2026-d459b31050de), [MiroFish: The AI Swarm Engine (Emelia)](https://emelia.io/hub/mirofish-ai-swarm-prediction)*
