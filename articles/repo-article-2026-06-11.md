# MiroShark is being rebuilt as a machine to read from, not a site to look at

Five of the eight pull requests MiroShark merged in the past week ship nothing a human clicks. They add JSON endpoints — a status probe, a multi-sim status lookup, a platform-wide outcome distribution, a signed result payload, and an activity feed. Each one lands a new OpenAPI block and its own unit-test file. The web app is no longer the product's edge; the contract is.

## The claim
> MiroShark is hardening into a machine-consumable signal API, not a web app: 5 of 8 merged PRs this week (#149–#153) added documented, tested JSON endpoints.

## Evidence
The five API PRs share an identical shape, and that shape is the story. [#149](https://github.com/aaronjmars/MiroShark/pull/149) (`63cd4fe`→`891b9e6`) adds `/api/status.json` via a new `backend/app/services/platform_status.py` (+271) and a 428-line test. [#151](https://github.com/aaronjmars/MiroShark/pull/151) adds `/api/stats/distribution.json` backed by `outcome_distribution.py` (+533) and an 810-line test. [#150](https://github.com/aaronjmars/MiroShark/pull/150) adds `POST /api/simulation/batch-status` (`batch_status.py`, +394). [#153](https://github.com/aaronjmars/MiroShark/pull/153) adds `/api/activity.json`, a "what just completed" polling feed (`activity_feed.py`, +439, with a 694-line test). Every one of these PRs also edits `backend/openapi.yaml` — +176, +398, +205, and +248 lines respectively — so the spec moves in lockstep with the code.

Two details under the surface confirm this is a plan, not a coincidence. First, all five PRs also edit `backend/app/services/surfaces_catalog.py` (+9 to +10 lines each) — every new endpoint registers itself into a catalog of "surfaces," so the API is becoming self-describing and discoverable rather than a loose pile of routes. Second, the spec churn is large: those five PRs add roughly 1,195 lines to `backend/openapi.yaml` in a single week. A spec that grows that fast is a spec someone expects to be read by a code generator.

The clearest tell is [#152](https://github.com/aaronjmars/MiroShark/pull/152) (`7b79e7b`): `signed-result.json`, an HMAC-SHA256, offline-verifiable signal payload (`signed_result.py`, +215). You do not sign a response for a browser tab to render. You sign it so a third party can consume a MiroShark prediction, verify it wasn't tampered with, and trust it without calling back. That is an infrastructure feature, not a UI one.

The documentation has caught up to the intent. `docs/API.md` now tells integrators to "point [`openapi-generator`](https://openapi-generator.tech/) at the spec to produce a Python / TypeScript / Go SDK in one command," and the running backend serves an OpenAPI 3.1 spec at `/api/openapi.yaml` alongside Swagger UI at `/api/docs`. The endpoint table runs to dozens of routes — belief drift, influence leaderboards, interaction networks — all read paths designed to be polled.

## Counter-evidence / what would change my mind
The week was not API-only, and pretending otherwise would be dishonest. Two of the eight merged PRs were README translations — [#155](https://github.com/aaronjmars/MiroShark/pull/155) (`README.zh-CN.md`) and [#156](https://github.com/aaronjmars/MiroShark/pull/156) (`README.ja.md`) — and [#148](https://github.com/aaronjmars/MiroShark/pull/148) added i18n test coverage ahead of a localization refactor. That is a parallel push aimed squarely at human readers in new locales, which cuts against a pure machine-first reading. Every API PR also touched `frontend/src/api/simulation.js`, so the web client is still a first-class consumer, not an afterthought. The thesis would be wrong if next week's merges skew back toward UI and copy, or if the new endpoints stop arriving with spec and test coverage.

## Why it matters
MiroShark already has named external integrators citing it as AI infrastructure — RevaultDrops, AntFleet's miroshark-bench, and Capacitr among them. Those consumers do not want a screenshot; they want a stable, documented, verifiable contract. A signed payload and an SDK-generatable OpenAPI spec are exactly what turns "a cool simulation site" into "a dependency you build on." With 1,255 stars and 265 forks, the audience that compounds is the one writing code against the API, not the one watching agents argue in a browser. This week's commits read like a project deciding which of those audiences it is for.

---
*Sources*
- [MiroShark PR #152 — signed-result.json (HMAC-SHA256)](https://github.com/aaronjmars/MiroShark/pull/152)
- [MiroShark PR #153 — /api/activity.json polling feed](https://github.com/aaronjmars/MiroShark/pull/153)
- [MiroShark PR #151 — /api/stats/distribution.json](https://github.com/aaronjmars/MiroShark/pull/151)
- [MiroShark PR #149 — /api/status.json platform probe](https://github.com/aaronjmars/MiroShark/pull/149)
- [docs/API.md — OpenAPI spec + SDK generation](https://github.com/aaronjmars/MiroShark/blob/main/docs/API.md)
- [MiroShark — Openflows profile (external)](https://openflows.org/currency/currents/miroshark/)
