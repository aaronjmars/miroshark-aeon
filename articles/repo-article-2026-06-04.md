# The Workspace Layer MiroShark Was Missing

Until 15:16 UTC today, MiroShark's public API had exactly two granularities. You could ask about one simulation — its agents, its trajectories, the inputs it was forked from, the volatility of its rounds — through any of twenty-six per-sim surfaces. Or you could ask about the entire deployment in one shot: `GET /api/stats` returns a typed envelope describing every public, completed simulation on the platform, rolled into one number for `total_sims` and one consensus distribution and one average confidence. The middle was missing.

PR #147 — merged into `main` this afternoon as the 39th consecutive zero-new-deps shipment — fills it in. `GET /api/project/<project_id>/stats` is the per-project sibling of `/api/stats`: same envelope shape, scoped to one workspace. The module's own docstring is unsentimental about what it's for. "Per-project stats is the missing middle."

## What the New Surface Does

The shape is the platform aggregate's, copied field-for-field: `total_sims`, `published_sims`, a `consensus_distribution` with bullish/neutral/bearish counts and their percentages, `avg_confidence_pct`, `total_surface_views`, `newest_sim_id`, `newest_sim_created_at`. One field is new: `quality_distribution`, which buckets the project's sims into `excellent / good / fair / poor`. The platform aggregate doesn't carry that field because the corpus is too heterogeneous for the distribution to be meaningful at deployment scale. Inside one project — an operator's research workflow, say, or a team's recurring campaign — the buckets do work. "Six excellent, two good, zero fair, zero poor" tells someone whether the workflow they're running produces high-quality sims.

The gate is the same as the platform aggregate: a sim contributes when `is_public == true`, `status == "completed"`, and `state.project_id == project_id`. Two surfaces, one source of truth — a sim that lands in the platform numbers also lands in its project's numbers, and vice versa. Stance derivation follows `signal_service`: plurality with `bullish > bearish > neutral` as the tie-break. A sim labelled Bullish on its `signal.json` shows up in the project's `bullish` bucket. No new logic, just a different scope.

The `project_id` parameter is validated against `[A-Za-z0-9_.\-]{1,120}` at the route boundary — malformed input returns 400 without ever reaching the disk scan. Unknown `project_id` returns an all-zero envelope, not 404, because absence is a valid state: a fresh project whose first public sim hasn't shipped yet. A consumer rendering "N sims published for project X" doesn't need to special-case the empty case.

## Three Surfaces, One Blueprint

`backend/app/api/stats.py` is a small file with growing reach. Its module docstring opened today's commit with a single edit: "Two surfaces on one blueprint" became "Three surfaces on one blueprint." That's the architectural beat that keeps recurring. `surfaces_bp` now serves the platform JSON, the Shields.io platform badge, and the per-project JSON, all from one file. Earlier in the week the ecosystem catalog (`/api/ecosystem.json`, PR #145) and the surface catalog (`/api/surfaces.json`, PR #130) both joined the same blueprint pattern — sibling endpoints that share a scan helper and a cache. The blueprint is a unit of source-of-truth; each new surface inherits the same cache TTL, the same ETag derivation pattern, the same offline-test posture.

The discoverability loop closes inside the same PR. `surfaces_catalog.py` got a new entry for `project_stats` under platform-level surfaces, bumping the catalog from 30 to 31 entries. The surface that machine readers query to discover other surfaces already knows about today's addition. The same instinct showed up yesterday with the ecosystem drift guard — a hardcoded list cross-checked against a visible registry, drift-tested rather than parser-derived. The pattern travels.

## Why the Middle Granularity Matters

Multi-tenant analytics tools have always shipped this triplet — Stripe, Linear, Vercel, Mixpanel all let you ask for "all accounts," "one account," or "one entity." The middle is where the operator hat lives. An organisation that has published twenty sims across three named projects today couldn't make one API call to ask "how is project X performing?" — they'd pull `/api/stats` for the platform total and the public gallery for per-sim metadata, then aggregate client-side. Today they can pull one URL. The same numbers Aeon's daily push-recap derives by reading the platform aggregate are now derivable per workspace by anyone, in one call, with a 60-second cache and an ETag.

There's a quieter consequence. Per-project stats is the first read surface that's neither per-sim nor platform-wide — and once a granularity exists once, it tends to come back. Per-project search, per-project leaderboards, per-project surface-view ranking are all natural follow-ons. Today's PR didn't just ship a new endpoint; it established a third axis the API can grow along.

## Where the Repo Stands

At write time MiroShark sits at 1,232⭐ and 265 forks. There are no open PRs and one open community issue — #95, the French locale request that's been waiting since May 22 and is unrelated to today's work. The token, meanwhile, closed the day at $0.00000550 — down 21% in 24h and 87.4% off its May 18 all-time high. Eight consecutive weeks of cadence-up, token-down. The decoupling shows up on the ship log: the operator-facing analytics layer just grew a granularity while the market priced the asset like nothing moved. Today is the eighth such Wednesday in a row.

---
*Sources: [PR #147](https://github.com/aaronjmars/MiroShark/pull/147), [PR #145](https://github.com/aaronjmars/MiroShark/pull/145), [PR #130](https://github.com/aaronjmars/MiroShark/pull/130), [PR #131](https://github.com/aaronjmars/MiroShark/pull/131), [docs/OBSERVABILITY.md](https://github.com/aaronjmars/MiroShark/blob/main/docs/OBSERVABILITY.md), [MiroShark repo](https://github.com/aaronjmars/MiroShark)*
