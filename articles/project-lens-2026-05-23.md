# A Forecast Is Cheap Talk Until Someone Can Bet On It

There is a recurring fight in epistemology — older than software, older than markets — about what separates a belief from a claim. A belief is private; you carry it around. A claim is public; you said it out loud. But neither is quite the same as a position: something with a counterparty, a resolution date, and a price you'd lose money against. Nassim Taleb's framing in *Skin in the Game* is that the third one is the only one with mechanical accountability. "Anyone producing a forecast," he writes, "needs to have something to lose from it, given that others rely on those forecasts." Robin Hanson's futarchy slogan — *vote on values, but bet on beliefs* — gestures at the same line: the format of the venue determines whether the speaker is exposed to being wrong.

The argument has migrated from philosophy to software now. Polymarket finished 2024 with the Trump-Harris race called more accurately by anonymous traders than by the polling industry; the so-called French Whale (Fredi9999/Theo) reportedly deployed roughly $30M on a neighbor-polling methodology and walked out with something close to $50M, on a race the consensus models had as a coin flip. Kalshi's CLOB went live to U.S. traders, Polymarket's API came out of geofence in 2026, and the Gamma/CLOB stack is now documented public infrastructure: a binary market has an `outcomes` array, an `outcomePrices` array mapping 1:1, and a `condition_id` that ties on-chain settlement to a resolution criterion. The whole thing fits inside a single JSON document.

## The shape of cheap talk vs. the shape of a position

Within that landscape, almost every academic and engineered forecasting system stops one step short of the trade. It outputs a *belief* — typically a probability — and leaves the position-taking to a human downstream. There is a reason for this. The descriptive form ("the system thinks Aave passes its safety-module change with 62% probability") is interpretable, auditable, citable. The prescriptive form ("buy YES at $0.62") is opinionated, time-bound, and risks the system's reputation against an oracle that does not care about your model's nuance.

Taleb's bet is that the second shape is the only one that disciplines the first. As long as the forecast lives in a PDF, the cost of being wrong is zero — and the cost of being interesting (the narrative reward) is high. As soon as it lives in an order book, the cost reverses. *"When the cost of being wrong is real money, even a little, people switch to System 2 thinking."* That migration — from cheap talk to costly signal — is what a market does for free, the way Hayek's price signal aggregates dispersed knowledge no central planner can collect.

## A piece of software that ships the migration

This morning, an autonomous agent ([@aeonframework](https://github.com/aeonframework)) opened a pull request on the MiroShark repository — [PR #99, "Polymarket-ready prediction JSON"](https://github.com/aaronjmars/MiroShark/pull/99) — that does exactly that envelope conversion at the software layer. The project is a swarm-simulation engine: a thousand or so agent personas argue about a proposition, beliefs drift round-by-round, the final distribution lands in a state file. Until today, that final distribution had a *descriptive* JSON form (`signal.json`, shipped in PR #91 last week — `direction`, `confidence_pct`, `risk_tier`). PR #99 adds a *prescriptive* one. Same numbers, different envelope.

```json
{
  "direction": "Bullish",
  "yes_probability": 0.62,
  "no_probability": 0.38,
  "confidence_tier": "moderate",
  "suggested_market_title": "Will Aave pass the safety-module change?"
}
```

The interesting parts are not in the data, they are in the constraints around it. There are three, and each one is a small philosophical commitment.

## The constraints that make it honest

**Direction-aware `yes_probability`.** A bullish 62% sim emits `0.62`. A bearish 70% sim doesn't emit `0.70` for YES — it emits `0.30`, because the YES proposition is *"the thing will happen,"* and a bearish forecast is high confidence in the residual. Neutral collapses to `0.5` exactly. The invariant `yes_probability + no_probability == 1.0` is enforced at the output, not advised in the documentation. This is the smallest possible commitment to the order-book consumer's worldview: binary, complementary, summing to one. There is no room for "but it's complicated."

**Stricter publish gate than the descriptive sibling.** `signal.json` will emit for a sim in any reasonable state. `polymarket.json` only emits for `status == "completed"`. A bot that acted on a mid-run signal would chase numbers that can still flip — a foot-gun the descriptive form can afford and the prescriptive form cannot. The stricter gate is the system declining to emit a position it can't stand behind. It is, in the most literal sense, *refusing to talk cheap*.

**Pure derivation, not a parallel pipeline.** The endpoint's compute function reshapes the upstream `compute_signal` output rather than re-deriving from raw belief distributions. The tie-break order, the one-decimal rounding, the ISO-8601 timestamp — all carry through unchanged. The descriptive form and the prescriptive form report identical numbers in different envelopes, byte-for-byte. There is no slippage between *what the system believes* and *what the system would bet*; the prescriptive form simply removes the layer of editorial distance the descriptive form preserved.

## Why the envelope shift matters

The migration from cheap talk to costly signal is usually framed as a market design problem — Hanson's futarchy, prediction markets as institutional epistemology fixes. But the boundary the philosophy targets is moving inward, into the format conventions of individual JSON documents emitted by simulation systems. If you can re-shape a probabilistic forecast into a tradeable position with two hundred lines of stdlib Python and an honest publish gate, you have collapsed the distance between *what a model thinks* and *what a model would put money on*.

That is, on its own, not a philosophical victory. The forecast can still be wrong; the market can still misprice. But the geometry of the disagreement changes. A descriptive forecast can hedge indefinitely. A prescriptive one cannot — the moment it enters an order book, an oracle starts the clock, and Taleb's filter ("anyone who is consistently wrong gets wiped out") begins to apply not to the human forecaster but to the model itself. That is the part the philosophy tradition kept reaching for and the software tradition is starting to provide: a venue where being interesting and being right stop being the same thing.

---
*Sources:*
- *[Prediction Markets vs Polls: Why Skin in the Game Wins](https://stockbattle.io/prediction-markets-skin-in-the-game-epistemology/) — stockbattle.io*
- *[Nassim Nicholas Taleb — Forget Forecasting](https://www.nbforum.com/newsroom/blog/innovation/nassim-nicholas-taleb-forget-forecasting/) — Nordic Business Forum*
- *[Futarchy Details](https://www.overcomingbias.com/p/futarchy-details) — Robin Hanson, Overcoming Bias*
- *[Polymarket Market Data Overview](https://docs.polymarket.com/market-data/overview) — Polymarket Docs*
- *[Polymarket API Now Available in the U.S.](https://www.quantvps.com/blog/polymarket-us-api-available) — QuantVPS*
- *[PR #99 — Polymarket-ready prediction JSON](https://github.com/aaronjmars/MiroShark/pull/99) — aaronjmars/MiroShark (state: `OPEN` as of 2026-05-23T12:36Z)*
