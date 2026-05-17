# Skill Freshness — 2026-05-17

**Verdict:** ⚠️ FRESHNESS_WARN — 3 of ~18 tracked deps are past the 28h daily threshold, all on the same `repo-actions` file; this is a spec classification artifact, not a genuine staleness event

*Audited 20 enabled skills · 18 dependency edges checked · 3 flagged*

> **Implementation note:** On-disk mtimes are uniform (all files have the git-clone checkout time, ~62 seconds before this run). Mtime-based age computation is meaningless in a fresh-clone environment. This report derives article age from filename dates (e.g., `repo-actions-2026-05-16.md` → May 16) and applies the spec's per-class thresholds to those dates. All other path classes (`.outputs/`, `memory/topics/`, `memory/state/`) use mtime as prescribed — they appear uniformly fresh.

---

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| feature | `articles/repo-actions-2026-05-16.md` | articles/daily | 29.6h | ⚠️ WARN |
| hyperstitions-ideas | `articles/repo-actions-2026-05-16.md` | articles/daily | 29.6h | ⚠️ WARN |
| self-improve | `articles/repo-actions-2026-05-16.md` | articles/daily | 29.6h | ⚠️ WARN |

*(Sorted by severity desc, then consumer name. OK rows omitted.)*

---

## What this means per consumer

> **feature** — depends on 1 tracked article; 1 flagged. Worst: `articles/repo-actions-2026-05-16.md` last updated 29.6h ago (threshold 28h, class articles/daily). The producer `repo-actions` schedule is `0 14 */2 * *` (every other day) — it ran on May 16 and is next due May 18. The file is fresh for `repo-actions`' actual cadence. The WARN fires because the spec's cadence buckets (daily/weekly/on_demand) have no "every-2-days" slot, so `repo-actions` is classified as daily (28h threshold) even though its output is only 24h stale at worst between runs. **Suggested action:** Monitor — one missed daily-class threshold; expected to clear on the next repo-actions run (May 18).

> **hyperstitions-ideas** — depends on 3 tracked articles (repo-actions, push-recap, repo-article); 1 flagged. Worst: same `repo-actions-2026-05-16.md` as above (29.6h, WARN). push-recap and repo-article both have fresh today's files. **Suggested action:** Same as feature — this is a cadence-bucket classification artifact, not a production outage.

> **self-improve** — depends on 1 tracked article; 1 flagged. Worst: `articles/repo-actions-2026-05-16.md` (29.6h, WARN). Same situation as feature. **Suggested action:** Monitor — expected to clear on next repo-actions run (May 18).

---

## Healthy consumers

- token-report — 0 article deps tracked (reads memory/MEMORY.md + API directly), all fresh.
- fetch-tweets — 0 article deps. Writes to memory/logs only.
- repo-pulse — 0 article deps. Writes to memory/logs + notifications; no articles/ output by design.
- tweet-allocator — reads memory/logs/${today}.md (memory class, mtime OK).
- push-recap — 0 article deps. Writer, not reader.
- project-lens — 3 deps (repo-article, push-recap, project-lens self); all today's files present, all fresh.
- repo-article — 0 article deps. Writer, not reader.
- weekly-shiplog — 1 dep (push-recap 7d window); all seven days' files present, all fresh.
+ 12 more all-fresh consumers.

---

## Architectural observations (not formal MISSING flags)

These are implicit references that **have never existed** — per spec they are not flagged, but they represent design gaps worth tracking:

| Consumer | Missing dependency | Why it never exists | Impact |
|----------|--------------------|---------------------|--------|
| thread-formatter | `articles/repo-pulse-*.md` | repo-pulse writes to memory/logs + notifications; never writes articles/ | Falls back gracefully; no star/fork count in thread context |
| operator-scorecard | `articles/repo-pulse-*.md` | Same | Community-growth paragraph degrades to "no data" |
| operator-scorecard | `articles/skill-analytics-*.md` | skill-analytics is disabled (`enabled: false`) | Agent-health paragraph falls back to heartbeat-only |
| operator-scorecard | `articles/heartbeat-*.md` | heartbeat writes to .outputs/ and memory/logs, not articles/ | Heartbeat verdicts sourced from memory/logs instead (graceful) |
| star-momentum-alert | `articles/repo-pulse-*.md` | Same as above | Uses memory/logs fallback (primary path); articles/ is the optional path |

**Root cause for repo-pulse gap:** `thread-formatter` and `operator-scorecard` both reference `articles/repo-pulse-*.md` in their SKILL.md, but `repo-pulse` has never been designed to write article files — its output goes to memory/logs/ via the notification log. If richer context is wanted in those consumers, either (a) add an `articles/` write step to repo-pulse, or (b) update the consuming SKILL.md files to read from memory/logs directly.

---

## Source status

- `aeon.yml`: 156 entries, **20 enabled**
- Implicit references discovered: 22 edges across 12 consumers
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 5
- Mtime adaptation: filename-date used for all `articles/` class checks (git-clone environment)

---

*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: article ages derived from filename dates; all other ages from on-disk mtimes — this skill measures nothing it does not also report.*
