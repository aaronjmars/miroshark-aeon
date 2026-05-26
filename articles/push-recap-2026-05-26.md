# Push Recap — 2026-05-26

## Overview
Three substantive merges landed across the two watched repos in the last 24 hours: a new community-authored ecosystem registry, a new analytics surface, and an agent self-fix. The thrust was **legibility from two directions** — MiroShark made its integrator base visible (ECOSYSTEM.md) and its belief data machine-readable (peak-round analytics), while the Aeon agent patched a crash that had silently broken its own tweet-payout pipeline. Notably, one of the three merges came from an external contributor.

**Stats:** 12 files changed, +893 / -4 lines across 3 substantive commits (2 repos, 3 distinct authors). The miroshark-aeon repo had ~38 additional commits in-window, all scheduler/skill auto-commits (`chore(cron)` / `auto-commit`) — excluded as noise.

---

## aaronjmars/MiroShark

### Ecosystem Registry — First Formal Integrator Index (external)
**Summary:** A new top-level `ECOSYSTEM.md` page now lists the projects, agents, and products built on top of MiroShark, with guidelines for adding new entries. This is the first time the integrator network has a canonical, curated home in the repo itself rather than living only in scattered tweets and logs.

**Commits:**
- `5917e73` — Add ECOSYSTEM.md (#109) — **by NurstarK (external contributor)**
  - New file `ECOSYSTEM.md` (+41 lines): centered logo header, a "Building on MiroShark" table of 10 named projects — AntFleet, Blue Agent, Crucible Sim, Echo, Monitor, Nookplot, RootAI, Signa, Supercompact, Xerg — each with X handle and/or repo/site link.
  - Includes an "Add your project" section with PR guidelines: public self-identification as MiroShark-built, one alphabetized row per project, at least an X handle or public link, and an explicit exclusion of stock forks that merely re-run the engine.

**Impact:** Turns the loose collection of ecosystem mentions into a maintained registry with a clear contribution path. It is also the merge mechanism itself that matters — a fork-owner (NurstarK appears in today's repo-pulse fork list) opened and landed the PR, making this the latest in the project's run of external contributions. The "no stock forks" rule keeps the list signal-heavy (products/integrations, not mirrors).

### New Surface: Peak-Round Belief Analytics
**Summary:** A new published-only endpoint, `GET /api/simulation/<id>/peak-round`, collapses a simulation's entire belief trajectory into a single machine-readable inflection summary — which round each stance peaked, the most volatile round, the largest round-over-round swing, and the total round count. It is the analytical counterpart to the existing `trajectory.csv` (raw rows) and `chart.svg` (the visual).

**Commits:**
- `d1756a5` — feat: peak-round belief analytics (#108) — by @aaronjmars / aeon
  - New file `backend/app/services/peak_round.py` (+187 lines): `load_trajectory_rounds()` projects `trajectory.json` snapshots into a per-round stance-split list (skips malformed rows, sorts ascending by round), and `compute_peak_rounds()` does one O(n) pass tracking each stance's earliest max and the round with the largest summed `|Δbullish|+|Δneutral|+|Δbearish|`. Pure stdlib; reuses `trajectory_export.compute_stance_split` (±0.2 threshold) so peaks match `trajectory.csv` byte-for-byte. Ties resolve to the earliest round (strict `>`); empty input returns `None` so the route can emit a clean 404.
  - Changed `backend/app/api/simulation.py` (+85 lines): publish-gated route mirroring the `signal.json` handler — 403 if not published, 404 if no trajectory data yet (lets a consumer tell "not ready" from "private"), pretty-printed sorted-key JSON, 5-minute cache, and a `peak_round` surface-stat increment.
  - Changed `backend/app/services/surface_stats.py` (+3/-1) and `backend/tests/test_unit_surface_stats.py` (+2): registers the new `peak_round` surface key.
  - Changed `backend/openapi.yaml` (+118 lines): `/peak-round` path plus `PeakRoundResponse` / `StancePeak` schemas.
  - New file `backend/tests/test_unit_peak_round.py` (+231 lines): 19 offline tests plus wiring guards.
  - Changed `frontend/src/api/simulation.js` (+46) and `frontend/src/components/EmbedDialog.vue` (+139 lines): `getPeakRound`/`getPeakRoundUrl` helpers and a 📊 "Peak beliefs" section in the embed dialog.
  - Changed `docs/API.md` (+1) and `docs/FEATURES.md` (+32): documents the surface under Analytics / Features.

**Impact:** Adds *shape* on top of existing data without new computation or dependencies — a quant tool or research script can read "bullish peaked at 71% on round 4, most volatile round was 7" in one request instead of parsing 100 trajectory rows. The schema is versioned (`schema_version: "1"`) and the determinism rules (first-occurrence peaks, two-decimal rounding to avoid swallowing small swings) are documented, so downstream consumers can rely on stable output. Zero new dependencies.

---

## aaronjmars/miroshark-aeon

### Agent Self-Hardening: bankr-prefetch Crash Guard
**Summary:** Fixed a latent crash in the tweet-payout prefetch script that fired on any day with no candidate tweets — including today, where it had already broken the tweet-allocator pipeline.

**Commits:**
- `68c2066` — improve: stop bankr-prefetch crashing on tweetless days (#46) — by @aaronjmars / aeon
  - Changed `scripts/prefetch-bankr.sh` (+8 / -3): appended `|| true` to the three handle-collection command substitutions (`.xai-cache` handle scan, `memory/logs` x.com-URL scan, and the reserved-path/project-account filter). Added a comment documenting the gotcha.
  - The bug: under `set -euo pipefail`, a `grep` that matches nothing exits 1, `pipefail` propagates it through the pipeline, and `set -e` kills the script *before* it reaches the graceful "no-candidates" branch. With no x.com URLs in today's log (fetch-tweets had no handles to surface), the script crashed with exit 1 and stamped a false `"crashed"` status.

**Impact:** Directly resolves the cause of today's `TWEET_ALLOCATOR_EMPTY` + "Bankr prefetch crashed (exit_code=1)" failure logged at the start of the day. A tweetless day now falls through to the intended `no-candidates` status instead of looking like a misconfiguration. This complements the earlier PR #45 EXIT-trap sidecar, which correctly *detected* the crash but couldn't prevent it — #46 removes the crash itself.

---

## Developer Notes
- **New dependencies:** None. Both MiroShark changes (#108, #109) and the aeon fix (#46) are zero-dependency — the post-Nemotron zero-deps streak continues.
- **Breaking changes:** None. `peak_round` is a new additive surface key (now the 22nd); the prefetch fix only adds `|| true` guards and a comment.
- **Architecture shifts:** Peak-round follows the established surface pattern exactly (publish gate → service module → surface-stat increment → openapi → tests → EmbedDialog), so the surface inventory grows without new structure. ECOSYSTEM.md introduces a new *governance* artifact (a contribution-gated registry) rather than code.
- **Tech debt:** The peak-round PR note (carried from the build log) flags that pytest could not be run in the sandbox (python not allowlisted) and the frontend was not browser-tested — both rely on CI for validation. The prefetch fix could not be `bash -n`-checked in-sandbox; it rests on deterministic bash semantics and the next prefetch run will confirm it.

## What's Next
- **Open MiroShark PR:** #106 (Railway deployment prep, external author DYAI2025) remains the only open PR — a likely next merge candidate.
- **May-24 idea batch:** with Peak-Round (#108) and oEmbed (#107) now shipped, the unbuilt items are Operator Profile, Agent Persona Export JSON, and Simulation Search JSON API.
- **Today's repo-actions queue:** Per-Agent Stance Sparklines, CN+JP README, Scenario Clone Button, Webhook Event Filtering, and an Ecosystem JSON Registry API — the last is a natural machine-readable companion to the new ECOSYSTEM.md just merged.
- **Pipeline check:** the next bankr-prefetch run should now report `no-candidates` cleanly on a tweetless day; worth confirming tomorrow that tweet-allocator no longer goes EMPTY for the wrong reason.
