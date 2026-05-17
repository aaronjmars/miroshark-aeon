*Feature Built — 2026-05-17*

SMTP Completion Email Notifications
MiroShark can now email you when a simulation finishes. Set two environment variables (`SMTP_HOST` and `SMTP_TO`) and every completed or failed simulation ships a properly-formatted email to whoever needs to know — research teammates, your hedge-fund back-office, or just your own inbox. The email has both a plain-text version with Unicode belief bars and an HTML version with a consensus-coloured "View simulation →" button.

Why this matters:
MiroShark already notified Discord and Slack channels (PR #83, May 15) and posted raw JSON to a generic webhook (PR #46). But Discord and Slack both require their respective platform accounts and an incoming-webhook URL. Email is the one notification channel that requires *neither* — every operator already has a mailbox, every research team already has a mailing list. This closes a clear four-channel quadrant: Webhook for automation tools, Discord for community channels, Slack for ops, and now Email for everyone else. Triggered by the May-16 repo-actions batch idea #3.

What was built:
- backend/app/services/email_notify.py (NEW, ~600 LoC stdlib): full SMTP notifier mirroring the discord_notify / slack_notify shape from PR #83 — daemon-thread fire-and-forget dispatch with per-process (sim_id, status) dedup, transport selection by port (465 ⇒ SMTP_SSL, 587 ⇒ SMTP+STARTTLS, 25 ⇒ plain), auth-optional so unauthenticated LAN relays work alongside Gmail/SendGrid/Mailgun, plus a credential-leak refusal that aborts the send if STARTTLS fails on a credentialed connection.
- backend/app/services/simulation_runner.py: three new dispatch sites (exit-code-monitor completed/failed paths + the simulation_end action-log event path) wired to email_notify.notify_if_configured the same way the existing Discord/Slack channels are wired.
- backend/app/api/notifications.py + backend/openapi.yaml: extends the public `/api/config/notifications` envelope with `email_configured: bool` so the SPA can render a live status chip without leaking any SMTP config.
- backend/tests/test_unit_email_notify.py (NEW, 34 offline tests) + extended backend/tests/test_unit_notifications_config.py: covers env-var pinning, is_configured guards (both SMTP_HOST AND SMTP_TO required), port resolution edge cases, subject/plain/HTML body builders, dedup, transport selection per port, auth skip when credentials blank, the credential-leak refusal, exception swallowing.
- frontend/src/components/EmbedDialog.vue: adds a fourth "Email" chip alongside the existing Webhook/Discord/Slack chips in the notifications callout, with bilingual tooltips and the extended notifConfig reactive object.
- .env.example + docs/NOTIFICATIONS.md + docs/FEATURES.md + docs/FEATURES.zh-CN.md + README.md (en + zh): full setup walkthrough with Gmail App Password recipe, SendGrid/Mailgun API-key recipe, unauthenticated-relay recipe, and a smtplib-only test snippet.

How it works:
On every simulation.completed / simulation.failed event, the simulation_runner calls email_notify.notify_if_configured(...). The notifier reads SMTP_HOST and SMTP_TO; either unset means no-op. The webhook_service.build_payload(...) helper (already used by Discord, Slack, and the generic webhook) assembles the canonical event dict — no duplication of artifact-reading code. The MIME builder then produces a multipart/alternative envelope: subject "[MiroShark] Bullish: <scenario>" so inbox filters can triage by direction alone, a plain-text part using the same Unicode block bars (█████░░░░░ 62.0%) Slack uses for visual consistency, and an HTML part rendered as a single <table> (the only layout Outlook + Gmail + Apple Mail all render consistently) with inline-CSS colour swatches matching the Discord embed border and a consensus-coloured "View simulation →" CTA. Custom X-MiroShark-Sim-Id and X-MiroShark-Event headers let Sieve/Gmail/Outlook filters route without scanning the subject. The dispatch runs in a daemon thread so a slow SMTP relay never blocks the simulation runner.

What's next:
The four-channel notification quadrant is now complete. Next up from the May-16 batch: oEmbed Endpoint (#1, auto-unfurl in Notion/Substack/Ghost/WordPress), Farcaster Frame for the share page (#2, Base-chain Warpcast distribution), Peak-Round Belief Analytics (#4), and Operator Profile Page (#5). The oEmbed and Farcaster ideas both hinge on whether the share page can inject custom meta tags server-side — likely needs a small SSR shim first.

PR: https://github.com/aaronjmars/MiroShark/pull/87
