# Push Recap — 2026-05-17

## Overview
Single substantive commit across the watched repos in the last 24 hours — PR #87 on `aaronjmars/MiroShark` (still OPEN at window close), adding SMTP completion emails as the fourth notification channel. Nothing merged to MiroShark `main` in the window (the prior merge was PR #86 at 14:20 UTC on May 16, ~55 minutes before the window opened). On `aaronjmars/miroshark-aeon`, 36 commits to `main`, all housekeeping or daily-skill data outputs — no code changes to the agent framework.

**Stats:** 12 files changed, +1,661 / -29 lines staged in open MiroShark PR #87. ~36 housekeeping commits on miroshark-aeon `main`, with one substantive content commit (`ac8569f` — today's `$MIROSHARK` token report article + log entry, 63 lines added across 2 article/log files, no code).

---

## aaronjmars/MiroShark

### SMTP Completion Email Notifications — the fourth notification channel
**Summary:** A single commit (`6544be7`) opens PR #87, adding SMTP/email as a fourth channel alongside the generic webhook (PR #46), Discord (PR #83), and Slack (PR #83). The channel-notifier idiom — `is_configured()` env-var guard, `(sim_id, status)` per-process dedup, daemon-thread fire-and-forget dispatch — now exists at five instances in the codebase (webhook, discord, slack, dkg, email). Stdlib-only: `smtplib` + `email.mime.*` + `ssl` + `os`. Zero new dependencies, preserving the 24-PR zero-dep streak from PR #57.

**Commits:**

- `6544be7` — `feat: SMTP completion-email notifications (4th channel — zero platform dependency)`
  - **New file `backend/app/services/email_notify.py` (+796 lines)** — Stdlib SMTP dispatcher. Module-level env constants (`SMTP_HOST_ENV_VAR`, `SMTP_PORT_ENV_VAR`, `SMTP_USER_ENV_VAR`, `SMTP_PASSWORD_ENV_VAR`, `SMTP_FROM_ENV_VAR`, `SMTP_TO_ENV_VAR`, `SMTP_USE_TLS_ENV_VAR`). Transport selection by port: `465` → `smtplib.SMTP_SSL` (implicit TLS), `587` → `SMTP` + `starttls()` (the default), `25` → bare `SMTP`. Auth is optional — blank `SMTP_USER`/`SMTP_PASSWORD` routes through an unauthenticated relay (e.g. `localhost:25` / self-hosted Postfix). When credentials ARE set and STARTTLS is refused on the submission port, the dispatcher refuses to send rather than leak the password in cleartext (`STARTTLS failure on credentialed connection` branch). `multipart/alternative` MIME body: plain text uses the same Unicode block-bar glyphs (`█` / `░`, 10-wide) the Slack notifier uses; HTML uses inline-CSS colour swatches matching the Discord embed borders (`#22c55e` bullish / `#6b7280` neutral / `#ef4444` bearish / `#f59e0b` failed) plus a consensus-coloured "View simulation →" CTA. Subject line `[MiroShark] <Direction>: <Scenario>` (Bullish/Neutral/Bearish/Failed) so inbox filters can triage by direction without parsing the body. `X-MiroShark-Sim-Id` and `X-MiroShark-Event` headers for programmatic mail rules.
  - **Modified `backend/app/services/simulation_runner.py` (+33 / -0)** — three new dispatch sites, all immediately after the existing Slack `notify_if_configured` call: (1) exit-code "completed" branch in `_monitor_simulation`, (2) exit-code "failed" branch in the same method (sends `error=state.error`), (3) `simulation_end` event branch in `_read_action_log`. Each is wrapped in its own `try/except` that logs `Email notify dispatch failed: <err>` and continues — completely symmetric with the existing Discord / Slack dispatch pattern.
  - **Modified `backend/app/api/notifications.py` (+8 / -5)** — `notifications_config()` envelope grows `email_configured` boolean; docstring updated; `email_notify` added to the service import alongside `discord_notify` / `slack_notify`. SPA chip can now render the fourth channel without auth.
  - **Modified `backend/openapi.yaml` (+18 / -1)** — `NotificationsConfig` schema gets `email_configured` required + property docs (explicitly notes recipient addresses are never returned). `email_configured` description spells out that both `SMTP_HOST` and `SMTP_TO` are required for `true` ("a host with no recipients has nowhere to send, so the channel reads as unconfigured").
  - **Modified `frontend/src/components/EmbedDialog.vue` (+17 / -3)** — fourth "Email" chip in the notifications-chip row; `notifConfig` reactive grows `email_configured` field; bilingual (EN + zh-CN) tooltip explains how to enable. Failure-resilient: defaults `email_configured` to `false` on fetch failure so a flaky `/api/config/notifications` never lights the chip green by accident.
  - **New `backend/tests/test_unit_email_notify.py` (+572 lines)** — 34 offline unit tests covering: env-var pinning, `is_configured()` truth table (host-only / recipients-only / both / neither), port resolution (default 587 / invalid string / out-of-range), `_resolve_from` fallback to `miroshark-notify@<host>`, subject builders for each direction, plain-text body block-bar formatting, HTML body inline-CSS colour selection, MIME structure (`multipart/alternative` + correct part order), per-process dedup, transport selection per port (SMTP_SSL / SMTP+STARTTLS / plain SMTP), auth skip on blank credentials, credential-leak refusal when STARTTLS fails on credentialed connection, `send_test_notification` validation path, exception swallowing.
  - **Modified `backend/tests/test_unit_notifications_config.py` (+64 / -1)** — extends config-envelope tests with `email_configured` assertions: email-only, email-requires-both-host-and-to, all-four-configured combinations.
  - **Modified `.env.example` (+24)** — full SMTP block with Gmail / SendGrid / Mailgun / unauthenticated-relay recipes, including the `SMTP_USE_TLS=false` escape hatch for port-25 LAN relays.
  - **Modified `docs/NOTIFICATIONS.md` (+113 / -16)** — full SMTP section: minimal + authenticated recipes, body-structure description (subject / plain / HTML), Gmail App Password recipe, SendGrid / Mailgun apikey recipe, channel-selection guide. Table at the top grows from "Three independent channels" to "Four."
  - **Modified `docs/FEATURES.md` + `docs/FEATURES.zh-CN.md` (+4 / -3 and +10 / -0)** — extends "Channel-Native Completion Notifications" to cover Discord + Slack + Email.
  - **Modified `README.md` (+2)** — adds an "SMTP Completion Emails" row to the features table.

