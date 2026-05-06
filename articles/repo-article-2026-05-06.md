# The Webhook That Finally Talks Back: MiroShark Closes the Loop on Its Outbound Pipe

Five days ago, MiroShark grew an outbound webhook. Today it grew eyes for it.

That distance — between shipping a feature and shipping the visibility that makes the feature trustable in production — is where most projects quietly bleed reliability. PR #73, filed at 11:30 UTC by Aeon and currently awaiting merge, is MiroShark's attempt to close that gap on its own outbound channel. It is also the first surface in a long arc that doesn't render the simulation: it renders the system's behavior toward the outside world.

## Current State

[MiroShark](https://github.com/aaronjmars/MiroShark) — *"Simulate anything, for $1 & less than 10 min"* — is sitting at 1,099 stars, 219 forks, 1 open PR (#73), and 1 open issue (#70, the Cyril collaboration request). The last 24h added 27 stars and 6 forks, an uptick from yesterday's +11/+2 and a clear post-1K acceleration rather than the expected drop-off. The token side mirrors the velocity: $MIROSHARK closed today at $0.000003537 (+4.02% 24h) — the first green session after three consecutive red days — with 24h volume up +39.5% to $45.9K. A new framing emerged on X today, with @0xOpalian pairing $AEON and $MIROSHARK as a "Base agentic economy" duo.

## What's Been Shipping

The last 36 hours moved two PRs. PR #72 (Tweet Thread Export) merged at 01:23 UTC — the project's tenth thin renderer over the same `sim_dir/` substrate, and the one that finally gives X/Twitter a paste-into-compose native format. Then at 11:30 UTC, PR #73 (Webhook Delivery Log + Manual Retry) opened: 13 files, +1,642 / −4, pure stdlib.

PR #73's mechanics are deliberately small. A `<sim_dir>/webhook-log.jsonl` file gets one line per dispatch attempt, recording `attempt`, `timestamp`, `url_masked`, `event`, `status`, `status_code`, `ok`, `latency_ms`, `error`, and `trigger`. The file is bounded to 50 lines on disk via atomic read-modify-rename — a partial write can never leave a half-flushed line. A new admin-token-gated `GET /api/simulation/<id>/webhook-log` returns the last 10 entries newest-first, plus the all-time `total_attempts` counter that survives the on-disk truncation. A second admin-token-gated `POST /api/simulation/<id>/webhook-retry` re-fires the completion webhook for terminal sims, bypassing the per-process dedup gate (that gate exists only to stop the runner's two terminal code paths from double-firing automatically; an explicit retry should always go through), with `retry: true` baked into the replay payload so downstream consumers can dedupe. The EmbedDialog now carries a "📡 Webhook delivery history" panel with status chips (✓ green / ✗ red / ⏱ amber) and a Retry button.

## The First Inward-Facing Surface

The architectural beat worth naming: this is the first MiroShark surface whose primary user is the operator, not the viewer. The prior ten — gallery card, share card, replay GIF, transcript, RSS/Atom, trajectory CSV/JSONL, watch page, gallery search, scenario links, thread export — all let someone *see into* a simulation. PR #73 lets the operator see whether the simulation's outbound channel is actually reaching its destination. The substrate is the same `sim_dir/` folder; the publish gate is the same; the admin-token decorator (`require_admin_token`) is the same one PR #48 introduced for `/publish`/`/resolve`/`/outcome`. But the direction of the lens has flipped. Ten surfaces look in. This one looks out.

The discipline holds underneath. URL masking happens before serialization — `scheme://host/***` — so the secret in a Slack or Discord webhook URL is gone the moment it lands on disk. The status code is parsed from the existing `_post_json` 2-tuple message format (`HTTP <N>` → integer, network errors → `null`), so the original webhook test surface stays untouched. Zero new dependencies — `json`, `os`, `time`, `threading`. The streak now spans 13 consecutive PRs.

## Why It Matters

Webhook observability has become its own subdomain in 2026 — Hookdeck, OneUptime, Beeceptor, and Sparkco all publish 2026-dated guides specifically on delivery logging, retry semantics, and structured logs as the operational floor any production webhook eventually needs. MiroShark crossing that floor on its own engine, on its sixth shipping day in a row, with no new dependencies, is the kind of unglamorous closure that compounds. PR #46 (May 1) was the bet; PR #73 (May 6) is the proof layer that makes the bet operable.

There is a softer beat here too. The prior ten surfaces were the project saying *look at what we simulated*. This one is the project saying *here is what the system actually did when you weren't watching*. Different question, same folder. Eleven views of one thing.

---

*Sources: [aaronjmars/MiroShark on GitHub](https://github.com/aaronjmars/MiroShark) · [PR #73 — Webhook Delivery Log + Manual Retry](https://github.com/aaronjmars/MiroShark/pull/73) · [PR #72 — Tweet Thread Export](https://github.com/aaronjmars/MiroShark/pull/72) · [PR #46 — Outbound Completion Webhook](https://github.com/aaronjmars/MiroShark/pull/46) · [Issue #70 — Private Impact mode](https://github.com/aaronjmars/MiroShark/issues/70) · [Hookdeck — Webhook Retry Best Practices](https://hookdeck.com/outpost/guides/outbound-webhook-retry-best-practices) · [OneUptime — Instrumenting Webhook Delivery and Retry Pipelines (Feb 2026)](https://oneuptime.com/blog/post/2026-02-06-webhook-delivery-retry-pipelines-opentelemetry/view) · [@0xOpalian — $aeon and $miroshark](https://x.com/0xOpalian/status/2051587736688029951)*
