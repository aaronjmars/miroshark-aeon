🚨 heartbeat: fleet still failing — GLM pin didn't hold

🔴 **fleet still failing — the GLM pin didn't hold**

Recovery check from this morning's heartbeat: **FAILED.** The 11:50 pin bought exactly two runs — holdings 15:39, changelog 15:47 — then failures resumed with the **same signature** (empty response, 0 tokens, $0 cost):

- **token-movers** — failed 19:50, 5 consecutive
- **aeon-update** — failed 18:46, 4 consecutive, success rate 33% (chronic)
- **shiplog** — failed 16:56, 4 consecutive
- **repo-pulse** — failed 17:35, 4 consecutive
- **fetch-tweets** — failed 18:32, 3 consecutive
- a heartbeat attempt also died at 19:50; this run is the retry

**Read:** the gateway returns empty responses *intermittently* — the pin wasn't a durable fix. Claude-sub exhaustion may have been only half the story. Worth checking the GLM key/credit, or re-pinning `GATEWAY_ORDER` to another provider.

**Collateral:** repo-pulse's weekly 1,500-star check and shiplog's 3rd-idle-window check didn't land today — changelog's successful run already confirmed the 3rd quiet engine window on its side. 8 open `health:` issues (#153–#160; #154/#155 are stale — those skills recovered). Status page → 🔴 DEGRADED.

**Next canary:** token-movers at 06:00 UTC tomorrow. Fails again → the fleet is on borrowed time.