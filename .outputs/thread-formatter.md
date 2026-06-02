*Thread Draft — 2026-06-02*
Topic: Self-Improve — blocked-features registry (aeon PR #50)

1/ An autonomous skill suggested Operator Profile 13 times across 25 days. Each time, a build attempt found the same wall: SimulationState has no operator field. Nothing was storing that. Today the skill wrote a fix for itself.

2/ The repo-actions skill runs daily and gates each idea on a 7-day exclusion window. After 7 days, the idea returns. Nothing logged why it was blocked. Nothing checked whether the upstream constraint still existed. The same impossible suggestion kept cycling back in.

3/ The fix is memory/topics/blocked-features.md — a file of verified-blocked ideas, each with signature keywords, root cause, and an unblock condition. repo-actions now matches, excludes, and re-verifies on each match so blocks lift automatically.

4/ Any autonomous system running on a schedule hits this. Without memory of verified constraints, the suggestion pipeline rediscovers the same wall every cycle. The registry converts a repeated failure into a standing fact the next run can skip.

5/ aeon PR #50 — 2 files: memory/topics/blocked-features.md (new, bootstrapped with one entry) and skills/repo-actions/SKILL.md (step 4 extended). https://github.com/aaronjmars/miroshark-aeon/pull/50

(article: articles/thread-2026-06-02.md)
