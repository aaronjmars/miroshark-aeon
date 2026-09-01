✅ Fleet recovered — 08-31 outage closed

✅ **Outage over — fleet recovered.** The 08-31 gateway outage is closed: both watch-canaries went green today (token-movers 06:26 UTC, fetch-tweets 17:14 UTC), and every skill the outage touched has since succeeded. 0 consecutive failures fleet-wide.

**Residual flag:** aeon-update's rolling success rate is 43% (4 of 7 runs — all with the outage's zero-token signature). The chronic-failure bar keeps the status page 🔴 until its next clean weekly run (4/8 clears it); the skill itself succeeded today at 01:45 UTC and its framework-sync PR #161 merged at 14:59 UTC.

**Housekeeping:** health threads #153–#160 are all stale — every named skill has recovered — and `skill-health` is disabled, so nothing will auto-close them. Close manually or re-enable the loop.

Status page regenerated → 🔴 DEGRADED (aeon-update rolling rate only; everything else green).