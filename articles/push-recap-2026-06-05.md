# Push Recap — 2026-06-05

## Overview
Two MiroShark merges this morning, both inside a 17-minute window (12:43Z and 13:01Z), one Aeon-built and one from a different Aeon instance — neither shipped a user-facing feature, both did infrastructure prep. PR #149 closed the platform-surface family (`/api/stats` + `/api/surfaces.json` + new `/api/status.json`), pushing the catalog 31 → 32 and rewriting its own auth posture mid-PR after a docs-vs-code mismatch surfaced. PR #148 froze the locale-helper contract in 343 lines of tests so the `dict[str, str]`-form `_t()` refactor that French-locale issue #95 needs as a prerequisite can land without churning 195 call sites. miroshark-aeon was effectively quiet on default branch — yesterday's PR #52 (pre-existing-features registry) merged at 15:42Z Jun-4 inside the rolling 24h window but was covered in yesterday's recap; everything else was scheduler/cron auto-commit churn.

**Stats:** ~13 files changed, +1,463 / -1 lines across 2 substantive commits (1 PR-squash counting as 3 review-commits internally). Both MiroShark PRs zero new dependencies — 40-PR streak holds.

---

## aaronjmars/MiroShark

### Theme 1: Platform-surface family completes — the third leg
**Summary:** The platform-surface family on MiroShark has had two legs for weeks — `/api/stats` ("what does the corpus look like") and `/api/surfaces.json` ("what can this deployment do"). PR #149 adds the third one: `GET /api/status.json` ("is this MiroShark instance currently working"). Designed for external status monitors (Upptime, BetterUptime, Statuspage.io) and Aeon's own heartbeat skill — the first MiroShark API endpoint that's deliberately public-without-auth.

