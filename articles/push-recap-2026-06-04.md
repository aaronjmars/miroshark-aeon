# Push Recap — 2026-06-04

## Overview

Two substantive PRs landed on `main` across the watched repos in the last 24h, both Aeon-built: PR #147 on MiroShark added a per-project aggregate-stats endpoint (the missing middle between the platform-wide `/api/stats` and the per-sim signal surfaces), and PR #52 on miroshark-aeon shipped a `pre-existing-features` registry — the sibling to yesterday's `blocked-features.md`, closing the second half of the "stop re-suggesting things we already have" problem. One additional non-code commit landed yesterday afternoon on the aeon repo: the `repo-article` skill's saved output from the 2026-06-03 drift-guard article. The day's thrust is two distinct moves on the same theme — **filtering noise** (don't propose what already exists) and **scoping numbers** (don't collapse what should stay separated).

**Stats:** ~22 files changed, +2,218 / -20 lines across 3 substantive commits (cron auto-commit churn excluded per May-31 convention).

---

## aaronjmars/MiroShark

### Theme 1: Per-Project Aggregate Statistics — the missing middle of the stats family

**Summary:** PR #147 (`feat: per-project simulation statistics (/api/project/<id>/stats)`) shipped a per-project sibling of `/api/stats`: same envelope shape, scoped to a single `project_id`, plus one new field — `quality_distribution` — that wouldn't make sense at platform granularity but is the whole point at per-project granularity. Aeon-built, opened 11:24 UTC, merged 15:16 UTC. 13 files, +1,864 / -10.