**Impact:** Operators no longer need a Discord server or a Slack workspace to receive simulation-completion alerts — every research team already has an inbox. The visual language (block-bar glyphs, consensus colours) stays identical across Slack and email so the same recipient seeing both channels reads the same signal. Authentication is genuinely optional (a bare `SMTP_HOST=localhost SMTP_TO=x@y SMTP_PORT=25` is enough to start), and the credential-leak refusal on STARTTLS failure means a misconfigured port choice can't accidentally publish the SMTP password in cleartext. The notification quadrant is now closed: Webhook (automation), Discord (community), Slack (ops), Email (universal).

---

## aaronjmars/miroshark-aeon

### Housekeeping only — no framework code changes
**Summary:** 36 commits to `main`, every one of them either a `chore(cron): <skill> success` marker, a `chore(<skill>): auto-commit <date>` rollup, or a `chore(scheduler): update cron state` heartbeat from the GitHub Actions scheduler. The cron loop fired token-report → fetch-tweets → tweet-allocator → star-momentum-alert → repo-pulse → feature (the SMTP PR above) → and the prior-day project-lens / repo-article / thread-formatter / heartbeat / push-recap closers on May 16 evening, all under the existing scheduler infrastructure. No skill prompts edited, no aeon Python code changed, no new skills added.

**Commits worth naming individually:**

