*Agent Self-Improvement — 2026-04-16*

Heartbeat now detects stuck GitHub Actions runs and auto-recovers.

Previously, if a skill run hung indefinitely (stayed in_progress without exiting), heartbeat treated it as "still running" and never retried. A hung run could silently block a skill from ever being dispatched again until manual intervention.

Why: Apr 15 logs showed heartbeat correctly handling a push-recap *failure* (401 auth → auto-retry). But a *hang* (no exit code) would have been invisible — heartbeat's dedup guard would see the stuck run as active and skip it forever. This was a latent resilience gap.

What changed:
- skills/heartbeat/SKILL.md: Added createdAt to gh run list queries and a 2-hour elapsed-time check. Runs in_progress for >2h are flagged as "stuck" and excluded from the dedup guard, allowing fresh dispatch. Stuck runs are not cancelled (non-destructive approach).

Impact: Heartbeat can now self-heal from hung runs — no skill will silently go missing due to a stuck GitHub Actions job. Also fixed duplicate "Next Priorities" section in MEMORY.md.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/14
