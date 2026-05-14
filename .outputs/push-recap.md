*Push Recap — 2026-05-14*
MiroShark — 2 commits by aaronjmars (Aeon co-author) | aeon — 30 commits, 6 substantive PRs

*External Discovery Layer Closed Out*: PR #81 (filtered RSS/Atom feed, +1280/-37) and PR #82 (sitemap.xml + robots.txt, +1273/-2) merged 11 minutes apart. Filtered feed grafts the gallery's `select_filtered_cards` onto the syndication channel — six new query knobs (`?consensus=`, `?quality=`, `?outcome=`, `?q=`, `?sort=`, `?limit=`) make "subscribe to my bullish-consensus stream" a one-URL operation in Feedly / n8n / Zapier. Sitemap is sitemaps.org 0.9 XML over public sims (priority 0.8 per `/share/<id>`, 0.7 per `/watch/<id>`), byte-deterministic via id-ascending sort, behind `ENABLE_SITEMAP=true`. Together they close the May-12 repo-actions batch entirely (5/5 resolved — 3 redundant, 1 deferred, 2 = these PRs). Zero-new-deps streak: 20 consecutive PRs (#57 → #82).

*Skill Catalog Refresh*: PR #36 (+1964/-2) syncs 7 skills from aeon-agent, PR #37 (+5696/-14) syncs 22 skills from aeon upstream — 13 minutes apart, catalog roughly doubles (skills.json 55 → 84 entries). All `enabled:false` so the operator picks rollout cadence. First-class fleet vocabulary lands: `fleet-state`, `fork-skill-digest`, `fork-release-tracker`, `fork-contributor-leaderboard` — miroshark-aeon now structurally aware it's one of multiple operator forks.

*Selective Rollout + Self-Correction*: PR #38 enables 6 launch-comms / weekly-visibility skills (`star-milestone`, `star-momentum-alert`, `thread-formatter`, `contributor-spotlight`, `operator-scorecard`, `ai-framework-watch`) — all silent on quiet days. PR #39 disables `contributor-spotlight` 2 minutes later because its dependency `fork-cohort` is still `enabled:false`; pre-flight check working as intended, caught before first Sunday firing.

*Self-Improve Pair*: PR #34 (+280/-96) adds "repo root OFF-LIMITS" guidance to feature skill + .gitignore hardening + removes 3 past scratch leaks (`sig_smoke.py`, `_smoke_webhook.py`, `.aeon-tmp-verify-trending.py`). PR #35 (+28/-5) inserts a new step 6 — grep backend routes / SPA router / OpenAPI / docs before building — bails to next candidate if surface already exists. Both lessons surfaced in earlier push-recaps, fixed same week.

Key changes:
- `backend/app/services/sitemap.py` (+362, new) — pure-stdlib XML renderer, byte-deterministic via id-ascending sort, `<lastmod>` fallback chain `updated_at → created_at → state.json mtime`, `<changefreq>` `always`/`weekly`/`daily` per status, cap 50,000 URLs
- `backend/app/services/feed.py` (+209/-15) — `select_public_cards` and `render_feed` gain six new kwargs + `surface_stats_reader` callback; reuses `gallery_filters.select_filtered_cards` so gallery and feed answer the same question identically
- 29 new SKILL.md files across aeon (avg ~240 LoC each) — including 4 first-class "fleet" skills, 6 daily launch-comms skills (3 now live in cron), 3 crypto skills (kalshi, aixbt, price-threshold), 2 social spend skills paused-by-default for safety

Stats: 70 files changed, +10,528 / -163 lines across 8 substantive PRs
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-14.md
