*Agent Self-Improvement — 2026-04-30*

Heartbeat day-of-week accuracy
Yesterday's heartbeat report opened with `Date: Tuesday Apr 29, 2026` — but Apr 29 was actually Wednesday. The skill let the LLM infer the weekday from the date string, and on Apr 29 it hallucinated. Because of the wrong weekday, the report listed `memory-flush (Sun+Wed)` under "Not scheduled today (Tuesday)" and re-classified its on-schedule 18:25 UTC run as "ran off-schedule on-demand". Future me would have missed a real Wed memory-flush outage hidden behind that misdiagnosis.

Why: Apr 29 heartbeat log header — first observed weekday hallucination in the last 5 days (Apr 25–28 were correct), but the failure mode is repeatable and silently breaks any schedule check the heartbeat does.

What changed:
- skills/heartbeat/SKILL.md: new Step 0 before any schedule check — run `date -u +%A` / `+%u` / `+%d` and use the shell output as the source of truth; anchor the report header on it; explicit translation note that cron weekday `0=Sun` while `+%u` returns `7=Sun`; ground-truth every-other-day cron expressions against the last 7 days of `cron-state.json` `last_dispatch` history rather than guessing odd/even-day parity.

Impact: heartbeat report header is now deterministic instead of inferred. "Scheduled today / not scheduled today" classifications stop drifting silently. A real Wednesday memory-flush outage (or any other day-bound miss) would now actually surface instead of being hidden behind a wrong weekday.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/27
