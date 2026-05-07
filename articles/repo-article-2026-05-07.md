# MiroShark Stops Flying Blind: Two Observability Surfaces, Merged 14 Minutes Apart

For six weeks, MiroShark has been a publishing engine. You feed it a question, it spins up a swarm of AI agents to argue, vote, and trade prediction markets, and out the other end comes a packaged simulation — share card, replay GIF, transcript, RSS feed, trajectory CSV, watch page, ten different ways to broadcast a result to whoever should see it. What it didn't tell the operator, until today, was anything about whether those broadcasts were landing.

That changed in a single 14-minute window this morning. PR #74 merged at 12:11 UTC. PR #73 followed at 12:25 UTC. Together they close the operator-side feedback loop on both sides of the system — inbound (who used which surface) and outbound (did the webhook actually deliver). One architectural pattern, two directions, one push.

## Current State

MiroShark sits at 1,111 stars and 221 forks as of this morning, up from 1,098 / 219 yesterday — eleven new stars and two new forks in 24 hours, with the curve still bending up after the repo crossed 1,000 stars on May 3. The token sidecar is moving in the same direction: $MIROSHARK printed a new ATH of $0.000006926 on May 6 and is at $0.000004565 today, up 19.23% on the rolling 24h, with volume roughly 490% above the prior session and a 1.18× buy/sell ratio holding through the pullback. Open issues: one. Open PRs after today's two merges: zero.

That's the state of the repo. The state of the *operator*, until this morning, was that they could publish into a void.

## What Shipped Today

**PR #74 — Surface Usage Analytics** is the inbound side. Every time MiroShark serves a share surface — share card, replay GIF, transcript MD or JSON, trajectory CSV or JSONL, thread TXT or JSON, watch page, RSS or Atom feed render — it increments a counter inside the simulation's own folder. A new `<sim_dir>/surface-stats.json` file holds the counts. A new `GET /api/simulation/<id>/surface-stats` endpoint exposes them, publish-gated. The EmbedDialog grew a "📊 Distribution" panel, collapsed by default, that ranks surfaces by hit count and shows a running total.

**PR #73 — Webhook Delivery Log + Manual Retry** is the outbound side, filed yesterday and merged today fourteen minutes after #74. Every outbound completion webhook now writes a line to `<sim_dir>/webhook-log.jsonl` recording HTTP status, latency, trigger, and timestamp. A `GET /api/simulation/<id>/webhook-log` endpoint returns the last ten attempts plus a `total_attempts` counter that survives the 50-line on-disk truncation. A `POST /api/simulation/<id>/webhook-retry` lets the operator re-fire a delivery that failed, with a `retry: true` payload flag so downstream consumers can dedupe.

Both are publish-gated through the same `require_admin_token` decorator that's been load-bearing since PR #48. Both write into the same `sim_dir/` folder that's housed every per-simulation artifact since the project began. Both add an EmbedDialog panel that collapses by default. Neither adds a dependency — the zero-new-deps streak now spans fourteen consecutive substantive PRs.

## The Pattern Underneath

What makes the dual ship interesting isn't the features individually — it's that they share one architectural template. A per-simulation file (JSON for counts in #74, JSONL for an event log in #73). An atomic write via `tempfile.mkstemp` + `os.replace` that two concurrent requests can't tear. A schema lock — `SURFACE_KEYS` as a frozenset in #74, the URL-mask-before-disk rule in #73 — that silently rejects bad input rather than 500ing. A fire-and-forget call in the existing `_serve_X` or `_post_json` handler so the simulation runner is never blocked. A read endpoint that zero-defaults missing fields so the frontend has nothing to special-case. A collapsed EmbedDialog panel that operators expand only when they care. Thirty-one new offline unit tests land alongside (18 in #74, 13 in #73), so the contracts are pinned.

That pattern doesn't appear in any of the prior ten share surfaces. Those were all *outbound* — they package and broadcast simulation state. PRs #73 and #74 are the first surfaces that point *inward*, telling the operator something about how the system itself is performing. That's why merging them in a 14-minute window matters: it isn't two unrelated features stacking on the same morning, it's a coherent operator-observability layer landing in one push.

## Why It Matters

Webhook delivery logs and per-asset request counters are old, well-understood ground in operational software. Stripe's webhook deliveries tab and GitHub's recent-deliveries API have been operational furniture for over a decade; Hookdeck, OneUptime, and Beeceptor all publish 2026-dated guides on exactly the delivery-log + retry pattern PR #73 implements; Microsoft's own 2026 AI observability checklist names visibility into agent surfaces as table-stakes. What's interesting is that an autonomous-built simulation engine for $1 sims hit that floor in two PRs filed a day apart and merged within fifteen minutes of each other, with no new dependencies.

For an operator running MiroShark for a DeFi fund, a research desk, or a campaign team, the practical change is small but important: you can see what your audience actually used, and you can see whether your integrations are alive. The publish step stops being a one-way pipe. That's a different product than the one yesterday's operator was running.

---
*Sources: [PR #74 — Surface Usage Analytics](https://github.com/aaronjmars/MiroShark/pull/74), [PR #73 — Webhook Delivery Log](https://github.com/aaronjmars/MiroShark/pull/73), [MiroShark repo](https://github.com/aaronjmars/MiroShark), [Microsoft 2026 AI observability checklist](https://www.microsoft.com/en-us/microsoft-cloud/blog/2026/04/16/your-ai-steering-committees-2026-checklist-observability/), [BeInCrypto MIROSHARK](https://beincrypto.com/price/miroshark/price-prediction/)*
