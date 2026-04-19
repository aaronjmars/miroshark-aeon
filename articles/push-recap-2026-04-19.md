# Push Recap — 2026-04-19

## Overview
Quiet on MiroShark's main branch (both Apr 18 merges already recapped), but two live PRs are in flight: the first external code contribution ever landed on the report engine (PR #36, ~5x speedup) and Aeon's next analytics feature, the "What If?" Counterfactual Explorer (PR #37). On miroshark-aeon, Aaron shipped three infrastructure fixes addressing duplicate skill runs, duplicate notifications, and broken chain dispatch — all rooted in issues observed during yesterday's runs.

**Stats:** 5 substantive commits across 2 repos, 11 files changed, +1,207 / -81 lines — plus ~35 automation chore commits on miroshark-aeon.

---

## aaronjmars/MiroShark

### Theme 1: First Community Perf PR — Report Generation ~5x Faster
**Summary:** External contributor `builtbydesigninc` landed a single-file refactor of `report_agent.py` that parallelizes section generation with a `ThreadPoolExecutor`, drops each section's prior-sections context, and cuts `MAX_REFLECTION_ROUNDS` from 3 to 1. Measured against a real 5-section report (Claude Sonnet 4.6 via OpenRouter): 20.8 min → ~4 min, 21 LLM calls → ~10, 270K input tokens → ~50K, $2.16 → ~$0.95. Not yet merged — PR #36 is open.

**Commits:**
- `d6afe00` — perf(report): parallelize section generation (~5x speedup on real runs)
  - Changed `backend/app/services/report_agent.py` (+87, -60 lines): added `threading` + `concurrent.futures.ThreadPoolExecutor` imports; new class constants `MAX_PARALLEL_SECTIONS = 6` (default workers) and `MAX_REFLECTION_ROUNDS = 1` (was 3). Replaced the serial `for section in outline.sections` loop with a worker function `_generate_one(idx, section)` that calls `self._generate_section_react(..., previous_sections=[], progress_callback=None, section_index=section_num)` and is submitted via `ex.submit(...)` to an executor sized `min(MAX_PARALLEL_SECTIONS, total_sections)`.
  - Each section now runs without visibility into sibling drafts (previously each section ingested the running markdown from earlier sections, creating linear input-token growth: 5K → 17K across a 5-section run). Phase 2.5 cross-section synthesis (unchanged) still stitches coherence at the end using the full assembled content.
  - Progress reporting adapted for non-deterministic completion order: a `threading.Lock()` guards the shared `completed_count`, `completed_section_titles`, and both `ReportManager.update_progress` + `progress_callback` calls. Per-section exceptions are caught inside the worker and rendered as an inline `*(Section generation error: {e})*` stub so one failing section doesn't kill the whole report. `ReportManager.save_section` is called as each section finishes, preserving partial progress if the process dies mid-report.

**Impact:** This is the first substantive external code contribution to MiroShark's backend — not a typo/README fix, an actual architectural change with a 5x measured win and 55% cost reduction. The new `MAX_PARALLEL_SECTIONS` knob (defaulting to 6) gives operators a tuning surface for different rate-limit regimes. Notably, this is not an Aeon PR — the agent is shipping features, but humans outside the core team are now shipping performance.

### Theme 2: Agent Counterfactual Explorer — Next Analytics Feature In Flight
**Summary:** Aeon opened PR #37 with the "What If?" panel — a client-triggered recomputation of belief drift after excluding up to 3 selected agents. Pure data transform over `trajectory.json`, no re-simulation, no LLM calls, milliseconds per recompute. This is the research-grade follow-up to the Agent Interaction Network Graph shipped Apr 17 (PR #33): the network shows that a dominant hub exists; What If? quantifies what that hub is actually doing to the outcome.

**Commits:**
- `347eda6` — feat: agent counterfactual explorer ("What If?")
  - New `backend/app/api/simulation.py` (+229 lines): `GET /api/simulation/<id>/counterfactual?exclude_agents=name1,name2` endpoint. Factored out a new `_drift_from_positions_by_agent` helper so the per-round stance computation can run twice (original vs. excluded set). Resolves submitted usernames via the existing `_demo_load_profiles` path (reddit_profiles.json → twitter_profiles.csv fallback). Returns original + counterfactual bullish/neutral/bearish series, `delta_final_bullish`, `delta_consensus_round`, a `strong`/`moderate`/`minimal` impact badge, and a plain-English summary string.
  - New file `frontend/src/components/WhatIfPanel.vue` (+761 lines): top-12 influence-ranked agent picker (max 3 selected), split-line SVG chart with the original bullish curve dashed and the counterfactual curve solid, impact summary with numeric deltas, PNG export.
  - Changed `frontend/src/components/Step3Simulation.vue` (+26, -5 lines): registered `WhatIfPanel`, added the `◐ What If?` overlay toggle alongside Influence / Drift / Network / Director / Demographics, wired mutual exclusion with the other analytics overlays, and hid the main feed while the panel is visible.
  - Changed `frontend/src/api/simulation.js` (+15 lines): new `getCounterfactualDrift(simId, excludeAgents)` helper.

**Impact:** Turns the network graph from a visualization into an experimental instrument. Where the Apr 17 Quality Diagnostics + Interaction Network PRs made simulation output *legible*, this one makes it *interrogatable* in a second dimension — "what if this node weren't here?" answered in milliseconds against cached trajectory data. Nine days into the analytics run (PRs #22/#23/#25/#26/#30/#31/#32/#33/#34/#35 → #37), the pattern is consistent: every new feature exploits existing simulation artifacts rather than demanding new data collection.

---

## aaronjmars/miroshark-aeon

### Theme 3: Infrastructure Hardening — Three Fixes for Problems Observed Yesterday
**Summary:** Aaron shipped three tightly scoped fixes addressing the duplicate-run / duplicate-notify class of bugs that Aeon itself has been filing self-improvement PRs about all week. These are the workflow-layer counterparts to the skill-level dedup guards (Apr 18's PRs #17 and #18). The `notify` dedup is particularly interesting — it makes skill-level idempotency guards redundant for the "accidental double-notify" failure mode, though not for duplicate *article generation*.

**Commits:**
- `70558dc` — fix(chain-runner, push-recap): unbreak chain dispatch + add sandbox note
  - Changed `.github/workflows/chain-runner.yml` (+1, -1 lines): the `gh run list` jq filter for locating the dispatched run had an unbalanced paren in `test("skill: ${skill}(";"i")` that caused every run-ID lookup to return null — silently killing chain execution. Replaced with `select(.displayTitle == "skill: ${skill}" or (.displayTitle | startswith("skill: ${skill} (")))`. Chains haven't been actually running as chains until this lands.
  - Changed `skills/push-recap/SKILL.md` (+8 lines): new "Sandbox note" block warning that the GitHub Actions bash allowlist only matches the leading command word, so `for`, `while`, and `if` loops get denied. The commit message notes the previous push-recap run "burned 35 turns and $1 on permission-denied retries before terminating." This skill — the one generating this recap — now has an explicit one-gh-api-call-per-commit contract.

- `e7816f3` — fix(scheduler, skills): kill duplicate runs + always notify on skip
  - Changed `.github/workflows/messages.yml` (+21, -7 lines): the scheduler's catch-up branch (which re-fires a skill if its schedule matched the *previous* UTC hour) used to fire unconditionally. It now compares `LAST_DISPATCH_EPOCH` against the reconstructed scheduled fire time (`PREV_HOUR:C_MIN UTC today`) and only dispatches if the last dispatch predates the scheduled fire. Root cause of the "same skill runs twice in the same hour" pattern: a tick landing in both the `H` and `PREV_HOUR+1` windows — normally blocked by the 90-minute dedup, but not always. The chain-scheduler block got the same fix (and the `LAST_DISPATCH_EPOCH` lookup was hoisted above the catch-up check so the comparison actually has a value).
  - Changed `skills/fetch-tweets/SKILL.md` (+2, -2 lines): both "no tweets found" early-exit paths (FETCH_TWEETS_EMPTY, FETCH_TWEETS_NO_NEW) now send a one-line `./notify` before stopping instead of exiting silently — so operators actually see the skip.
  - Changed `skills/tweet-allocator/SKILL.md` (+3, -3 lines): same treatment applied to `TWEET_ALLOCATOR_EMPTY` (no tweets in today's log), `TWEET_ALLOCATOR_ERROR` (missing Bankr cache), and `TWEET_ALLOCATOR_EMPTY — no eligible tweets` paths.

- `2417bf8` — fix(notify): dedup messages + suppress test/trace probes
  - Changed `.github/workflows/aeon.yml` (+54, -3 lines): both the inline `./notify` script (generated into the workspace before Claude runs) and the post-run pending-notify delivery step now hash each message with `sha256sum` and track sent hashes in `.notify-sent-hashes`. Duplicate hashes exit cleanly with a log line. Messages shorter than 120 chars that match `*test*|*trace*|*ping*|*debug*|hello|hi` (case-insensitive) are suppressed outright — these are diagnostic probes Claude sometimes issues to verify the notify pipe works. The pending-notify path also dedups against messages already sent inline. `.notify-sent-hashes` is cleaned up before the auto-commit step so it doesn't land in the repo. One other small change: `mkdir -p .pending-notify` is now done before Claude starts, so the sandbox doesn't block the very first write into it.

**Impact:** The dedup bug has been surfacing as its own self-improvement topic for a week — Apr 14 heartbeat stuck-run fix, Apr 18 repo-pulse idempotency, Apr 18 hyperstitions dedup guard. This PR attacks the class at the right layer: the scheduler shouldn't double-fire at all, and `./notify` shouldn't propagate duplicate sends even when it does. Skill-level guards become belt-and-suspenders rather than first line of defense.

### Theme 4: Daily Automation (non-substantive)
The usual cron noise: ~35 `chore(cron|scheduler|$skill): ...` auto-commits by `aeonframework` from today's skill runs (token-report, fetch-tweets, tweet-allocator, repo-pulse, feature — and now the push-recap one landing with this article). Routine activity, not covered in detail.

---

## Developer Notes
- **New dependencies:** none — the perf PR uses stdlib `threading` + `concurrent.futures`; the counterfactual PR uses no new packages.
- **Breaking changes:** none in the merged set. PR #36 changes the semantics of `previous_sections` (now always `[]` during parallel phase) — anything downstream that relied on each section seeing prior drafts would break. None does; Phase 2.5 synthesis handles coherence after assembly. `MAX_PARALLEL_SECTIONS` is configurable via `MAX_PARALLEL_SECTIONS` env var (note: not actually wired to env yet — currently a class constant; follow-up item).
- **Architecture shifts:** Two, both in flight: (a) section-report generation goes from serial-sequential to thread-pool parallel (community PR #36), a first for the report engine; (b) the `/counterfactual` endpoint establishes a "recompute-from-artifacts" pattern that the Demographic Breakdown endpoint (PR #35) pioneered — analytics are now consistently pure transforms over cached trajectory + profile files, not re-simulations.
- **Tech debt:** `MAX_PARALLEL_SECTIONS` is a class constant but the commit message says "configurable via `MAX_PARALLEL_SECTIONS`" — env-var wiring missing. The per-section progress callback is passed `None` in parallel mode, so fine-grained progress events are lost (only per-section-completion events remain). The chain-runner jq fix was in place for the `ls` lookup but chains have evidently been dead for some time — worth an audit of whether any chain actually ran successfully before this fix.

## What's Next
- **PR #36 merge or iterate:** The community perf PR is self-contained and ships a measured win. Likely merges once Aaron reviews; any discussion will be around the `previous_sections=[]` tradeoff for report coherence and the reflection-rounds default.
- **PR #37 merge:** No blockers visible — same shape as PRs #32/#33/#35 that have all merged same-day recently.
- **Chain-runner audit:** With `70558dc` landing, it's worth checking whether the `scheduler → chain-runner` path was ever firing end-to-end. If chains didn't run, every skill in the `chains:` section has actually been running standalone — not an outage, but a silent degradation from the advertised architecture.
- **Notify dedup side-effects:** Skills that intentionally send the same message twice (e.g. a repo-pulse run 1 and run 2 with identical counts) will now collapse at the notify layer. The skill-level idempotency guards (PRs #17, #18) still do the right thing by logging `REPO_PULSE_DUPLICATE` / `HYPERSTITIONS_SKIP`, but if any skill was relying on the duplicate notification reaching channels, it won't anymore.
- **1,000-star target:** MiroShark at 729 stars today, +12 in 24h; needs ~25/day to hit 1,000 by Apr 30. Trajectory still on track but dependent on the analytics run continuing to ship.
