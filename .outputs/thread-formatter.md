*Thread Draft — 2026-05-17*
Topic: SMTP Completion Email Notifications — MiroShark PR #87

1/ MiroShark PR #87 ships SMTP email notifications today — the fourth completion channel and the first one that needs zero vendor accounts. Point SMTP_HOST at localhost:25, and your own relay handles delivery. 25th consecutive zero-dependency PR.

2/ Webhook needed a vendor endpoint. Discord needed a webhook URL. Slack needed a webhook URL. All three require a third-party account before anything leaves the host. Email doesn't — you can route it through any SMTP relay you control, including one running locally.

3/ The transport is selected by port: 465 locks to SMTP_SSL, 587 uses STARTTLS, 25 sends plain. If STARTTLS fails and credentials are set, it refuses to send — no cleartext fallback. A secret that crosses a degraded boundary is no longer a secret.

4/ The notification shape in MiroShark is now five wide: webhook, Discord, Slack, on-chain DKG, email. Each one checks for its env var, dispatches on a daemon thread, and deduplicates per process. The fifth channel will be a copy of the fourth.

5/ 34 tests, zero new dependencies, the 25th streak PR. It's open on MiroShark: https://github.com/aaronjmars/MiroShark/pull/87

(article: articles/thread-2026-05-17.md)
