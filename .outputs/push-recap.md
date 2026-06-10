*Push Recap — 2026-06-10*
aaronjmars/MiroShark — 1 substantive commit; aaronjmars/miroshark-aeon — 3 substantive + 26 cron auto-commits excluded as noise per the May-31 convention.

New Chinese-Locale Front Door: PR #155 merged on MiroShark — promotes the embedded `## 中文` block out of README.md into standalone `README.zh-CN.md` (+142 lines), mirrors the per-file `.zh-CN.md` pattern already used by CONTRIBUTING + 12 docs/*. README.md trimmed −108/+9, language switcher now cross-file link, English H3s promoted to H2. Directly addresses the Jun-15 Chinese-locale hyperstition (5 days out) — the contributor-angle resolution path; coverage-angle already hit via btcbabycow tweet May 16. Zero deps; catalog stays at 35; auth/openapi untouched.

Project-Lens Contrarian #5: aeon committed `articles/project-lens-2026-06-09.md` — *Webhooks Won the Argument. Polling Won the Integration.* Re-frames PR #153's polling-shape `activity.json` against the 2026 webhook+MCP creed; argues webhooks fit one-consumer-with-infra, polling fits N-unknown-consumers where every integration is a `curl` + `sleep`.

Self-Improve Bookkeeping: aeon log entry for PR #56 (improve/feature-hyperstition-tiebreaker) — encodes today's in-flight Chinese-README pick as mechanical step 2.b rule (reads Active Targets, picks unbuilt candidate matching ≤10-day hyperstition over higher-impact evergreen). 3rd SKILL.md tightening in 4 days (siblings PR #55 push-recap noise, PR #53 feature auth-posture).

Key changes:
- `README.zh-CN.md` new file +142 lines: full Chinese mirror of English README — badges row, hero + demo image, 6 H2 sections, localized overview image `miroshark-overview-cn-v2.jpg`, section-deep-linked `docs/INSTALL.zh-CN.md` anchors, license block.
- `README.md` −108/+9 lines: removed embedded `## 中文` section, dropped `<a id="english">` + `## English` scaffold, promoted 6 orphaned H3s to H2, switcher chip changed from `#中文` anchor to `./README.zh-CN.md`.
- `articles/project-lens-2026-06-09.md` new file +50 lines: contrarian essay on polling vs webhooks, positions activity.json as discovery-cluster sibling to feed_atom + feed_rss.

Stats: 5 files changed, +201/-108 lines across 4 substantive commits (26 cron auto-commits excluded as noise).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-10.md
