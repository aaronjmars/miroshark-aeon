# Push Recap — 2026-04-25

## Overview

A single-repo, single-feature day. MiroShark received one substantive
push — `a91aa6e` on `feat/openapi-swagger-docs`, opening PR #45 — that
adds a 1.9K-line handwritten OpenAPI 3.1 spec, a Flask docs blueprint
serving Swagger UI at `/api/docs`, and a CI-grade drift test that walks
every Flask blueprint and fails if the spec falls behind the
implementation. miroshark-aeon saw no substantive commits — only the
expected ~31 chore commits from the cron scheduler and per-skill
auto-commits of logs and articles.

**Stats:** 7 files changed, +2,577/−2 across 1 substantive commit (1
authoring branch, PR #45 open, not yet merged at the close of the
window).

---

## aaronjmars/MiroShark

### REST surface gets its own spec — OpenAPI 3.1 + Swagger UI (PR #45, open)

**Summary:** Until today, the answer to "what HTTP endpoints can I call
on a running MiroShark backend?" was a hand-maintained markdown table
in `docs/API.md` plus reading `app/api/*.py`. PR #45 promotes the
HTTP surface to a first-class artefact: a handwritten 1.9K-line
`backend/openapi.yaml`, an in-app Swagger UI rendered straight off the
spec, and a unit test that statically scans every Flask blueprint and
fails CI the moment the spec drifts away from the routes. This is the
natural follow-on to yesterday's PR #44 MCP onboarding panel — same
audience (developers wiring MiroShark into other tooling), different
protocol (REST instead of MCP-over-stdio).

**Commits:**
- `a91aa6e` — *feat: OpenAPI 3.1 spec + Swagger UI at /api/docs*
  - **New `backend/openapi.yaml` (+1,966 lines)** — handwritten spec
    covering ~85 paths grouped under 13 tags: Setup & Discovery, Graph
    Build, Simulation Lifecycle, Live State, Analytics, Interaction,
    Publish & Embed, Export, Report Agent, Observability, Settings &
    Push, Integrations, Documentation. Named schemas
    (`SuccessEnvelope`, `ErrorEnvelope`, `RunStatus`, `BeliefDrift`,
    `EmbedSummary`, `GalleryCard`, `McpStatus`, `SettingsUpdate`,
    `PushSubscription`, `SuggestionsEnvelope`, `TrendingEnvelope`,
    `TaskEnvelope`, `DirectorEvent`) plus a shared `SimulationIdPath`
    parameter and reusable `BadRequest`/`NotFound`/`Forbidden`/
    `RateLimited` responses. Two `servers:` entries: `localhost:5001`
    for the launcher default and a `{scheme}://{host}` template for
    custom deployments. Header documents the `{success: true, data: …}`
    envelope, the public-by-default deployment posture, and the
    sliding-window rate limit on Setup & Discovery endpoints.
  - **New `backend/app/api/docs.py` (+268 lines)** — Flask blueprint
    serving three views of the spec. `GET /api/docs` returns
    Swagger-UI HTML pinned to `swagger-ui-dist@5.17.14` from
    jsDelivr, with a MiroShark-branded top banner and the default
    Swagger top bar hidden. `GET /api/openapi.yaml` returns the raw
    YAML as `application/yaml; charset=utf-8` with
    `Content-Disposition: inline`. `GET /api/openapi.json` round-trips
    the same content via `yaml.safe_load`, with pyyaml soft-imported
    so a missing dependency degrades to a placeholder JSON instead of
    breaking the docs page. The module reads the YAML from disk on
    every call (cheap; allows operators to edit the spec in place
    without restarting), and falls back to a stub `paths: {}` doc if
    `openapi.yaml` is missing rather than 500ing.
  - **New `backend/tests/test_unit_openapi.py` (+321 lines)** — eight
    offline tests. The centerpiece is **drift detection**: a regex scan
    of every `app/api/*.py` for `@<bp>_bp.route(...)` decorators that
    converts Flask `<id>`-style placeholders to OpenAPI `{id}`-style,
    fully qualifies them with the blueprint's `url_prefix` from
    `app/__init__.py`, and asserts the spec's path set equals the
    registered Flask path set minus an explicit allowlist of internal
    routes (config / env / report-tools). Other tests verify the spec
    parses, has the OpenAPI 3.x minimum shape, declares every tag used
    by an operation, that the Swagger UI HTML references the spec URL
    and pins the CDN version in both the CSS and JS bundle URLs, and
    that the JSON variant round-trips the same path set as the YAML.
  - **`backend/app/api/__init__.py` (+2)** — re-export `docs_bp`.
  - **`backend/app/__init__.py` (+5/−1)** — register `docs_bp` at
    `/api` (no extra sub-prefix, so the spec URL is short:
    `/api/openapi.yaml`).
  - **`docs/API.md` (+14)** — opening callout pointing at the
    interactive docs and pitching `openapi-generator`; new
    "Interactive Documentation" section listing the three URLs and
    explaining the drift test.
  - **`README.md` (+1/−1)** — Documentation table row now references
    the live `/api/docs` Swagger UI alongside the markdown.

