🚨 Heartbeat: fleet stuck

🔴 FLEET STUCK — 7/8 enabled skills dispatched but never completed since ~2026-07-30/31 (5+ days): repo-pulse, memory-flush, shiplog, token-movers, fetch-tweets, changelog, holdings. Each shows a fresh dispatch (08-02/08-03) but `last_success` stuck days earlier — success rates are still 100% historically, so this looks like the outcome-write step (or the scheduler's git commit-back) broke fleet-wide, not per-skill bugs. No `memory/logs/` file has been written since 2026-07-30, confirming nothing has actually completed since.

🟡 heartbeat self-check: last success 2026-07-30T19:18 UTC (~4 days stale). Its own 08-03 19:00 UTC scheduled dispatch is missing from cron-state.json entirely.

🔵 P1/P2 clean — 0 open PRs, issue #117 (fetch-tweets health) open but not urgent, nothing new flagged in memory.

Status page → 🔴 DEGRADED (docs/status.md updated). Worth checking the GitHub Actions run history directly — the scheduler workflow itself may need a look.