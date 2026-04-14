# Push Recap — 2026-04-14

## Overview

Yesterday's push window was a high-output batch merge: aaronjmars merged 5 PRs into MiroShark in under 30 minutes, closing out the observability sprint with simulation history search, prediction accuracy tracking, belief drift charting, a shared markdown renderer, and a one-click article generator. In parallel, miroshark-aeon gained two new content skills (project-lens and weekly-shiplog), moved push-recap to a daily schedule, and fixed a YAML comment parsing bug that was silently mangling model names in the CI harness. 17 commits across both repos; the main thrust was closing the loop between simulation output and shareable content.

**Stats:** ~20 files changed, ~1,100 additions / ~240 deletions across 17 commits

---

## aaronjmars/MiroShark

### New Feature: One-Click Article Generator (PR #25)

**Summary:** Any completed simulation can now produce a 400–600 word Substack-style article in one click. The backend calls an LLM with the full simulation context (agents, market prices, key findings) and returns an abstract, key findings, market dynamics, implications, and caveats section. Results are cached in `generated_article.json` so reopening the drawer doesn't re-invoke the model.

**Commits:**
- `56f757d` — feat: one-click article generator from simulation results
  - `backend/app/api/simulation.py` (+177/-1): New `POST /<simulation_id>/article` endpoint. Builds a rich prompt from the simulation's agents, trajectory, and Polymarket prices; calls `create_smart_llm_client`; caches result; supports `force_regenerate` flag.
  - `frontend/src/api/simulation.js` (+9): New `generateSimulationArticle(simulationId, options)` API wrapper.
  - `frontend/src/components/Step3Simulation.vue` (+275/-1): ✍ Article button appears once simulation is complete (phase 2, allActions populated). Click opens a slide-out drawer showing the generated text with Copy and Download .md buttons.

**Impact:** Users can go from a finished simulation run to a shareable write-up without leaving the app. This closes the "so what?" gap that previously required manual synthesis of the leaderboard, market prices, and round data.

---

### Refactor: Shared Sanitized Markdown Renderer (PR #24)

**Summary:** The markdown rendering logic that was duplicated across `Step4Report.vue` and `Step5Interaction.vue` was extracted into a shared `frontend/src/utils/markdown.js` utility using `marked` + `DOMPurify`. Both components now import the shared renderer, removing ~194 lines of duplicated code.

**Commits:**
- `93dad5c` — refactor: extract shared sanitized markdown renderer
  - `frontend/src/utils/markdown.js` (+82, new file): `renderMarkdown(text)` function — parses with `marked`, sanitizes with `DOMPurify`, safe for `v-html` binding.
  - `frontend/src/components/Step4Report.vue` (+2/-106): Replaced inline renderer with `import { renderMarkdown }`.
  - `frontend/src/components/Step5Interaction.vue` (+2/-88): Same replacement.
  - `frontend/package.json` / `package-lock.json` (+2/+30): Added `marked` and `dompurify` as explicit dependencies.

**Impact:** XSS risk from raw `v-html` is now centrally guarded. New components rendering LLM output get safe markdown for free.

---

### Feature: Aggregate Belief Drift Chart — Bug Fix (PR #23)

