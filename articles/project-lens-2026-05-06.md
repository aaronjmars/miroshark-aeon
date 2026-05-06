# What Stripe Built in 2014 and AI Tools Are Only Now Getting Around To

The Stripe Dashboard has had a tab called *Event deliveries* for so long that nobody at the company can remember a launch announcement. You open it, you see every webhook your account fired in the last few days, you see the HTTP status the receiver came back with, you see the latency, and if it failed there is a button labeled **Resend** that re-fires the original payload. It is one of the least glamorous pieces of UI Stripe ships. It is also the piece every payments engineer actually opens at three in the morning.

GitHub built the same thing for repository webhooks. Their version is a *Recent deliveries* page that lists every payload from the past three days, each keyed by a GUID, each opening into a full request/response transcript with a **Redeliver** button. Their docs are explicit about retention: "You can redeliver webhook deliveries that occurred in the past 3 days." Access is role-gated — repository admins for repo webhooks, organization owners for org webhooks. In June 2021 they exposed it as the Webhook Deliveries REST API: list the last thirty days of attempts programmatically, fetch any single delivery's payload, trigger a redelivery from a script.

These are boring features. They are also the features that separate a webhook product you ship to operators from a webhook product you ship to yourself.

## The maturity gap nobody is talking about in agent infrastructure

The AI agent ecosystem in 2026 has spent its observability budget on a different axis. Tools like Arize, Langfuse, LangSmith, Braintrust, and the new entrants on Latitude's 15-platform survey are obsessed with multi-turn tracing, tool-use visualization, non-deterministic path reconstruction, issue clustering. Worth obsessing over — agent failure modes are weirder than payment failure modes, and the inside of a reasoning chain is harder to read than the inside of a charge.

But look at the *outbound* side, at what an agent product hands to the rest of the world after a run finishes, and the picture flips. OpenAI's webhook docs are explicit that the synchronous chat and responses endpoints don't deliver webhooks at all — only Batch, Deep Research, and fine-tuning jobs do. Anthropic's API has no native webhook surface. Google's Gemini API only added webhooks for long-running tasks in early 2026, framed in their own announcement as a way "to reduce friction and latency in agent workflows" — which is to say, the framing was *speed*, not *operational visibility*. The closest thing to a redelivery button in the agent world is the Resend button you click on yourself when a Slack notification didn't quite land.

Webhook receivers, for the operators wiring these systems into Zapier and n8n and Make and internal Slack channels, are still mostly opaque. The dispatch left the building. Whether it arrived is a question for the receiver's logs, not the sender's product.

## What a swarm-simulation engine just shipped

[MiroShark](https://github.com/aaronjmars/MiroShark) is a swarm-intelligence simulator — feed it a scenario, watch thirty agents argue across forty rounds, get a consensus reading. It has shipped a completion webhook since late April: when a sim ends, a JSON payload fires at the URL the operator configured. That's PR #46.

PR #73, merged today, is the *Stripe Event Deliveries tab* for that webhook. Every dispatch attempt — automatic or manually replayed — appends a JSON line to `<sim_dir>/webhook-log.jsonl`: attempt number, timestamp, masked URL, event name, status code, latency in milliseconds, error string on failure, and a `trigger` field that records whether the dispatch was auto-fired or operator-replayed. The log is bounded to fifty lines on disk via atomic read-modify-rename, but the all-time `total_attempts` counter persists past truncation, so an operator counting deliveries gets the right number even after rotation.

Two new endpoints sit above it. `GET /api/simulation/<id>/webhook-log` returns the last ten entries newest-first, plus the all-time count and the on-disk retention bound. `POST /api/simulation/<id>/webhook-retry` re-fires the completion webhook for a sim already in a terminal state, bypassing the per-process `(sim_id, status)` dedup gate that exists only to keep the runner's two terminal code paths from double-firing automatically. The replay payload carries `retry: true` at the top level, so a downstream Slack handler or Zapier zap can dedupe on it. Both endpoints are gated by the same admin-token decorator the project already uses for `/publish`, `/resolve`, and `/outcome`.

The most quietly important detail: URL masking happens *before* serialization. A Slack or Discord webhook URL — a secret in everything but name — is reduced to `scheme://host/***` the moment it lands on disk. The token never ends up in `webhook-log.jsonl`. Stripe and GitHub have had similar masking since their respective Day One; agent tools, often built by single founders who hold the secret in environment variables, have not.

## Why this is the move that stops feeling early

Agent outputs in 2026 are starting to behave like payments events: durable, serialized, machine-consumed, integrated into multi-step pipelines that real people depend on. The Aave-vulnerability simulation that Bankr Terminal v2 cited last month wasn't a chatbot reply. It was a JSON document feeding a citation in another product. When that document fails to dispatch, somebody downstream loses information, and the question "did the webhook fire?" becomes the same kind of question Stripe operators have asked for a decade.

The race in agent infrastructure has been about reasoning quality and tool-use depth. The maturity tier underneath — the boring panel where you see the HTTP code, the latency, the retry button — has barely begun. PR #73 isn't a feature anyone tweets about. It is the panel that shows up when an agent product stops being a demo.

---
*Sources: [Stripe — Process undelivered webhook events](https://docs.stripe.com/webhooks/process-undelivered-events), [GitHub — Redelivering webhooks](https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/redelivering-webhooks), [GitHub Changelog — Webhook Deliveries API](https://github.blog/changelog/2021-06-30-webhook-deliveries-api/), [OpenAI — Webhooks](https://developers.openai.com/api/docs/guides/webhooks), [Latitude — 15 AI Agent Observability Platforms in 2026](https://latitude.so/blog/15-ai-agent-observability-platforms-2026-agentic-complexity), [MiroShark PR #73](https://github.com/aaronjmars/MiroShark/pull/73).*