**Commits:**
- `570cd00` — *feat: per-project simulation statistics (/api/project/`<id>`/stats) (#147)*
  - New `backend/app/services/project_stats.py` (+522): stdlib-only scan + 60-second per-`(sim_root, project_id)` cache. Reuses `signal_service.compute_signal` for stance derivation (so a sim labelled Bullish on its `signal.json` lands in the project's `bullish` bucket — same source-of-truth chain as the per-sim surface), and `surface_stats.SURFACE_KEYS` for the surface-views aggregate. `PROJECT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.\-]{1,120}$")` rejects malformed IDs at the API boundary before any disk scan runs.
  - `backend/app/api/stats.py` (+109/-9): added second blueprint `project_stats_bp` on the same file, mounted at `/api/project` so the URL `/api/project/<project_id>/stats` stays canonical even as the platform-stats namespace grows. Module docstring rewritten *"Two surfaces on one blueprint"* → *"Three surfaces on one blueprint"*; the third entry is the per-project route. ETag set to `"project-<total>-<newest_id_prefix>"` — distinct from the platform ETag so a dashboard polling both surfaces gets accurate `304` short-circuits on each.
  - `backend/app/__init__.py` (+6/-1) and `backend/app/api/__init__.py` (+5): blueprint registration wired.
  - `backend/app/services/surfaces_catalog.py` (+9): new `project_stats` entry under platform-level surfaces. The catalog count goes 30 → 31, and `/api/surfaces.json` discoverers see the new endpoint immediately.
  - `backend/openapi.yaml` (+279): full `/api/project/{project_id}/stats` path + `ProjectStats` schema component, ETag header, 304/400 responses documented.
  - `backend/tests/test_unit_project_stats.py` (new, +843): 28 offline tests covering empty/missing `sim_root`, unknown `project_id`, case-sensitive match, unpublished/incomplete exclusion, mixed-direction counts, quality bucketing (incl. unknown-value exclusion from the four-bucket sum), surface-views per-project boundary, newest-sim selection, avg confidence rounding, 60s cache + `force_refresh` + per-project cache isolation, ETag derivation + distinctness from platform ETag, `is_valid_project_id` accept/reject, openapi/route/blueprint wiring guards.
  - `backend/tests/test_unit_openapi.py` (+4) + `backend/tests/test_unit_surfaces_catalog.py` (+2): drift guards updated for the new blueprint and the new catalog entry.
  - `docs/API.md` (+1) + `docs/FEATURES.md` (+40): table row + full section between Ecosystem JSON Registry and BibTeX Academic Citation.
  - `docs/OBSERVABILITY.md` (+8): new "Aggregate Metrics" section listing the three platform-level endpoints together for the first time (`/api/stats`, `/api/stats/badge.svg`, `/api/project/<id>/stats`).
  - `frontend/src/api/simulation.js` (+36): `getProjectStats(projectId)` + `getProjectStatsUrl(projectId, origin)` helpers. No Vue view — this is an operator/integrator-facing API, not a user-facing screen.

**Impact:** This closes a slice the gallery filter set has been doing client-side. An operator running several named projects could pull `/api/stats` and the public gallery and aggregate themselves; now `GET /api/project/<id>/stats` returns the same numbers in one call, scoped to one workspace, with a quality distribution that the platform-level surface deliberately omits. The new `quality_distribution` (excellent/good/fair/poor) is the only field that's not a strict subset of the platform envelope — the rationale documented in the module docstring is that at platform scale the bucket counts are too heterogeneous to be useful ("the corpus is too heterogeneous for the distribution to be useful"), but inside a single project they tell an operator whether their workflow is producing high-quality sims at all. Also notable: unknown `project_id` returns an all-zero envelope, not 404, because "absence of a project is a valid state for an operator iterating projects in a dashboard, not an error." That's a deliberate ergonomic choice for the dashboard-polling use case. **Zero new dependencies** — 39th consecutive zero-deps PR streak on MiroShark.

---

## aaronjmars/miroshark-aeon

### Theme 2: Aeon stops re-suggesting features that already exist — pre-existing-features registry

**Summary:** PR #52 (`improve: pre-existing-features registry — sibling to blocked-features`) added the second half of Aeon's "do not suggest" memory layer. Yesterday's `blocked-features.md` (PR #50, merged 2026-06-03) handled *architecturally-blocked* ideas — the ones that can't be built because an upstream constraint is missing (e.g. Operator Profile needing an `operator` field on `SimulationState`). Today's `pre-existing-features.md` handles the other half: ideas that have *already been shipped* on the watched repo under a different name, path, or surface. Different lifecycle, different exclusion note in the article output, but the same shape of registry. Aeon-built (self-improve skill), opened 13:37 UTC, merged 15:42 UTC.

**Commits:**
- `ab8b6ef` — *improve: pre-existing-features registry — sibling to blocked-features (#52)*
  - New `memory/topics/pre-existing-features.md` (+71): the registry itself, bootstrapped with 8 entries extracted from MEMORY.md "Next Priorities" and dated `memory/logs/` verifications — Gallery JSON (`/api/simulation/public`), Gallery Trending (`?sort=trending`), Compare API (`/api/simulation/compare`), Compare UI View (`/compare/:id1?/:id2?` → `ComparisonView.vue`), RSS/Atom Feed (`/api/feed.rss` + `/api/feed.atom`), Per-Sim Surface Engagement (`/surface-stats`), Webhook Test Ping (`POST /api/settings/test-webhook` + UI button), Simulation Search JSON (functionally redundant with `/api/simulation/public` filter set). Each entry has signature keywords + lives-at path + verifying log + suggestion history. No "Unblock when" — features don't unship, so entries are permanent unless the upstream feature is deleted.
  - `skills/repo-actions/SKILL.md` (+2): step 4 extended to read the new registry alongside `blocked-features.md`. Distinct exclusion notes in the article output — `Excluded (blocked): <title> — <reason>` vs `Excluded (pre-existing): <title> — lives at <path>` — so the operator can see at a glance whether an idea was filtered because it can't be built or because it already is. No 30-second re-verification (unlike blocked, where the upstream constraint could lift).
  - `skills/feature/SKILL.md` (+1/-1): step 6 reads the registry **before** the upstream grep (cheap short-circuit), and **writes back** new entries when its grep discovers a previously-unknown pre-existing surface. Discovery cost paid once.
  - Plus 5 churn files from the self-improve skill's auto-commit (`.outputs/self-improve.md`, `dashboard/outputs/self-improve-…json`, `memory/MEMORY.md`, `memory/logs/2026-06-04.md`, `memory/token-usage.csv`) bundled into the same merge — bookkeeping, not the change.

- `ebe0fba` — *repo-article: drift guard caught its first drift in 52 minutes*
  - `articles/repo-article-2026-06-03.md` (new, +38): the saved 905-word article from yesterday afternoon's `repo-article` skill run. Frame: PR #145's `test_catalog_names_match_ecosystem_md` drift guard (shipped at 14:03 UTC) caught its first live drift at 14:55 UTC when sparkleware merged PR #144 (a one-row addition to `ECOSYSTEM.md` only), and PR #146 closed the loop 5m48s later. First live save of a speculative test. Not a code change, but the only non-cron `aeonframework` push between yesterday's recap window-close and today's window-open.
  - `memory/MEMORY.md` (+1/-1): Recent Articles row prepended; oldest row (2026-05-27 "Week That Subtracted More Than It Added") dropped to keep 8-row cap.
  - `memory/logs/2026-06-03.md` (+20): repo-article log entry.

**Impact:** Pairs with `blocked-features.md` to give Aeon a complete "do not suggest" memory layer. Quantitative motivation: across May-20 → Jun-01 `repo-actions` batches, 8 distinct ideas were re-suggested after the watched repo had already shipped them; May-28 had 3/5 pre-existing in the batch, Jun-01 had 3/5 — i.e. on a bad day, only 2 of 5 suggested ideas were net-new. The `feature` skill already catches these in step 6 (60-second grep upstream) and pivots, but they keep eating idea slots in `repo-actions`, plus the operator confusion of seeing the same already-shipped feature surface week after week. The registry shorts that out at the suggestion stage (not the build stage), freeing ~1–3 idea slots per `repo-actions` run for net-new suggestions. Design decision worth noting: the file lives separately from `blocked-features.md` even though both are "don't suggest" lists — conceptually distinct (can't build vs already built), and different lifecycles (blocked auto-unblocks on upstream change; pre-existing is permanent unless the feature is deleted).

---

## Developer Notes

- **New dependencies:** none (39th consecutive zero-deps PR on MiroShark — streak unbroken since the Nemotron addition).
- **Breaking changes:** none. PR #147 adds a new endpoint and blueprint — existing `/api/stats` URL, ETag, and envelope are untouched. PR #52 is internal to Aeon's skill memory layer.
- **Architecture shifts:** PR #147 establishes the precedent of two blueprints on one stats file (`stats_bp` + `project_stats_bp`) — the comment in the source reads *"Two blueprints, one file — both surfaces are conceptually the 'stats' family and share helpers."* If future per-org / per-tenant aggregates land, this is the shape they'll follow.
- **Surface count:** MiroShark `/api/surfaces.json` catalog 30 → 31 (added `project_stats`). At window close: 26 publish-gated per-sim + 4 platform + 1 ecosystem + 1 self-ref ≈ 32 distinct surface entries on the catalog, including the Sparkleware-driven Jun-3 increment.
- **Tech debt:** none introduced; `pre-existing-features.md` actually *retires* a recurring class of operator-confusion noise.

## What's Next

- **MiroShark open PRs: 0** at window close (PR #147 merged 15:16 UTC). With the per-project surface in, the natural next step in the same family is per-project quality drilldown or a multi-project compare endpoint — but neither is in the current `repo-actions` batch.
- **Jun-02 batch status:** 2 of 5 addressed (#1 Ecosystem JSON Registry → PR #145 merged Jun 3; #5 Per-Project Simulation Statistics → PR #147 merged today). Still unbuilt: #2 Scenario Clone Button (frontend), #4 Simulation Batch Create API (backend, larger scope), #3 Japanese README (medium effort, JP community signal active since @m000_crypto May 17).
- **Jun-04 batch (today's `repo-actions` run):** 5 fresh ideas surfaced — Webhook Delivery Log API, Platform Status API, Multi-Sim Status Lookup, All-Time Simulation Leaderboard API, Webhook Manual Retry. All small-effort DX/Integration ideas; `feature` skill's next pick will likely come from this batch.
- **aeon open PRs: 0** at window close. With both `blocked-features.md` and `pre-existing-features.md` shipped, the "do not suggest" memory layer is structurally complete; the natural next self-improve target is something on a different axis (quality regression detection? skill cross-validation? not yet picked).
- **Branches created but not merged:** none observed via commit history.
