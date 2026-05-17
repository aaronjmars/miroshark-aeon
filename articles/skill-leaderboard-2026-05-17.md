# Skill Leaderboard — 2026-05-17

*1 active aeon-instance fork scanned (pushed in last 30 days) — 107 total active forks across all source repos*

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

All 14 enabled skills qualify at 100% adoption — still an artifact of a single-fork fleet, not a measure of broad consensus. AITOBIAS04/miroshark-aeon has held this exact 14-skill profile for five consecutive weekly samples (Apr 20, May 3, May 10, and now May 17 — Apr 19 predates the current AITOBIAS04 stable set). Zero additions, removals, or toggle events in any run.

The 14 skills continue to fall into four functional layers:

- **Daily market intelligence:** token-report, fetch-tweets, repo-pulse — data that degrades within 24 hours if skipped
- **Daily shipping loop:** push-recap, feature — the output of a project that ships every working day
- **Timed content cadence:** project-lens (Mon/Wed/Fri), repo-actions (every 2 days), repo-article (off-days from project-lens), self-improve (every 2 days), weekly-shiplog (Monday), hyperstitions-ideas (Saturday) — skills whose value compounds on schedule, not as daily noise
- **Infrastructure:** heartbeat (daily), memory-flush (Sun+Wed), skill-leaderboard (Sunday) — the layer that keeps the other 11 honest

One observation this run: AITOBIAS04's fork pushed at 2026-05-17T15:39:37Z — approximately 90 minutes before this leaderboard ran. The fork is active on today's Sunday schedule, reading the same leaderboard it will appear in. The mutual observation has now recurred across four consecutive Sunday runs.

## Adoption Gaps

The source repo (aaronjmars/miroshark-aeon) has one enabled skill that appears in zero forks:

**tweet-allocator** — distributes $MIROSHARK token rewards to tweet authors. Requires per-instance setup: Bankr API key, wallet configuration, spend allowance. The gap is structural and intentional — a spending skill should not auto-inherit from a template fork. Four consecutive weekly leaderboards (Apr 20, May 3, May 10, May 17) confirm zero fork adoption, which is the expected outcome.

All other disabled skills in the source (80+) represent the full available catalog — unchanged categories from prior runs:

- **Content & research:** article, rss-digest, paper-digest, research-brief, deep-research, hacker-news-digest, paper-pick, technical-explainer, digest, search-papers
- **Social & publishing:** write-tweet, remix-tweets, reply-maker, agent-buzz, farcaster-digest, vibecoding-digest, tweet-roundup
- **Token & DeFi:** token-alert, token-movers, trending-coins, on-chain-monitor, defi-monitor, wallet-digest, monitor-polymarket, polymarket
- **GitHub ops:** issue-triage, pr-review, auto-merge, github-monitor, github-issues, github-trending, code-health, vuln-scanner
- **Fleet & meta:** fork-fleet, fleet-control, skill-health, self-review, skill-evals, skill-update-check, spawn-instance, cost-report

## Week-over-Week

Comparing to 2026-05-10 (last leaderboard — 7 days ago):

- **Rank changes:** None — all 14 skills hold identical positions for the 5th consecutive week
- **New entries:** None
- **Dropouts:** None
- **Configuration drift in AITOBIAS04:** Zero — enabled-skill set is byte-for-byte identical across five consecutive samples (Apr 20 → May 17)

One fleet-level shift: **total active forks dropped from 117 to 107**. This is not churn — it is the 30-day rolling window advancing. Forks that were active between April 10–17 have now aged past the cutoff. MiroShark's underlying pool continues growing (1,143 stars / 226 forks on May 13 → 1,166 stars / 235 forks on May 17), so active forking activity is healthy; the filter is simply more selective as older forks settle.

The source repo gained one new enabled skill since the last leaderboard: `auto-merge-agent-prs` (auto-merges green agent-authored PRs, disabled) is present in source but not yet reflected in AITOBIAS04's fork. It is disabled in the source as well, so it does not create a new adoption gap, but it marks the source is diverging slightly in catalog breadth ahead of the fork.

## Fleet Summary

- **Source repos scanned:** aaronjmars/MiroShark, aaronjmars/miroshark-aeon
- **Active forks scanned:** 107 total (106 MiroShark application forks + 1 miroshark-aeon aeon-instance fork)
- **Forks with readable aeon.yml:** 1 (AITOBIAS04/miroshark-aeon)
- **Total skill slots enabled (across all aeon-instance forks):** 14
- **Unique skills seen:** 14
- **Forks with no aeon.yml:** 106 (all MiroShark forks — application repos by design)
- **Notification sent:** No — fleet below 2-fork threshold (SKILL_LEADERBOARD_INSUFFICIENT_DATA)

---
*Source: GitHub API — forks of aaronjmars/MiroShark, aaronjmars/miroshark-aeon*