**Summary:** The belief drift chart shipped yesterday (PR #23) had a duplicate key bug — `belief_drift_summary` was returned twice in the API response payload. One line removed.

**Commits:**
- `38dc46d` — fix: remove duplicate belief_drift_summary key from API response
  - `backend/app/api/simulation.py` (-1): Removed redundant `"belief_drift_summary": summary` field that was duplicating the already-present `"summary"` key in the `/belief-drift` endpoint response.

**Impact:** Prevents client-side confusion from ambiguous JSON keys; API now returns a clean, unambiguous schema.

---

### Feature: Prediction Resolution & Accuracy Tracking — Hardening (PR #22)

**Summary:** The prediction resolution feature (which records YES/NO outcomes and auto-computes accuracy from Polymarket prices) got two defensive fixes before it landed on main: sqlite3 connections are now managed with context managers, and the accuracy_score null guard was extended to the template to prevent rendering crashes on unresolved simulations.

**Commits:**
- `f23d4ab` — fix: use sqlite3 context manager and guard accuracy_score null in template
  - `backend/app/api/simulation.py` (+22/-24): Replaced raw `con = sqlite3.connect()` / `cur = con.cursor()` pairs with `with sqlite3.connect(db_path) as con:` context managers throughout `resolve_simulation`. Prevents dangling connections on exceptions.
  - `frontend/src/components/HistoryDatabase.vue` (+2/-2): Updated accuracy display logic to short-circuit correctly when `accuracy_score` is `null` rather than `0`, preventing `✗ Incorrect` from appearing on unresolved simulations.
- `b47046b` — merge: resolve conflicts with main (history search from #20)
  - `HistoryDatabase.vue`: Rebased prediction resolution changes on top of the history search/filter additions from PR #20.

**Impact:** Prevents connection leaks in the resolve endpoint and stops incorrect "wrong prediction" labels on simulations that haven't been resolved yet.

---

### Feature: Simulation History Search & Filter (PR #20)

**Summary:** The simulation history modal now has a real search and filter layer. A text search box filters by simulation title/scenario; dropdowns filter by status and date range; a sort control orders by date, stars, or divergence; a "forks only" toggle isolates branched runs; and the last filter state persists to localStorage.

**Commits:**
- `f1ba36e` — Merge pull request #20 from aaronjmars/feat/history-search-filter
  - `frontend/src/components/HistoryDatabase.vue` (+294/-5): Full filter bar added — search input, status `<select>`, date `<select>`, sort `<select>`, forks-only checkbox, no-results empty state with clear-filters CTA. All state reactive; localStorage persistence on filter change.

**Impact:** As the history table grows (especially with fork-heavy exploratory sessions), users can now quickly find a specific scenario, compare runs, or audit predictions without scrolling through an unbounded list.

---

## aaronjmars/miroshark-aeon

### New Skills: project-lens and weekly-shiplog (PR via Aaron's direct push)

**Summary:** Two new content skills and a schedule promotion. `push-recap` moved from every-2-days to daily (0 15 * * *). `project-lens` was added on a Mon/Wed/Fri cadence — it writes articles that explain MiroShark through an unexpected external lens (a news event, a philosophy, a comparable project) rather than tracking repo progress. `weekly-shiplog` was added on Monday mornings as a narrative summary of everything shipped that week across both watched repos.

**Commits:**
- `6fe8c15` — Add weekly-shiplog and project-lens skills, make push-recap daily
  - `aeon.yml` (+9/-5): push-recap schedule changed from `0 15 */2 * *` to `0 15 * * *`. New entries for `project-lens: { schedule: "0 16 * * 1,3,5" }` and `weekly-shiplog: { schedule: "0 9 * * 1" }`. `repo-article` constrained to off-days from project-lens to avoid duplicate content.
  - `skills/project-lens/SKILL.md` (+92, new file): Angle-selection logic that checks what's trending vs. what angles have been used recently. Produces ~600-word articles connecting the project to a broader frame. Explicitly forbidden from repeating repo-progress updates.
  - `skills/weekly-shiplog/SKILL.md` (+95, new file): Collects 7 days of commits and merged PRs, groups by theme, and writes a narrative shiplog in a changelog-plus-story hybrid format.

**Impact:** Significantly increases the cadence and diversity of Aeon's content output. push-recap was the most frequently missing skill in heartbeat reports; running it daily removes the every-other-day gap. project-lens and weekly-shiplog bring new angles to the content mix.

---

### Fix: YAML Comment Stripping in Workflow Model Parsing

**Summary:** The CI harness was failing to correctly parse per-skill model overrides when the `aeon.yml` entry included an inline YAML comment (e.g., `model: "claude-sonnet-4-6"  # Mon, Wed, Fri`). The comment text was being captured as part of the model string, silently mangling the model name passed to Claude Code.

**Commits:**
- `22aec26` — fix(workflow): strip YAML comments from model parsing
  - `.github/workflows/aeon.yml` (+1/-1): Added `| sed 's/#.*//'` before the model-name extraction `sed` in `SKILL_MODEL` parsing. Comments are now stripped before the regex extracts the value.

**Impact:** Skills with inline YAML comments on their model line were silently using a garbage model name (e.g., `claude-sonnet-4-6` → `claude-sonnet-4-6  # Mon` → bad API call). This is a silent correctness fix that affects any skill scheduled with a day-of-week comment, which is now the pattern for project-lens and weekly-shiplog.

---

### Aeon Activity Auto-Commits

The remaining miroshark-aeon commits (`fd45ae9`, `4d2018c`, `8790182`, `9b41bd1`, `f53c5d4`, `22118b6`) are automated log commits from Aeon's daily skill runs: token-report, fetch-tweets, repo-pulse, feature build (trace interview PR #26), self-improve (heartbeat auto-trigger PR #11), and repo-actions. No skill logic changed; these are pure artifact commits.

---

## Developer Notes
- **New dependencies:** `marked`, `dompurify` added to `frontend/package.json` (via PR #24)
- **Architecture shifts:** Markdown rendering is now centralized in `utils/markdown.js` — any future component rendering LLM or user-authored text should import from there
- **Breaking changes:** `/belief-drift` API no longer returns the `belief_drift_summary` key (only `summary`); any client code reading the old key will silently get `undefined`
- **Aeon schedule change:** push-recap is now daily. project-lens runs Mon/Wed/Fri. weekly-shiplog runs Monday morning. The every-2-day content slots (repo-article) shift to the off-days.

## What's Next
- PR #26 (trace interview) is open on MiroShark — likely next merge
- repo-actions-2026-04-14.md has 5 new ideas; top pick is statistical batch runs with aggregate dashboard
- weekly-shiplog and project-lens will run for the first time today/this week — first outputs will reveal whether the prompts need calibration
- The YAML comment parsing fix unblocks clean inline documentation in aeon.yml, which should be applied retroactively to other scheduled skills
