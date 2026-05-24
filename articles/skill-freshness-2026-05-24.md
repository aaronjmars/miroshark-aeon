# Skill Freshness — 2026-05-24

**Verdict:** 🔴 FRESHNESS_STALE — tweet-allocator has not produced since 2026-05-17 (7 days); operator-scorecard will read a week-old reward ledger on its next Monday run

*Audited 20 enabled skills · 15 dependencies checked · 1 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| operator-scorecard | `articles/tweet-allocator-2026-05-17.md` | articles/daily-producer | 168h (7 days) | 🔴 STALE |

*(Sorted by severity desc. OK rows omitted — 14 deps are fresh.)*

## What this means per consumer

> **operator-scorecard** — depends on 5 files; 1 flagged. Worst: `articles/tweet-allocator-2026-05-17.md` last updated 168h ago (threshold 28h, class daily-article). The producer `tweet-allocator` runs at `0 8 * * *`; it has produced no article since 2026-05-17 — 7 consecutive skipped daily runs. operator-scorecard is a weekly skill (Monday 10:30 UTC); when it next runs on 2026-05-25, it will read last week's reward ledger for $AEON distributed totals and recipient counts, silently understating activity from May 18–24. Suggested action: verify `tweet-allocator` is still on schedule; if so, the producer ran but did not write a new article.

## Healthy consumers

- token-report — 0 external deps, self-sufficient.
- fetch-tweets — 0 external deps, self-sufficient.
- repo-pulse — 0 external deps, self-sufficient.
- push-recap — 0 external deps, self-sufficient.
- project-lens — 0 external deps, self-sufficient.
- repo-actions — 0 external deps, self-sufficient.
- repo-article — 0 external deps, self-sufficient.
- weekly-shiplog — 1 dep (`push-recap`), fresh (2026-05-24, 0h old).
- feature — 1 dep (`repo-actions`), fresh (2026-05-24, 0h old).
- self-improve — 1 dep (`repo-actions`), fresh (2026-05-24, 0h old).
- thread-formatter — 2 deps (`repo-pulse`, `token-report`), all fresh (2026-05-24).
- star-momentum-alert — 1 dep (`repo-pulse`), fresh (2026-05-24).
- star-milestone — 1 dep (`memory/topics/milestones.md`), within 7d topic threshold.
- hyperstitions-ideas — 3 deps (`push-recap`, `repo-article`, `repo-actions`), all fresh.

+ 6 more all-fresh consumers (heartbeat, memory-flush, skill-leaderboard, ai-framework-watch, weekly-shiplog counted above, operator-scorecard flagged above).

## Source status

- `aeon.yml`: 77 entries, 20 enabled
- Implicit references discovered: 15 (consumer:dep pairs after filtering self-references)
- Explicit `chains: consume:` edges: 0 (all chains are commented out)
- Files not yet on disk (skipped — implicit refs that never existed or disabled producers): 4 (`articles/heartbeat-*.md` never produced; `articles/skill-analytics-*.md`, `articles/distribute-tokens-*.md`, `articles/fork-contributor-leaderboard-*.md` — producers disabled)

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk filename dates (GitHub Actions git checkout sets uniform mtime; filename suffix is the authoritative freshness signal). This skill measures nothing it does not also report.*
