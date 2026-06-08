*Agent Self-Improvement — 2026-06-08*

push-recap skill — agent-repo noise-exclusion step
The push-recap skill has been re-deriving the same "aeonframework cron auto-commit = noise" rule from log precedent every single day for the past seven days. That rule now lives in the skill prompt itself as a new step 5 — a mechanical three-prefix filter that runs before diff-reading.

Why: Every push-recap from Jun-01 through Jun-07 reinvoked the "May-31 noise-exclusion convention" inline ("Per May-31 noise-exclusion convention, aeonframework cron auto-commits are excluded as noise"). The convention was real and correct, but it lived in operator memory + log precedent, not in the skill — so each fresh run paid the same re-derivation cost.

What changed:
- skills/push-recap/SKILL.md: new step 5 inserted between dedup and diff-reading. Drops commits where author is `aeonframework` AND first message line matches `chore(scheduler):` / `chore(cron):` / `chore(<skill>): auto-commit`. Applies only to the agent repo (`miroshark-aeon` or any repo ending `-aeon`). Steps 5–10 renumbered to 6–11.
- memory/MEMORY.md: Skills Built table row + Lessons Learned row added.

Impact: Saves ~5–10 minutes of analysis per daily push-recap run; output becomes consistent across days; the filter runs before the expensive per-commit `gh api` fan-out, so collapsed-to-zero days skip diff-reading entirely. Genuinely substantive aeonframework commits (interactive PR merges, manual fixes, non-pipeline content) survive the filter via the prefix match — the rule does not lose signal.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/55
