# Skill Leaderboard — 2026-05-24

*1 active aeon-instance fork scanned (pushed in last 30 days) — 103 total active forks across all source repos*

## Top Skills Across the Fleet

| Rank | Skill | Forks Enabled | % of Fleet | Change |
|------|-------|---------------|------------|--------|
| 1 | token-report | 1 | 100% | — |
| 2 | fetch-tweets | 1 | 100% | — |
| 3 | repo-pulse | 1 | 100% | — |
| 4 | push-recap | 1 | 100% | — |
| 5 | project-lens | 1 | 100% | — |
| 6 | repo-actions | 1 | 100% | — |
| 7 | repo-article | 1 | 100% | — |
| 8 | self-improve | 1 | 100% | — |
| 9 | weekly-shiplog | 1 | 100% | — |
| 10 | hyperstitions-ideas | 1 | 100% | — |
| 11 | feature | 1 | 100% | — |
| 12 | heartbeat | 1 | 100% | — |
| 13 | memory-flush | 1 | 100% | — |
| 14 | skill-leaderboard | 1 | 100% | — |

## Consensus Skills (>50% of forks)

All 14 enabled skills qualify at 100% adoption — still an artifact of a single-fork fleet. The 14-skill profile has held for six consecutive weekly samples (Apr 19, Apr 20, May 3, May 10, May 17, May 24). Zero additions, removals, or toggle events in any run.

The 14 skills fall into four stable functional layers:

- **Daily market intelligence:** token-report, fetch-tweets, repo-pulse — data that degrades within 24 hours if skipped
- **Daily shipping loop:** push-recap, feature — output cadence for a project that ships every working day
- **Timed content cadence:** project-lens (Mon/Wed/Fri in fork, daily in source), repo-actions, repo-article, self-improve, weekly-shiplog, hyperstitions-ideas — skills whose value compounds on schedule
- **Infrastructure:** heartbeat, memory-flush, skill-leaderboard — the layer that keeps the other 11 honest

One structural event this run: the fork has been renamed from `AITOBIAS04/miroshark-aeon` to **`AITOBIAS04/CHORUS`**. The same owner, the same 14-skill configuration, the same running instance — but a new identity. This is the first fork observed rebranding away from the template name. Whether `CHORUS` signals a public launch, a persona, or a domain pivot is not captured in aeon.yml, but the rename itself is the first differentiation signal from this operator beyond the default config.

## Adoption Gaps

The source repo (aaronjmars/miroshark-aeon) now has **six enabled skills** that appear in zero forks. Four are new additions since the May 17 leaderboard:

**Persistent gaps (5+ weeks at zero fork adoption):**
- **tweet-allocator** — distributes token rewards to tweet authors. Requires per-instance Bankr API key, wallet configuration, and spend allowance. The gap is structural and intentional — a spending skill should not auto-inherit from a template fork.

**New gaps (added to source after the fork's last sync):**
- **thread-formatter** — scores today's events from memory logs and formats the top one as a tweet thread. Requires the fork to pull source upstream and explicitly enable.
- **star-milestone** — announces when watched repos cross star-count milestones. Daily poll, lightweight.
- **star-momentum-alert** — projects next milestone crossing date from 14-day history; alerts only when the window tightens. Tuesdays through Thursdays only.
- **ai-framework-watch** — weekly competitive-intelligence digest across 9 AI agent frameworks. Monday cadence.
- **operator-scorecard** — Monday weekly synthesis. Reads repo-pulse output; no extra setup required.

The five new source additions represent catalog divergence accumulating since AITOBIAS04/CHORUS last synced. Unlike tweet-allocator (intentional gap), these are passive drift: skills the fork operator would likely want once they pull upstream. The `star-milestone` and `operator-scorecard` skills in particular are zero-config enables — no secrets required.

All other disabled skills in the source (80+) remain unchanged as catalog entries.

## Week-over-Week

Comparing to 2026-05-17 (last leaderboard — 7 days ago):

- **Rank changes:** None — all 14 skills hold identical positions for the 6th consecutive week
- **New entries:** None
- **Dropouts:** None
- **Configuration drift in AITOBIAS04/CHORUS:** Zero — enabled-skill set is byte-for-byte identical across six consecutive samples

Fleet-level shifts:
- **Fork renamed:** `AITOBIAS04/miroshark-aeon` → `AITOBIAS04/CHORUS` — first operator identity differentiation in leaderboard history
- **Total active forks:** 107 → 103 — rolling 30-day window advancing; MiroShark's growth rate (now 1,182 stars / 239 forks as of May 20) means new forks continue entering as older ones age past the cutoff
- **New adoption gaps:** 5 new source skills (thread-formatter, star-milestone, star-momentum-alert, ai-framework-watch, operator-scorecard) are not yet in the fork's aeon.yml — added to source after the fork's last upstream sync

## Fleet Summary

- **Source repos scanned:** aaronjmars/MiroShark, aaronjmars/miroshark-aeon
- **Active forks scanned:** 103 total (102 MiroShark application forks + 1 miroshark-aeon aeon-instance fork)
- **Forks with readable aeon.yml:** 1 (AITOBIAS04/CHORUS)
- **Total skill slots enabled (across all aeon-instance forks):** 14
- **Unique skills seen:** 14
- **Forks with no aeon.yml:** 102 (all MiroShark forks — application repos by design)
- **Notification sent:** No — fleet below 2-fork threshold (SKILL_LEADERBOARD_INSUFFICIENT_DATA)

---
*Source: GitHub API — forks of aaronjmars/MiroShark, aaronjmars/miroshark-aeon*