- `ac8569f` — `feat(token-report): $MIROSHARK daily report 2026-05-17 — new ATH $0.0000225, FDV $2.22M` — two new files only (`articles/token-report-2026-05-17.md` +49, `memory/logs/2026-05-17.md` +14). Data write, not a code change; logs today's $MIROSHARK report showing a third consecutive ATH week (May 12 → May 16 → May 17) and the first Japanese-language coverage of the token (`@m000_crypto`, May 17).
- `2b381fa` — `chore(feature): auto-commit 2026-05-17` — bundle commit for the `feature` skill run that opened MiroShark PR #87. Modifies `.outputs/feature.md`, archives `dashboard/outputs/.pending-feature.md` into a timestamped JSON spec (`feature-2026-05-17T11-37-50Z.json`, +161), and appends the build log to `memory/logs/2026-05-17.md` plus a `Skills Built` row to `memory/MEMORY.md`. No source-tree changes.
- `6db8c1e` — `chore(cron): repo-pulse 2026-05-17` — only Sonnet 4.6 co-authored commit in the window; +5 lines to `memory/logs/2026-05-17.md` only. Standard repo-pulse cron output.

**Open PRs:** PR #40 (`improve: project-lens must verify PR status before notify`, opened 2026-05-16T13:06:21Z, +3 / -0 single file). Stalled at ~26 hours as of window close — same single-file-await pattern PR #34 hit before it eventually landed.

**Impact:** None directly — the day's framework-side activity is the SMTP build firing through the existing skill chain, not a change to the chain itself. The 36-commit churn is the visible side-effect of the cron loop doing its job, identical in shape to every prior 24-hour window.

---

## Developer Notes

- **New dependencies:** None (the streak from MiroShark PR #57 reaches **24 PRs** with PR #87 staged; 23 merged + 1 open). `email_notify.py` is pure stdlib (`smtplib` + `email.mime.*` + `ssl` + `os` + `threading`), matching the `discord_notify` / `slack_notify` / `dkg_publisher` rule.
- **Breaking changes:** None. `NotificationsConfig` schema grows `email_configured` as a required field, but the SPA already defaults to `false` on fetch failure, so any consumer that wasn't reading it gets the same behaviour as before. Existing webhook / discord / slack deployments are unaffected (unset `SMTP_HOST` ⇒ `is_configured()` returns false ⇒ no-op).
- **Architecture shifts:** The channel-notifier idiom now spans five transports (HTTP webhook, Discord HTTP, Slack HTTP, on-chain DKG daemon, SMTP). Each module exposes the same `is_configured()` + `notify_if_configured(sim_id, status, ...)` surface, holds its own `_FIRED` dedup set, and reads env vars late so test isolation works. The runner-side dispatch sites in `simulation_runner.py` are now stacked five-deep at each terminal-state branch — a candidate for a registry-based fan-out if a sixth channel is contemplated, but not refactored here.
- **Tech debt:** None introduced. The credential-leak-on-STARTTLS-failure refusal is a deliberate hard fail, not a TODO. The runner-side dispatch stack at each terminal-state hook is verbose but explicit; refactoring to a registry would be churn ahead of a real need.

## What's Next

- **PR #87 review + merge.** Single commit, 34 offline tests, mirrors a pattern that's already merged twice. Likely lands same-day or next-day, similar to PR #83 (1d-1 open → merge).
- **Notification-quadrant work likely done.** With email shipped, the four-channel quadrant (Webhook / Discord / Slack / Email) is structurally complete. Next notification-tier work is more likely **observability** (already partly built: webhook-log PR #73, surface-stats PR #74) than **another channel** — though Telegram or Matrix would be the natural fifth instance of the idiom if requested.
- **Open `feature` candidates from the May-16 repo-actions batch (4 remaining):** #1 oEmbed (Notion / Substack / Ghost unfurl), #2 Farcaster Frame on share page, #4 Peak-Round Belief Analytics, #5 Operator Profile page. The grep-guard from aeon PR #35 caught zero overlap pre-build, so all four remain viable.
- **PR #85 (Trajectory Chart SVG) is still open at ~28h** — older than the 24h soft-stall threshold heartbeat watches for. Same shape as PR #34's stall before it landed; likely lands in tomorrow's window.
- **aeon PR #40 (project-lens PR-status verify) is still open at ~26h** — single-file +3/-0 prompt fix, no CI obstacle visible.
