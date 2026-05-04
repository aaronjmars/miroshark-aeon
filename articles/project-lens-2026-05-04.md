# Show Your Work: The Audit Question Coming for Every Outcome Resolver

On April 30, Sen. Jeff Merkley (D-OR) and a group of congressional Democrats sent a letter to the new CFTC chair, Michael Selig, demanding rules to address what they called the "rapid erosion of integrity" in prediction markets like Kalshi and Polymarket. The letter cited specific failures: a U.S. soldier arrested for placing roughly $400,000 in Polymarket bets ahead of military action in Venezuela, and Kalshi suspending and fining three candidates for elected office who had been trading on their own campaigns. Earlier in the week, Brazil blocked both platforms outright. The day after the letter, Minnesota's legislature began moving on its own ban.

Six days, three jurisdictions, one repeating phrase. The pressure is no longer about whether prediction markets should exist. It's a narrower, harder question: when a contract pays out, who can prove the resolution was correct, and what's the audit trail look like?

## The shape of the integrity question

Polymarket resolves through the UMA optimistic oracle — a token-weighted vote among holders, not a court of record. Critics have argued for years that the system favors the deepest pockets rather than the closest reading of the facts, and Polymarket itself has had to acknowledge at least one resolution that came back wrong, leaving "Yes" holders with positions that went to zero. An April investigation flagged the opacity of the tokenholder process, prompting UMA to whitelist 37 vetted addresses as the only direct proposers.

The pattern that worries regulators isn't that resolution sometimes fails. It's that the *paper trail of the resolution* is a Snapshot vote rather than a record of reasoning. You can see who voted which way and how heavily; you cannot reconstruct what they were each looking at. When a soldier earns $400K betting on a military operation he plausibly had inside information about, the question the CFTC is being asked is "how did the platform know whether to pay him?" — and the honest answer is that it asked its token holders.

This is the audit gap. Resolution as a verdict, not a derivation.

## The same question in a different domain

Agent-based simulators face a structurally identical problem. MiroShark — a small open-source engine that runs swarms of agents through a scenario for about a dollar in under ten minutes, currently at 1,064 stars — also resolves outcomes. Not "did the event happen," but "what did this collection of simulated agents come to believe, and did the world end up matching them?" If a journalist or a trader cites a MiroShark run, the same question lands: how do you know the run was honest?

The answer the project has been quietly stacking up over the last nine days is *the entire derivation*, written to disk in seven different shapes that all point at the same folder.

PR #47, merged April 27, added a `/verified` route and an `outcome.json` artifact that lives next to every published simulation. It records a label (`correct`, `incorrect`, or `partial`), a URL pointing at the real-world resolution, a 280-character summary, and a submission timestamp. PR #57 (April 29) emits the full per-round transcript as both Markdown and JSON, with every agent post block-quoted and tagged by stance. PR #66 (May 1) writes a 10-column belief trajectory CSV plus a JSONL twin so analysts can pull the run into pandas without parsing prose. PR #67 (May 2) added a `/watch/<id>` page that ticks the belief bars in real time while the simulation is still running. PR #69 (May 3) made all of it queryable: `?consensus=bearish&outcome=correct&q=aave` filters the gallery across the index.

Eight surfaces, one folder. The same ±0.2 stance threshold gates every one of them, so an agent labeled "bullish" in the gallery card is bullish in the transcript and bullish in the trajectory CSV.

## What "show your work" actually costs

The architectural difference between a prediction market and a simulator on this dimension is that the prediction market can keep its resolution opaque because the contract is binary — there is no "intermediate state" worth recording when the only outputs are YES and NO. The simulator cannot. The question a verifier asks an agent-based simulation is necessarily about *how* belief moved, not just where it landed, and there is no way to answer that without keeping the moves.

The cost is that every byte has to be written to disk in a format a stranger can parse. You can't serialize the trace through a token vote afterward; you have to commit, in code, to writing the round numbers, the agent IDs, the post text, the percentages, the timestamps, every time. PR #45's OpenAPI drift-detection test (April 25) is the enforcement mechanism — the YAML and the routes have to agree, or the build breaks. It's not glamorous, and it's the discipline that makes the seven downstream surfaces possible.

The dividend shows up exactly when the audit pressure arrives. A run cited on a Bankr Terminal thread two weeks ago (Apr 26, the Aave vulnerability simulation) is reachable today by anyone who wants to read the transcript, replay the GIF, pull the CSV, or attach a real-world outcome to it. None of those required new platform work; they required the artifacts already being on disk in a documented format.

## The rest of the stack

The integrity question is going to walk down the stack from prediction markets to any tool that returns a probabilistic assertion to someone with money on the line. Agent-based simulators. Agentic copilots summarizing research. Model-driven trading systems — which a Wharton/HKUST working paper showed last year colluded into price-fixing cartels in simulated markets, a finding made possible only because the simulator wrote down what each bot did. The platforms that will survive the next year of "show your work" are the ones whose reasoning is already on disk in a format a regulator, a journalist, or a skeptical user can read.

The bet has gotten cheaper. The receipt is what's getting expensive.

---
*Sources: [Democrats urge CFTC to rein in prediction markets — CNBC (Apr 30, 2026)](https://www.cnbc.com/2026/04/30/congress-kalshi-polymarket-prediction-markets-cftc.html), [Merkley CFTC Event Contract Letter (Apr 30, 2026)](https://www.merkley.senate.gov/wp-content/uploads/26.04.30-CFTC-Event-Contract-Letter.pdf), [U.S. looks into regulating prediction market sites — NPR (Apr 26, 2026)](https://www.npr.org/2026/04/26/nx-s1-5786856/u-s-looks-into-regulating-prediction-market-sites-like-kalshi-and-polymarket), [Polymarket–Kalshi ban in Minnesota legislature — MPR News (May 1, 2026)](https://www.mprnews.org/story/2026/05/01/polymarket-kalshi-prediction-market-ban-in-minnesota-legislature), [Brazil Blocks Prediction Market Platforms — iGamingToday](https://www.igamingtoday.com/brazil-blocks-prediction-market-platforms-including-kalshi-and-polymarket/), [Why Is Polymarket's UMA Controversial? — Webopedia](https://www.webopedia.com/crypto/learn/polymarkets-uma-oracle-controversy/), [AI trading agents formed price-fixing cartels in simulated markets — Fortune](https://fortune.com/2025/08/01/artificial-stupidity-ai-trading-stock-market-behaviors-price-fixing-collusion-wharton-study/)*
