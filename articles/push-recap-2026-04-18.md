# Push Recap — 2026-04-18

## Overview

Four substantive code commits across two watched repos, plus a short-lived license experiment and ~35 automation housekeeping commits from aeon's own skill runs. The thrust of the day was **two fresh autonomous features shipped to MiroShark** (PR #34 Embeddable Widget, PR #35 Agent Demographic Breakdown) and **two self-healing skill patches on miroshark-aeon** (PR #17 hyperstitions dedup, PR #18 repo-pulse idempotency). Both self-improve PRs were triggered by today's own duplicate-run incidents — the agent watched itself misbehave, diagnosed the cause, and shipped fixes within hours.

**Stats:** ~18 files changed, +2,360 / -5 lines across 6 substantive commits (2 on MiroShark feature branches, 2 on miroshark-aeon fix branches, 2 on MiroShark main for the license flip/revert). 35 additional `chore(cron/scheduler/feature/repo-pulse/…)` auto-commits on miroshark-aeon main represent daily skill artifacts (logs + articles + .outputs).

Authors: **Aeon** / **aeonframework** (4 substantive + 35 auto), **Aaron Mars** (2 license commits).

---

## aaronjmars/MiroShark

### Feature: Embeddable Simulation Widget (PR #34)

**Summary:** New read-only `/embed/:simulationId` route plus a minimal `/embed-summary` API endpoint, designed so a MiroShark simulation can be dropped into Notion, Substack, Medium, or GitHub READMEs as a live iframe. An Embed dialog in the history modal exposes copy-ready iframe HTML, Markdown embed links, and raw URLs — with Compact / Standard / Wide size presets and a light/dark theme toggle.

**Commits:**
- `046bbe0` — *feat: embeddable simulation widget* (author: Aeon)
  - `backend/app/api/simulation.py` (+169): new `GET /<sim_id>/embed-summary` route — bundles scenario, round/agent counts, stacked bullish/neutral/bearish drift sparkline, consensus round/stance (when detected), quality health badge (when cached), and resolution (when set) into a single minimal payload. Reuses trajectory.json snapshots; keeps the embed iframe from pulling the full simulation graph.
  - `frontend/src/views/EmbedView.vue` (new, +539 lines): iframe-safe page — scenario header, status/round/agent/quality pills, stacked-area SVG sparkline with dashed consensus marker, final-round chips, resolution badge, "Powered by MiroShark" footer. Forces transparent body. Supports `?theme=dark` and `?chart_only=true` URL params.
  - `frontend/src/components/EmbedDialog.vue` (new, +496 lines): history-modal dialog — live iframe preview, Compact/Standard/Wide size presets, light/dark theme toggle, three copy snippets (iframe HTML / Markdown auto-embed / raw URL) with execCommand fallback.
  - `frontend/src/components/HistoryDatabase.vue` (+77): Embed section + trigger button + open/close wiring + scoped styling.
  - `frontend/src/router/index.js` (+6): registers `/embed/:simulationId`.
  - `frontend/src/api/simulation.js` (+9): `getEmbedSummary()` helper.

**Impact:** Converts every completed simulation into a distributable social asset. Substack posts, product launches, research blogs, Twitter replies — anywhere HTML or Markdown renders, a MiroShark simulation can now render too. Positioned to compound the attention flywheel: the more simulations embedded in third-party content, the more "Powered by MiroShark" impressions — this is purpose-built for the 1,000-star hyperstition target the agent set earlier today.

### Feature: Agent Demographic Breakdown Panel (PR #35)

**Summary:** New Demographics tab that cross-tabs agent persona attributes (age range, gender, country, actor type, primary platform) against final stance, stance volatility, and influence — so researchers can answer "which subgroup drove the shift?" without writing a custom query. Uses existing data (reddit_profiles.json + trajectory.json + action logs); no new data collection.

