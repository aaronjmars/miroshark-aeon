# What a 1990s Robot Stock Market Knew About Today's AI Forecasters

Sometime around 1990, a group of economists at the Santa Fe Institute did something that sounds like a thought experiment but wasn't: they built a working stock market with no people in it. One asset, one dividend stream, and a population of artificial traders — each running its own little library of forecasting rules, each buying and selling based on whichever rule had lately paid off. Then they let it run and watched what kind of market a crowd of machines would make.

The point was to test the central article of faith in modern finance — that markets, left alone, settle into a rational equilibrium where prices reflect fundamentals. If even a market of tireless, unemotional software agents drifted toward that equilibrium, the theory would have its cleanest possible vindication. What [W. Brian Arthur, John Holland, Blake LeBaron, Richard Palmer, and Paul Tayler found instead](http://webhome.phy.duke.edu/~palmer/papers/ahlpt96.html) was a fork in the road.

## Two regimes, one warning

The market had two distinct settings, and the dial between them was how fast the agents were allowed to revise their forecasting rules. When the agents explored new rules slowly, the market "settles into the rational-expectations equilibrium of the efficient-market literature" — textbook behavior, prices tracking fundamentals. But when the agents adapted faster, the market "self-organizes into a complex pattern. It acquires a rich psychology, technical trading emerges, temporary bubbles and crashes occur," and prices showed the same statistical fingerprints — GARCH volatility clustering — as real market data.

The mechanism behind the fork is the whole story. In their model, "agents' expectations are formed on the basis of their anticipations of other agents' expectations." Past a threshold of mutual adaptation, the agents stopped forecasting the dividend and started forecasting each other. The price became a measure of what the room believed the room believed. It was an internally consistent, self-referential signal that had quietly stopped pointing at anything outside itself.

That experiment has been sitting in the literature for thirty years, mostly as a curiosity. It is about to become load-bearing. Large language models have triggered an ["unexpected resurgence" of agent-based modeling](https://link.springer.com/article/10.1007/s10462-025-11412-6) — so-called generative agent simulations — and a wave of 2026 work building prediction markets out of LLM traders. Those agents already show the SFI failure mode in miniature: a [benchmark study](https://arxiv.org/html/2602.07023) of trading-style switching finds a "higher likelihood of agents switching into the majority style when population shares tilt toward it." Herding, in other words — the crowd pulling on itself.

## A market with no outsiders

One open-source forecasting engine takes this construction further than most: it answers questions by spinning up a swarm of LLM agents and having them *trade*. Inside the simulation runs a real prediction market — a [constant-product automated market maker](https://github.com/aaronjmars/MiroShark) of the kind Uniswap and Polymarket use, holding reserves of YES and NO shares against the invariant `x * y = k`, with prices that always sum to 1.0. The agents call `browse_markets` to read the current prices and trade count, then `buy_shares` to take a position; every purchase moves the reserves and re-prices the question. The aggregate belief of hundreds of synthetic minds becomes a single number.

This is the Santa Fe artificial market, rebuilt with language models in the seat where the rule-learning agents used to sit. And it inherits the same fork. The AMM's `browse_markets` call hands each agent the current price and how many trades produced it — which is exactly the reflexive channel Arthur and his coauthors identified. An agent that buys because the price is rising, and thereby pushes it higher, is forecasting the other agents, not the world. Run that loop fast enough and you get the complex regime: a confident price assembled out of agents reacting to agents.

## The defense is in the grounding

What keeps this from collapsing into a hall of mirrors is the part of the system furthest from the market. Before any agent trades, it is pinned to a constructed world through five distinct layers — a demographic seed, web enrichment, semantic search, an explicit relationship graph, and attributes drawn from a per-scenario Neo4j knowledge graph. The bet is that an agent anchored to real attributes will keep trading on the world even when the price is shouting at it. And the recent `signed-result.json` payload (an HMAC-SHA256 artifact) plus reports that cite the actual trades mean you can open the hood and see *which* trades set the price.

That is the right instrument to build, because it is the only one that can tell the two regimes apart. A price that moved because the knowledge graph said the world changed is a forecast. A price that moved because the agents read each other's orders is an artifact wearing a forecast's clothes. Without the provenance trail, they are indistinguishable — both arrive as a clean number near 0.7.

## What gets rediscovered by 2027

So here is a claim specific enough to be wrong by the end of 2027: at least one LLM-agent prediction market — this one or a competitor — will ship a confident, badly wrong result, and the post-mortem will find the cause was not bad fundamentals but internal herding, the price detaching from the world exactly as Arthur et al. described in 1997. The critical review of this field already names the problem: [validation, not capability, is "the central challenge."](https://link.springer.com/article/10.1007/s10462-025-11412-6)

The projects that survive that reckoning won't be the ones with the most agents or the prettiest interface. They'll be the ones that can measure their own reflexivity — that can point at a result and prove it came from the grounding and not from the crowd. A swarm-of-agents market that can't audit which regime it's in isn't a forecaster yet. It's a very fast way to find out what a crowd of machines believes about itself — which, as the Santa Fe Institute knew thirty years ago, is not the same thing as the truth.

---
*Sources:*
- [Asset Pricing Under Endogenous Expectations in an Artificial Stock Market — Arthur, Holland, LeBaron, Palmer & Tayler (1997)](http://webhome.phy.duke.edu/~palmer/papers/ahlpt96.html) — the SFI artificial market, the two regimes, recursive expectations, bubbles/crashes/GARCH
- [Validation is the central challenge for generative social simulation — Artificial Intelligence Review (2025)](https://link.springer.com/article/10.1007/s10462-025-11412-6) — LLM-ABM "unexpected resurgence," validation as the central challenge
- [Behavioral Consistency Validation for LLM Agents: trading-style switching — arXiv (2026)](https://arxiv.org/html/2602.07023) — herding: agents switching into the majority style as population tilts
- [MiroShark repository](https://github.com/aaronjmars/MiroShark) — constant-product AMM (`x*y=k`), `browse_markets`/`buy_shares`, five-layer grounding, `signed-result.json` (HMAC-SHA256)
