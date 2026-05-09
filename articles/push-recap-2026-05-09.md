# Push Recap — 2026-05-09

## Overview

Two repos, one substantive feature push and ~28 routine cron auto-commits. MiroShark gained PR #76 — *Simulation Lineage Navigator* — a direct sequel to yesterday's PR #75 that turns the one-directional `parent_simulation_id` pointer into a navigable graph in both directions. The aeon repo had no feature work today; just the day's scheduled-skill chore commits and the still-open PR #32 from yesterday (MEMORY.md row caps) sitting unchanged.

**Stats:** 11 files changed, +1,778 / -0 lines on MiroShark in 1 substantive commit. miroshark-aeon: ~28 chore commits (token-report / fetch-tweets / tweet-allocator / repo-pulse / hyperstitions-ideas / feature / repo-article / project-lens / heartbeat scheduler runs).

---

## aaronjmars/MiroShark

### Simulation Lineage Navigator (PR #76, open)

**Summary:** Yesterday's PR #75 (Reproducibility Config Export) wrote `parent_simulation_id` + `lineage.kind` + counterfactual trigger metadata into every `reproduce.json`. The data was on disk, but the link was *one-directional* — a child sim knew its parent, the parent had no view into its children. Run a base scenario then trigger three counterfactual branches, and there was no way to walk from the parent to "the three branches that diverged at round 12" without remembering each child sim id. PR #76 closes that gap by adding the reverse pointer: a new `GET /api/simulation/<id>/lineage` endpoint that returns the parent + every public child, plus an EmbedDialog panel that renders the resulting graph slice.

**Commits:**

