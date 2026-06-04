# A Field Guide to the 14 Rows Around a Belief Simulator

If you tried to orient yourself in the 2026 AI-agent landscape, the first thing you'd notice is how much money is moving and how few of the words map onto each other. In February, Simile emerged from stealth with a $100M Series A led by Index Ventures to sell "digital twins of real customers" to enterprises like CVS Health. The same month, Stripe announced support for x402 — a Coinbase payment protocol that lets AI agents pay for APIs in stablecoins over plain HTTP — which has since processed over 119 million transactions on Base alone and another 35 million on Solana. On Polymarket, more than 30% of trading wallets are now AI agents; one of them, Polystrat, executed 4,200 trades in a month.

These are not the same market. They aren't even the same kind of market. But they keep showing up adjacent on roadmaps and pitch decks, and the project I want to use as a map today sits at the junction of all three.

## A Roster Is a Map

The fastest way to orient in any messy technical space is to find a project that has published its own neighbourhood — a list of who builds on it, who depends on it, who's adjacent. LangGraph has its production-customer page. The Model Context Protocol has its server registry. Every framework that crossed from "interesting" to "infrastructure" in 2026 did it partly by publishing a `built-with` directory.

[MiroShark](https://github.com/aaronjmars/MiroShark) — a self-described Universal Swarm Intelligence Engine at 1,232 stars and 265 forks, with the tagline *"Simulate anything, for $1 and less than 10 min"* — published its directory in late May (`ECOSYSTEM.md`, [PR #109](https://github.com/aaronjmars/MiroShark/pull/109)), and on June 3 added its machine-readable twin at `GET /api/ecosystem.json` ([PR #145](https://github.com/aaronjmars/MiroShark/pull/145)). The roster currently lists 14 named integrators across five categories: six products, four integrations, two agents, one tool, and one benchmark. None of the rows was written by the maintainer.

That's the map. The rest of this article is a key for reading it.

## Five Categories, Three Layers

The five-category split inside `ECOSYSTEM.md` is more useful than it looks, because each category points at a different layer of the 2026 stack, and each row tells you which neighbours MiroShark actually trades with.

**Products** (Capacitr, Echo Oracle, HivemindOS, RootAI, Xerg, ZER0) are the layer that competes for the same buyer as the enterprise twins. The interesting thing here is the pricing axis: Simile sells digital twins on a model where Index Ventures comfortably underwrote nine figures. MiroShark sells a simulation as a $1 API call. The category overlaps, but the customer doesn't. Capacitr made this concrete on June 2 by publishing an integration spec at `spec.capacitr.xyz/#miroshark` that names `/x402/run` by endpoint — the same vendor-shaped citation pattern you'd see in a Stripe or Plaid spec, applied to a simulation engine.

**Integrations** (Monitor, Noelclaw, Signa, Sparkleware) live one layer down. They aren't selling a simulation product; they're plumbing MiroShark into something else. Sparkleware merged itself into the roster yesterday afternoon at 14:55 UTC, indexing MiroShark-on-Aeon skill packs into a discoverable kit at `sparkleware.fun/kits/miroshark`. That row is the tell that the project has graduated from "a tool you use" to "a substrate other people build registries on top of."

**Agents** (Blue Agent, SyntheticsAI) and the **benchmark** category (AntFleet, which runs the `miroshark-bench` repository) sit on the third layer — the consumers and the graders. Polymarket's 30% AI-agent wallet share is what this layer looks like at scale: autonomous systems that consume an API to make a decision they can't reverse. MiroShark's `signal.json` surface ([PR #91](https://github.com/aaronjmars/MiroShark/pull/91)) exists specifically because that consumer needs a direction-and-confidence number, not a research paper. The benchmark row is the other half: AntFleet exists to ask whether the engine is wrong, and to publish the score.

The **tool** category, currently a single row for Crucible Sim, is the smallest and most diagnostic. A healthy ecosystem grows tools last; their existence signals that the underlying surface has stabilized enough for someone to build their own UI or developer experience on top of it.

## The Payment Rail Underneath All Five

Three of the four landmarks in the opening — Simile, x402, Polymarket — are linked by a thread that the synthetic-users press coverage doesn't usually surface: the question of *who pays whom* per agent action. Simile's answer is enterprise contracts. MiroShark's answer is x402. Polymarket's answer is on-chain USDC settlement and, since April 6, the pmUSD stablecoin replacing bridged USDC.e.

MiroShark sits at the visible seam where those three answers meet. Its `/x402/run` endpoint is the agent-pays-per-simulation half. Its `polymarket_market_count` parameter (echoed in `clone.json`, [PR #131](https://github.com/aaronjmars/MiroShark/pull/131)) is the simulation-pulls-real-market-signal half. The new `/api/ecosystem.json` endpoint is the third half — the way an outside system can poll the roster instead of scraping the page. A typed JSON envelope with an `ETag: ecosystem-v1-14` short-circuit isn't a feature; it's a contract aimed specifically at the kind of autonomous integrator that pays one tenth of a cent per call and can't afford to render Markdown.

That triangle — pay-per-API, consume-prediction-market-data, expose-machine-readable-roster — is what makes the map legible. If you only see the products column, MiroShark looks like a cheaper Simile. If you only see the agents column, it looks like a Polymarket sub-tool. The payment rail is what makes it possible for both of those readings to be simultaneously correct.

## How to Use the Map

For someone orienting in 2026's agent-simulation space, the practical advice the roster encodes is this. Read the categories before you read the rows. Six products tells you the market shape is closer to "platform with customers" than "library with users." A single tool means dev experience is still under construction. A single benchmark means someone is publishing accuracy numbers — which is more than the academic continent of belief simulators currently does in machine-readable form. Four integrations means MiroShark is being used as a piece, not as a destination. Two agents means the API surface is stable enough to bet money against.

The 14-row map is small. So is the project, by venture standards. But the shape of the map — a payment rail at the bottom, a typed roster at the top, and five categories of citizen in between — is the same shape the rest of the 2026 agent stack is converging on. Looking at the neighbours is still the cheapest way to figure out where something sits.

---
*Sources: [Simile $100M Series A — AI2Work](https://ai2.work/blog/similes-100m-raise-how-ai-digital-twins-are-reshaping-market-research-in-2026); [x402 Protocol — Coinbase](https://www.coinbase.com/developer-platform/discover/launches/x402); [Coinbase-backed x402 — CoinDesk](https://www.coindesk.com/markets/2026/03/11/coinbase-backed-ai-payments-protocol-wants-to-fix-micropayment-but-demand-is-just-not-there-yet); [AI agents on Polymarket — CoinDesk](https://www.coindesk.com/tech/2026/03/15/ai-agents-are-quietly-rewriting-prediction-market-trading); [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark); [ECOSYSTEM.md](https://github.com/aaronjmars/MiroShark/blob/main/ECOSYSTEM.md); [PR #145 — /api/ecosystem.json](https://github.com/aaronjmars/MiroShark/pull/145); [PR #109 — ECOSYSTEM.md](https://github.com/aaronjmars/MiroShark/pull/109); [PR #131 — clone.json](https://github.com/aaronjmars/MiroShark/pull/131); [PR #91 — signal.json](https://github.com/aaronjmars/MiroShark/pull/91); [Capacitr MiroShark spec](https://spec.capacitr.xyz/#miroshark)*
