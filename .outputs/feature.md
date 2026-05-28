## Summary

Built **WEBHOOK_EVENTS dispatch filter** for MiroShark — picked from 2026-05-26 repo-actions batch (idea #4, net-new). PR opened: https://github.com/aaronjmars/MiroShark/pull/120

**What shipped**
- `backend/app/services/webhook_service.py` (+237 LoC) — token constants, category frozensets, `_resolve_event_filter`, `_payload_direction` / `_payload_confidence_pct` / `_payload_quality_key` helpers, `payload_passes_event_filter(payload, events) -> (bool, trace)`. Filter wired between `_mark_fired` and `_start_dispatch_thread` in `fire_webhook_for_simulation`.
- `backend/tests/test_unit_webhook_events.py` (new, 25 offline tests) — parser, all three categories, AND across / OR within, confidence floors, quality bucket inclusion, unknown-token handling, failed-sim bypass, end-to-end fire/skip behavior.
- `.env.example`, `docs/WEBHOOKS.md` (new "Filtering events" section), `docs/FEATURES.md` (new "Webhook Event Filtering" entry).

**Design choices** (recorded in commit + PR body):
- OR within category, AND across categories
- Failed sims bypass the filter
- Unknown tokens silently ignored
- Manual retries bypass (matches existing dedup-bypass pattern)
- Late-bound env read (no restart)
- Direction rule matches share-card / Discord embed colour (no drift between filter and visual)
- Suppressed deliveries log but don't write to `webhook-log.jsonl`

**Memory**: appended detailed entry to `memory/logs/2026-05-28.md`, added row to `MEMORY.md` Skills Built table, bumped "Next Priorities" to show 3/5 May-26 batch addressed.

**Notification**: queued at `.pending-notify/1779971119.md` (sandbox blocked direct `./notify` invocation; the workflow's post-run "Re-deliver pending notifications" step will fan it out to Telegram/Discord/Slack from there).

**Validation note**: pytest blocked in sandbox (`python` not allowlisted, consistent with prior skill runs) — CI is authoritative. Logic reviewed offline against the existing `discord_notify._consensus_color` plurality rule and `signal_service._confidence_tier` thresholds for consistency.