- `d6dd47c` — *feat: simulation lineage navigator — fork / counterfactual graph traversal* (1,778 / 0 across 11 files)

  - **New file `backend/app/services/lineage_service.py`** (+390): pure stdlib (`json` + `os`), no new dependencies, no writes. The contract:
    - `MAX_CHILDREN = 50` literal cap (defense-in-depth against a pathologically forked sim — 99% of sims have zero or one children, ten branches is already an outlier) plus `SCENARIO_PREVIEW_CHARS = 80` to match the YAML front-matter shape used by the transcript export.
    - `_load_state(sim_dir)` / `_load_config_scenario(sim_dir)` / `_load_counterfactual(sim_dir)` defensive readers — every disk read swallows missing files, corrupt JSON, and mid-rewrite races and returns `None` so the navigator never crashes a parent's load on a single bad child.
    - `_kind_for(state, cf)` discriminator: no `parent_simulation_id` ⇒ `"original"`; parent set + counterfactual file present ⇒ `"counterfactual"`; parent set + no counterfactual file ⇒ `"fork"`. Mirrors `lineage.kind` from PR #75's reproduce.json so the two surfaces never disagree.
    - `_build_counterfactual_marker(cf)` extracts `{trigger_round, label}` so the badge can render "🔀 Counterfactual at round 12 (ceo_resigns)" without a second fetch.
    - `_entry_for_sim(sim_id, sim_dir, state, *, include_kind=False)` composes the per-row payload. When the parent has been unpublished after the fact, scenario travels as `""` and `is_public=False` — the SPA renders a bare placeholder rather than a click-through.
    - `_iter_candidate_sim_ids(data_dir)` walks the simulations dir skipping dotfiles + non-directories; missing data dir yields zero matches without raising.
    - `find_children(parent_id, data_dir, *, max_children=MAX_CHILDREN)` is the reverse-pointer scanner: for each candidate sim, load `state.json`, check `parent_simulation_id == parent_id`, check `is_public is True`, skip self-pointers, append. Sorts oldest-first by `created_at` (the natural narrative order — "branch A first, then branch B"). Caps at `max_children`.
    - `build_lineage_payload(simulation_id, data_dir)` is the public entry point. Composes `{simulation_id, lineage_kind, parent | null, children: [...], total_children, counterfactual | null}`. `total_children` reflects the *uncapped* scan total so a paginated future form (or a "showing first N of M" UI hint) has the honest count.

  - **Modified `backend/app/api/simulation.py`** (+101): adds the `GET /api/simulation/<simulation_id>/lineage` route between the `reproduce.json` route and the webhook delivery log routes. Same publish gate as the share card / transcript / trajectory / thread / `reproduce.json` endpoints — `_build_embed_summary_payload` checks `is_public`; 403 on unpublished sims, 404 on unknown sim ids. `Cache-Control: public, max-age=300` matches the reproduce endpoint (graph slice is stable once the parent + its branches reach terminal states). The route handler delegates the actual graph composition to `lineage_service.build_lineage_payload`.

  - **New file `backend/tests/test_unit_lineage.py`** (+501, ~16 unit tests, all offline). Pins every shape promise + degradation path: `MAX_CHILDREN` literal value pin (can't silently grow the cap), scenario preview truncation at 80 chars with ellipsis, original-with-no-children empty payload, fork carries the parent entry, counterfactual carries `{trigger_round, label}`, three-branch reverse-pointer discovery, private children excluded from a public parent's view, oldest-first child sort, corrupt child `state.json` silently skipped without blanking the rest, max-children cap with honest `total_children`, state-level `simulation_requirement` fallback for legacy sims that wrote the requirement onto state instead of config, unpublished-parent renders bare entry (`is_public=false`, `scenario_preview=""`), self-pointer doesn't recurse, missing data dir doesn't crash, route-decorator presence guard, OpenAPI schema declaration guard, route module imports the service guard.

  - **Modified `backend/openapi.yaml`** (+189): new path `/api/simulation/{simulation_id}/lineage` under the `Analytics` tag, plus a new `SimulationLineage` schema component documenting every key (`simulation_id`, `lineage_kind` enum, `parent` nullable object with `{simulation_id, scenario_preview, created_at, is_public}`, `children` array of `{simulation_id, scenario_preview, created_at, is_public, kind, counterfactual}` shapes, `total_children` integer, `counterfactual` nullable). Drift-detection test passes (the route extends the existing `simulation_bp` blueprint, no new blueprint registered).

  - **Modified `frontend/src/components/EmbedDialog.vue`** (+505): adds the `🌳 Lineage` panel between the reproducibility config section and the verified-prediction annotation section. Shows only when `hasLineageGraph` is true (`v-if="hasLineageGraph"`) — originals with no forks see no panel at all, dialog stays compact. Eager-fetches lineage on dialog open + on `isPublic` flip; click-to-toggle expand. Parent row shows the truncated 60-char scenario + "Open parent ↗" link to `/watch/<parent_id>`. Children list with one row per public child, each tagged `🪐 Forked` (indigo badge) or `🔀 Counterfactual` (orange badge). Counterfactual rows surface trigger round + label inline ("At round 12 (ceo_resigns) · scenario preview…") so the row reads as the narrative event, not a slightly different scenario. Click any row to open that sim's `/watch/<id>` in a new tab. New CSS classes for `.lineage-section` (green tint to distinguish from the indigo repro section + the orange watch surface), `.lineage-parent-row`, `.lineage-child-row`, `.lineage-child-badge-fork`, `.lineage-child-badge-cf`, with a responsive collapse at the 600px breakpoint.

  - **Modified `frontend/src/api/simulation.js`** (+38): new helper `getSimulationLineage(simId)` calling `service.get('/api/simulation/${simulationId}/lineage')` with full JSDoc documenting the response shape. Lives directly below `getReproduction` so the two related fetchers sit together.

  - **Modified `README.md`** (+2 lines, en + zh-CN mirrors): adds a `Lineage Navigator` row to the features table beneath the existing `Reproducibility Config` row.

  - **Modified `docs/FEATURES.md` + `docs/FEATURES.zh-CN.md`** (+25 each): full *Simulation Lineage Navigator* section between *Reproducibility Config Export* and *Webhook Delivery Log*. Spells out the navigation-gap framing, the response shape, the implementation guarantees (pure stdlib, read-only, public-children-only, defense-in-depth, bounded), the cache duration, the publish gate, and the EmbedDialog panel behavior.

  - **Modified `docs/API.md` + `docs/API.zh-CN.md`** (+1 each): adds the `/api/simulation/<id>/lineage` row to the API reference table.

**Impact:**

- **Citation graph completeness.** PR #75 made finished sims *citable* via `reproduce.json`'s file hash. PR #76 makes the *graph behind a citation* navigable — a reader who lands on `/watch/<sim_id>` for a counterfactual branch can now follow the lineage back to the base scenario and forward to sibling branches without leaving the page.
- **Counterfactual branch UX.** The counterfactual badge renders the trigger round + label inline ("Counterfactual at round 12 (ceo_resigns)"), which is the actual narrative event a reader cares about. Without that, three counterfactual branches off the same parent would all read as "slightly different scenarios" instead of "what happened at round 12 vs round 18 vs round 22".
- **Public-only filter is a privacy primitive.** Operators forking privately for in-progress work no longer leak those branches into a tweeted parent's lineage view — a sharp distinction the design rationale calls out explicitly.
- **Defense-in-depth pattern compounds.** Like PR #75 before it, the implementation never raises on disk corruption or mid-write races. The 16-test pin includes the corrupt-state and self-pointer cases. Combined with PR #75's bytewise-stable JSON, this is now two consecutive PRs of "the public discovery surface tolerates a single bad artifact without blanking out".

---

## aaronjmars/miroshark-aeon

### Routine cron auto-commits

**Summary:** No substantive feature or fix commits today. Just the day's scheduled-skill auto-commits — `chore(<skill>): auto-commit 2026-05-09` followed by `chore(cron): <skill> success` for each of token-report, fetch-tweets, tweet-allocator, repo-pulse, hyperstitions-ideas, feature, push-recap, and the scheduler state-update churn between them. ~28 commits total, all by `aeonframework` (the agent's own commit identity), all touching `memory/logs/2026-05-09.md`, `articles/`, `.outputs/`, `.scheduler/`, `.notify-sent-hashes`, etc.

