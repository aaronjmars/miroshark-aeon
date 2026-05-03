# Skill Leaderboard — 2026-05-03

*1 active fork scanned (pushed in last 30 days) — 147 total active forks across all source repos*

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

With one active aeon-instance fork (AITOBIAS04/miroshark-aeon, pushed 2026-05-03T15:33Z), all 14 enabled skills are technically at 100% adoption. The configuration has held stable for two consecutive weekly runs (Apr 20 → May 3), which is a signal of operational maturity rather than stagnation.

The 14 skills divide into a clear hierarchy of cadence:

- **Daily market & social monitoring:** token-report, fetch-tweets, repo-pulse — the three skills that require fresh data every day to stay accurate
- **Daily shipping intelligence:** push-recap, feature — continuous output tied to the repo's daily commit velocity
- **Mon/Wed/Fri (fork-adjusted):** project-lens — the fork runs this on a tighter cadence than source (every day), suggesting the operator has load-balanced away from the source's daily run
- **Every-other-day:** repo-actions, repo-article, self-improve — skills with compounding output that don't need daily runs
- **Weekly:** weekly-shiplog (Mon), hyperstitions-ideas (Sat), skill-leaderboard (Sun) — the cadence is deliberate, not defaulted
- **Housekeeping:** heartbeat (daily), memory-flush (Sun+Wed) — the infrastructure that keeps the other 12 reliable

The unchanged configuration after two weeks means the fork operator has found a stable production configuration. No skill has been toggled in or out since the fork was first observed.

## Adoption Gaps

One enabled skill in the source repo is absent from the fleet:

**Present in source, absent from every fork:**
- **tweet-allocator** — distributes $MIROSHARK token rewards to tweet authors. Requires explicit opt-in: wallet configuration, spend allowance, and `BANKR_API_KEY` secret. The barrier is intentional — nobody should inherit a spending skill by default. Zero adoption across two consecutive weeks confirms the pattern.

The broader pool of disabled skills in the source (80+) represents the full discoverability surface. Zero-fork-adoption categories (same as Apr 20 baseline):

- **Content & research:** article, rss-digest, paper-digest, research-brief, deep-research, hacker-news-digest, paper-pick, technical-explainer, digest
- **Social & publishing:** write-tweet, remix-tweets, reply-maker, agent-buzz, farcaster-digest, vibecoding-digest, tweet-roundup
- **Token & DeFi:** token-alert, token-movers, trending-coins, on-chain-monitor, defi-monitor, wallet-digest, monitor-polymarket, polymarket
- **GitHub ops:** issue-triage, pr-review, auto-merge, github-monitor, github-issues, github-trending, code-health, vuln-scanner
- **Fleet & meta:** fork-fleet, fleet-control, skill-health, self-review, skill-evals, skill-update-check, spawn-instance, cost-report

## Week-over-Week

Comparing to 2026-04-20 (last leaderboard — 13 days ago):

- **Rank changes:** None — all 14 skills hold the same positions
- **New entries:** None
- **Dropouts:** None
- **Configuration drift:** Zero — the fork's enabled-skill set is identical

One structural change visible at the fleet level: the fork's `project-lens` schedule now runs Mon/Wed/Fri (`0 16 * * 1,3,5`) versus source's daily schedule. This is a cadence tuning, not an enable/disable toggle, so it doesn't affect the leaderboard counts.

The fleet has also grown substantially since the last run: 146 new active MiroShark forks pushed in the last 30 days (vs. essentially none two weeks ago), reflecting the crossover past 1,000 stars on May 3. These are all application forks — none contain `aeon.yml` — but the scale of the fork pool is notable. If even 1% of these forks evolve into running aeon instances, the fleet doubles.

## Fleet Summary

- **Source repos scanned:** aaronjmars/MiroShark, aaronjmars/miroshark-aeon
- **Active forks scanned:** 147 total (146 MiroShark application forks + 1 miroshark-aeon aeon-instance fork)
- **Forks with readable aeon.yml:** 1 (AITOBIAS04/miroshark-aeon)
- **Total skill slots enabled (across all aeon-instance forks):** 14
- **Unique skills seen:** 14
- **Forks with no aeon.yml:** 146 (all MiroShark forks — application repos by design)
- **Notification sent:** No — fleet below 2-fork threshold for notification

---
*Source: GitHub API — forks of aaronjmars/MiroShark, aaronjmars/miroshark-aeon*
