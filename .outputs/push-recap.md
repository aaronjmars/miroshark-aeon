*Push Recap — 2026-05-17*
MiroShark + miroshark-aeon — 1 substantive PR opened, 0 merges to MiroShark main, 36 housekeeping commits on aeon main.

Notification quadrant closes: PR #87 (open) lands SMTP email as the 4th completion-notification channel alongside webhook / Discord / Slack. Pure stdlib (`smtplib` + `email.mime`), zero new deps — the 24-PR no-dependency streak from PR #57 is preserved (23 merged + 1 open). Mirrors the `discord_notify` / `slack_notify` shape exactly; runner-side dispatch sites now five-deep at each terminal-state branch.

Auth-optional, zero-platform-dependency design: blank `SMTP_USER`/`SMTP_PASSWORD` routes through an unauthenticated LAN relay (`localhost:25` / self-hosted Postfix). Every research team already has an inbox — no Discord server or Slack workspace required for completion alerts. Visual language stays identical: same Unicode block bars Slack uses, same consensus colours Discord uses (#22c55e/#6b7280/#ef4444/#f59e0b), plus subject `[MiroShark] <Direction>: <Scenario>` for inbox triage.

Credential-leak refusal as security posture: STARTTLS failure on a credentialed connection refuses to send rather than fall back to cleartext — same "secret never crosses a degraded boundary" rule as HMAC signing in PR #79. The channel-notifier idiom now spans 5 transports (HTTP webhook, Discord HTTP, Slack HTTP, on-chain DKG daemon, SMTP).

Aeon-side window is pure housekeeping — 36 chore/auto-commit pairs from the cron loop firing token-report → fetch-tweets → tweet-allocator → star-momentum-alert → repo-pulse → feature. No skill prompts edited, no aeon Python code touched. One substantive content commit: today's $MIROSHARK token report logging a 3rd consecutive ATH week ($0.0000225, FDV $2.22M).

Key changes:
- `backend/app/services/email_notify.py` — new 796 LoC stdlib SMTP dispatcher; transport selects by port (465 ⇒ SMTP_SSL, 587 ⇒ SMTP+STARTTLS, 25 ⇒ plain); per-process `(sim_id, status)` dedup; fire-and-forget daemon-thread dispatch
- `backend/app/services/simulation_runner.py` — 3 new dispatch sites (exit-code completed, exit-code failed, `simulation_end` action-log event), each wrapped in try/except mirroring Discord/Slack
- `backend/tests/test_unit_email_notify.py` — 34 offline unit tests (env-var pinning, port resolution, transport selection, dedup, credential-leak refusal, MIME structure)
- `frontend/src/components/EmbedDialog.vue` — 4th "Email" notification chip + reactive `email_configured` field

Stats: 12 files changed, +1,661 / -29 lines in PR #87.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-17.md
