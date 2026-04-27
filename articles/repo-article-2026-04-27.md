# From Citation to Surface: MiroShark Builds the Page That Survives the Tweet

Yesterday a Bankr Terminal v2 thread cited MiroShark's Aave vulnerability simulation. The thread cleared 15M views and put the project in front of the audience it has been building for. Today, [PR #47](https://github.com/aaronjmars/MiroShark/pull/47) merged at 13:46 UTC and PR #48/#49 followed eighteen minutes later at 14:04 UTC. The first turns that citation into a permanent product surface — a `/verified` gallery of simulations that called real-world events. The second locks the door on every endpoint that can change what shows up there. Two PRs, fifty-eight minutes apart, and the credibility moment now lives inside the repo.

## Current state

[MiroShark](https://github.com/aaronjmars/MiroShark) sits at **838 stars and 158 forks** as of this writing — thirty-eight days after the first commit. The repo description is unchanged from April 21: *"Simulate anything, for $1 & less than 10 min — Universal Swarm Intelligence Engine"*. Zero open PRs. The 1K-by-April-30 target needs roughly fifty-four stars per day across the next three days; today added nine. The token closed yesterday's session +34.75% and the intraday high today crossed the previous April 14 ATH by 25%. The week's shipping calendar reads as one continuous arc — graph memory on the 21st, share card on the 22nd, public gallery on the 23rd, MCP onboarding on the 24th, OpenAPI on the 25th, completion webhook on the 26th, and `/verified` on the 27th. Seven straight days, each PR depending on something merged within the same week.

## What's been shipping

PR #47 adds a **Verified Prediction** annotation layer on top of every public simulation. From the Embed dialog, an operator picks **Called it / Partial / Called wrong**, pastes the article or tweet that confirmed the outcome, writes a one-sentence summary (≤280 chars), and saves. The annotation lands on `<sim_dir>/outcome.json` and immediately renders a 📍/⚠/◑ pill on the gallery card, adds a coloured left-edge accent so the hall reads at a glance, counts toward a new **verified** stat chip, and becomes filterable via a `/verified` URL. The annotation is intentionally distinct from the existing `/resolve` endpoint, which is binary YES/NO tied to Polymarket consensus and drives the `accuracy_score`. A simulation can have both — the resolve endpoint scores the prediction, the outcome annotation curates the credibility surface.

PR #48/#49 — filed and merged the same hour — applies a `require_admin_token` decorator to `/publish`, `/resolve`, and the new `/outcome` mutation route. The decorator reads `MIROSHARK_ADMIN_TOKEN` per-request, checks `Authorization: Bearer`, and returns **503 if the env var is unset** (so an operator who forgot to configure can't ship an open mutation surface) and **401 with a generic "Unauthorized"** if the token is wrong. Constant-time compare via `hmac.compare_digest`. Seventeen new unit tests pin down header parsing, env loading, fail-closed semantics, and per-view decorator presence.

## Technical depth

The interesting design decision in PR #47 isn't *that* the gallery gets a verified filter — every gallery has one. It's where the data lives.

`<sim_dir>/outcome.json` is a flat artifact alongside the existing `simulation_config.json`, `quality.json`, `trajectory.json`, `resolution.json`, and `state.json`. There is no new database table, no new schema migration, no new ORM. The `_read_outcome_file()` helper validates the label, truncates oversized summaries with `[:277].rstrip() + "…"`, and **strips any non-http URL** — defense-in-depth so a corrupt artifact can never land a `javascript:` value on a gallery card. `_build_gallery_card_payload()` surfaces a new `outcome` field on every card. `GET /api/simulation/public?verified=1` filters before pagination so `total` and `has_more` reflect the filtered set.

This is the third time in a week the same beat lands. PR #42's share card, PR #43's public gallery, and PR #47's verified hall all read from the simulation directory, transform with a small helper, and project a new view. **Sim dir is the schema**; views are cheap. The architectural payoff is that PR #47 ships in 1,194 lines across nine files with eight new unit tests — and the OpenAPI drift-detection test that PR #45 introduced two days ago **passes on first run** because the new Flask route is properly documented in `openapi.yaml`. The contract enforces itself.

PR #48/#49 closes the loophole that the new write endpoint surfaced. The 503-vs-401 split is the load-bearing detail: 503 is "you forgot to configure" (an actionable signal for ops alerting), 401 is "someone is probing" (a generic refusal that doesn't fingerprint). The decorator is reusable for any future mutation endpoint.

## Why it matters

A 15M-view thread is a moment. A `/verified` page indexed by Google, embedded in pitch decks, and linked into every future thread about pre-incident swarm simulations is a surface. The Bankr Terminal v2 citation will fade out of the X feed within a week — the page that catalogues outcomes like it doesn't. PR #47 is the move that converts a transient credibility spike into a compounding asset, and PR #48/#49 is the recognition that a compounding asset is worth gating. The week's shipping rhythm has been about making MiroShark addressable from the outside (MCP, OpenAPI, Webhook). Today's two merges are about making the inside legible to the outside while keeping the keys.

---
*Sources: [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) · [PR #47](https://github.com/aaronjmars/MiroShark/pull/47) · [PR #49](https://github.com/aaronjmars/MiroShark/pull/49) · [PR #45](https://github.com/aaronjmars/MiroShark/pull/45) · [PR #46](https://github.com/aaronjmars/MiroShark/pull/46)*
