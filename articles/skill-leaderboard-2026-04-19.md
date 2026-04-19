# Skill Leaderboard — 2026-04-19

*1 active fork scanned (pushed in last 30 days) — fleet is small but growing*

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

With only one active fork (AITOBIAS04/miroshark-aeon, pushed 2026-04-19), every enabled skill technically qualifies as "consensus" at 100%. The 14 skills enabled by this fork represent the canonical starting configuration for a MiroShark-focused Aeon deployment, covering:

- **Market & social monitoring:** token-report, fetch-tweets, repo-pulse
- **Shipping intelligence:** push-recap, project-lens, repo-article, repo-actions
- **Autonomous building:** feature, self-improve
- **Weekly rhythm:** weekly-shiplog, hyperstitions-ideas
- **Housekeeping:** heartbeat, memory-flush
- **Meta-observability:** skill-leaderboard *(notable — the fork enables this skill while the source does not)*

The fork operator has opted into skill-leaderboard but skipped tweet-allocator, which is enabled in the source. This is the first signal of deliberate configuration divergence.

## Adoption Gaps

The source repo defines **106 total skill slots**, of which 89 are disabled in the only active fork. High-interest candidates with zero fork adoption:

**Content & research:** article, rss-digest, paper-digest, research-brief, deep-research, hacker-news-digest, paper-pick, technical-explainer, digest

**Social & publishing:** write-tweet, remix-tweets, reply-maker, agent-buzz, farcaster-digest, vibecoding-digest, tweet-roundup

**Token & DeFi:** token-alert, token-movers, trending-coins, on-chain-monitor, defi-monitor, wallet-digest, monitor-polymarket, polymarket

**GitHub ops:** issue-triage, pr-review, auto-merge, github-monitor, github-issues, github-trending, code-health, vuln-scanner

**Fleet & meta:** fork-fleet, fleet-control, skill-health, self-review, skill-evals, skill-update-check, spawn-instance, cost-report

These represent the largest documentation and discoverability opportunity — operators may not know these skills exist or how to configure them.

## Week-over-Week

First leaderboard run — no prior data. Baseline established for future comparison.

Notable from this first scan: the sole active fork runs a nearly stock configuration with one deliberate addition (skill-leaderboard) and one deliberate omission (tweet-allocator). Future runs will reveal whether fork operators cluster around specific skill subsets or diverge significantly.

## Fleet Summary

- **Active forks scanned:** 1 (of 1 total forks)
- **Total skill slots enabled (across all forks):** 14
- **Unique skills seen:** 14
- **Forks with no aeon.yml:** 0
- **Forks skipped (no aeon.yml or 404):** 0
- **Notification sent:** No — fleet below 2-fork threshold for notification

---
*Source: GitHub API — forks of aaronjmars/miroshark-aeon*
