🚨 Heartbeat — fleet outage 2026-08-31 (recovering)

🔴 **Heartbeat — fleet outage 2026-08-31 (recovering)**

All five Monday weeklies plus the daily token report failed today — 6 skills, 06:00–11:47 UTC, all with the same signature: empty response, 0 tokens, 0 cost.

**Root cause identified:** the Claude subscription was exhausted. Operator's `9479fa2` (11:50 UTC) pins the harness to a GLM gateway — and this heartbeat ran through that pin successfully, so the fix is live.

| Skill | Last good | Consec. fails |
|-------|-----------|--------------:|
| token-movers | 08-30 | 3 |
| holdings | 08-24 | 3 |
| changelog | 08-24 | 3 |
| shiplog | 08-24 | 3 |
| repo-pulse | 08-24 | 3 |
| aeon-update | 08-25 | 2 |

**Watch:** the failed skills haven't recorded a post-fix success yet. Next scheduled runs — fetch-tweets 17:00 UTC today, token-movers 06:00 UTC tomorrow — will confirm recovery.

**Also dropped:** today's `token-movers` was the weekly Monday snapshot; no fresh token data since 08-30.

Health threads auto-filed: #153–#158 (one per skill). Status page → 🔴 DEGRADED until they re-run green.

🔗 https://github.com/aaronjmars/miroshark-aeon/commit/9479fa2