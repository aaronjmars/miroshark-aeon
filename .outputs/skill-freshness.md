⚠️ *Skill Freshness — 2026-05-17*
FRESHNESS_WARN — 3 of 18 deps flagged across 3 of 20 enabled consumers

Worst:
- feature ← articles/repo-actions-2026-05-16.md (29.6h old, class articles/daily, sev WARN)
- hyperstitions-ideas ← articles/repo-actions-2026-05-16.md (29.6h old, same dep)
- self-improve ← articles/repo-actions-2026-05-16.md (29.6h old, same dep)

Context: repo-actions runs every 2 days (0 14 */2 * *) — it ran May 16, next run May 18. The WARN is a spec cadence-bucket artifact (daily threshold = 28h; every-2-day cadence supports 52h). No genuine staleness; these consumers will read the correct most-recent output.

Architectural note: repo-pulse has never written articles/ (referenced by thread-formatter + operator-scorecard). operator-scorecard also references missing skill-analytics and heartbeat articles — degrades gracefully.

Action: Monitor — expected to clear when repo-actions runs tomorrow (May 18 ~14:00 UTC).
Full: articles/skill-freshness-2026-05-17.md
