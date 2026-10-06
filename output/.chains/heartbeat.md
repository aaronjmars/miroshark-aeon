🚨 Heartbeat: fleet degraded

🔴 FAILED:
- **token-movers** — 3 consecutive failures, last failed 2026-10-06 07:35 UTC (last success 2026-10-05 06:43 UTC). Zero-token "completed" harness signature (`total_cost_usd: 0`, all usage fields zero).
- **fetch-tweets** — 4 consecutive failures, last failed 2026-10-06 17:05 UTC (last success 2026-10-04 18:05 UTC, now past 2× its daily schedule interval). Same zero-token signature.

🟡 WATCH:
- **heartbeat self-check** — last success 2026-10-04 19:24 UTC (47h+ stale); 2 consecutive failures recorded 2026-10-05, same zero-token signature, before this run completed cleanly.
- Shared root cause suspected: identical zero-token signature across all three skills matches the 2026-08-31 / 2026-09-22 Claude-subscription-exhaustion pattern (then tracked as #182) — now recurring after ~2 weeks quiet. Skill-health has already filed/updated votable threads: [#182](https://github.com/aaronjmars/miroshark-aeon/issues/182) (token-movers), [#195](https://github.com/aaronjmars/miroshark-aeon/issues/195) (fetch-tweets), [#196](https://github.com/aaronjmars/miroshark-aeon/issues/196) (heartbeat). No fix landed yet.

✅ Clear: 0 open PRs / urgent issues across `aaronjmars/miroshark-aeon` and `MiroShark/MiroShark`; no missing dispatches; all other 6 enabled skills (repo-pulse, holdings, changelog, shiplog, memory-flush, aeon-update) current and green.

Status page → 🔴 DEGRADED (docs/status.md updated).

🔗 https://github.com/aaronjmars/miroshark-aeon/issues/195