**Impact:** Three things become possible on the next merge:

1. **In-browser try-it-out.** Anyone running `./miroshark` can hit
   `/api/docs` and exercise every public endpoint without leaving the
   app — the same audience PR #44 onboarded into MCP-over-stdio gets
   a parallel surface for plain REST.
2. **SDK generation.** `/api/openapi.json` is exactly what tools like
   `openapi-generator` and `oapi-codegen` consume. Anyone can
   `openapi-generator generate -i http://localhost:5001/api/openapi.json
   -g typescript-fetch -o ./miroshark-sdk` and get a typed client in
   any of ~50 target languages.
3. **Public API directory listings.** A canonical OpenAPI spec is the
   submission requirement for APIs.guru, RapidAPI's directory, and
   Postman's Public API Network. PR #45 turns "submit MiroShark to
   APIs.guru" from an undefined item into a single 5-minute PR
   against `apis-guru/openapi-directory`.

The drift test is the load-bearing piece. Without it the spec rots in
weeks; with it, the YAML is contractually tied to the implementation —
every new route must either land in the spec or be added to an
explicit internal allowlist, both of which surface in code review.

---

## aaronjmars/miroshark-aeon

No substantive commits in the window (Apr 24 15:35 UTC → Apr 25 15:22
UTC). ~31 chore commits — scheduler cron-state updates, per-skill
auto-commits of `articles/` + `memory/logs/`, and `chore(cron): X
success` markers — that are bookkeeping for the day's skill runs
(`token-report`, `fetch-tweets`, `tweet-allocator`, `repo-pulse`,
`hyperstitions-ideas`, `feature` and the rest of the morning batch),
not feature work.

The substantive feature work today (`feature` skill output → PR #45 on
MiroShark) lives entirely in the watched repo, not in aeon itself.

---

## Developer Notes

- **New dependencies (effective):** none in MiroShark proper — Swagger
  UI is loaded from a pinned jsDelivr CDN URL (`swagger-ui-dist@5.17.14`)
  rather than vendored or installed. **pyyaml** moves from
  best-effort optional to "needed in the unit-test workflow"; the
  runtime backend still soft-imports it.
- **Breaking changes:** none. PR #45 is purely additive — a new
  blueprint mounted at `/api`, three new GET routes, no existing
  routes touched.
- **Architecture shifts:** the spec joins `mcp_server.py` as the
  second canonical, drift-tested public-surface artefact. Both have
  the same shape — handwritten source of truth + a regex-based unit
  test that statically scans the implementation for drift. Worth
  watching whether a third surface (e.g. Web Push payloads, embed
  iframe contract) follows the same pattern.
- **Tech debt:** none introduced. `_read_spec_bytes()` reads the YAML
  on every call, which is fine for the docs page but would want a
  cache-with-mtime if `/api/openapi.json` ever lands on a hot path.

## What's Next

- **PR #45 merge.** Filed 11:17 UTC, no reviewers requested at window
  close — likely lands tomorrow on the same cadence as #43 and #44.
- **APIs.guru / RapidAPI submissions.** The spec unblocks both;
  whether to file them is a downstream skill decision (probably
  `repo-actions`).
- **First SDK build.** Most natural next push: `openapi-generator`
  output as a separate `miroshark-sdk-py` or `miroshark-sdk-ts` repo,
  or as a `sdks/` subdirectory in MiroShark itself. None of that is
  in the window's commits.
- **MCP and REST surfaces converging.** With PR #44 (MCP onboarding)
  and PR #45 (OpenAPI), MiroShark now exposes the same simulation
  engine through two formally documented protocols. The follow-on
  question — visible in the spec's tag layout but not in any commit
  yet — is whether the MCP tool catalog and the REST endpoint set
  should be checked for parity (e.g. is there a REST equivalent of
  every MCP tool, or a deliberate split?).

The 1K-stars-by-Apr-30 sprint context is unchanged: 823 stars / 152
forks at the start of the window per today's `repo-pulse`, needing
~35 stars/day with 5 days left. PR #45 is a developer-relations
push more than a star-driver — its lever pulls on third-party API
listings (APIs.guru gets crawled by AI tools, RapidAPI has its own
discovery) and on every "is this thing scriptable?" reader of the
README rather than on direct in-feed virality.
