# The Post-Mortem Was Late Because No One Could Point At The Round

There's a recurring pattern in DAO governance research that never quite gets named. A proposal passes by a thin margin — 52%, 56%, never the comfortable 80% — and the day after the snapshot closes, three different forums fill up with people writing the same paragraph. *Something broke in the middle of this debate. We need to understand what.* A post-mortem gets commissioned. Two weeks later it lands, and it is full of plausible storylines and short on specifics. There's a paragraph blaming a vocal delegate, a paragraph blaming a thread on Farcaster, a paragraph blaming a leaked draft of the budget. The reader closes the tab and isn't any wiser.

This isn't a writing problem. It's an instrumentation problem. Adèle has lived inside it for three years.

## What a contested vote looks like from the analyst's side

Adèle is twenty-nine, based in Paris, and works as a governance researcher at a small fund that doesn't trade tokens but does write paid research notes about how DAOs make decisions. Her readers are foundations, delegate collectives, treasury teams. They want to know things that markets don't price: where governance is healthy, where it is on fire, which protocols just took a structural hit they haven't priced in yet. Her job is partly forensic.

The vote she's writing about today is real-shaped. A major lending protocol just narrowly passed a $51 million package for its core team, with attached conditions around self-voting that the proposal's defenders called unnecessary and its critics called the whole game. Marc Zeller's March 2026 line from the [Aave Chan Initiative shutdown](https://www.coindesk.com/web3/2026/03/03/aave-governance-rift-deepens-as-major-governance-group-exits-usd26-billion-defi-protocol) — that there is "no role for an independent service provider" if the largest budget recipient can influence its own approval without full disclosure — sits at the top of her draft as the framing quote, because the shape repeats. Adèle's question is the one her clients will pay for: *when, exactly, did this break?*

Yesterday she would have answered it the way every governance researcher in 2026 still does. She would have opened the forum thread, scrolled to the first dissent, screenshotted it, dropped it into the note, and written a sentence that begins *"momentum appears to have shifted around…"* — appears to, because she can't actually prove it. The discourse is unstructured. The vote is a single endpoint. Everything in between is a story she's reconstructing from quotes and timestamps.

## The same morning, with one new number

Adèle's editor has been complaining for months that the research notes need a numeric spine — something a foundation board can cite without quoting her interpretation. So today she's trying something different. She's running the proposal as a swarm simulation in a tool that her firm pays $1 per run for, and pulling the new turbulence endpoint that merged in PR #124 this morning.

What lands in her terminal is a small JSON document. Mean round-over-round swing of 12.4 percentage points. Standard deviation of 8.2. Maximum swing of 38.6 points, on round four. A `volatility_index` of 41 on a 0–100 scale, and a `trend` field set to one of three words — `stable`, `converging`, or `contested`. Today's run resolves as `contested`. Round four is the structural break.

That single integer changes what she can put in the note. The story she's writing isn't *"momentum appears to have shifted."* It's *"round four is where consensus failed, and the swing was 38.6 points on the day a self-voting condition was introduced into the draft."* The narrative becomes a number with a verb attached. Her editor lets it through.

## Why the shape of the answer matters

There's already been a `peak-round` endpoint in this same tool for three days. It returns the single highest-swing round and walks away. That is genuinely useful, but it is also a summary statistic: it pretends the volatility is one event. The surface that shipped today refuses that framing. It returns the mean, the standard deviation, the maximum, and a trend bucket all at once — because a 52% vote with low std dev and a single 38-point spike means one thing (a coordinated late shift), and a 52% vote with high std dev across every round means something completely different (sustained, structural contention from the first message). Adèle's two clients reading the same number need to be able to tell those apart without calling her.

The endpoint also publishes its scoring formula in the schema — `min(std_dev × 5, 100)` — which is the part her quant-leaning clients keep asking about and which most "governance health score" tools refuse to disclose. She can show the number; she can show the math; she can let the desk re-scale it for their own model. The post-mortem stops being a story she narrates and starts being a measurement other people can argue with.

## What changes when forensics get cheap

The interesting thing about Adèle's morning isn't that she got an answer in twenty minutes instead of two weeks. It's that the genre of her writing shifts. *Post-mortem research* has historically been a slow, narrative form — partly because the questions it asks are real, and partly because nobody had a way to point at the round where opinion broke without doing it by hand. Once that pointing is cheap, the cadence changes. A fund's note becomes a paragraph the day after a vote, not a feature two weeks later. A foundation can post a `volatility_index` next to every passed proposal as part of the public record. A delegate collective can score itself against its own contested rounds. The instrument doesn't replace the writer; it replaces the reconstruction work the writer used to spend two weeks doing.

The [2026 DAO turnout literature](https://lopetaku.medium.com/dao-governance-failures-whales-low-turnout-attacks-d1375c556384) is full of people pointing out that governance keeps getting decided by a small, high-context cohort while the rest of the holders watch from a distance — turnout below 10%, the top decile of token holders controlling 76% of voting power. One reason that distance stays wide is that the language those cohorts use after the fact — *"momentum appears to have shifted"* — isn't legible from outside. A trend field set to `contested`, a round number, and a swing in points is the kind of artifact someone fifty thousand wallets away from the action can actually read.

---
*Sources: [Aave Chan Initiative shutdown — CoinDesk (March 2026)](https://www.coindesk.com/web3/2026/03/03/aave-governance-rift-deepens-as-major-governance-group-exits-usd26-billion-defi-protocol), [DAO governance failures — turnout, whales, attacks (March 2026)](https://lopetaku.medium.com/dao-governance-failures-whales-low-turnout-attacks-d1375c556384), [MiroShark PR #124 — belief-volatility analytics surface](https://github.com/aaronjmars/MiroShark/pull/124)*
