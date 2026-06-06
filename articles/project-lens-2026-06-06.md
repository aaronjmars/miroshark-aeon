# Fourteen Workloads, One Question: A Day in the Life of a Pre-Trade Scenario Sweep

On May 5, 2026, Google added event-driven webhooks to the Gemini API, framing the change as "eliminating the need for polling in long-running AI jobs." The pitch ran in lockstep with Anthropic's Batch API (24-hour SLA, 50% discount), OpenAI's Batch endpoint (same), and Cloudflare Workers AI's async queue. The trade is consistent across vendors: hand the platform a fleet of work, give up live latency, save on cost, and ideally stop having to ask whether the work is done yet.

The unfashionable side of that trade is that webhooks aren't always an option. If your "fleet" isn't ten thousand independent prompts but fourteen long-running simulations on a server you don't control, "is any of them done yet" is still a question someone has to ask, every minute, until the answer changes. The shape of that question is the difference between a polling loop that scales and one that doesn't.

## Maya's Tuesday morning

Maya is a junior analyst at a five-person research shop publishing desk notes on prediction-market events. Polymarket set a single-day volume record of $425M on February 28 and the desk's edge is writing the note before consensus catches up. Maya's morning job: translate an open question — "does the jobs report move the 'Fed cut in July' market more than five points" — into a set of belief simulations parameterised over demographic mixes the desk thinks might dominate the response.

Each simulation costs about a dollar and takes under ten minutes. Maya runs fourteen of them in parallel: seven demographic mixes crossed with two prompt framings. She fires them off at 09:00, and by 09:15 the first ones are starting to land. Until today, her loop looked like this:

```
for sim_id in MY_SIMS:
    r = requests.get(f"https://miroshark.com/api/simulation/{sim_id}/state")
```

Fourteen HTTP calls per cycle. Roughly four hundred and twenty per hour at a thirty-second cadence. Each call returns the full simulation state object — round count, agent positions, transcript pointers — none of which Maya needs until the simulation has actually completed. The bandwidth cost is hers; the request-count cost is the platform's. Her code is correct. It is also fourteen times the size it needs to be.

## What changed

PR #150 was opened on the watched repo at 11:34 UTC this morning. It introduces a single new endpoint — `POST /api/simulation/batch-status` — that accepts a list of up to twenty simulation IDs and returns one entry per ID, parallel to the input. For Maya, the loop collapses to one call:

```
r = requests.post(
    "https://miroshark.com/api/simulation/batch-status",
    json={"sim_ids": MY_SIMS},
)
```

The response contains a `count`, a `schema_version`, and a `results` list whose `i`-th entry corresponds to the `i`-th input ID. The status field tells her whether each simulation is running, completed, failed, or cancelled. Completed entries also carry the four fields she actually wants — `direction`, `confidence_pct`, `quality_health`, `completed_at` — computed byte-for-byte from the same `compute_signal` service that powers each sim's per-sim `signal.json`. There is exactly one source of truth for the math, which means a sim Maya checks via batch can't disagree with the sim Maya checks via the per-sim surface.

Fourteen polls became one. Four hundred and twenty hourly requests became thirty.

## The detail that matters more than the count reduction

The temptation when reading this surface is to file it under "convenience endpoint." It isn't. The piece worth dwelling on is what the response looks like when one of Maya's fourteen IDs is wrong — a typo, a deleted sim, a sim from a different user — versus when it's correct but private.

In both cases the response is byte-identical: `{found: false, status: null, direction: null, ...}`. There is a dedicated test, `test_private_and_unknown_are_indistinguishable`, that asserts the two shapes are equal except for the `sim_id` field. Maya cannot use the batch endpoint to probe for the existence of someone else's private sim, because the endpoint can't tell her whether the sim doesn't exist or whether it exists and isn't hers. The privacy invariant is not a comment in a README. It's a unit test.

This is the boundary that makes the surface usable beyond Maya's single-tenant case. If a competing desk hits the same endpoint with a list of Maya's IDs, hoping to learn whether her sims are running, they get the unknown-ID envelope back. The information they would have wanted to leak across users — that the IDs are valid at all — is absent from the wire. The batch primitive composes with the publish-gate the platform already had, instead of going around it.

## What this kind of user wants next

Maya isn't the only persona pulling against this endpoint. The Capacitr integration spec — public at spec.capacitr.xyz/#miroshark since June 2 — names `/x402/run` as the request side of an agent-to-agent payment flow. A batch-status surface is what its caller hits to know which of the dozens of x402-paid sims in flight are ready to act on. The repo's `internal_auth_guard` allow-list now contains exactly three platform endpoints — `/openapi.json`, `/health`, and (since yesterday's merged PR #149) `/api/status.json` — and as of this morning's opened PR, a fourth: `/api/simulation/batch-status`. Each is something an external integrator hits before they hit anything that needs a key.

The pattern emerging from Maya's morning isn't sophisticated. It's the recognition that the answer to "stop polling" is usually "poll less, not stop." For workloads where webhooks are available and reliable, replace the loop. For workloads where the platform is someone else's server and the integration is a stranger's spec page, give the loop a primitive of the right shape — one call, list semantics, identical envelopes for the cases the caller isn't supposed to distinguish — and let it run. Maya's HTTP graph this afternoon looks the same as it did yesterday. The bill underneath it does not.

---
*Sources: [Gemini API webhooks](https://www.marktechpost.com/2026/05/05/google-adds-event-driven-webhooks-to-the-gemini-api-eliminating-the-need-for-polling-in-long-running-ai-jobs/), [Anthropic Batch API guide](https://claudereadiness.com/blog/claude-batch-api-enterprise/), [OpenAI Batch API](https://tokenmix.ai/blog/openai-batch-api-pricing), [Polymarket Feb 28 $425M record](https://metamask.io/news/prediction-market-overview-trends-2026), [Cloudflare Workers AI Batch](https://developers.cloudflare.com/workers-ai/features/batch-api/), [MiroShark PR #150](https://github.com/aaronjmars/MiroShark/pull/150)*
