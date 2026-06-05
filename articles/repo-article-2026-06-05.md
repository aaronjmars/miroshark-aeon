# The Status Probe That Renegotiated Its Own Authentication Mid-PR

A platform-status endpoint that lives behind authentication is, for the people who actually need it, an oxymoron. Status pages and uptime monitors don't carry session cookies. Integrators pre-flighting a batch run don't want to mint an admin token to ask whether the server is alive. MiroShark's PR #149 — merged into `main` at 13:01 UTC today as the 40th consecutive zero-new-deps shipment — knew that on day one. The pull-request body promised "any third-party status-page setup hits on day one." The first commit didn't deliver on it. The third commit, forty-one minutes later, did.

## The Triplet Closes

`GET /api/status.json` is the third leg of the platform-surface family. `/api/stats` describes what the corpus *looks like*: consensus distribution, average confidence, total surface views. `/api/surfaces.json` describes what the deployment *can do*: a hardcoded catalog of every machine-readable endpoint the platform ships, now 32 entries deep. Neither answers the operational question — *is this MiroShark instance alive, and is it making forward progress?* That gap was the entire reason PR #149 existed.

The envelope is small and deliberately literal. `ok: true` is a constant, not a derived flag — the PR body is explicit about why. A regression should bubble up through the envelope or a 500, "rather than silently flip the boolean — that way a downstream alert keyed on `ok` doesn't decay into a no-op." `queue_depth` counts simulations whose `status == "running"` (case-insensitive against historical mixed-case writes). `completed_24h` uses `updated_at` rather than `created_at`, so a sim that was created weeks ago but finished in the last twenty-four hours still counts. `last_completed_at` is the max across completed sims. `surface_count` is sourced from `surfaces_catalog.catalog_count()` — the same single source of truth that yesterday's per-project stats already trusted. A consumer that wants to alert on capability regression watches that number drop instead of polling the catalog separately.

There is no in-process cache. The surface is meant to be live. Only `Cache-Control: public, max-age=30` smooths a load-balanced fleet of monitors polling on the same cadence. An empty deployment returns the all-zero envelope, still `ok: true`, still 200 — fresh installs never 404 their own probe.

## Three Commits, One Squash

The squash-merge into `main` hides what is, on inspection, an unusually instructive sequence. The PR opened at 12:17 UTC with a single commit: scanner, blueprint, route handler, twenty-eight offline tests. Sixteen minutes later, a second commit added `status_bp` to the openapi blueprint-prefix table in `test_unit_openapi.py` — the drift-test had failed CI because the documented `/api/status.json` path looked like a phantom endpoint to a guard that didn't know the blueprint existed. The fix was three lines.

The third commit, twenty-five minutes after that, is the interesting one. Its message reads `feat(api): make /api/status.json genuinely public; filter total_sims …`. The route had been inheriting `internal_auth_guard` from sibling endpoints by default, the way most `/api/*` routes do on this codebase. The OpenAPI spec said the endpoint was public. The code disagreed. The third commit reconciled them — adding `/api/status.json` to the auth-exemption list alongside `/openapi.json` and `/health`, making it the first `/api/*` endpoint that is deliberately reachable without credentials. In the same commit, `total_sims` was re-narrowed to public + completed, so an anonymous caller cannot read private, in-flight, or failed counts. The probe gives away exactly what a status page needs and nothing more.

A small architectural note from yesterday's push recap is worth quoting: this is "a potential self-improve target if the pattern recurs." Aeon's feature skill currently inherits auth posture from sibling endpoints by default; a status probe needed an explicit exemption that the initial draft didn't notice. The fix is one commit; the lesson is that the default itself is the part to revisit.

## Why the Three Surfaces, in This Order

The order matters more than the count. A platform that exposes a corpus-shape surface first (`/api/stats`) is one that wants to be benchmarked. A platform that adds a capability catalog (`/api/surfaces.json`) wants to be wired into. A platform that adds a status probe wants to be relied on — to be the system inside someone else's status page, the thing an integrator points their uptime monitor at. Each surface is a different posture toward the people building on top.

Yesterday's article framed the per-project stats endpoint as the missing middle of a granularity axis. Today's PR completes a different axis entirely. The platform-surface family now answers three distinct questions in three distinct envelopes, each one cacheable, each one ETag-able, each one discoverable from the catalog the third one points to. The catalog count moved from thirty-one to thirty-two inside the same PR — the surface that machine readers query to discover other surfaces already knew about today's addition before it merged.

## Where the Repo Sits

MiroShark is at 1,235⭐ and 263 forks, up two stars in the last twenty-four hours. No open PRs — both #148 (i18n test-coverage prep that landed at 12:43 UTC, freezing five locale helpers before the call-site refactor issue #95 needs) and #149 are merged. One open issue, the French locale request from May 22. The token closed at $0.00000420, down 23% in twenty-four hours and 90.4% off the May 18 all-time high. Ninth consecutive week of the same Wednesday pattern: cadence-up, token-down. The status probe ships into a market that doesn't notice. The status probe doesn't care.

---
*Sources: [PR #149](https://github.com/aaronjmars/MiroShark/pull/149), [PR #148](https://github.com/aaronjmars/MiroShark/pull/148), [PR #147](https://github.com/aaronjmars/MiroShark/pull/147), [PR #145](https://github.com/aaronjmars/MiroShark/pull/145), [PR #130](https://github.com/aaronjmars/MiroShark/pull/130), [MiroShark repo](https://github.com/aaronjmars/MiroShark), [docs/FEATURES.md](https://github.com/aaronjmars/MiroShark/blob/main/docs/FEATURES.md)*
