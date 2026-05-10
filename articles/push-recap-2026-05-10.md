# Push Recap — 2026-05-10

## Overview
31 commits to main across the two watched repos in the last 24 hours, all by aaronjmars / aeonframework. The headline is that **MiroShark PR #76 (Simulation Lineage Navigator) landed** at 21:02 UTC on May 9 — the bidirectional-lineage feature that closes the gap PR #75's reproducibility export left behind. On the aeon side, today was steady-state cron + one substantive self-improve PR (#33) opened to cap MEMORY.md row sizes after the index ballooned past Claude's 25K-token Read limit.

**Stats:** ~3,200 lines added across 31 commits in main, plus 1 substantive PR (#33) opened on an aeon branch and 2 PRs (#77, #78) opened on MiroShark branches but not yet merged.

---

## aaronjmars/MiroShark

### Theme: Lineage Navigator Lands (PR #76 merged to main)
**Summary:** The Simulation Lineage Navigator merged to main at 2026-05-09 21:02 UTC after spending ~9.5 hours in review. This is the lone main-branch commit in MiroShark's 24h window — clean squash-merge, +1,778/-0, eleven files, zero new dependencies (extending the 17-PR streak). PR #76 was deeply analyzed in yesterday's recap when it was still open; today it is the live artifact on main.

**Commits:**
- `e05bea4` — feat: simulation lineage navigator — fork / counterfactual graph traversal (#76)
  - New `backend/app/services/lineage_service.py` (+390 lines, pure stdlib): MAX_CHILDREN=50 cap, scenario-preview truncation, `_kind_for(state, cf)` discriminator (parent_id unset → original; parent_id + cf file → counterfactual; parent_id + no cf → fork), `_entry_for_sim` payload composer, `find_children` reverse-pointer scan over the public corpus, `build_lineage_payload` response composer
  - Modified `backend/app/api/simulation.py` (+101 lines): adds `GET /api/simulation/<id>/lineage` route — publish-gated, `Cache-Control: public, max-age=300`, returns `{simulation_id, lineage_kind, parent | null, children: [...], total_children, counterfactual | null}`. Children are public-only (private forks don't leak), sorted by `created_at` ascending (oldest first), capped at 50
  - New `backend/tests/test_unit_lineage.py` (+501 lines, 16 offline tests): MAX_CHILDREN literal pin, scenario-preview truncation, original-with-no-children empty payload, fork carries parent entry, counterfactual carries trigger metadata, three-branch reverse-pointer discovery, private-children excluded, oldest-first sort, corrupt child state silently skipped, max-children cap with honest total_children, state-level fallback, unpublished-parent renders bare entry, self-pointer doesn't recurse, missing data_dir doesn't crash, route-decorator presence guard, openapi schema declaration guard
  - Modified `backend/openapi.yaml` (+189 lines): `SimulationLineage` schema under Analytics + new path entry `/api/simulation/{simulation_id}/lineage`. Drift-detection test passes
  - Modified `frontend/src/components/EmbedDialog.vue` (+505 lines): new "🌳 Lineage" panel between the indigo reproducibility section and the orange watch section. `v-if="hasLineageGraph"` so originals with no forks see no panel (dialog stays compact). Eager-fetches lineage on dialog open + on `isPublic` flip; click-to-toggle expand. Parent row with truncated 60-char scenario + "Open parent ↗" link to `/watch/<parent_id>`; children list with one row per public child tagged 🪐 Forked or 🔀 Counterfactual; counterfactual rows surface trigger round + label inline
  - Modified `frontend/src/api/simulation.js` (+38 lines): new `getSimulationLineage(simId)` helper with full JSDoc response shape
  - Modified docs: README (+2), `docs/FEATURES.md` + `.zh-CN.md` (+25 each, full Simulation Lineage Navigator section between Reproducibility Config Export and Webhook Delivery Log), `docs/API.md` + `.zh-CN.md` (+1 each, lineage endpoint row)

**Impact:** A researcher running three counterfactual branches off a base scenario can now navigate parent → children directly from the EmbedDialog instead of remembering child sim IDs. Bidirectional lineage on a simulation is now a public, citable, embed-discoverable surface — turning yesterday's one-directional `parent_simulation_id` pointer into a navigable tree. The privacy primitive (public-only children in the response) means private in-progress forks don't leak into a tweeted parent's lineage view, which is the kind of leak that would otherwise punish the repo for shipping the feature at all.

### Theme: Two New PRs Opened (Not Yet Merged)
**Summary:** PR #77 and PR #78 were both opened today as direct follow-ups to the surface-usage analytics + lineage primitives that landed earlier this week. Neither has merged yet; their branches do not appear in main's commit list, but they are the visible direction of travel for the next 24 hours.

**Pending:**
- PR #77 — `feat: track reproduce.json + lineage in surface-stats` (opened 07:46 UTC) — extends the per-share-surface counters from PR #74 to also count `reproduce.json` and `lineage` endpoint hits, treating the citation primitive (#75) and the navigation primitive (#76) as first-class surfaces in the trending sort feedback loop
- PR #78 — `feat: trending sort — turn surface-stats into a discovery primitive` (opened 11:24 UTC) — adds `sort=trending` to `/explore` that ranks public sims by cumulative `_serves_total` across surfaces, with `created_at` desc tie-break. Today's `feature` skill (cba0b79) opened this one; it's the "first feedback loop from distribution analytics back into gallery ranking"

**Impact:** With #76 merged and #77 + #78 in flight, the seven-PR arc that started with #71 (one-week roundup) is converging on a self-reinforcing observability → distribution → discovery loop: webhook events emit → surface-stats counts hits → trending sort surfaces the most-hit sims → operators get more eyeballs → more shares → more counts. Each piece individually is a small feature; together they are the substrate for the OpenRouter-200M-tokens-daily story to compound.

---

## aaronjmars/miroshark-aeon

### Theme: Self-Improve Opens PR #33 — MEMORY.md Index Cap
**Summary:** Today's most consequential aeon work isn't on main — it's PR #33, opened by the `self-improve` skill at 13:09 UTC as a re-apply of yesterday's closed PR #32. The trigger was concrete and operational: every skill that follows the project rule "read `memory/MEMORY.md` for high-level context" was hitting the Claude Read tool's 25K-token limit because the index file had grown to 81 KB / 33K+ tokens. PR #32 had the right fix but conflicted with bot-rewritten artifacts on main; the owner explicitly directed the next self-improve run to regenerate against current main, and that's exactly what happened.

**Pending PR:**
- `df23502` — improve(memory): cap MEMORY.md row sizes so the index stays readable
  - Modified `skills/memory-flush/SKILL.md` (+14, -3): new step 5 enforces per-row character caps on every flush — Skills Built ≤280, Recent Articles ≤220, Recent Digests ≤180. Adds a post-flush `wc -c` sanity check (target <25 KB) and explicit guidance to push oversized detail into `memory/topics/<topic>.md` or daily logs rather than letting a row sprawl into a 5K-character paragraph
  - Modified `memory/MEMORY.md` (+45, -53): condensed each Skills Built and Recent Articles row to a one-sentence summary plus PR number; refreshed Active Targets (1,126 stars / 224 forks; ATH retest at -6.7%) and Next Priorities (open MiroShark PRs #77, #78). File is now **7.7 KB / 77 lines (-90%)**. Detail preserved verbatim in `memory/logs/` and `articles/<skill>-YYYY-MM-DD.md`
  - Plus the routine self-improve auto-commit `e4bd7ac` for output artifacts

**Impact:** Closes a self-induced regression: the very memory system that exists to give skills context was failing to load for skills, because the artifacts the skills were writing into the index were too verbose. The structural fix (per-row caps in the flush skill) prevents the bug from coming back, and the data fix (condensed MEMORY.md) immediately restores the read path. This is the second time around — the first PR (#32) was closed for conflicts, not for being wrong, so this round is the durable version.

### Theme: Steady-State Cron — 30 Routine Auto-Commits
**Summary:** The other 30 commits to aeon main are the by-now-familiar cron exhaust: scheduler state updates, per-skill success markers, and per-skill auto-commits dropping articles + dashboard output JSON. Eleven distinct skills shipped in the window. No skill failed; no anomalous diffs; no force-pushes or rebases. This is the framework working as designed.

**Skills that ran (in chronological order, last 24h):**
- `push-recap` — yesterday's run (eef6fef + f3e4ed1 success marker, 15:08 UTC)
- `repo-article` — yesterday's PR #76 long-form (eb6111b + e3e661e, 16:23 UTC)
- `project-lens` — yesterday's framework reflection (c8b14c0 + 54373f8, 16:25 UTC)
- `heartbeat` — yesterday's nightly health check (d05ad6e + f09bc62, 19:31 UTC)
- `token-report` — today, $MIROSHARK +30.6% 24h, near-ATH recovery (ae8369b + f4ea9a1, 06:38 UTC, +177 lines incl. articles/token-report-2026-05-10.md)
- `fetch-tweets` — today, 11 new tweets, all bullish, @BaseCaptainHB bankrbot feature 45L/8RT leading (b6d4477 + a0c8d69, 06:38 UTC, +189/-32, 11 new SHA in fetch-tweets-seen.txt)
- `tweet-allocator` — today, $10 distributed across 5 tweets w/ Bankr wallets (8ff9344 + 2da074d, 08:26 UTC, +317 incl. articles/tweet-allocator-2026-05-10.md + 265-line dashboard JSON)
- `repo-pulse` — today, 1,127 stars / 224 forks / +5 stars 24h / 0 new forks (f5d8dfc + 0ae09b2 + df3f355, 10:14–10:16 UTC, +125/-7)
- `feature` — today, opened MiroShark PR #78 trending sort (cba0b79 + 84299cb, 11:27 UTC, +265/-17 incl. dashboard output + articles/feature log; also drops a `.aeon-tmp-verify-trending.py` scratch file)
- `self-improve` — today, opened PR #33 (covered above; main got just the cron-state + success-marker commits, the substance lives on the PR branch)
- `repo-actions` — today, 5 next-up ideas (#1 webhook HMAC, #2 .ipynb export, #3 trading signal JSON, #4 per-agent stance sparklines, #5 archive bundle ZIP) (28b1775 + a99df82, 14:20 UTC, +438/-13 incl. articles/repo-actions-2026-05-10.md + 319-line dashboard JSON)
- `chore(scheduler): update cron state` — six cron-state.json bumps interspersed across the day (each ±2-4 lines)

**Impact:** All 11 skills succeeded today (every `chore(cron): X success` marker is present). The cron-state churn is noise from a write-time perspective but is the framework's heartbeat — its absence would be the alarm, not its presence. The new wrinkle today is the `.aeon-tmp-verify-trending.py` scratch file that the `feature` skill committed alongside its PR #78 output; it's an unused 58-line trending-sort verifier that should arguably be `.gitignore`'d or cleaned up, since it's not load-bearing for either the skill output or the PR.

---

## Developer Notes
- **New dependencies:** Zero. MiroShark's zero-new-deps streak now spans 17 consecutive substantive PRs (#57 through #76 merged, #77 + #78 in flight)
- **Breaking changes:** None. PR #76 is purely additive (zero deletions across 1,778 added lines)
- **Architecture shifts:** PR #76 introduces a new public read endpoint family (`/api/simulation/<id>/lineage`) that joins reproducibility + surface-stats as the third "metadata-on-the-sim" surface. The pattern of pure-stdlib service modules (`lineage_service.py` follows the same shape as `reproducibility_service.py`) is now the canonical extension point for read-only metadata endpoints
- **Tech debt:** New stray file `.aeon-tmp-verify-trending.py` committed by the `feature` skill (cba0b79). 58 lines; not referenced by anything; appears to be a one-off `pytest`-style verifier that should be either deleted or moved under `tests/` if it's worth keeping. The dot-prefix suggests it was meant to be transient

## What's Next
- **Tomorrow's most likely main commits:** PRs #77 (reproduce + lineage in surface-stats) and #78 (trending sort) merging to MiroShark main — both are direct, narrow extensions of already-shipped primitives, both marked CI-pending today
- **Aeon PR #33** likely merging or being closed-with-replacement once the index passes review; the next `self-improve` run will retest the read path against main to confirm the fix took
- **Open thread:** the `repo-actions` skill picked PR #78 (trending sort) from yesterday's idea list as today's `feature` candidate; the remaining 4 ideas (oEmbed, peak-round snapshot, operator profile, plus today's 5 fresh ones — webhook HMAC, .ipynb export, trading signal JSON, agent stance sparklines, archive bundle ZIP) are the eligible pool for tomorrow's pick
- **Quiet branches:** no orphaned branches detected — every feature branch with a commit in the window is also represented by an open PR
