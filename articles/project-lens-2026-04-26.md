# When the Bots Started Citing Each Other: Mapping the Agent Integration Economy

On Friday, the account belonging to Bankr Terminal v2 — the "web-native agent runtime" Bankr launched on April 14 with a sandboxed file system, CLI, MCP server connectivity, and configurable skills — posted a roundup tweet pinning five tools its operator had used during the week. One of them was @miroshark_, an open-source agent-based simulator: *miroshark — simulating Aave vulnerabilities prior to the rsETH incident.* The tweet picked up 156 likes and 40 retweets in a day. The quote-tweet thread it sat inside reached an estimated 15 million views over the weekend.

The numbers are mostly noise. The shape is the signal: an autonomous on-chain agent publicly cited an autonomous off-chain simulator — naming it, attributing a prediction to it, linking to it — in front of an audience the size of a mid-tier news network. This is what the integration economy looks like when machines join it.

## A map of who's citing whom

Draw three columns.

The left column is **citation sources** — systems that publicly name other tools as part of their normal operation. Bankr Terminal v2 sits here. So does Bankr's older bot, BankrBot, which Privy's case study describes as something Grok has [autonomously triggered](https://privy.io/blog/bankrbot-case-study) to deploy a token with no human in the loop. So do AI assistants with tool access — Claude Desktop, Cursor, Windsurf, Continue — every one of which now lists which servers it connected to in a given session. And so do the prosumer automation runners: Zapier, n8n, Pipedream, Make.

The right column is **citation targets** — tools that publish enough machine-readable surface to *be* cited. Five years ago this column was empty for almost every project. Today the entry requirement is three things: a tool catalog to call, a discovery spec to read, a push channel to subscribe to.

The middle column is **the protocol stack** linking the two. Three rungs, each from a different decade.

- **Webhook** (2007). Jeff Lindsay coined the term — your service POSTs to my URL when something happens. Stripe wired it in around its 2011 launch; GitHub and Twilio normalized it across the early 2010s; Salesforce, Shopify, Slack followed. By the time Zapier hit a million users, *firing a webhook on completion* was the lowest bar for joining the economy.
- **OpenAPI** (Swagger 2010, OpenAPI 3.0 2017, 3.1 2021). The discovery spec. Tells a foreign system every endpoint, parameter, and response. The format that made automatic SDK generation routine.
- **MCP — Model Context Protocol** (Anthropic, [November 25, 2024](https://www.anthropic.com/news/model-context-protocol)). A read protocol for AI assistants. Twelve months in: 97M monthly SDK downloads, 10,000+ active servers, adoption from OpenAI, Microsoft, and Google. The youngest rung — and the one that turned every integration-economy citizen into a potential citation source.

Each rung took years to consolidate when it appeared. Most teams shipping in 2026 inherit all three as commodity infrastructure.

## How fast joining the economy got

Here is what fully entering this map now looks like, measured in calendar days.

**April 24** — MiroShark's [PR #44](https://github.com/aaronjmars/MiroShark/pull/44) ships MCP onboarding: `GET /api/mcp/status`, server-resolved client snippets for Claude Desktop / Cursor / Windsurf / Continue, a Neo4j liveness probe, and a regex drift test that scans `mcp_server.py` against the published tool catalog. Read protocol live.

**April 25** — [PR #45](https://github.com/aaronjmars/MiroShark/pull/45) ships OpenAPI 3.1 + Swagger UI: a 1,900-line `openapi.yaml` covering ~85 paths under 13 tags, a Flask blueprint at `/api/docs`, and a static-analysis test that scrapes `@<bp>_bp.route(...)` decorators in `app/api/*.py` and asserts equality with the spec's path set. Discovery protocol live.

**April 26** — [PR #46](https://github.com/aaronjmars/MiroShark/pull/46) ships completion webhooks: a stdlib-only `webhook_service.py` with fire-and-forget daemon-thread POSTs deduped by `(sim_id, status)` so the runner's exit-code path and its `simulation_end` event path can both call it without double-firing, URL masking at the settings boundary, a "Send test event" button, and 18 offline unit tests. Push protocol live.

Three protocols, three days. Stripe's webhook story took years from incorporation to production; GitHub's took longer. It now collapses to a weekend because the protocols are no longer R&D — they are commodity public goods with reference implementations and lint tools. The cost of being citable used to be a roadmap. It is now a sprint.

## What changes when the citation graph is machine-driven

When the loudest external mention you receive comes from a bot reading another bot's output, three things change.

The unit of adoption stops being downloads or stars and starts being *citations* — the count of distinct autonomous systems that name your tool in their workflow. MiroShark crossed 829 stars and 153 forks today; the more interesting number is "one Bankr Terminal v2 roundup, fifteen million views." That kind of metric did not exist as a category a year ago.

The cost of producing a citation collapses with it. Bankr Terminal v2 didn't have to learn MiroShark's API — it had to read tweets about it. The instant a project is *visible enough to be talked about*, an MCP-equipped agent can cite it; the instant it is *legible enough to be queried*, a webhook-equipped runner can route around it. Visibility and legibility were the two slow steps. Both are now publishable in days.

And the integration economy stops being a B2B story. The map of who calls whom used to be drawn between SaaS companies. It is starting to be drawn between any two things with a public surface — a Telegram bot, a Polymarket-trading agent, a research simulator, a Zapier flow, a Discord webhook receiver. The arrows go both ways, and they are increasingly drawn by the agents themselves.

A 15-million-view footnote citing an open-source simulator is not a marketing event. It is the first visible row of a new ledger — written into webhooks, queried over MCP, discovered over OpenAPI, and read by autonomous systems that have never met a human user. The interesting projects in 2026 are the ones that finished joining this economy the week the rest of the world realized it existed.

---
*Sources: [Webhook — Wikipedia](https://en.wikipedia.org/wiki/Webhook) · [Stripe, Inc. — Wikipedia](https://en.wikipedia.org/wiki/Stripe,_Inc.) · [Introducing the Model Context Protocol — Anthropic, Nov 25 2024](https://www.anthropic.com/news/model-context-protocol) · [One Year of MCP — Zuplo](https://zuplo.com/blog/one-year-of-mcp) · [Bankr v2 / Bankr Terminal — Bitrue](https://www.bitrue.com/blog/what-is-bankr-bnkr) · [Getting Started with Bankr Terminal — Bankless](https://www.bankless.com/read/getting-started-with-bankr-terminal) · [BankrBot case study — Privy](https://privy.io/blog/bankrbot-case-study) · [Bankr launches x402 Cloud — Chainwire, Apr 2 2026](https://chainwire.org/2026/04/02/bankr-launches-x402-cloud-on-4-02-day-as-x402-protocol-joins-the-linux-foundation/) · [@bankrbot/status/2048026489707442360](https://x.com/bankrbot/status/2048026489707442360) · [@aaronjmars/status/2048170438107271382](https://x.com/aaronjmars/status/2048170438107271382) · [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) (829 stars) · [PR #44 — MCP Onboarding](https://github.com/aaronjmars/MiroShark/pull/44) · [PR #45 — OpenAPI 3.1 + Swagger UI](https://github.com/aaronjmars/MiroShark/pull/45) · [PR #46 — Completion Webhook](https://github.com/aaronjmars/MiroShark/pull/46)*
