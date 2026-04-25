# Two Protocols in Two Days: MiroShark Files Its Second Formal Spec

Yesterday MiroShark turned its hidden MCP server into a click-and-paste Settings panel for four AI editors. Today, [PR #45](https://github.com/aaronjmars/MiroShark/pull/45) does the same trick for the REST surface — handwritten OpenAPI 3.1 spec, Swagger UI at `/api/docs`, JSON variant for SDK generators, and a regex-driven drift test that fails CI the moment the spec and the routes disagree. Two days, two machine-readable contracts over the same engine, each backed by a unit test that holds the implementation to the spec.

## Current state

[MiroShark](https://github.com/aaronjmars/MiroShark) sits at 829 stars and 152 forks today, thirty-six days after the first commit. PR #44 (MCP Onboarding) merged yesterday at 13:20 UTC. PR #45 (OpenAPI + Swagger) was filed at 11:17 UTC today and is still open at the time of writing — same cadence, same author rhythm of "feature shipped one day, related self-improve the next."

The product is unchanged in shape: drop a document or a headline in, hundreds of grounded agents react hour-by-hour across a synthetic Twitter, Reddit, and prediction market, beliefs drift, a quality-scored report falls out the back. What's changing is who can reach in. Yesterday it became any MCP-aware AI editor. Today it becomes any HTTP client with a JSON parser.

## What's been shipping

This week's pattern keeps holding — every PR surfaces a substrate that was already there:

- **Mon Apr 21** — direct-push graph memory stack lands the bi-temporal graph, Leiden clustering, ReACT reasoning trace, and an MCP server with eight retrieval tools. UI: untouched.
- **Mon Apr 21** — [PR #41](https://github.com/aaronjmars/MiroShark/pull/41) siphons fourteen features from four sibling repos behind env flags, plus the first CI test suite (62 unit tests).
- **Wed Apr 22** — [PR #42](https://github.com/aaronjmars/MiroShark/pull/42) ships the Pillow-rendered share card. README slims 698 → 243 lines.
- **Thu Apr 23** — [PR #43](https://github.com/aaronjmars/MiroShark/pull/43) ships `/explore`, reusing the share card PNG as gallery thumbnail.
- **Fri Apr 24** — [PR #44](https://github.com/aaronjmars/MiroShark/pull/44) gives the MCP server its onboarding panel and a tool-catalog drift test.
- **Sat Apr 25** — [PR #45](https://github.com/aaronjmars/MiroShark/pull/45) hands the same engine a formal REST contract: 1.9K lines of OpenAPI 3.1 across ~85 paths in 13 tags, a Flask blueprint serving Swagger UI from a CDN-pinned bundle, and the second drift-detection test of the week.

Six straight days of shipping, each PR depending on something merged within the same week.

## Technical depth

The interesting choice in PR #45 isn't the spec itself — most projects can scrape `flasgger` or `apispec` and produce a YAML blob. The choice worth naming is **handwritten spec plus a static drift test**. The 1,966-line `backend/openapi.yaml` is authored by hand, with named schemas (`SuccessEnvelope`, `RunStatus`, `BeliefDrift`, `EmbedSummary`, `GalleryCard`, `McpStatus`, `SettingsUpdate`, `PushSubscription`, …) and reusable parameters. Then `backend/tests/test_unit_openapi.py` walks every `backend/app/api/*.py`, regex-scrapes each `@<bp>_bp.route(...)` decorator, converts Flask `<id>` patterns to OpenAPI `{id}`, fully-qualifies them with the blueprint `url_prefix`, and asserts the resulting set equals the spec's path set — minus an explicit allowlist of internal routes (config / env / report-tools). Add a route, forget the spec, CI breaks.

That's the same shape as PR #44's tool-catalog drift test, which regex-scrapes `mcp_server.py` for `@mcp.tool()` and asserts the API's `_TOOLS` array matches. Two surfaces, two specs, two drift tests in two days. Each spec is a hand-curated source of truth, and each test refuses to let the implementation diverge silently.

The Swagger UI bundle is pinned to `swagger-ui-dist@5.17.14` on jsDelivr — immutable URL, CDN-cached, no npm dependency. The JSON variant routes through `yaml.safe_load` with pyyaml as a soft-optional import. The whole blueprint is 268 lines.

## Why it matters

The week's external signal is the substrate audience showing up. Paradigm CTO [@gakonst](https://x.com/gakonst) starred the repo. OriginTrail's founder co-signed it for DKG V10. The `$MIROSHARK` token is +503% over thirty days as of this morning, with @TheGodfath13541 citing the Paradigm and OriginTrail validation as the catalyst. None of that audience cares about a Vue dashboard. They care about whether there's a graph and an API under it.

Two days ago that audience could only reach MiroShark through the browser. Yesterday they could plug it into Claude Desktop or Cursor over MCP. Today they can hit `/api/docs`, see ~85 endpoints in a try-it-out console, and pipe the same spec through `openapi-generator` to produce Python, TypeScript, Go, or Java SDKs in one command. The spec also qualifies MiroShark for APIs.guru and RapidAPI listings — discovery surfaces that the MCP-aware audience routinely searches.

The 1,000-stars-by-April-30 sprint has 5 days left and ~171 stars to go (~34/day; yesterday delivered 26). The two-protocol week is the kind of move that compounds the sprint without depending on it. MCP and OpenAPI together close a positioning question the demo couldn't answer alone: is this a simulation app, or a simulation engine you can build on? After this week, the answer is documented twice, in two formats, with two failing tests if anyone forgets to update them.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark) · [PR #45 OpenAPI 3.1 + Swagger UI](https://github.com/aaronjmars/MiroShark/pull/45) · [PR #44 MCP Onboarding](https://github.com/aaronjmars/MiroShark/pull/44) · [PR #43 /explore](https://github.com/aaronjmars/MiroShark/pull/43) · [PR #42 Social Share Card](https://github.com/aaronjmars/MiroShark/pull/42) · [PR #41 Sibling-Repo Siphon](https://github.com/aaronjmars/MiroShark/pull/41) · [docs/API.md](https://github.com/aaronjmars/MiroShark/blob/main/docs/API.md)*