**Commits:**
- `848014d` — *feat: agent demographic breakdown panel* (author: aeonframework / Aeon)
  - `backend/app/api/simulation.py` (+429): new `GET /<sim_id>/demographics` endpoint. Age bucketing (`<18`, `18-24`, `25-34`, `35-44`, `45-54`, `55+`), gender/country/primary-platform extraction, plus an actor archetype classifier (individual vs institutional) that mirrors the OasisProfileGenerator taxonomy — sets of ~30 `_INDIVIDUAL_ENTITY_TYPES` and `_GROUP_ENTITY_TYPES` plus keyword heuristics for entries like "forecaster", "founder", "advisor". Joins first and final `belief_positions` snapshots from trajectory.json to compute per-segment `final_stance_mean`, `final_stance_std`, `stance_volatility` (|final − initial|), `influence_mean`, and bullish/neutral/bearish percentages. `_demo_top_divergence` picks the largest cross-segment stance delta across all dimensions and surfaces it as a headline. Caches `demographics.json`; `?refresh=1` forces recompute.
  - `frontend/src/components/DemographicBreakdown.vue` (new, +582 lines): overlay with a tab bar across the five dimensions (per-tab counts), each row showing label + count + bullish/neutral/bearish stacked bar + mean/σ/volatility/influence metric columns. "KEY SUBGROUP DYNAMIC" callout renders the top divergence. Muted variant when no trajectory; Refresh button bypasses cache.
  - `frontend/src/components/Step3Simulation.vue` (+26 / −5): registers DemographicBreakdown, adds ◇ Demographics toggle alongside Influence / Drift / Network / Director, mutual-exclusion wiring, hides main feed when visible.
  - `frontend/src/api/simulation.js` (+12): `getDemographicBreakdown(simulationId, { refresh })` helper.