**Commits:**
- `891b9e6` — feat(api): platform status probe at /api/status.json (PR #149, merged 2026-06-05T13:01:00Z by Aaron)
  - New `backend/app/services/platform_status.py` (+271 lines, pure stdlib `os` + `json` + `time` + `datetime`) — scanner + envelope builder, `RECENT_WINDOW_SECONDS = 86400` constant, ISO UTC formatting with trailing `Z`, tolerant of corrupt `state.json` + dotfile directories
  - New `backend/app/api/status.py` (+109 lines) — `status_bp` blueprint, `GET /status.json` route handler, defensive `surface_count` read so a catalog regression can't tank the probe
  - Modified `backend/app/__init__.py` (+15/-1) and `backend/app/api/__init__.py` (+7) — blueprint wiring at `/api`. The `-1` removed line is the original deletion that flipped the status surface from gated to deliberately-public (third review-commit landed mid-PR — see below)
  - Modified `backend/app/services/surfaces_catalog.py` (+9) — `platform_status` catalog entry; catalog 31 → 32
  - Modified `backend/openapi.yaml` (+176) — `/api/status.json` path + `PlatformStatus` schema in components
  - New `backend/tests/test_unit_platform_status.py` (+428 lines) — 28 offline tests covering empty/missing/unreadable sim_root, queue_depth incrementing, mixed-case status matching (defensive against historical writes), 24h window using `updated_at` not `created_at` (so a sim created weeks ago but completed today still counts), `last_completed_at` maxing across all completed sims, `total_sims` cumulative count (public + private + in-flight + failed), surface_count injection (including negative clamp), ISO `check_at` reflection, envelope JSON round-trip, corrupt-state tolerance, blueprint-wiring drift guard, catalog-entry discoverability, OpenAPI spec coverage
  - Modified `backend/tests/test_unit_internal_auth.py` (+22) — locks in the `/api/status.json` exemption from `internal_auth_guard`
  - Modified `backend/tests/test_unit_openapi.py` (+4) — `status_bp → /api` added to the blueprint-prefix map so the static route scan stops treating the documented path as a phantom (second review-commit landed mid-PR — see below)
  - Modified `docs/API.md` (+1) and `docs/FEATURES.md` (+43) — Platform section table row + full feature deep-dive
  - Modified `frontend/src/api/simulation.js` (+35) — `getPlatformStatusUrl(origin)` + `getPlatformStatus()` helpers, parallel shape to `getPlatformStats` / `getSurfacesCatalog`

  **What's interesting:** the merged PR squashes three distinct review-commits — the iteration history is in the merge message itself:
  1. **Initial implementation** — scanner, blueprint, openapi entry, 28 tests
  2. **Drift-test fix** — `test_documented_paths_exist_in_flask` failed on CI because `status_bp` was wired but absent from `_BLUEPRINT_PREFIXES` in `test_unit_openapi.py`, making the documented path look like a phantom. Two-line fix mirroring `surfaces_bp → /api`. Co-authored by Claude Opus 4.8 1M-context.
  3. **Make it genuinely public** — original PR shipped under `internal_auth_guard` (inherited from `/api/*` siblings) but openapi.yaml documented it as unauthenticated. The probe is built for external, keyless callers, so returning 401/503 to those callers contradicted the contract. This commit (a) exempts `/api/status.json` from the auth guard alongside `/openapi.json` and `/health`, (b) filters `total_sims` to `is_public AND status == "completed"` so an anonymous caller can't infer the volume of private / in-flight / failed sims, (c) updates the openapi descriptions to match, (d) adds `test_status_probe_without_internal_key` locking in the exemption. Co-authored by Claude Opus 4.8 1M-context.

  Pattern worth noting: the platform-status surface is the first `/api/*` endpoint on MiroShark that's deliberately public-without-auth (sibling `/api/stats` and `/api/surfaces.json` stay gated). The third commit had to actively *remove* a default protection to deliver the documented contract.

**Impact:** Status-page consumers (Upptime, BetterUptime, Statuspage.io) and Aeon's heartbeat now have a single endpoint to poll for liveness. The `ok: true` literal is a deliberate stable anchor for body-matchers on status-page services (a regression should bubble up via envelope drift or 500, not silently flip the boolean). The `surface_count` field sourced from `surfaces_catalog.catalog_count()` means a downstream alert keyed on capability regression doesn't need to poll the catalog separately. Empty deployments return the all-zero envelope still `ok: true` 200 — fresh installs never 404 their own probe. Closes repo-actions Jun-04 idea #2.

### Theme 2: Locale-helper contract lockdown — prep for the French-locale PR
**Summary:** Issue #95 (French locale, opened by a community member, still open) needs a `dict[str, str]`-form `_t()` refactor as a prerequisite — the current `_t(en, zh)` two-argument shape doesn't extend to arbitrary locales without refactoring all 195 call sites across 6 backend files. PR #148 (from a different Aeon instance — `aeon-aaron`, distinct from this miroshark-aeon repo) lands the test contract on the helper module *before* the refactor, so whoever ships the dict refactor only has to preserve the same return values for the same inputs.

**Commits:**
- `63cd4fe` — test(i18n): unit-cover locale helpers before the dict-form _t() refactor (PR #148, merged 2026-06-05T12:43:25Z by Aaron)
  - New `backend/tests/test_unit_i18n.py` (+343 lines, only file in the PR) — 26 tests across 6 public surfaces of `backend/app/utils/i18n.py`:
    - `normalize_locale` — `None` / empty / `Accept-Language` lists / BCP-47 prefix matching (`zh-TW` → `zh-CN`, `en-GB` → `en`) / unknown-tag fallback / loop guarantee that every output lands in `SUPPORTED` so downstream indexing stays safe
    - `get_locale` — full `?lang=` > `X-MiroShark-Locale` > `Accept-Language` precedence chain, including a `_RaisingDict` stub that forces per-source `try/except` fall-through for malformed `request.args` / `request.headers`
    - `t` — EN default, ZH-CN selection, empty-`zh` fallback under `zh-CN`, unknown-locale fallback (the exact contract the `fr` PR needs)
    - `apply_i18n` — sibling-key overrides, default-locale `i18n` stripping, unknown-locale passthrough, nested-dict + nested-list recursion, scalar passthrough, malformed `i18n` block tolerated
    - `_strip_i18n` — top-level + deep recursive stripping
    - `use_locale` — activates inside block, restores on exit, normalises raw input via `normalize_locale`, nests correctly, resets on exception
  - Zero production-code changes — the module already exists with ~175 LoC of locale negotiation + string selection + recursive `i18n` block merging, but had no direct unit coverage (only `use_locale` was exercised indirectly via `test_unit_prompt_registry.py`)

**Impact:** The dict-form `_t()` refactor — whoever ships it — now has a frozen behavioural contract to keep matching. That refactor touches 195 call sites across `backend/app/api/{simulation,share,watch,report,templates,graph}.py`, exactly the kind of large mechanical change where pre-existing test coverage on the helper itself is the cheapest insurance. The `t()` "unknown-locale fallback" test in particular is the exact path `fr` will exercise on day one before the locale table is populated. Note: this PR is from `aeon-aaron` (Aaron's personal Aeon instance), not this miroshark-aeon repo — same architecture, different operator. It's the second time a non-miroshark-aeon Aeon instance has shipped a MiroShark PR this week.

---

## aaronjmars/miroshark-aeon

Quiet on substantive changes inside the 24h window — `ab8b6ef` (PR #52, pre-existing-features registry sibling to blocked-features) merged at 2026-06-04T15:42:01Z, technically inside the rolling 24-hour window-start of 15:28:12Z but already covered in yesterday's push-recap (logged at 2026-06-04T15:51:06Z). No re-coverage today.

Everything else on `main` since yesterday's recap close (24 commits) was `aeonframework` cron auto-commit churn from the scheduled skill runs: 1× scheduler state update (×4), token-report success (×1), repo-pulse success (×1), star-momentum-alert success (×1), feature success (×1), and yesterday-end markers for heartbeat / thread-formatter / project-lens / repo-article / push-recap / star-milestone. All excluded as noise per the May-31 convention.

---

## Developer Notes
- **New dependencies:** none. PR #149 = 40th consecutive MiroShark PR holding the stdlib-only streak; PR #148 = test-only, no runtime change.
- **Breaking changes:** none. `/api/status.json` is net-new; the i18n test file freezes existing helper behaviour.
- **Architecture shifts:** the platform-surface family is now a settled triplet (`/api/stats` corpus shape + `/api/surfaces.json` capability catalog + `/api/status.json` health probe). One of them (`/api/status.json`) is now publicly callable without `internal_auth_guard` — first such endpoint in `/api/*`. The auth-exemption list now reads: `/openapi.json`, `/health`, `/api/status.json`.
- **Catalog count delta:** MiroShark surfaces catalog 31 → 32 (added `platform_status` under platform-level surfaces).
- **Tech debt:** PR #149's mid-PR rewrite of its own auth posture (the third review-commit) suggests Aeon's `feature` skill default-inherits `internal_auth_guard` from sibling endpoints without checking whether the openapi documentation marks the endpoint as public — worth a self-improve scan if this pattern recurs.

## What's Next
- French-locale PR (issue #95) is the obvious follow-on to PR #148 — the test contract is now frozen, the `dict[str, str]` `_t()` refactor is the prerequisite, and the `fr` locale strings land on top. Aaron's PR #148 body explicitly named the chain.
- Remaining Jun-04 batch ideas still unbuilt: #3 Multi-Sim Status Lookup (`POST /api/simulation/batch-status`, sibling of the new `/api/status.json`), #4 All-Time Simulation Leaderboard (`GET /api/leaderboard.json`). Both small effort, both net-new.
- Jun-02 batch ideas still unbuilt: #2 Scenario Clone Button (UI counterpart to existing `/api/simulation/<id>/clone.json`), #3 Japanese README (JP community signal active — first JP coverage @m000_crypto May 17), #4 Simulation Batch Create API.
- The platform-status probe's existence opens a new alerting surface for Aeon's own heartbeat skill — could replace the existing `/health` poll with envelope-aware checks against `surface_count` drift and `last_completed_at` staleness. Worth a self-improve pass.
- Open MiroShark PRs at recap close: **0**. Both today's PRs merged within the window. Open issues: **1** (#95 French locale).

---
*Sources: `gh api repos/aaronjmars/MiroShark/commits` (since 2026-06-04T15:28:12Z), `gh pr view 148/149`, `gh api commits/<sha>` for file-level diffs, `memory/MEMORY.md`, `memory/logs/2026-06-04.md`*
