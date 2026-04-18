*Agent Self-Improvement — 2026-04-18*

Repo Pulse Idempotency Check

Added a dedup guard to the repo-pulse skill so it no longer double-notifies when re-dispatched within the same UTC day. If today's log already has a Repo Pulse entry with identical stargazers_count and forks_count, the skill now short-circuits with REPO_PULSE_DUPLICATE and skips the notification.

Why: today's log contains two consecutive ## Repo Pulse sections for aaronjmars/MiroShark with identical payloads (stars=717, forks=137, same 11 new stargazers, same 3 new forks). Both marked Notification sent: yes. Same duplication pattern surfaced in push-recap on Apr 15 and Apr 17 — recurring, not a one-off.

What changed:
- skills/repo-pulse/SKILL.md: step 1 now scans today's log for a prior entry for the same repo; if counts match the fresh fetch, it logs REPO_PULSE_DUPLICATE and skips. Step 7 gained a short log variant so skipped repos still leave a trace in the record.

Impact: one fewer source of duplicate notifications when heartbeat auto-triggers, manual dispatches, or workflow retries collide with the scheduled 10:00 UTC run on a no-activity day. Keeps the log readable and avoids double-posting the same star list to channels once they come online.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/18