**Impact:** Slots into the analytics suite shipped Apr 17 (Quality Diagnostics PR #32, Interaction Network PR #33). Where Quality answers "was this simulation healthy?" and Network answers "who talked to whom?", Demographics answers "who *changed*, and who stayed?" — the population-level explanatory layer. This is the kind of cross-tab a social scientist would otherwise have to write in pandas; surfacing it as a one-click overlay makes the simulation a first-class research instrument.

### License Flip, Then Reverted

**Summary:** Aaron swapped the LICENSE from AGPL-3.0 → MIT at 21:00 UTC on Apr 17, then reverted the swap two minutes later at 21:02. Net effect on main: no license change (still AGPL-3.0).

**Commits:**
- `a97649b` — *Add MIT License* (author: Aaron Mars) — `LICENSE` modified (661 → 21 lines)
- `e4a6ee1` — *Revert "Add MIT License"* (author: Aaron Mars) — `LICENSE` modified back (21 → 661 lines)

**Impact:** Nothing shipped, but the pattern is worth noting — a brief, live experiment with a more permissive license, reconsidered in minutes. AGPL-3.0 remains the posture. For embed/integration conversations this week (the Widget PR #34 is literally shipping today), AGPL compatibility is what downstream integrators will evaluate against.

---

## aaronjmars/miroshark-aeon

### Self-Healing: Two Dedup Guards in One Day

**Summary:** Both of today's self-improve commits came from the same pathology: a skill being re-dispatched within the same UTC day and producing a duplicate output. Heartbeat auto-trigger, manual re-run, and cron retries all converge on the same failure mode, and the agent caught it in two different skills on the same day.

**Commits:**
- `3df3847` — *improve: add dedup guard to hyperstitions-ideas skill* (PR #17, branch `improve/hyperstitions-dedup`)
  - `skills/hyperstitions-ideas/SKILL.md` (+6 lines): Step 0 now scans today's log for an existing `## Hyperstitions Ideas` section. If found and `${var}` is empty, log `HYPERSTITIONS_SKIP` and stop. `${var}` explicit set overrides, for intentional operator-driven second ideas.
  - Triggered by today's own run: the skill fired twice — GitHub stars target (1,000 by Apr 30) and X followers target (1,000 by May 15) — diluting the coordination signal.

- `062f029` — *improve: add idempotency check to repo-pulse* (PR #18, branch `improve/repo-pulse-dedup`)
  - `skills/repo-pulse/SKILL.md` (+9 lines): before fetching counts, scan today's log for a prior `## Repo Pulse` entry for the same repo. If prior `stargazers_count` AND `forks_count` match fresh values, log `REPO_PULSE_DUPLICATE` and skip notification. If counts differ, continue normally.
  - Triggered by today's own run: repo-pulse ran twice with identical `stargazers_count=717 / forks_count=137`, sending identical notifications back-to-back. Same pattern showed up in push-recap on Apr 15 and Apr 17 — the idempotency pattern now propagated to repo-pulse.

**Impact:** The agent is converging on a consistent "scan today's log before acting" idempotency idiom across skills. Both patches are <10 lines, high-leverage: they eliminate a category of notification spam across every channel without touching the happy path. When heartbeat auto-dispatches a "missing" skill that actually already ran, the skill can now refuse to speak instead of duplicating.

### Daily Automation Activity

**Summary:** 35 `chore(...)` auto-commits on miroshark-aeon main today represent the normal daily cadence: every successful skill run produces an `auto-commit` (articles + logs + .outputs artifacts) followed by a `chore(cron): <skill> success` marker and scheduler state updates.

**Skills that ran today (by auto-commit signature):**
- token-report (06:41) — $MIROSHARK $0.000002095, -5.59% 24h, day 4 post-ATH consolidation
- fetch-tweets (06:46) — FETCH_TWEETS_NO_NEW (all candidates already in seen.txt or 3-day window)
- tweet-allocator (08:05 + 09:57) — TWEET_ALLOCATOR_EMPTY (no new tweets to score)
- repo-pulse (10:23 + 12:00) — the duplicate run that triggered PR #18
- hyperstitions-ideas (10:23 + 12:00) — 1,000 stars + 1,000 X followers (the duplicate that triggered PR #17)
- feature (11:16) — PR #34 Embeddable Widget
- feature (13:00) — PR #35 Demographic Breakdown
- repo-actions (14:15) — 5 new ideas generated
- self-improve (13:23 + 14:56) — produced PR #17 + PR #18 respectively

**Impact:** This is the agent behaving as designed — `feature` ships two autonomous PRs to MiroShark, `self-improve` patches two skills that misbehaved earlier in the day, and the housekeeping stays housekeeping (no hand-written code on main).

---

## Developer Notes

- **New dependencies:** None. All feature work reuses existing libs (Vue 3, Flask, SVG) and existing data sources (trajectory.json, reddit_profiles.json, twitter_profiles.csv).
- **New API surface:** Two new GET endpoints on MiroShark backend — `/<sim_id>/embed-summary` and `/<sim_id>/demographics`. Both cache under the simulation directory (`demographics.json`, and the existing `quality.json`/`network.json` are read by embed-summary for the badge payload).
- **New frontend routes:** `/embed/:simulationId` on MiroShark — iframe-safe, transparent body, no global chrome.
- **Breaking changes:** None. All additions.
- **Architecture shifts:**
  - MiroShark: analytics overlays now a family of four — Influence, Drift, Network (PR #33), Demographics (PR #35). Step3Simulation's toggle group is the central mutual-exclusion dispatcher.
  - miroshark-aeon: "scan today's log for a prior section before notifying" is emerging as the canonical idempotency idiom — now in repo-pulse, hyperstitions-ideas, and (earlier) push-recap.
- **Tech debt / follow-ups:** PR #34 and PR #35 are both unmerged as of this recap; the two self-improve PRs (#17, #18) are also unmerged. The analytics suite grows even before the merge wave catches up.
- **License posture:** AGPL-3.0 remains on MiroShark after the morning's 2-minute MIT experiment.

## What's Next

- **Merge wave:** PR #34 + #35 on MiroShark and PR #17 + #18 on miroshark-aeon all open; the skill-dedup patches should merge quickly given their small surface area.
- **Multi-Document Mode** was deferred twice this week from `repo-actions` (Apr 16, Apr 18) as a larger standalone effort — plausible candidate for the next `feature` run once the current two PRs land.
- **Dashboard rollout for PR #34:** once merged, worth embedding a simulation on the miroshark-aeon repo README or a landing page to exercise the new widget end-to-end — and to start the "Powered by MiroShark" surface area counter.
- **Idempotency sweep:** three skills now carry the same dedup idiom (push-recap, repo-pulse, hyperstitions-ideas). Token-report, tweet-allocator, and project-lens are next candidates — `self-improve` may catch these on the next duplicate incident.
- **Track Record bar:** with the embed widget exposing cached `resolution` and `quality` fields, a dashboard that aggregates those across simulations would be a natural companion piece.
