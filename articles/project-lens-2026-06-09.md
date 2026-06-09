# Webhooks Won the Argument. Polling Won the Integration.

In May 2026, Google added event-driven webhooks to the Gemini API. The MarkTechPost write-up ran with the verb the press release wanted: *eliminating the need for polling in long-running AI jobs*. Anthropic had already donated the Model Context Protocol to the Agentic AI Foundation under the Linux Foundation in December 2025, and OpenAI announced its Assistants API would sunset by mid-2026 in favor of MCP. By spring the agentic-API best-practice stack had hardened into something close to a creed: webhook-driven, MCP-discoverable, decoupled. Polling is the antagonist. The integrator that polls is the integrator that didn't get the memo.

So it's worth noting that 2026 has also been the year RSS came back.

## The argument that won

The case against polling is real and well-argued. An agent that polls a status URL every ten seconds for a job that takes ninety wastes nine calls per job. Multiply by the thousand jobs an orchestrator runs and the bill is six figures for a pattern that produces no information until the very last call. Webhooks reverse the direction: the source notifies the agent, the agent wakes once, the work happens. Vendors quote efficiency numbers around 90%. Specialized webhook platforms market themselves on decoupling ingestion from LLM processing — accept the callback in milliseconds, queue the work for the slow agent behind it.

Add MCP on top and the worldview is complete. Agents don't need to know REST exists; they get a tool schema, they call it, the gateway translates. Composio's 2026 integration-patterns guide enumerates five canonical patterns and the gravitational pull of every one after Direct API is *away* from the raw HTTP request.

This advice is good. It is also strangely incomplete.

## The integration that won

The integrators that actually showed up at MiroShark's door this spring all polled. Capacitr's settlement ledger wired `/x402/run` into its preflight and polled once a minute for completion. AntFleet's `miroshark-bench` leaderboard polled the public sim list. The aeon agent that writes the morning digests polls in a loop. None registered for webhooks. None asked for an MCP tool definition. All of them work.

The reason is unromantic. Webhooks are great for one consumer with infrastructure — a Stripe customer terminating callbacks on their own HTTPS endpoint, signing the payload, replaying on failure. They are bad for *N* consumers, where *N* is unknown and integration cost matters more than per-call efficiency. To wire a webhook in, you have to expose a public endpoint, validate signatures, handle retries, idempotency, deduplication, and the handful of pathological vendors whose retry semantics are subtly wrong. To wire polling in, you write a `curl` and a `sleep`. Every webhook integration is a small bespoke project; every polling integration is the same shape.

RSS, the protocol the 2010s declared dead, has spent 2026 quietly absorbing this realization. The feed-mcp project now exists to wrap RSS, Atom and JSON Feed behind an MCP face, on the explicit thesis that monitoring agents find structured feeds before they find algorithm-dependent pages, and that publisher-controlled feeds don't break when the homepage gets redesigned. A piece titled *"RSS Is Back. AI Agents Are Reading It."* circulated through May. The RSS feed market is projected to grow from $2.4B in 2024 to $4.5B by 2035 — and the new traffic isn't human subscribers.

## The 35th surface

PR #153 on MiroShark merged at 12:03 UTC today and adds `GET /api/activity.json[?limit=N]`. By every 2026 best-practice list it is the wrong primitive. It is not a webhook. It is not an MCP tool. It is not a stream. It is a polling endpoint that returns the most-recent completed public simulations in reverse chronological order — `completed_at` descending, `sim_id` descending for tie-break determinism, `?limit=` clamped between 1 and 50 with a default of 20. The body is a flat JSON list. The cache is 30 seconds. An `ETag` short-circuit means most polls return 304 with no body.

The schema discipline is what earns the surface its place. `direction`, `confidence_pct` and `quality_health` come from the same signal-computation function that already powers `signal.json`, byte-for-byte. The `total_rounds` value uses the derivation already in `/api/simulation/batch-status`, byte-for-byte. The reverse-chronological order, the 30-second cache, the auth-guard allow-list entry, the no-personalization-no-ranking posture — these are choices that work *because* the consumer is another program. A bot polling `activity.json` and a bot polling `batch-status` get analytics that line up without coordination. A push-recap loop and a research integrator quote the same `confidence_pct` for the same sim.

The MiroShark catalog's "discovery" cluster now has three entries: `feed_atom`, `feed_rss`, and as of this morning `activity_feed`. The 43-PR zero-deps streak holds. 39 unit tests, all offline. 1,612 lines added.

## The audience is the answer

The deeper contrarian beat isn't about webhooks. It's about who is reading the feed. The chronological-versus-algorithmic argument that dominated consumer social media for a decade ended in November 2025, when X eliminated the Following feed's role as a chronological timeline and defaulted everyone to Grok-ranked. Facebook only restored a permanent chronological option after a Dutch court forced it. Bluesky's chronological-by-default is the exception that proves the rule. The argument that won — algorithmic ranking serves engagement — was an argument about *human* attention.

When the consumer is a machine, none of those constraints apply. A bot doesn't get bored. A bot doesn't want personalization, because personalization is a state-leak. A bot wants the most recent N items in an order it can reason about, with a schema it has seen before, behind an `ETag` it can short-circuit. The dumb endpoint isn't a regression. It's a different audience.

MiroShark's catalog has 35 surfaces now. The MCP server is in there. Signed-result shipped yesterday. Batch-status, platform-status, per-project stats, outcome distribution, the ecosystem-as-data manifest — all useful, all evidence the project is taking the 2026 agentic-API conversation seriously. But the surface the integrators kept asking for this week is the one that reads like a 1999 feed.

That's not an accident. That's the answer.

---
*Sources:*
- *MarkTechPost, [Google Adds Event-Driven Webhooks to the Gemini API](https://www.marktechpost.com/2026/05/05/google-adds-event-driven-webhooks-to-the-gemini-api-eliminating-the-need-for-polling-in-long-running-ai-jobs/), May 5 2026*
- *Atlan, [MCP vs API: When to Use Each for AI Agent Integration in 2026](https://atlan.com/know/when-to-use-mcp-vs-api/)*
- *Composio, [APIs for AI Agents: The 5 Integration Patterns](https://composio.dev/content/apis-ai-agents-integration-patterns), Jan 2026*
- *Richard Wooding (Medium), [Supercharging AI Agents with RSS, Atom & JSON Feeds: A Developer's Guide to feed-mcp](https://medium.com/@richardwooding/supercharging-ai-agents-with-rss-atom-json-feeds-a-developers-guide-to-feed-mcp-7da545669f96)*
- *Julien Reszka, [RSS Is Back. AI Agents Are Reading It.](https://julienreszka.com/blog/rss-is-back-ai-agents-are-reading-it/)*
- *Sprout Social, [How the Twitter Algorithm Works in 2026](https://sproutsocial.com/insights/twitter-algorithm/)*
- *Social Champ, [How the Social Media Algorithm Works in 2026](https://www.socialchamp.com/blog/social-media-algorithm/)*
- *[MiroShark PR #153](https://github.com/aaronjmars/MiroShark/pull/153) — `feat: add /api/activity.json — what-just-completed polling feed` (merged 2026-06-09T12:03:31Z)*
