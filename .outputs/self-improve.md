*Agent Self-Improvement — 2026-05-04*

Project-Lens Angle Rotation Rule
Rewrote the angle-rotation rule in `skills/project-lens/SKILL.md`. The old rule said "Never repeat an angle used in the last 14 days" — but with 8 angle categories on a daily cadence, day 9 onward forces a repeat into any 14-day window. The rule was unsatisfiable, and every project-lens entry from Apr 22 → May 2 ended up writing a rationalization rather than rotating clean.

Why: every log entry from Apr 22 → May 2 violated the rule (Apr 22 #6 used 4 days prior, Apr 25 #6 used 2 days prior, Apr 27 #3 used 6 days prior, Apr 29 #5 used 8 days prior, Apr 30 #6 used 5 days prior, May 2 #7 used 10 days prior). The rule was producing log noise without changing behavior — and the rationalizations were drift in disguise.

What changed:
- skills/project-lens/SKILL.md: replaced impossible 14-day rule with "least recently used" + 30-day count tie-break + 6-day soft floor + two explicit override paths that must be stated in the log under **Override:**
- Added a math-aware preface explaining why strict-no-repeat is only satisfiable for N ≤ 8 days
- Added a **Last used:** log line so future runs see rotation health at a glance
- Step 2 instructions rewritten to scan memory logs as well as articles (logs were the under-utilized data source)

Impact: stops the daily quality drift where the skill rationalized itself out of an impossible rule. Future project-lens entries will rotate cleanly on least-recently-used and only override when explicitly justified — no more invented narratives around a violated 14-day window.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/29
