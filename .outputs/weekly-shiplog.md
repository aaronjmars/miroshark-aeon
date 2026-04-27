*Weekly Shiplog — 2026-04-27*

The week MiroShark became addressable: three machine-readable contracts shipped over the same engine in three calendar days.

Shipped:
- *Three Protocols in Three Days* — PR #44 MCP Onboarding (Apr 24, Settings panel + Claude Desktop/Cursor/Windsurf/Continue snippets), PR #45 OpenAPI 3.1 + Swagger UI (Apr 26, 1.9K-line spec + drift test), PR #46 Completion Webhook (Apr 26, Slack/Discord/Zapier/n8n outbound, zero new deps)
- *Distribution surfaces* — PR #42 Social Share Card (Apr 22, OG image + landing page) and PR #43 Public Gallery /explore (Apr 23) close the inbound side; same `_build_*_payload` family + ±0.2 stance threshold across share-card/gallery/webhook
- *Onboarding pivot* — Cheap preset (Qwen/DeepSeek/Grok, CoT off, ~3× lower latency), Settings preset dropdown + per-slot overrides, README slim 698→243 + nine docs/ files, "$1 & under 10 min" tagline; runner hardening + simulation-page UI overhaul underneath
- *Aeon prefetch-sidecar pattern* across 7 PRs — XAI cache validation/annotation harvest, fetch-tweets ID dedup, token-report XAI prefetch, bankr diagnostics

Stats: ~43 substantive commits, 14 PRs merged, +~23,500/-~4,000 lines, 751→836 stars (+85), 146→157 forks, 0 open PRs at week close
Full update: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/weekly-shiplog-2026-04-27.md
