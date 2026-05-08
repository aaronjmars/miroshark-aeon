# Push Recap — 2026-05-08

## Overview
Two repos, two substantive commits, one merge: aaronjmars/MiroShark merged PR #75 (Reproducibility Config Export — the citation primitive that closes the surface-multiplication arc behind every share surface) and aaronjmars/miroshark-aeon opened PR #32 fixing a self-inflicted blocker where MEMORY.md had grown to 76KB / 31K+ tokens — past the Read tool's 25K limit, locking every skill out of its own index. The day's other ~33 aeon pushes are routine `chore(cron)` / `chore(scheduler)` auto-commits from the daily skill schedule.

**Stats:** 13 files changed, +1,961 / -42 lines across 2 substantive commits (35 commits total counting cron auto-commits).

---

## aaronjmars/MiroShark

### Reproducibility Config Export — the citation primitive (PR #75, merged 13:27 UTC)

**Summary:** Six of the ten share surfaces (transcript, trajectory, thread, watch, GIF, share card) make a finished simulation *citable*; this PR makes it *reproducible*. The new `GET /api/simulation/<id>/reproduce.json` endpoint returns a v1-schema JSON document carrying every parameter another operator needs to re-run the same simulation — scenario, agent count, total rounds, platform toggles, time-config knobs, director events, and lineage (original / fork / counterfactual + parent ID + 140-char preview). Pretty-printed with `sort_keys=True + indent=2` so identical exports of a finished sim are bytewise-identical and the file hash becomes a stable citation key for paper appendices and threads. Pivot from May 6 repo-actions idea #1, picked over #2 Python SDK CI (PAT lacks workflows scope), #3 Director Event Overlay (chartjs-plugin-annotation pin), and #5 Comparative Run View (lower research-side leverage).

