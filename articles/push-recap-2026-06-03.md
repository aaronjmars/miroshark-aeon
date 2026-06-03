# Push Recap — 2026-06-03

## Overview
Seven substantive commits across two repos. The dominant thrust today was finishing the **ecosystem-as-a-contract** arc that opened on Jun 2: the `ECOSYSTEM.md` registry got a logo column (and lost two dormant rows), got linked from the README in English and Chinese, gained a 13th integrator (Sparkleware), and — most consequentially — gained a machine-readable JSON twin at `GET /api/ecosystem.json` (PR #145, Aeon-built, +953/-19 across 10 files). One quieter but structurally important change landed in this repo: PR #50 added a `blocked-features` registry so the `repo-actions` skill stops re-suggesting Operator Profile for a 14th time.

**Stats:** ~12 distinct files changed, +1,003 / -36 lines across 7 substantive commits (6 on MiroShark, 1 on miroshark-aeon). Cron-churn auto-commits on this repo excluded as noise.

---

## aaronjmars/MiroShark

### Theme 1 — The ECOSYSTEM table became a contract
**Summary:** Yesterday's recap framed Capacitr's published integration spec (`spec.capacitr.xyz/#miroshark`) as the inflection point — the first time an external project pointed at a specific MiroShark endpoint by name in its own vendor-shaped docs. Today's commits ratified that shift by giving the *other* side — MiroShark's own ecosystem registry — the same shape: a visual catalog (logos), a navigation seam (README link), a programmatic interface (`/api/ecosystem.json`), and an external write (Sparkleware) all on the same day.

**Commits:**

- `f7e539a` — **feat: ecosystem.json — machine-readable counterpart of ECOSYSTEM.md (#145)** — merged 2026-06-03T14:03:39Z by @aaronjmars (Aeon-built)
  - New `backend/app/services/ecosystem_catalog.py` (+263 lines, pure stdlib): a literal list of 13 integrator dicts at module scope, each carrying `name`, `url`, `description` (≤160 chars), `category` (one of `product`/`tool`/`integration`/`agent`/`benchmark`), `x_handle` (no `@`, nullable), and `repo` (GitHub URL or `null`). The module's docstring is unusually explicit about *why* it's hardcoded rather than parsed from `ECOSYSTEM.md`: "the Markdown shape is fragile (cells contain links, images, and free text) and a silent parser drift would degrade the public contract."
  - Changed `backend/app/api/surfaces.py` (+88, -19): added a `GET /api/ecosystem.json` route on the existing `surfaces_bp` blueprint — same posture as `/api/surfaces.json`, same `Cache-Control: public, max-age=3600`, same ETag-short-circuits-to-304 envelope, same `{schema_version, count, ecosystem}` response shape. The blueprint's module docstring was rewritten from "one endpoint" to "two endpoints" to reflect that the surfaces and ecosystem catalogs now both ship from the same place.
  - New `backend/tests/test_unit_ecosystem_catalog.py` (+306, 15 offline tests): drift guard cross-checks the catalog's `name` set against `ECOSYSTEM.md` line-by-line so neither side can drift silently; schema invariants on every entry; alphabetical-order check; OpenAPI presence guard; wiring guard that the blueprint actually exposes the route.
  - Changed `backend/app/services/surfaces_catalog.py` (+9): appended an `ecosystem_catalog` entry so the new endpoint shows up in `GET /api/surfaces.json` itself — the catalog catalogues itself.
  - Changed `backend/openapi.yaml` (+185): full `/api/ecosystem.json` path entry plus new `EcosystemEntry` and `EcosystemRegistry` schemas.
  - Changed `frontend/src/api/simulation.js` (+34): added `getEcosystemUrl()` and `getEcosystem()` helpers — mirror shape of the existing `getSurfacesCatalogUrl()` / `getSurfacesCatalog()` helpers from PR #130.
  - Changed `ECOSYSTEM.md` (+2): one-line note near the top pointing machine readers at `/api/ecosystem.json`.
  - Changed `docs/API.md` (+1), `docs/FEATURES.md` (+47), `docs/FEATURES.zh-CN.md` (+18): endpoint documented in all three places, with the same section structure used for the Surface Catalog API in PR #130.

- `42e03cc` — **docs: add logo column to ECOSYSTEM.md (#143)** — merged 2026-06-02T20:25:48Z by @aaronjmars
  - Changed `ECOSYSTEM.md` (+15, -17): two-commit PR. First commit added a `Logo` column to the integrator table with profile-image `<img>` tags (40px width) for AntFleet, Blue Agent, Capacitr, Crucible Sim, Echo Oracle, HivemindOS, Monitor, and Noelclaw — the rest of the rows had empty logo cells. Second commit filled in logos for RootAI, Signa, SyntheticsAI, Xerg, and ZER0 *and* dropped the Nookplot and Supercompact rows. Net effect: 14 visible rows → 13, every row now has a logo. The drop of Nookplot/Supercompact tightens the registry to projects with active operator-visible self-disclosure.

- `20300cf` — **docs: link ECOSYSTEM.md from README (#142)** — merged 2026-06-02T19:09:50Z by @aaronjmars
  - Changed `README.md` (+2): added an `[Ecosystem](ECOSYSTEM.md)` row to the Documentation table in both the English and Chinese (`中文`) sections. The PR description notes this matches how aeon's own README links to its ecosystem page — closing a discoverability gap where the registry existed on disk but was reachable only by navigation, not by reading.

- `a20583f` — **docs: add Capacitr to ecosystem (#140)** — merged 2026-06-02T16:16:57Z by Sayeed Mehrjerdian (external contributor, Capacitr founder)
  - Changed `ECOSYSTEM.md` (+1): added the Capacitr row. PR was open at yesterday's window-close, so it lands in today's recap. The PR description points at `spec.capacitr.xyz/#miroshark` — the published integration spec that yesterday's repo-article ("The Day MiroShark's Endpoints Showed Up in Someone Else's Spec") treated as the qualitative shift. The row itself includes three distinct links: `capacitr.xyz`, the integration spec URL, and the X handle.

- `16afc08` — **docs(ecosystem): add Sparkleware (#144)** — merged 2026-06-03T14:55:04Z by sparkleware (external contributor)
  - Changed `ECOSYSTEM.md` (+1): a new row for Sparkleware, with logo at `sparkleware.fun/logo.png`, X handle `@sparklewarefun`, and a link to a "miroshark kit" page at `sparkleware.fun/kits/miroshark/`. The PR landed 52 minutes after PR #145 merged — meaning the first external integrator PR after the JSON catalog shipped immediately created a drift between the two sources, which is exactly the failure mode the drift-guard test was written to catch.

- `4429c40` — **fix(ecosystem): add Sparkleware to machine-readable catalog (#146)** — merged 2026-06-03T15:00:52Z by @aaronjmars
  - Changed `backend/app/services/ecosystem_catalog.py` (+8): added the Sparkleware entry to the literal list (`name`, `url: https://sparkleware.fun`, description "Discovery registry that indexes MiroShark-on-Aeon skill packs and bundles them into an installable kit.", `category: integration`, `x_handle: sparklewarefun`, `repo: None`). The commit message names the cause: "Restores catalog/ECOSYSTEM.md sync broken by #144; drift-guard test passes." This is the drift-guard's first live save: PR #144 added the Markdown row, the drift test in `test_unit_ecosystem_catalog.py` would have failed CI, and PR #146 closed the gap five minutes after #144 merged. PR #145 documented the two-file write requirement; PR #146 enforced it.

**Impact:** Until today, the ecosystem registry was a curated Markdown file — useful for human readers, but invisible to anything that wanted to iterate. With `/api/ecosystem.json` shipped on the same blueprint as `/api/surfaces.json`, the platform now exposes the two meta-questions a new integrator hits on day one as twin JSON endpoints — "what surfaces can I call?" (`surfaces.json`, 27 entries) and "who else is building on this?" (`ecosystem.json`, 13 entries). The Sparkleware drift incident immediately validated the design choice: hand-edited Markdown will silently desync from a literal list, and the test catches it within one CI run. Per-entry the schema is intentionally narrow (six fields, five categories) so an ecosystem-tooling builder downstream can write to it without future schema churn. Zero new dependencies — 38th consecutive zero-dep PR on MiroShark.

---

## aaronjmars/miroshark-aeon

### Theme 2 — Aeon learned to forget the same idea on purpose
**Summary:** The `repo-actions` skill generates five action-item ideas per run and runs every other day. A 7-day exclusion window keeps each generated idea out of the eligible pool for a week, but ideas that are *architecturally blocked* — not redundant, just unbuildable — keep cycling back as soon as the window expires. Operator Profile suggested itself 13 times across May 8 → Jun 1. Yesterday's `feature` skill pivoted off it the 14th time after confirming via grep that `SimulationState` has no `operator` field. PR #50 makes that pivot durable: a memory file the skill reads before generating ideas.

**Commits:**

- `575ca43` — **improve(repo-actions): add blocked-features registry to stop re-suggesting Operator Profile (#50)** — merged 2026-06-03T14:03:40Z by @aaronjmars
  - New `memory/topics/blocked-features.md` (+21): a registry file documenting the schema (signature keywords / category / reason / verifying log / suggestion history / unblock condition) and a single bootstrapped entry for Operator Profile. The entry's signature keywords are five rough variants on the title (`operator profile`, `/api/operator`, `/profile/<operator`, `per-operator gallery`, `operator identity layer`) chosen so a renamed idea ("Operator Identity Layer", "Per-Operator Gallery") still matches. The "Verified" line points at the 2026-06-02 log entry that holds the pivot trail. The "Unblock when" line names the exact upstream change that lifts the block: `SimulationState` gaining an `operator` / `created_by` field at `backend/app/models/simulation_state.py`.
  - Changed `skills/repo-actions/SKILL.md` (+2): step 4 now reads the registry, does case-insensitive substring matches against each candidate idea's title and implementation path, excludes hits from the 5-idea batch with a one-line `Excluded (blocked): <title> — <reason>` note in the article's Selection Rationale section so the operator sees what was filtered, and runs a 30-second re-verification against the entry's "Unblock when" condition before excluding — if the upstream constraint has lifted, the registry entry is deleted in the same run and the idea returns to the eligible pool.

**Impact:** Frees one idea slot per `repo-actions` run for net-new suggestions (this run generates five ideas; one was being burned on the blocked one). Prevents `feature` from pivoting off Operator Profile on every other-day cycle. The auto-unblock design means the registry doesn't accumulate stale entries — if Aaron lands an `operator` field upstream, the next `repo-actions` run lifts the block and the idea returns to the pool the same day. The Operator Profile entry is intentionally bootstrapped as the first row so the file demonstrates its own schema by example.

---

## Developer Notes

- **New dependencies:** none. PR #145 (`ecosystem_catalog.py`) is pure stdlib — `typing` for type hints, no Markdown parser, no Neo4j touch, no outbound network. 38th consecutive zero-dep PR on MiroShark since the Nemotron addition.
- **Breaking changes:** none. Both new endpoints (`/api/ecosystem.json`, indirect via the new `ecosystem_catalog` entry in `/api/surfaces.json`) are additive. ECOSYSTEM.md's table shape changed (`| Project | Links |` → `| Logo | Project | Links |`), but no downstream parser had been documented against the old shape — PR #145 explicitly justified hardcoding the catalog rather than parsing Markdown for exactly this reason.
- **Architecture shifts:** the `surfaces_bp` blueprint is now the platform's catalog-of-catalogs surface — it serves both `surfaces.json` (capability surface) and `ecosystem.json` (integrator surface) under the same `_cache_header()` and ETag posture. The module docstring was rewritten today to reflect the shift. Two further catalog endpoints could ship on the same blueprint with the same shape (e.g. `models.json`, `regions.json`) without restructuring.
- **Tech debt:** one self-correcting incident — PR #144 (Sparkleware row) merged before PR #146 (catalog entry), creating a drift-test failure window that closed five minutes later. The drift guard worked as designed, but the contributor experience of "your Markdown PR merges, then a separate maintainer PR follows" is a manual two-step. Future work could either auto-open a paired catalog PR on Markdown-only changes or document the two-file rule in `ECOSYSTEM.md`'s "Add your project" section (the section exists but doesn't currently mention the catalog file). Six commits today touched ecosystem code; only one was a maintenance cleanup, so the drift cost remains low.

## What's Next

- The Capacitr PR #140 landed today as the row addition, but the deeper unfinished thread from yesterday is the integration itself: Capacitr's published spec POSTs to `/x402/run` and polls a status JSON. Their spec is now public; MiroShark's `/x402/run` is now formally listed in `/api/surfaces.json`. The integration is now describable from both sides — next visible step is observable traffic against `/x402/run` from a non-MiroShark origin.
- The `Sparkleware` row claims a "miroshark kit" page at `sparkleware.fun/kits/miroshark/`. Worth a follow-up web-fetch to confirm what shape of integration that is — kit-builder is a category MiroShark hasn't catalogued yet (closest neighbour is Signa's skills repo, but those are operator-facing not integrator-facing).
- On the aeon side, the next `repo-actions` run (Jun 5, every-other-day cadence) is the first real validation of PR #50. The Operator Profile keyword should be excluded; the Selection Rationale section should carry the one-line note; the 30-second re-verify should grep the upstream model file and find no `operator` field. If any of those don't happen, the registry primitive needs a fix.
- Open MiroShark PRs at window close: 0. Open miroshark-aeon PRs at window close: 0. Both repos cleared in the same 24h window — first time in the past week that both ledgers ended empty simultaneously.
- The catalog of catalogs idea — `surfaces.json` listing `ecosystem.json` as a discoverable surface — invites a third entry: a `policies.json` or `models.json` describing the platform-level capability axes that aren't per-sim endpoints (e.g. supported models, supported chains, rate-limit tiers). No commit today proposes it, but the blueprint posture now supports it cheaply.

## Sources
- MiroShark commits and diffs fetched via `gh api repos/aaronjmars/MiroShark/commits` (window 2026-06-02T15:55:28Z → 2026-06-03T15:55:25Z).
- miroshark-aeon commits and diffs fetched via `gh api repos/aaronjmars/miroshark-aeon/commits` (same window). Cron auto-commit churn (~12 chore commits) excluded as noise.
- PR descriptions and merge timestamps cross-checked against `repos/aaronjmars/MiroShark/events` (PushEvent slice).
