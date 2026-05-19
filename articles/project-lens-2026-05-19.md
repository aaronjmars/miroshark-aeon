# Where Trading Signals Come From: A 2026 Map of the Forecast-and-Signal Stack

In April 2026, Numerai closed a $30M Series C at a $500M valuation, with a $500M capacity commitment from J.P. Morgan and the tournament migration to a new system scheduled for June. A few weeks later, Metaculus wrapped its Spring 2026 AI Forecasting Benchmark and announced a $50k purse for the Summer FutureEval Bot Tournament. Polymarket and Kalshi data are now plumbing — Prediction Hunt sells a Dev tier that exposes `/api/v2/arb` and `/api/v2/ev` signal endpoints behind a single header, and Predly claims 89% alert accuracy detecting mispricings across both venues.

There is a quiet boom in *machine-readable forecasts*. And in any boom, the interesting question isn't which signal is best — it's where each one **comes from**. The origin of a number is a load-bearing property, and most signal consumers don't know how to read it.

This article is a map. Five wells signals are drawn from in 2026. One cell that's still empty. And a small project that just walked into it.

## Five Wells

**Market-derived.** Polymarket and Kalshi are the canonical examples. A price *is* a belief, weighted by the capital willing to defend it. Polymarket's CLOB requires a Polygon wallet and EIP-712 signing; Kalshi takes RSA key pairs. Both are queryable for free on the data side. The new entrant, Opinion, reportedly reached roughly 31% of global prediction-market volume in early 2026 on the back of a Hack VC and Jump Crypto raise. The signal is the price. The provenance is the order book.

**Tournament-derived.** Metaculus's FutureEval benchmark grades AI bots against ground-truth questions in science, technology, health, geopolitics, and AI. The Spring 2026 Bot Tournament has wrapped; the Summer 2026 has a $50k pot; Bridgewater is running a competition through Metaculus this year. Bot makers must be willing to share code or a description of how their bot works. The signal is a probability submission. The provenance is the bot's source.

**Crowd-model-derived.** Numerai Signals is the archetype. Data scientists bring their own features — "a feed of information, numerical data about stocks" — and Numerai compounds them into a meta-model. The new YIEDL crypto dataset adds price-volume-momentum, sentiment, and on-chain features over a decade of cryptocurrency data. The signal is a numeric vector keyed to a security. The provenance is whoever the staker is.

**Sentiment-derived.** LunarCrush, Santiment, IntoTheBlock. Off-chain social plus on-chain analytics, engineered into rolling features. The signal is a feature value. The provenance is the social/on-chain corpus on the day of measurement.

**AI-analytics-derived.** A newer category. Predly and Prediction Hunt sit on top of the market venues and emit *derived* signals — arbitrage opportunities, expected-value scores, mispricing alerts. The signal is downstream of the markets. The provenance is whichever model the platform runs.

These five wells share something useful: each is *machine-readable* and *real-time queryable*. They share something problematic too: with the exception of tournament-bots (whose code is at least inspectable), the *generative process* of the signal is opaque. You can read the number. You usually cannot re-run the number.

## The Empty Cell

Here is what nobody in the five categories above produces: **agent-derived signals from a closed-loop belief simulation, queryable as an API, reproducible from a config and a seed, and cryptographically anchored to that config**.

Academic agent-based models (NetLogo, Mesa, AgentPy) have done belief-dynamics simulation for thirty years, but their outputs are research papers. You can't `GET /signal.json` against a NetLogo model. The reproducibility is theoretically intact (the paper has the parameters), but the surface is wrong — the signal is locked inside a PDF.

The cell is empty for a structural reason. Markets and tournaments resolve against the real world, which gives them ground truth. Belief simulations don't have ground truth in the same sense — the agents argue, and the final-state distribution is what you get. Without ground truth, nobody quite knew what shape the surface should take.

## A Project That Just Walked In

The MiroShark repo on GitHub opened PR #91 today, May 19, 2026. The file is `backend/app/services/signal_service.py`, ~210 lines of pure Python standard library. The endpoint is `GET /api/simulation/<simulation_id>/signal.json`. The payload is small: `direction` (Bullish, Neutral, or Bearish), `confidence_pct` (0 when the agents split evenly, 100 when they're unanimous), `risk_tier` (mapped from a quality-health score), and three component percentages.

What makes the cell occupiable isn't the route. It's the chain underneath it. MiroShark runs multi-agent LLM debates — agents start with priors, exchange arguments, update beliefs, and end up at a distribution. The signal is a *pure derivation* of that final-state distribution and the simulation's quality health. There is no new computation. A "Bullish 62%" emitted from `signal.json` byte-matches the same value rendered in the chart SVG, the trajectory CSV, the Jupyter notebook, the share-card PNG, and the Farcaster Frame metadata (PR #90, merged earlier today). All eleven publish-gated surfaces are downstream of one summary payload.

The reproducibility comes from a separate piece of plumbing that landed earlier this month: PR #84 anchored MiroShark's `reproduce.json` SHA-256 hash to the OriginTrail Decentralized Knowledge Graph as a Knowledge Asset. Given the citation, the config is recoverable; given the config and the same model weights, the simulation can be re-run; given the simulation, the signal is determined. That's the chain. Polymarket can't offer it. Numerai can't offer it. Metaculus can offer the bot code but not a queryable signal feed.

## What the Map Shows

Two trends sit underneath the five wells. The first is **aggregation**: Numerai's JPMorgan capacity, the Bridgewater × Metaculus tournament, Prediction Hunt's unified header. Capital is consolidating around platforms that own the aggregation layer, not the origination layer. The second is **scale of audience**: machine-readable signals are increasingly the input to other software. Numerai's submitters are bots; Metaculus's tournament is bots; Predly's alerts feed dashboards.

The empty cell — reproducible agent-derived signals — is small. It is also the only well where the generative process is itself the artifact. You don't trust the signal because the source is a market; you trust it because you can re-run the source. Whether that turns out to be valuable is an open question. But it's a question the map didn't have a name for last quarter.

---
*Sources: [Prediction Hunt — Best API for Prediction Markets in 2026](https://www.predictionhunt.com/blog/best-api-for-prediction-markets); [Numerai Signals overview](https://docs.numer.ai/numerai-signals/signals-overview); [Numerai Crypto](https://crypto.numer.ai/); [Metaculus AI Forecasting Benchmark](https://www.metaculus.com/aib/); [Metaculus FutureEval](https://www.metaculus.com/futureeval/); [Bridgewater × Metaculus 2026](https://www.bridgewater.com/bridgewater-x-metaculus-2026-competition); [Awesome Prediction Market Tools](https://github.com/aarora4/Awesome-Prediction-Market-Tools); [MiroShark PR #91 (trading signal JSON)](https://github.com/aaronjmars/MiroShark/pull/91); [MiroShark PR #90 (Farcaster Frame v2, merged)](https://github.com/aaronjmars/MiroShark/pull/90); [MiroShark PR #84 (OriginTrail DKG anchor)](https://github.com/aaronjmars/MiroShark/pull/84)*
