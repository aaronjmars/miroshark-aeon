# Skill Leaderboard — 2026-04-20

*1 active fork scanned (pushed in last 30 days)*

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

With one active fork (AITOBIAS04/miroshark-aeon, pushed 2026-04-20T18:13Z), every enabled skill is technically at 100%. The 14 skills form a stable core that hasn't changed from last week's baseline:

- **Market & social monitoring:** token-report, fetch-tweets, repo-pulse
- **Shipping intelligence:** push-recap, project-lens, repo-article, repo-actions
- **Autonomous building:** feature, self-improve
- **Weekly rhythm:** weekly-shiplog, hyperstitions-ideas
- **Housekeeping:** heartbeat, memory-flush
- **Meta-observability:** skill-leaderboard

The configuration lock is a signal of intent: the fork operator is running a production workload, not experimenting. Every scheduled slot is deliberate.

## Adoption Gaps

The source repo (aaronjmars/miroshark-aeon) has **15 enabled skills** vs the fork's 14. The one divergence:

**New in source, absent from fork:**
- **tweet-allocator** — added to source after the fork was configured; distributes $MIROSHARK token rewards to tweet authors. This is the only skill that requires configuring a wallet/spend allowance, which explains the deliberate omission — operators need to opt in with intent, not inherit it by default.

The broader pool of **86 disabled skills** in the source represents the full discoverability gap. High-interest zero-adoption categories (same as Apr 19 baseline):

- **Content & research:** article, rss-digest, paper-digest, research-brief, deep-research, hacker-news-digest, paper-pick, technical-explainer, digest
- **Social & publishing:** write-tweet, remix-tweets, reply-maker, agent-buzz, farcaster-digest, vibecoding-digest, tweet-roundup
- **Token & DeFi:** token-alert, token-movers, trending-coins, on-chain-monitor, defi-monitor, wallet-digest, monitor-polymarket, polymarket
- **GitHub ops:** issue-triage, pr-review, auto-merge, github-monitor, github-issues, github-trending, code-health, vuln-scanner
- **Fleet & meta:** fork-fleet, fleet-control, skill-health, self-review, skill-evals, skill-update-check, spawn-instance, cost-report

## Week-over-Week

First comparison against last week's baseline (2026-04-19):

- **Rank changes:** None — all 14 skills hold the same positions
- **New entries:** None
- **Dropouts:** None
- **Configuration drift:** Zero — the fork's aeon.yml is identical in enabled-skill composition to last week

The only change visible at the fleet level: the *source* repo added tweet-allocator between Apr 19 and Apr 20. No fork has picked it up yet, which establishes it as an immediate adoption gap watch item for next week.

One structural note: the fork was pushed at 18:13 UTC today — after this skill's scheduled 17:00 UTC run — which means the push captured the fork in a live-running state. The configuration itself didn't change; the timestamp update likely reflects automated commits from the fork's own Aeon instance.

## Fleet Summary

- **Active forks scanned:** 1 (of 1 total forks)
- **Total skill slots enabled (across all forks):** 14
- **Unique skills seen:** 14
- **Forks with no aeon.yml:** 0
- **Forks skipped (no aeon.yml or 404):** 0
- **Notification sent:** No — fleet below 2-fork threshold for notification

---
*Source: GitHub API — forks of aaronjmars/miroshark-aeon*
