# Skill Leaderboard — 2026-05-10

*1 active aeon-instance fork scanned (pushed in last 30 days) — 117 total active forks across all source repos*

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

All 14 enabled skills qualify at 100% adoption — an artifact of the single-fork fleet, not a measurement of broad consensus. Still, the configuration itself is instructive. AITOBIAS04/miroshark-aeon runs the same 14-skill profile it has held since at least April 20 (three consecutive leaderboard samples), with zero additions, removals, or enable/disable toggles.

The 14 skills break into four functional layers:

- **Daily market intelligence:** token-report, fetch-tweets, repo-pulse — data that degrades within 24 hours if skipped
- **Daily shipping loop:** push-recap, feature — the output of a project that ships every working day
- **Timed content cadence:** project-lens (Mon/Wed/Fri), repo-actions and repo-article (every 2 days), self-improve (every 2 days), weekly-shiplog (Monday), hyperstitions-ideas (Saturday) — skills whose value compounds on a deliberate schedule, not daily noise
- **Infrastructure:** heartbeat (daily), memory-flush (Sun+Wed), skill-leaderboard (Sunday) — the layer that keeps the other 11 honest

One incidental signal from today's run: AITOBIAS04's fork shows `pushed_at: 2026-05-10T17:16:34Z` — meaning the fork itself ran skills at 17:00 UTC this afternoon (its own skill-leaderboard schedule is `0 17 * * 0`, Sundays). This leaderboard is running at the same cadence as its subject. Both this instance and the fork are scanning each other on the same Sunday clock.

## Adoption Gaps

The source repo (aaronjmars/miroshark-aeon) has one skill enabled that does not appear in any fork:

**tweet-allocator** — distributes $MIROSHARK token rewards to tweet authors. Requires explicit per-instance setup: Bankr API key, wallet configuration, spend allowance. The barrier is structural and intentional — a spending skill should never auto-inherit from a fork. Three consecutive weekly leaderboards (Apr 20, May 3, May 10) confirm zero fork adoption, which is the expected and correct outcome.

All other disabled skills in the source (80+) represent the full available catalog. Zero-fork-adoption categories (unchanged from prior runs):

- **Content & research:** article, rss-digest, paper-digest, research-brief, deep-research, hacker-news-digest, paper-pick, technical-explainer, digest, search-papers
- **Social & publishing:** write-tweet, remix-tweets, reply-maker, agent-buzz, farcaster-digest, vibecoding-digest, tweet-roundup
- **Token & DeFi:** token-alert, token-movers, trending-coins, on-chain-monitor, defi-monitor, wallet-digest, monitor-polymarket, polymarket
- **GitHub ops:** issue-triage, pr-review, auto-merge, github-monitor, github-issues, github-trending, code-health, vuln-scanner
- **Fleet & meta:** fork-fleet, fleet-control, skill-health, self-review, skill-evals, skill-update-check, spawn-instance, cost-report

## Week-over-Week

Comparing to 2026-05-03 (last leaderboard — 7 days ago):

- **Rank changes:** None — all 14 skills hold identical positions
- **New entries:** None
- **Dropouts:** None
- **Configuration drift:** Zero — AITOBIAS04's enabled-skill set is byte-for-byte identical across three consecutive weekly samples (Apr 20, May 3, May 10)

One structural shift at the fleet level: **total active forks dropped from 147 to 117**. This is not churn — it is the 30-day rolling window moving forward. Forks that were active between April 3–10 (when the May 3 window opened) have now aged past the cutoff. The underlying pool of MiroShark application forks continues to grow (1,127 stars / 224 forks on May 10 vs. 1,098 stars / 219 forks on May 6), but the 30-day active-push filter naturally narrows as older forks go quiet after the initial fork event.

The count of aeon-instance forks with a readable `aeon.yml` remains 1 — unchanged since the first leaderboard run on April 19.

## Fleet Summary

- **Source repos scanned:** aaronjmars/MiroShark, aaronjmars/miroshark-aeon
- **Active forks scanned:** 117 total (116 MiroShark application forks + 1 miroshark-aeon aeon-instance fork)
- **Forks with readable aeon.yml:** 1 (AITOBIAS04/miroshark-aeon)
- **Total skill slots enabled (across all aeon-instance forks):** 14
- **Unique skills seen:** 14
- **Forks with no aeon.yml:** 116 (all MiroShark forks — application repos by design)
- **Notification sent:** No — fleet below 2-fork threshold for notification (SKILL_LEADERBOARD_INSUFFICIENT_DATA)

---
*Source: GitHub API — forks of aaronjmars/MiroShark, aaronjmars/miroshark-aeon*
