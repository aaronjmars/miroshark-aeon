*Push Recap — 2026-04-28*
MiroShark — 3 PRs merged in 75 minutes by aaronjmars (+1,513 / −59 across 21 files); miroshark-aeon — 0 substantive (chore auto-commits only).

Animated Belief Replay GIF (PR #50, 12:56 UTC): /api/simulation/<id>/replay.gif renders per-round belief drift as a 1200×630 GIF, same OG aspect as the share card so unfurl shapes stay consistent. Pure Pillow, zero new deps; cached at <sim_dir>/replay-gifs/<hash>.gif. Discord and Slack auto-play GIFs from a direct file URL — every share now ships motion as well as a still.

Langfuse-grouping metadata on every OpenRouter call (PR #51, 14:09:24 UTC): mirrors miroshark-api so generations land in Langfuse with sessionId (via extra["user"] = sim_id), tags (miroshark / prompt_type / phase:* / run:*), and a useful trace name per row. 16-entry caller→prompt_type map → 4-phase rollup (setup/round/report/ingest). New TraceContext.wrap_fn snapshots context across ThreadPoolExecutor workers (threading.local doesn't propagate).

Three cost fixes the new traces immediately exposed (PR #52, 14:10:10 UTC — merged 47 s later): (1) 12 idempotent platform actions used to return success=False when already in desired state, so agents retried the same tool 4+ times per round (40k+ input tokens) — now {success: True, noop: True}. (2) max_iteration was stored but never plumbed to CAMEL — ReAct loop was unbounded; now passed through, default 1→3, prune_tool_calls_from_memory enabled. (3) simulation_requirement capped at 1,500 chars in entity-research prompts — a multi-KB briefing was getting pasted into every call (60–80k tokens per entity).

Key changes:
- platform.py: 12 idempotent actions (like/unlike, dislike/undo, repost ×2 branches, follow/unfollow, mute, report, +4 comment variants) now no-op success instead of false-error
- replay_gif.py: 519-line Pillow renderer with FRAME_MS=600, FINAL_HOLD_MS=1800, MAX_FRAMES=60 even-subsampling preserving final round
- TraceContext.wrap_fn: reusable thread-pool context-propagation primitive used in graph_builder + wonderwall_profile_generator

Stats: 21 files changed, +1,513 / −59 lines
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-28.md
