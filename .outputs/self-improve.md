*Agent Self-Improvement — 2026-04-26*

Tweet Allocator now classifies Bankr prefetch failures into five distinct states (no-api-key / no-candidates / lookups-failed / completed-no-wallets / completed) instead of guessing "missing or empty cache → BANKR_API_KEY unset". The misleading daily error notification stops, and a real Bankr API outage now shows an accurate "Bankr Agent API unreachable" message with the actual lookup-failure count.

Why: TWEET_ALLOCATOR_ERROR fired Apr 25 and Apr 26 with the same text — "BANKR_API_KEY likely not set". But the secret IS set (5 wallets verified daily Apr 22–24); when it's unset the prefetch exits before creating the cache, so an empty cache means lookups silently failed. The bot was telling its operator to chase a wild goose for two days running.

What changed:
- `scripts/prefetch-bankr.sh`: new `write_status` helper writes `.bankr-cache/prefetch-status.json` at every exit with `{status, note, candidate_count, lookup_attempted, curl_failed, verified_count, null_count}`. Inline counters track per-handle outcomes so we can distinguish "all curl calls failed" from "Bankr returned null for everyone".
- `skills/tweet-allocator/SKILL.md`: step 4 branches on the sidecar's status field. `no-api-key` becomes `TWEET_ALLOCATOR_DISABLED` and is silent (no operator can fix it from the bot side — daily noise stops). `lookups-failed` keeps the loud alert but with accurate text. `completed-no-wallets` reuses the existing `_EMPTY` flow.

Impact: stops false-alarm daily notifications when the real cause is a Bankr API outage, AND silences the dormant-skill case entirely if BANKR_API_KEY ever gets rotated out. Future tweet-allocator alerts will be actionable.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/24