**Commits:** (representative — full chain visible in `git log`)

- `db114dd` — `chore(scheduler): update cron state`
- `77b3491` — `chore(cron): feature success`
- `4c2e626` — `chore(feature): auto-commit 2026-05-09` (PR #76 build artifacts written into `articles/` + `memory/logs/`)
- `c82a6d2` — `chore(cron): hyperstitions-ideas success`
- `1628d9f` — `chore(hyperstitions-ideas): auto-commit 2026-05-09` (today's hyperstition: external-operator deployment by 2026-06-30)
- `e15e6b1` — `chore(cron): repo-pulse success`
- `c80298c` — `chore(cron): tweet-allocator success`
- `4afa41d` — `chore(cron): fetch-tweets success`
- `5abdbbe` — `chore(cron): token-report success`
- (plus the matching `auto-commit` and `update cron state` commits between each)

**Open PR carry-over:** PR #32 (`improve/memory-md-row-caps`, +197 / −52 across 6 files) opened yesterday 2026-05-08 13:37 UTC is still open and unchanged today.

**Impact:** This is the steady-state baseline of the framework. The substantive engineering today is the MiroShark side; aeon is the engine that ran the daily skills that produced today's article, hyperstition, token report, tweet roster, and tweet payouts. No regressions visible in the auto-commit chain — every scheduled skill posted its `success` cron commit.

---

## Developer Notes

- **New dependencies:** None on either repo. Zero-new-deps streak on MiroShark now spans **16 consecutive substantive PRs** (#57 → #76; #63 / #64 README-only; assumes PR #76 merges as-shipped).
- **Breaking changes:** None. PR #76 is a pure addition — new endpoint, new service module, new test file, new dialog panel; no existing route, schema, or component signature changed.
- **Architecture shifts:** The `lineage_service` service module is the second pure-stdlib service composed against PR #75's on-disk artifacts (`state.json`, `simulation_config.json`, `counterfactual_injection.json`). The pattern is becoming load-bearing: **PR #75 wrote the citation primitive to disk, PR #76 reads it back in a different shape, the next surface against the same artifacts only needs another ~390 LoC of read-only composition**. No new blueprint, no new dependency, no new write path.
- **Tech debt:** None introduced. `MAX_CHILDREN = 50` cap is honest (`total_children` reflects the uncapped scan total), the corrupt-state degradation path is explicit, the public-only filter is documented as a privacy primitive rather than an arbitrary scope cut.
- **Tests:** +501 LoC of pure-stdlib unit tests on the new `test_unit_lineage.py`, including OpenAPI drift guard, route-decorator presence guard, and module-import guard. Frontend build green (`npm run build` 728 modules transformed, vite v7.2.7).

## What's Next

- **PR #76 merge.** Branch `feat/simulation-lineage-navigator` is open; assuming the same same-day-merge cadence as PR #74 / PR #75, expect this to land within 24h.
- **Lineage as a discovery signal.** With `lineage_kind` + `total_children` now available per-sim, the May 8 repo-actions idea #1 (Trending Simulations Sort) has a richer signal to draw on — "highly forked" or "spawned 5+ counterfactuals" is a natural discovery axis the gallery can rank by, separate from raw surface-stats totals.
- **Open thread on aeon side.** PR #32 (MEMORY.md row-size caps) is now 24h+ stale. The May 8 push-recap flagged this as the active aeon-side open PR; still no follow-up commits on the branch.
- **Ideas remaining from May 8 repo-actions batch:** #1 Trending Sort, #2 oEmbed Endpoint, #4 Peak-Round Snapshot, #5 Operator Profile + Attribution. Today's PR #76 picked #3 (Lineage Navigator) — the four remaining candidates form the bench for the next 4 days at the current 1-feature-per-day cadence.
- **External-operator hyperstition.** Today's hyperstitions-ideas skill picked the framework-side coordination question: "Will the Aeon agent framework be deployed by ≥1 external operator running publicly under their own project identity by June 30, 2026?" The MiroShark side keeps shipping; the aeon side's open question is whether anyone outside `aaronjmars/*` stands up their own deployment.
