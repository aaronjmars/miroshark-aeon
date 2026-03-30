# When Simulated Agents Start Trading: MiroShark and the Prediction Market Moment

Prediction markets hit $40 billion in annual volume in 2025. By early 2026, more than 30% of Polymarket wallets are running AI agents, and autonomous trading bots like Polystrat have executed over 4,200 trades in a single month with returns as high as 376% per position. But all of these agents are doing the same thing: reading real markets, placing real bets, optimizing for profit.

MiroShark is doing something different. Instead of deploying agents *into* prediction markets, it simulates the entire market — traders, social media, and opinion dynamics — inside a single engine. And that distinction matters more than it sounds.

## The Three-Platform Loop

Most multi-agent simulation tools model one platform at a time. You get a simulated Twitter, or a simulated forum, and agents post into it. MiroShark runs three platforms simultaneously — Twitter, Reddit, and a Polymarket-style prediction market called Wonderwall — and the key innovation is that they're not independent. They're connected.

When you upload a document (a policy draft, a merger announcement, an earnings report), MiroShark generates 100+ AI agents grounded in a Neo4j knowledge graph, each with distinct personas, biases, and influence levels. Then all three platforms execute in parallel via `asyncio.gather`. Every round, traders read what social media agents posted. Social media agents see how market prices moved. The cross-platform context bridge means a viral tweet criticizing a merger doesn't just shift Twitter sentiment — it moves the prediction market price, which in turn changes what Reddit commenters observe.

This feedback loop is what distinguishes simulation from automation. Polystrat reads real Polymarket data and trades on real spreads. MiroShark models the entire system — the social dynamics that *create* the spreads in the first place.

## How Wonderwall Works

MiroShark's prediction market implementation is deceptively simple but well-designed. During simulation setup, the LLM generates a single prediction market tailored to the document's core question — "Will the merger close above $50 per share?" or "Will public opinion turn negative within 48 hours?" — with a non-50/50 starting price based on the LLM's initial probability estimate.

The market uses constant-product AMM pricing (the same mechanism behind Uniswap and early Polymarket pools). Agents can buy YES, buy NO, or wait. Their trading decisions are informed by three inputs: their portfolio state, the current market price, and a curated observation prompt that includes actual Twitter posts and Reddit threads from the same simulation round.

Each agent also carries belief states — stance (−1 to +1), confidence (0 to 1), and trust scores for other agents — that update heuristically each round. A trader who watches a high-trust agent post a bullish thread will see their confidence shift, which changes their trading behavior, which moves the market price, which feeds back into the next round's social media prompts.

The result isn't a price prediction. It's a narrative about *how* prices form — which agents drive sentiment, where consensus breaks, and when cascades happen.

## Why Simulation Beats Trading Agents

The AI-in-prediction-markets narrative in 2026 has focused almost entirely on performance: Polystrat's 376% returns, the 14 bot wallets on Polymarket's top-20 leaderboard, the $40 million extracted through arbitrage. These are impressive engineering achievements, but they answer a narrow question: can bots trade better than humans?

MiroShark answers a broader one: *what happens before the trade?*

Policy teams don't need a bot that trades prediction markets faster. They need to understand how a proposed regulation might shift public opinion, which stakeholders will mobilize, and whether the resulting sentiment wave will be priced in or blindside the market. Communications strategists don't need a Polymarket position — they need to know which message framing triggers a cascade.

By simulating the full loop — social media discourse, opinion dynamics, and market formation together — MiroShark lets users explore counterfactuals. Upload two versions of a press release. Run the same agent population against both. Compare not just the final market prices but the paths they took: which agents drove polarization, where trust eroded, when the market diverged from social sentiment.

This is closer to what IOSG Ventures predicted when they called prediction market agents "a new product form" for 2026 — not just faster trading, but a new way to model information markets as complex adaptive systems.

## The Open-Source Advantage

Aaru charges enterprise rates for population-scale simulation. Polystrat requires an Olas protocol integration and real capital at risk. MiroShark is AGPL-licensed, runs locally with Ollama (no API key required), and has four setup paths including a Docker one-liner and Claude Code CLI support.

With 346 stars and 56 forks in ten days, four open PRs adding features like simulation replay and agent network visualization, and 28 commits in the past week, MiroShark is being built in public at a pace that closed alternatives can't match. The prediction market integration — the piece that makes it more than just another chatbot arena — shipped on March 26 and has been refined in every commit since.

For researchers studying information markets, teams modeling narrative risk, or developers building the next generation of forecasting tools, MiroShark is the only open-source option that treats prediction markets not as an endpoint for bot trading, but as one layer in a multi-platform simulation of how opinions form, spread, and get priced.

---

*Sources:*
- [MiroShark on GitHub](https://github.com/aaronjmars/MiroShark)
- [AI Agents Are Quietly Rewriting Prediction Market Trading — CoinDesk](https://www.coindesk.com/tech/2026/03/15/ai-agents-are-quietly-rewriting-prediction-market-trading)
- [Prediction Markets Are Turning Into a Bot Playground — Finance Magnates](https://www.financemagnates.com/trending/prediction-markets-are-turning-into-a-bot-playground/)
- [IOSG: Prediction Market Agents to Emerge as New Product Form in 2026 — KuCoin](https://www.kucoin.com/news/flash/iosg-prediction-market-agents-to-emerge-as-new-product-form-in-2026)
- [Prediction Markets in 2026: Key Trends — MetaMask](https://metamask.io/news/prediction-market-overview-trends-2026)
- [MiroShark on Microlaunch](https://microlaunch.net/p/miroshark)
- [@aaronjmars on X — MiroShark announcement](https://x.com/aaronjmars/status/2035881020302430571)
