*Push Recap — 2026-05-07*
aaronjmars/MiroShark + aaronjmars/miroshark-aeon — 3 substantive commits + ~24 cron auto-commits

*Observability loop closes (MiroShark):* PR #73 ships an outbound webhook delivery log + manual retry endpoint; PR #74 ships per-share-surface usage counters. Together they give operators end-to-end feedback over what MiroShark sent out (Slack/Discord/n8n delivery status, latency, retries) and what audiences pulled in (share card / replay GIF / transcript / trajectory / RSS / watch page). Both PRs land within 14 minutes of each other on the same `<sim_dir>/` substrate, same atomic-write contract, same EmbedDialog panel pattern, zero new deps.

*PR #73 caught its own concurrency hazards before merge:* a second commit on the same PR added a module-level write lock around the read-modify-rename log window (so two concurrent dispatches can't drop each other's entries — exactly the visibility failure the log is meant to surface) plus a 5-second per-sim cooldown on the retry endpoint (so a leaked admin token can't be weaponized as an amplifier against the configured downstream). Verified by a 32-thread barrier test.

*Heartbeat false-positive fix (aeon):* PR #31 tightens skill-ran detection in `skills/heartbeat/SKILL.md` from a free-text substring search of the full log to `^## ` header-line grep with explicit per-skill regexes. The bug it fixes: body text like "added a feature" was matching the `feature` skill name and masking real outages of the `feature` skill. Self-monitoring layer was lying.

Key changes:
- New backend module `surface_stats.py` (+215, frozen 11-key SURFACE_KEYS schema, atomic tempfile + os.replace, fire-and-forget) wired into every `_serve_X` handler in simulation.py, watch_landing (public sims only), and per-card feed dispatch
- `webhook_service.py` (+365): new `webhook-log.jsonl` (50-line atomic cap, URL-masked before write), GET `/webhook-log` (admin-token), POST `/webhook-retry` (admin-token, rate-limited, bypasses per-process auto-fire dedup with `retry: true` payload marker)
- `EmbedDialog.vue` grew two new collapsible panels (+499 + 342): "📡 Webhook delivery history" (✓/✗/⏱ chips, Refresh + Retry) and "📊 Distribution" (sorted table with stable-sort tiebreaker, explicit cache caveat so operators don't compare counts to CDN dashboards and conclude the counter is broken)

Stats: 26 file diffs, +2,987 / -5 lines on MiroShark; +15 / -8 on the aeon heartbeat fix; ~24 routine cron auto-commits.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-07.md
