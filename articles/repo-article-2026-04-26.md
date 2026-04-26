# Three Protocols in Three Days: MiroShark Closes the Outbound Side

Two days ago MiroShark shipped a click-and-paste MCP onboarding panel for Claude Desktop, Cursor, Windsurf, and Continue. Yesterday it shipped a 1.9K-line OpenAPI 3.1 spec with Swagger UI at `/api/docs` and a regex-driven drift test that fails CI the moment a route and the spec disagree. Today, [PR #46](https://github.com/aaronjmars/MiroShark/pull/46) lands the third leg: an outbound completion webhook that fires the moment a simulation reaches `completed` or `failed`, with one URL field that wires up Slack, Discord, Zapier, Make, n8n, IFTTT, or any custom listener. Three machine-readable contracts over the same engine in three calendar days.

## Current state

[MiroShark](https://github.com/aaronjmars/MiroShark) sits at 829 stars and 153 forks today, thirty-seven days after the first commit. PR #45 (OpenAPI) is still open, PR #46 (Webhook) was filed at 11:25 UTC and is open at the time of writing. The repo description was tightened on April 21 to *"Simulate anything, for $1 & less than 10 min — Universal Swarm Intelligence Engine"* and that's still the elevator pitch. What's changing this week isn't what the engine does — it's how many ways the outside world can talk to it.

## What's been shipping

The week reads as a single arc once you line it up:

- **Mon Apr 21** — direct-push graph memory stack with bi-temporal edges, Leiden clustering, ReACT reasoning trace, and an MCP server with eight retrieval tools. UI: untouched.
- **Tue Apr 22** — [PR #42](https://github.com/aaronjmars/MiroShark/pull/42) ships the Pillow-rendered share card.
- **Wed Apr 23** — [PR #43](https://github.com/aaronjmars/MiroShark/pull/43) ships `/explore`, the public simulation gallery.
- **Thu Apr 24** — [PR #44](https://github.com/aaronjmars/MiroShark/pull/44) gives the MCP server its onboarding panel and a tool-catalog drift test.
- **Fri Apr 25** — [PR #45](https://github.com/aaronjmars/MiroShark/pull/45) hands the same engine a formal REST contract: 1,966-line OpenAPI 3.1 across ~85 paths in 13 tags, plus a Flask blueprint serving Swagger UI from a CDN-pinned bundle, and a second drift-detection test.
- **Sat Apr 26** — PR #46 ships the outbound side: completion webhook, 1,413 additions across 10 files, zero new dependencies.

Six straight days of shipping, each PR depending on something merged within the same week.

## Technical depth

The interesting design decision in PR #46 isn't *that* a webhook fires — every SaaS app has one. The choices worth naming are how it stays consistent with the rest of the surface and how it stays out of the runner's way.

The new `backend/app/services/webhook_service.py` is 457 lines of stdlib-only Python — `urllib.request`, no `requests`, no `httpx`, no new dependencies. `build_payload()` reads `simulation_config.json`, `quality.json`, `trajectory.json`, `resolution.json`, and `state.json` directly from the simulation directory and applies the **same ±0.2 stance threshold** as the gallery card and the share card helpers. That single shared constant means the webhook reports the same bullish/neutral/bearish split the user sees in the embed, the gallery thumbnail, and the OG image — three surfaces, one rule.

`fire_webhook_for_simulation()` runs on a daemon thread, so the runner returns instantly. It's deduped per `(sim_id, status)` so the runner's exit-code path *and* the platform-specific `simulation_end` event path can both call it without double-firing — and a `completed → failed` transition still gets two webhooks because the status differs. Every dispatch is wrapped in `try`/`except` that logs and swallows, so a misconfigured listener never takes down the simulation runner.

`validate_url()` accepts `http(s)://` only, rejecting `javascript:`, `file:`, `ftp:`, scheme-less, and overlong inputs. `mask_url()` reduces a saved Slack or Discord webhook to `scheme://host/***` so the secret token portion never round-trips through `GET /api/settings`. The new `POST /api/settings/test-webhook` returns `{success, message, latency_ms, url_masked}` as HTTP 200 regardless of outcome, so the Settings panel renders pass and fail uniformly.

There are 18 offline unit tests in `backend/tests/test_unit_webhook.py` covering payload shape (full, minimal, corrupt, long-scenario, failure), URL validation and masking, async dispatch, completed-plus-failed dedup, exception swallowing, and `send_test_webhook` end-to-end. Mocks `_post_json` so no real HTTP ever fires in CI.

## Why it matters

MCP is the inbound contract for AI editors. OpenAPI is the inbound contract for HTTP clients and SDK generators. The completion webhook is the *outbound* contract — the engine's voice into the operator's environment. Researchers running 50-agent, 20-round simulations close the tab and come back later. Until today, the only signal that a run finished was an in-app browser push that reaches one device. Pointed at a Slack Incoming Webhook, the same URL field reaches the whole team. Pointed at Zapier, Make, or n8n, it fans out to email, Notion, Airtable, Sheets, custom dashboards, or any of 5,000+ connected services.

External signal kept building. [Bankr Terminal v2's](https://x.com/bankrbot/status/2048026489707442360) roundup today cited [@miroshark_](https://x.com/miroshark_) for simulating Aave vulnerabilities prior to the rsETH incident — 156 likes, 40 retweets. `$MIROSHARK` closed +35% on the day, the closest it's come to its April 14 ATH since the ATH. The 1,000-stars-by-April-30 sprint has 4 days left and ~171 stars to go.

The three-protocol week leaves MiroShark with three documented ways for the outside world to call into it and one way to call back out. After today, the question isn't "is this a simulation app or a simulation engine you can build on" — it's documented thrice, in three formats, with three failing tests if anyone forgets to update them.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark) · [PR #46 Completion Webhook](https://github.com/aaronjmars/MiroShark/pull/46) · [PR #45 OpenAPI 3.1 + Swagger UI](https://github.com/aaronjmars/MiroShark/pull/45) · [PR #44 MCP Onboarding](https://github.com/aaronjmars/MiroShark/pull/44) · [docs/WEBHOOKS.md](https://github.com/aaronjmars/MiroShark/blob/feat/completion-webhook/docs/WEBHOOKS.md) · [Bankr Terminal v2 mention](https://x.com/bankrbot/status/2048026489707442360)*