**Commit:**
- `92acb3d` — feat: reproducibility config export — citation primitive for share surfaces (#75)

**File-by-file (+1,916 / -0 lines across 11 files, zero deletions):**

- **New `backend/app/services/repro_export.py`** (+487 lines, pure stdlib `json` + `os`)
  - `SCHEMA_VERSION = "1"` constant + `REQUIRED_KEYS` frozenset pinning every v1 field so a downstream parser can validate cheaply
  - `build_repro_config(state_dict, config_data, sim_dir)` composes the blob from `state.to_dict()` + `simulation_config.json` + `sim_dir/counterfactual_injection.json` + director events
  - `_build_lineage()` resolves three cases: no `parent_simulation_id` → `kind: "original"`; parent + counterfactual file → `kind: "counterfactual"` (carries `trigger_round` + `label` + 140-char preview matching parent-side `config_diff.counterfactual.preview` cap); parent + no counterfactual → `kind: "fork"`
  - `_read_director_events()` handles two historical storage shapes — current `director-events.jsonl` (JSON Lines, line-by-line tolerant of single corrupt lines) and legacy `director-events.json` (list-style or `{events: [...]}`); drops events with no label rather than emitting empty strings; sorts by round
  - `_derive_total_rounds()` mirrors `_build_embed_summary_payload`'s logic — prefer state's own `total_rounds`, otherwise reconstruct from `total_simulation_hours * 60 / minutes_per_round`, fall back to 0 so the blob is returnable even before the sim starts
  - `render_json_bytes()` returns bytes with `sort_keys=True, indent=2` — bytewise-stable for citation hashing
  - `validate_blob()` accept/reject helper for downstream consumers
  - Defense-in-depth: corrupt artifacts degrade to `null` rather than 500ing the export — the citation surface must be available even when ancillary files are missing
  - `_safe_int()` / `_safe_str()` coerce hand-edited config junk (`"agent_count": "lots"`) into `0` rather than crashing the read

- **`backend/app/api/simulation.py`** (+108 lines)
  - New `simulation_bp.route('/<simulation_id>/reproduce.json', methods=['GET'])` handler
  - Same publish gate as every other share surface — 403 if not `is_public`, 404 if sim missing
  - `Cache-Control: public, max-age=300` — 5-min cache because the reproduction blob is stable once the sim reaches a terminal state (slightly longer than the trajectory CSV's 60s)
  - `Content-Disposition: inline; filename="miroshark-{simulation_id[:12]}-reproduce.json"` — inline so SPA click renders in-tab; EmbedDialog uses an explicit `download` attribute when it wants save-as
  - 500 fallback logs full traceback rather than swallowing — citation surface failures should be diagnosable

- **New `backend/tests/test_unit_repro_export.py`** (+480 lines, 22 offline unit tests)
  - Schema invariants: `REQUIRED_KEYS` present on every successful export; `SCHEMA_VERSION` pinned to `"1"`
  - Scenario fallback path (state.simulation_requirement when config_data missing)
  - `total_rounds` derivation across both paths (state-direct + time-config-reconstructed)
  - Lineage shapes: original, fork, counterfactual (with + without injection_text)
  - Corrupt-file degradation: counterfactual_injection.json malformed → `kind: "fork"`; director-events.jsonl with mixed valid/corrupt lines preserves valid ones
  - Director events parsing across both storage formats (JSONL + legacy list-style)
  - `render_json_bytes()` determinism — same blob, same bytes, different invocations
  - `validate_blob()` accept + reject paths
  - Route + openapi drift guards — fails CI if the route disappears or the schema drifts from the implementation

- **`backend/openapi.yaml`** (+249 lines) — `ReproductionConfig` schema added under Publish & Embed; full per-field documentation; drift-detection test passes (extends existing route, no new blueprint)

- **`frontend/src/components/EmbedDialog.vue`** (+484 lines)
  - "🔬 Reproducibility config" panel sits between the Distribution panel and the Mark-outcome panel
  - Collapsed-by-default summary grid: Schema · Agents · Rounds · Platforms · Director events · Lineage — viewer who only cares about share / publish / outcome doesn't pay the network round-trip on every dialog open
  - Inline lineage badge: `🪐 Forked` or `🔀 Counterfactual` with parent-id tooltip and a description like "Counterfactual of sim_X at round 12 (ceo_resigns)" so the reader sees the relationship without opening the parent
  - Copy-ready curl snippet (`curl <origin>/api/simulation/<id>/reproduce.json > config.json`), Download `reproduce.json` button (uses `download` attribute for save-as), Copy URL button, Refresh button
  - State resets on dialog open and on `isPublic` flip — same lifecycle the surface-stats panel already uses
  - i18n: en + zh-CN strings throughout (all `$tr(en, zh)` calls present)

- **`frontend/src/api/simulation.js`** (+44 lines) — `getReproductionUrl(simulationId, origin)` + `getReproduction(simulationId)` helpers

- **Docs:** `README.md` (+2), `docs/FEATURES.md` (+30) + `docs/FEATURES.zh-CN.md` (+30) — feature row + full FEATURES section between Surface Usage Analytics and Webhook Delivery Log; `docs/API.md` (+1) + `docs/API.zh-CN.md` (+1)

**Impact:** Closes the **reproducibility gap** that PR #71's shareable scenario URLs left open. Those URLs carry the scenario text and template slug; this blob carries the agent count, rounds, platform mix, time-config, director events, and lineage parentage that determine the simulation's behavior. A researcher quoting a published sim now has every parameter needed to re-run it — the file hash is a citation key suitable for paper appendices, the lineage block surfaces fork/counterfactual provenance to readers without forcing them to open the parent, and the EmbedDialog UI makes both copy-paste curl and one-click download trivial. **Zero-new-deps streak now spans 15 consecutive substantive PRs** (#57 → #58 → #60 → #61 → #62 → #65 → #66 → #67 → #69 → #71 → #72 → #73 → #74 → #75; #63 / #64 README-only).

---

## aaronjmars/miroshark-aeon

### MEMORY.md self-rescue — capping rows so the index stops blocking its own skills (PR #32, open)

**Summary:** Aeon hit a self-inflicted ceiling: `memory/MEMORY.md` had grown to 76KB / 31K+ tokens — over the Read tool's 25K-token limit. Per CLAUDE.md, MEMORY.md is supposed to be a short index (~50 lines) that every skill reads at task start. Each `Skills Built` and `Recent Articles` row had bloated to 5K+ characters of full skill descriptions, which meant **every skill that tried to load the index was failing the Read call entirely**. The fix is two-pronged: tighten the `memory-flush` skill to enforce per-row character caps on every flush, and condense every existing row in MEMORY.md down to a one-sentence summary.

**Commit:**
- `367a2fd` — improve(memory): cap MEMORY.md row sizes so the index stays readable

**File-by-file (+45 / -42 lines across 2 files):**

- **`skills/memory-flush/SKILL.md`** (+10 / -4)
  - New step 5 enforces per-row caps: `Skills Built` Notes column ≤280 chars (one tweet-length sentence), `Recent Articles` Notes column ≤220 chars (angle in one sentence + word count), `Recent Digests` Key Topics ≤180 chars
  - When writing a new row OR finding an oversized existing row, condense in place; if a row truly needs more space, move detail to `memory/topics/<topic>.md` and replace the row body with a one-line summary + `→ topics/<topic>.md` pointer
  - **Sanity check:** every flush ends with `wc -c memory/MEMORY.md` — must print under ~25000 (≈25KB); if it exceeds, immediately re-tighten the longest rows or push detail into topic files; the byte count is logged under the flush entry
  - Existing rotation thresholds (Skills Built keep last 10, Recent Articles last 8, Recent Digests last 6) preserved; the step is renumbered (was 4–7, now 4–8)

- **`memory/MEMORY.md`** (+35 / -38)
  - File shrunk from 76KB / 31K+ tokens to 9.4KB / 79 lines
  - New top-of-file callout banner: **"Index file — keep concise. Per-row caps: Skills Built ≤280, Recent Articles ≤220, Recent Digests ≤180. Detailed notes belong in `memory/topics/<topic>.md` or `memory/logs/YYYY-MM-DD.md`. The full file must stay readable in one Read call (under ~25K tokens)."**
  - Each `Recent Articles` row condensed from a 5K-char paragraph to a one-sentence angle summary + word count — full article body still lives at `articles/<skill>-YYYY-MM-DD.md`, daily log entries still on disk, no information lost
  - "Last consolidated" date bumped from 2026-05-06 → 2026-05-08

**Impact:** Restores the contract every skill depends on — MEMORY.md is supposed to be an *index*, not a corpus, and every skill is supposed to be able to load it as part of its first-task context-loading step. The 76KB → 9.4KB reduction (8x smaller, 4x under the Read tool ceiling) plus the explicit `wc -c` guard in `memory-flush` should keep the index inside the cap going forward. The instinct that drove the bloat (preserve every detail of every skill run) was right; the location was wrong — daily logs in `memory/logs/YYYY-MM-DD.md` and topic files in `memory/topics/` are the correct homes for that detail, with MEMORY.md acting purely as the table of contents that points at them.

### Routine cron auto-commits

The remaining ~33 aeon pushes are `chore(cron):` / `chore(scheduler):` / `chore(<skill>): auto-commit` from the day's scheduled skill runs — token-report (06:12), fetch-tweets (06:55), tweet-allocator (08:12), repo-pulse (10:43), feature (11:40), self-improve (13:40), and repo-actions (14:25). All ran successfully. Their substantive outputs landed under `articles/`, `memory/logs/2026-05-08.md`, and `dashboard/outputs/` rather than via direct repo code changes, so no patch reading is needed for the recap.

---

## Developer Notes

- **New dependencies:** None. PR #75 sticks to pure stdlib (`json` + `os` + `datetime` + `typing`); the aeon improvement is pure Markdown.
- **Breaking changes:** None. PR #75 adds a new endpoint behind the existing publish gate; no existing surface changed shape. Aeon's MEMORY.md condensation kept the table schemas (`| Date | Title | Notes |`) intact.
- **Architecture shifts:** PR #75 follows the now-established "per-sim file + atomic write + schema lock + fire-and-forget read + zero-default fallback + collapsed UI panel + `require_admin_token`/publish gate" pattern that Surface Usage Analytics (PR #74) and Webhook Delivery Log (PR #73) introduced. Three observability/citation surfaces in three days, all sharing the same template — this is a deliberate substrate, not a coincidence.
- **Tech debt:** Aeon's MEMORY.md row-cap is enforced *only* during `memory-flush` runs (Sun + Wed). Any skill that appends to MEMORY.md mid-week could re-introduce oversized rows; future work might add a pre-commit `wc -c` guard or a more aggressive in-line cap check during every skill run.
- **Tests:** PR #75 ships 22 offline unit tests; the aeon improvement is a Markdown change with no test surface (the `wc -c` sanity check inside the skill is the runtime guard).

## What's Next

- **PR #32 still open** — the memory cap fix is on `improve/memory-md-row-caps` branch; will likely auto-merge once CI passes (chore-only branches in this repo typically merge same-day).
- **Surface multiplication arc has a natural close-out story** now: 11 share surfaces (PR #57's per-card feed entries → PR #65 trajectory → PR #66 thread → PR #67 watch → PR #69 dominant_stance ±0.2pp threshold → PR #71 shareable scenario URLs → PR #72 share card → PR #73 webhook delivery log → PR #74 surface usage analytics → PR #75 reproducibility config) over the shared `sim_dir/` substrate, with the publish gate + admin token + collapsed UI pattern repeated across all of them. Tomorrow's repo-actions batch (5 ideas: Trending Simulations Sort, oEmbed Endpoint, Simulation Lineage Navigator, Peak-Round Belief Snapshot, Operator Profile + Attribution) explicitly targets the *interconnection layer* between these surfaces — turning them from 11 isolated endpoints into a discovery and composition network.
- **Citation primitive unlocks downstream paths**: with bytewise-stable `reproduce.json`, the natural next moves are (a) a CLI/SDK that takes a `reproduce.json` and re-runs the sim end-to-end, (b) a "verified reproduction" badge that anchors a new sim against its parent's reproduce.json hash, and (c) academic-style permanent links (`/sim/<hash>` resolving to the bytewise-identical export). Idea #3 (Lineage Navigator) and the recent verified-prediction work converge here.
- **Branches created but not merged:** `improve/memory-md-row-caps` (aeon, PR #32 open). MiroShark has no open PRs — `feat/reproducibility-config-export` was deleted on merge.

**Sources:**
- MiroShark PR #75: https://github.com/aaronjmars/MiroShark/pull/75
- aeon PR #32: https://github.com/aaronjmars/miroshark-aeon/pull/32
- Commit `92acb3d` (MiroShark): https://github.com/aaronjmars/MiroShark/commit/92acb3d09ee87cddd1f43362b746772d287aa46b
- Commit `367a2fd` (aeon): https://github.com/aaronjmars/miroshark-aeon/commit/367a2fd
