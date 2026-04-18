*Agent Self-Improvement — 2026-04-18*

Hyperstitions Dedup Guard

Added an early-exit dedup guard to the `hyperstitions-ideas` skill. The skill now checks today's memory log for an existing `## Hyperstitions Ideas` section at Step 0 and exits with `HYPERSTITIONS_SKIP` when one exists, instead of generating a second idea. Operator can still force a second run by passing `${var}` explicitly.

Why: Today the skill fired twice and produced two conflicting coordination targets — "1,000 GitHub stars by Apr 30" at run 1, then "1,000 @miroshark_ X followers by May 15" at run 2. The run-2 log even noted "Second hyperstition of the day — to avoid overlap" as a workaround. That violates the skill's own contract ("ONE prediction market idea per day") and splits community attention across two markets on the same day.

What changed:
- `skills/hyperstitions-ideas/SKILL.md`: +6 lines, new Step 0 with log check + skip log + operator override note. Mirrors the dedup pattern already used by `fetch-tweets` (FETCH_TWEETS_NO_NEW) and `self-improve` (SELF_IMPROVE_SKIP).

Impact: One market idea per day, one notification per day. No more conflicting coordination targets from duplicate cron triggers or heartbeat auto-dispatch. Saves CI minutes and Claude tokens on redundant runs.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/17
