# When the Price of a Question Falls to a Dollar

In 1865 a British economist noticed something that still trips up everyone who reasons about cost. Make a resource cheaper to use, William Stanley Jevons argued, and a society does not use less of it. It uses more. Better steam engines burned coal more efficiently — and Britain's coal consumption went *up*, because efficiency made coal worth burning in places it never would have before.

The pattern has a name now — induced demand — and it is about to do something strange to the business of asking "what would a crowd do?"

## What gets cheap gets used differently

Run the numbers on language-model inference and the Jevons curve is almost vertical. Andreessen Horowitz, tracking what it calls ["LLMflation,"](https://a16z.com/llmflation-llm-inference-cost/) found the cost of a fixed level of model performance fell roughly 1,000x over three years — from $60 per million tokens in late 2021 to about $0.06 by 2024 — a 10x drop every year. [Epoch AI's price series](https://epoch.ai/data-insights/llm-inference-price-trends) puts the decline between 9x and 900x per year depending on the task, with the median jumping from 50x to 200x annually after January 2024. The fastest curves only start once the floor drops out.

Here is the part the spreadsheets miss. When inference gets this cheap, people don't run the same workloads for less money. They redesign the work to consume more of it. A 2026 arXiv paper, [*Photons = Tokens*](https://arxiv.org/pdf/2603.06630), takes the Jevons logic straight into AI: as the unit price of intelligence falls, demand doesn't relax, it expands. Developers reach for deeper reasoning loops, larger contexts, and multi-agent pipelines that multiply tokens per task. Cut the price and consumption more than makes up the difference.

That is the lens. The interesting question about cheap simulation is not "how much do you save." It is "what do you start doing that you'd never have done before."

## From a research project to a reflex

Consider the thing being undercut. Asking a representative crowd what it thinks is expensive and slow. A single focus group runs [$7,000 to $20,000](https://www.driveresearch.com/market-research-company-blog/how-much-does-market-research-cost/) once you count recruiting, facilities, moderation, and incentives. A custom quantitative study lands between $25,000 and $65,000. An online survey of 400 people starts around $5,000 — and response rates keep falling, so each real human costs more every year.

At those prices you ask once. You scope the question for months, because a wrong question wastes a quarter's budget. The cost structure makes you careful, and "careful" quietly means "rare."

Now drop the price of a crowd to a dollar. There is an open-source engine whose entire pitch is exactly that line — *simulate anything, for $1 and less than 10 minutes*. Spin up a scenario and it spawns hundreds of language-model agents, each seeded from real census data via its `demographic_sampler.py`, lets them argue across rounds, and has them trade an internal market until their aggregate belief settles into a number and a report.

The temptation is to read that as the $25,000 study, now cheaper. That reading misses the whole point of Jevons. At a dollar, you don't run the careful study once. You run the question forty ways before lunch. You stop treating simulation as research and start treating it as a reflex — the thing you do *before* you've decided what you're really asking.

## The tell is in the plumbing

You can see which bet a team is making by what it builds around the core product. A tool designed for the $25,000-study mindset gives you a results page: one run, one verdict, framed and final. The engine in question is building the opposite.

In early June it shipped `POST /api/simulation/batch-status` — a single call that looks up the state of *many* simulations at once. Nobody writes a batch-status endpoint for a user running one simulation. It shipped `/api/activity.json`, a polling feed of "what just completed" — a firehose, which only makes sense if completions are frequent enough to need a stream. And `/api/stats/distribution.json` collapses *every public completed run* on the platform into confidence tiers — an endpoint whose very existence presupposes a large, growing population of runs to aggregate.

Read those three together and the architecture stops looking like a research instrument and starts looking like infrastructure for volume. Batch lookups, an activity stream, a platform-wide distribution: these are the plumbing of a system that expects to be hit a thousand times, not consulted once a quarter. The team is not pricing for the budget. It is building for the behavior the price will cause.

## What gets built by the end of 2027

So a claim specific enough to be wrong on a schedule. By the end of 2027, the agent-simulation tools that matter will not be the ones with the most lifelike single run. They will be the ones cheap and fast enough that people run them speculatively — and the visible tell will be tooling for *managing many runs*: batch control, run-to-run diffing, searchable history, distributions over outcomes. The teams polishing one beautiful simulation are answering yesterday's question, the one priced like a focus group. The ones building the firehose have already read Jevons.

Britain didn't burn less coal when engines got efficient. It found a hundred new things to burn coal on. The cost of asking a synthetic crowd a question just fell three orders of magnitude in three years and is still dropping. The reflex that replaces the research project is the actual product — and the first engines wiring themselves for that flood, rather than for a tidy quarterly study, are the ones that will still be standing when everyone else realizes cheap didn't mean *the same, but less*.

---
*Sources:*
- [Welcome to LLMflation — Andreessen Horowitz](https://a16z.com/llmflation-llm-inference-cost/) — ~1,000x inference cost decline over three years, $60→$0.06 per million tokens, 10x/year
- [LLM inference prices have fallen rapidly but unequally — Epoch AI](https://epoch.ai/data-insights/llm-inference-price-trends) — 9x–900x annual decline, median 50x→200x after January 2024
- [Photons = Tokens: The Physics of AI and the Economics of Knowledge (2026) — arXiv](https://arxiv.org/pdf/2603.06630) — applies the Jevons paradox to AI inference; falling token prices expand rather than relax demand
- [How Much Does Market Research Cost? — Drive Research](https://www.driveresearch.com/market-research-company-blog/how-much-does-market-research-cost/) — focus group $7k–$20k, custom study $25k–$65k, survey baselines
- [MiroShark repository](https://github.com/aaronjmars/MiroShark) — "$1 & <10 min" engine, `demographic_sampler.py` census seeds, `POST /api/simulation/batch-status`, `/api/activity.json`, `/api/stats/distribution.json`
