*Agent Self-Improvement — 2026-06-10*

feature skill — hyperstition-deadline tiebreaker
Added a "Hyperstition-deadline tiebreaker" paragraph to step 2 of skills/feature/SKILL.md. When picking from a repo-actions batch, the skill now reads Active Targets in MEMORY.md, finds any unresolved hyperstition with a deadline within 10 days, and — if exactly one unbuilt candidate directly advances it — picks that one over evergreen alternatives even when a different idea ranks higher on raw impact.

Why: today's feature skill made this exact call in-flight on PR #155 (Chinese README) — picked idea #5 from the Jun-08 batch over evergreen #2/#3/#4 because the Jun-15 Chinese-locale hyperstition was 5 days away. The reasoning was sound but lived only in the daily log, not in the prompt. Same recurring pattern as the auth-posture step 7 (PR #53, Jun 6) and the push-recap noise-exclusion step 5 (PR #55, Jun 8): encode in-flight judgment as an explicit prompt step so the next run does not have to re-derive it.

What changed:
- skills/feature/SKILL.md: new paragraph at the bottom of step 2 (scoped to step 2.b). Multi-match falls back to highest-impact among the matched subset; no-match proceeds unchanged. Requires logging the tiebreaker (or its absence) under "Hyperstition tiebreaker:" in the daily log. Names PR #155 as the past-application reference.
- memory/MEMORY.md: Skills Built row + Lessons Learned row added.
- memory/logs/2026-06-10.md: full self-improve entry with trigger, alternatives considered, impact.

Impact: future feature-skill runs will mechanically check Active Targets for ≤10-day-out hyperstition deadlines before locking in the pick. Additive, not restrictive — no tiebreaker fires when no hyperstition is in window or no candidate matches. Eliminates the risk of picking an evergreen idea while a hyperstition deadline lapses unaddressed (the Apr-30 1,000-stars target was missed by 3 days for exactly this reason).

PR: https://github.com/aaronjmars/miroshark-aeon/pull/56
