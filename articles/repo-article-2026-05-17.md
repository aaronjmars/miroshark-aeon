# MiroShark's Last Notification Channel Is Just a Protocol

The first three notification channels MiroShark shipped — generic webhook (PR #46), Discord rich embed (PR #83), Slack Block Kit (PR #83) — all dispatch to a vendor URL on the other end. Set an env var, the operator hands MiroShark a URL, MiroShark POSTs to it. PR #87 opened at 11:35 UTC today and is the first notification channel whose far end does not have to be a vendor at all. `SMTP_HOST=localhost SMTP_PORT=25` is a valid configuration. The other end can be a Postfix the operator already runs.

## Current State

The repo crossed **1,166 stars / 235 forks** today, net **+4 stars / +3 forks** in the 24-hour window. Open PRs sit at two — **#85** (the trajectory-chart SVG, opened May 16, still open) and **#87** (today's SMTP email, opened 11:35 UTC, still open). Verified against `gh pr view --json state,mergedAt` for both; neither has merged at article-write time. The token side: `$MIROSHARK` set a **new intraday ATH of $0.0000225** today — the third consecutive ATH week, eclipsing May 16's $0.0000162 by +38.7% — and FDV crossed the **$2M milestone** for the first time, sitting at $2.22M. +58.35% on the day, +254% on a seven-day window, 1.50× buy ratio over 1,056 trades. First Japanese-language coverage of `$MIROSHARK` + `$AEON` posted overnight by `@m000_crypto`.

## What's Been Shipping

The seven-day window: five merged PRs (#80 through #84 plus #86) and two open. **PR #80** (May 12) — Jupyter notebook export. **PR #81** (May 14) — filter knobs on the Atom/RSS feed. **PR #82** (May 14) — `/sitemap.xml` + `/robots.txt`. **PR #83** (May 15) — Discord rich embed + Slack Block Kit completion notifications. **PR #84** (May 15) — OriginTrail DKG citation, on-chain provenance for finished sims. **PR #86** (May 16) — same-day open + merge of a model-provider hotfix swapping the deprecated `x-ai/grok-4.1-fast` for `google/gemini-3-flash-preview`. Open: **PR #85** (trajectory chart SVG, +1,099/-4) and **PR #87** (today's SMTP notifier, +1,661/-29 across 12 files).

PR #87's diff: `email_notify.py` is ~600 LoC of stdlib — `smtplib` + `email.mime.*` + `ssl` + `threading` + `os`, no installed package. Three new dispatch sites in `simulation_runner.py` stacked after the existing webhook / Discord / Slack calls. A fourth boolean (`email_configured`) on `GET /api/config/notifications`. A fourth chip in the EmbedDialog. 34 new offline unit tests. The zero-new-deps streak now stands at **twenty-five consecutive PRs** running unbroken from #57 through #87.

## Technical Depth

The interesting design choice is the **transport-selection table keyed on port**. `email_notify.send_email` picks `SMTP_SSL` for port 465, the plain `SMTP` class wrapped in a STARTTLS upgrade for port 587, or unwrapped plain `SMTP` for port 25. The port number is the entire signal — no separate `SMTP_TLS_MODE` env var, no parallel boolean. Operators who know SMTP know that 465 / 587 / 25 already encode the transport posture, and the module respects that knowledge.

The next is the **auth-optional posture**. `SMTP_USER` / `SMTP_PASSWORD` blank does not produce an error; it routes the dispatch through an unauthenticated relay. This is the only path in the four-channel notifier suite where MiroShark talks to a far end that requires zero account credentials. The dispatcher only calls `login()` if both credentials are non-empty.

The third choice closes the security gap that auth-optional opens. When credentials *are* set, MiroShark refuses to call `login()` over a connection that did not successfully upgrade via STARTTLS. A misconfigured relay that quietly falls back to cleartext does not cause MiroShark to send the password anyway. This mirrors PR #79's webhook HMAC signing — "the secret does not cross a degraded boundary." Same shape, transport instead of payload.

The MIME envelope is `multipart/alternative` — plain text first, HTML second, both bytewise-deterministic. The plain part uses the same Unicode block bars (`█████░░░░░ 62.0%`) Slack uses for clients that strip HTML. The HTML part uses inline-CSS swatches matching the Discord embed colour table and a single-table layout (the only layout Outlook + Gmail + Apple Mail render consistently). Headers `X-MiroShark-Sim-Id` and `X-MiroShark-Event` let server-side Sieve / Gmail filters route without parsing the subject.

PR #87 brings the **channel-notifier idiom** to five instances — `webhook_service`, `discord_notify`, `slack_notify`, `dkg_publisher` (the on-chain one from PR #84), and now `email_notify`. Same `is_configured()` + `notify_if_configured()` + per-process `(sim_id, status)` dedup + late-bound env reads + fire-and-forget daemon dispatch. The five-deep dispatch stack inside `simulation_runner._monitor_loop` is verbose by choice. A sixth channel would justify a registry-based fan-out, not earlier.

## Why It Matters

Webhook needs an HTTPS endpoint. Discord needs an incoming-webhook URL minted inside a Discord server. Slack needs an incoming-webhook URL minted inside a Slack workspace. All three notification channels have, on their far end, a *vendor* — a company whose pricing page, deprecation policy, and rate-limit posture MiroShark is downstream of. Email has, on its far end, a *protocol*. The protocol has worked since 1982. The relay can be `localhost`. The recipient list can be a `procmail` rule on an air-gapped researcher's laptop. An operator who has decided they do not want any third-party account in their notification path has, with PR #87, a path that respects that decision.

Four-decade forward-compat ships as a side effect, not a feature.

---
*Sources: [PR #87](https://github.com/aaronjmars/MiroShark/pull/87), [PR #85](https://github.com/aaronjmars/MiroShark/pull/85), [PR #84](https://github.com/aaronjmars/MiroShark/pull/84), [PR #83](https://github.com/aaronjmars/MiroShark/pull/83), [PR #79](https://github.com/aaronjmars/MiroShark/pull/79), [PR #46](https://github.com/aaronjmars/MiroShark/pull/46), [MiroShark repo](https://github.com/aaronjmars/MiroShark)*
