*Feature Built — 2026-06-03*

Ecosystem JSON Registry
MiroShark's `ECOSYSTEM.md` — the curated list of every project, agent, and product publicly identified as built on the platform — now has a machine-readable counterpart at `GET /api/ecosystem.json`. Anyone building tooling over MiroShark's growing integrator base (a benchmark dashboard, an integrator-of-integrators directory, an automated cross-reference with `/api/surfaces.json`) gets a typed JSON envelope instead of having to scrape a Markdown table.

Why this matters:
Yesterday afternoon (2026-06-02) four separate teams — HivemindOS, Echo Oracle, Capacitr, SyntheticsAI — opened ECOSYSTEM.md PRs inside the same 6-minute window. The ecosystem now has 13 named integrators with no machine-readable discovery path; integrators building on integrators (AntFleet's miroshark-bench security suite, Signa's Aeon skill pack, Capacitr's published integration spec) currently have to parse Markdown to know what else is built on the platform. This was repo-actions Jun-02 batch idea #1 and re-eligible May-26 #5 — deferred until the ecosystem had enough mass to justify the surface; four PRs in one day was that mass.

What was built:
- backend/app/services/ecosystem_catalog.py (~230 LoC stdlib): static literal list of 13 integrators mirroring ECOSYSTEM.md, with `get_ecosystem_catalog` / `catalog_count` / `catalog_etag` / `build_response_payload` helpers. Five-category taxonomy: `product` (Capacitr/Echo Oracle/HivemindOS/RootAI/Xerg/ZER0), `tool` (Crucible Sim), `integration` (Monitor/Noelclaw/Signa), `agent` (Blue Agent/SyntheticsAI), `benchmark` (AntFleet).
- backend/app/api/surfaces.py: new GET /ecosystem.json route on the existing surfaces_bp blueprint — identical posture to /surfaces.json (same ETag/304 short-circuit, same 1-hour cache header, same `{success, data: {schema_version, count, ecosystem}}` envelope).
- backend/tests/test_unit_ecosystem_catalog.py: 15 pure-offline tests covering schema invariants, category whitelist, alphabetised-order guard, ETag determinism, JSON-serialisability, a drift guard cross-checking the catalog's project name set against ECOSYSTEM.md, a wiring guard for the route decorator, and an OpenAPI presence check.
- backend/openapi.yaml + frontend/src/api/simulation.js + ECOSYSTEM.md + docs/API.md + docs/FEATURES.md + docs/FEATURES.zh-CN.md: full surround — typed schemas, JS helpers (`getEcosystemUrl`/`getEcosystem`), one-line machine-readable note on ECOSYSTEM.md, English + 中文 feature sections matching the Surface Catalog API pattern.

How it works:
Per-entry fields are locked: `name` (project's own canonical capitalisation, matches the ECOSYSTEM.md row), `url` (primary public link — repo when one exists, X otherwise), `description` (≤160 chars), `category` (one of the five), `x_handle` (without leading `@`, nullable so the consumer can compose `https://x.com/<x_handle>` URLs without trimming), `repo` (`https://github.com/…` or null for closed-source integrators). Static and hardcoded by design — explicitly NOT auto-derived from a Markdown parse of ECOSYSTEM.md, because the Markdown shape (cells with images, links, free text) is fragile and silent parser drift would degrade the public contract. Adding an integrator ships in two files (ECOSYSTEM.md row + catalog entry); the drift test cross-checks both sources so neither side can drift silently. The new endpoint also gets an entry in the surfaces catalog itself (PR #130's `/api/surfaces.json`), so a consumer iterating surfaces.json discovers ecosystem.json without reading docs.

What's next:
The natural follow-ups from the same Jun-02 batch are the Scenario Clone Button (UI entry point for last week's clone.json backend) and the Simulation Batch Create API (1 round-trip for N sims — relevant for AntFleet's benchmark suite and SyntheticsAI's pipelines now that the ecosystem has settled into roughly Bags-style monitor + benchmark + product shapes). 38th consecutive zero-dependency PR.

PR: https://github.com/aaronjmars/MiroShark/pull/145
