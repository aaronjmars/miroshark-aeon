# Push Recap — 2026-05-14

## Overview
Eight substantive PRs landed across the two watched repos in the last 24h — the heaviest deploy day on record for this recap. MiroShark merged its 2026-05-13 + 2026-05-14 feature pair (#81 filtered RSS/Atom feed, #82 sitemap.xml + robots.txt), closing the entire May-12 repo-actions batch in 27 minutes back-to-back. miroshark-aeon did a once-in-a-cycle catalog refresh: 29 new skills synced from upstream operator forks (PRs #36 + #37), then 6 flipped to `enabled:true` for a launch-comms + weekly-visibility push (#38), with one immediate revert when a dependency cycle surfaced (#39). On top of that, two self-improve PRs hardened the feature skill against recurring failure modes (#34 scratch-file leak, #35 grep-existing-routes pre-check).

**Stats:** 70 files changed, +10,528 / -163 lines across 8 substantive PRs (+22 cron auto-commits not counted).

---

## aaronjmars/MiroShark

### Theme 1: External Discovery Layer — Distribution Surfaces Closed Out
**Summary:** Two PRs merged 27 minutes apart turn the public-simulation corpus into something search engines and feed readers can actually find and slice. Both surfaces compose existing primitives (`gallery_filters.select_filtered_cards`, the `/share/:id` route, the `is_public` gate) into new external-facing channels — neither requires new algorithms, new schemas, or new dependencies. Together they finish the May-12 repo-actions batch (5/5 resolved: three were redundant or shipped, one deferred, two became PRs #81 + #82).

**Commits:**

- `d47de20` — **feat: filter knobs on /api/feed.atom + /api/feed.rss** (PR #81 merged 12:38 UTC, +1280 / -37 across 7 files)
  - **`backend/app/services/feed.py`** (+209 / -15): `select_public_cards` and `render_feed` gain six new optional kwargs — `q`, `consensus`, `quality`, `outcome`, `sort`, plus a `surface_stats_reader` callback. The implementation reuses `gallery_filters.select_filtered_cards` so the feed answers the exact same filter question the gallery API has answered since PR #69. The `_filter_chip` helper builds an EN/zh-CN active-filter summary that splices into the feed's channel `<title>` and `<subtitle>` so subscribers know which slice they're reading. `MAX_FEED_LIMIT = 50` (smaller than the gallery's 100) caps aggregator re-fetch cost. The pre-existing `verified_only` on-disk `outcome_reader` gate runs BEFORE the rest of the filter stack — preserves PR #60 semantics so embedded card-field drift doesn't drop legit verified sims.
  - **`backend/app/api/feed.py`** (+72 / -11): parses + normalises the six new query params via the existing `gallery_filters.normalise_*` helpers and plumbs them into the renderer. `sort=trending` lazily injects the surface-stats reader; every other sort key stays read-free.
  - **`backend/tests/test_unit_feed_filters.py`** (+622, new): 16 offline tests — ±0.2 stance threshold parity, `quality=` first-word match on "Good with caveats", logical-AND intersection, `surface_stats_reader` callback wiring, graceful unknown-value fallback, case-insensitive `q=` substring, `limit` clamping, `verified_only` no-regression, title/subtitle reflection, `rel="self"` query-string preservation (Substack auto-discovery contract), and a source-side drift guard that the route reads every new knob.
  - **`backend/openapi.yaml`** (+115 / -6): both `/api/feed.atom` and `/api/feed.rss` get full parameter docs with enums + defaults.
  - **`frontend/src/components/EmbedDialog.vue`** (+221): new "Build a filtered feed" block — three dropdowns (consensus, quality, sort) + live URL preview + copy button, wired to a reactive `feedFilters` map. EN/zh-CN strings included. No new deps; reuses the `--color-orange` palette.
  - **`frontend/src/api/simulation.js`** (+38 / -3): `getFeedUrl(...)` accepts the full filter set; empty params omitted from the query string so unfiltered subscribers see no URL drift.

- `404211b` — **feat: search-engine sitemap (/sitemap.xml + /robots.txt)** (PR #82 merged 12:49 UTC, +1273 / -2 across 15 files)
  - **`backend/app/services/sitemap.py`** (+362, new): pure-stdlib `xml.etree.ElementTree` renderer over the public-simulation corpus. One `<url>` block per `/share/<id>` (priority 0.8) and per `/watch/<id>` (priority 0.7). Sims sorted by `simulation_id` ascending so two consecutive renders against the same on-disk corpus produce byte-identical XML — lets the route layer set a meaningful ETag if it ever wants to. `<lastmod>` falls back through `updated_at` → `created_at` → `state.json` mtime so a long-lived in-progress sim whose `created_at` is days old still tells the crawler "the artifact changed today". `<changefreq>` is `always` for in-progress sims (belief bars genuinely change every round), `weekly` for completed share entries, `daily` for completed watch entries. Hard cap `MAX_SITEMAP_URLS = 50000` (sitemaps.org 0.9 ceiling).
  - **`backend/app/api/sitemap.py`** (+165, new): blueprint exposing `/sitemap.xml`, `/robots.txt`, and `/api/config/sitemap`. `ENABLE_SITEMAP=false` makes `/sitemap.xml` 404 AND drops the `Sitemap:` line from `robots.txt` — no leak through robots either. `Disallow: /api/` always served regardless of flag — even private deployments need crawler hygiene.
  - **`backend/tests/test_unit_sitemap.py`** (+437, new): 22 tests covering pinned invariants, public/private filtering, `<lastmod>` fallback chain, changefreq semantics, byte determinism (two renders → identical bytes), `MAX_SITEMAP_URLS` cap, `robots.txt` directives, XML round-trip via `ET.fromstring`, and 5 drift-detection guards (route decorators present, blueprint exported + mounted, Config flag declared).
  - **`backend/tests/test_unit_openapi.py`** (+4): registers `sitemap_bp` in the openapi drift-check prefix map (without this entry, the static scanner couldn't see the new routes and flagged them as documented-but-missing — companion commit catching that).
  - **`backend/openapi.yaml`** (+111): full path docs for all three new routes.
  - **`backend/app/config.py`** (+10 / -1): adds `ENABLE_SITEMAP` env flag (default `true`).
  - **`frontend/src/components/EmbedDialog.vue`** (+70): adds the 🔍 search-engine callout block — explains the `Sitemap:` directive, links to Google Search Console submission instructions, copy-button for the canonical sitemap URL.
  - Plus `docs/API.md` (+16), `docs/API.zh-CN.md` (+16), `docs/FEATURES.md` (+21), `.env.example` (+13), `README.md` (+2), `frontend/src/api/simulation.js` (+36).

**Impact:** MiroShark now has two external-discovery surfaces it didn't have yesterday morning. The filtered feed makes "subscribe to my bullish-consensus stream" a one-URL operation in Feedly / n8n / Zapier / Make. The sitemap submits once to Google Search Console and every newly published sim becomes searchable on the next crawl. Both surfaces preserve the `is_public` gate — private sims silently absent. Streak holds: **20 consecutive zero-new-deps PRs** (#57 → #82). Same ±0.2 stance threshold, same stdlib-only posture, same byte-determinism habit as the PR #75 reproduce.json + PR #80 notebook export — the "make the algorithm portable, plug in instance-specific I/O at the boundary" pattern is now the project's house style.

---

## aaronjmars/miroshark-aeon

### Theme 1: Skill Catalog Refresh — 29 New Skills Synced from Upstream Operator Forks
**Summary:** Two sync PRs land in 13 minutes, bringing miroshark-aeon's skill catalog in line with the broader fleet. PR #36 (+1964 / -2 across 11 files) pulls 7 skills from `aeon-agent`. PR #37 (+5696 / -14 across 27 files) pulls 22 skills from `aeon` upstream. All 29 land with `enabled:false` so the operator can choose the rollout cadence in a follow-up. Total catalog goes from ~55 entries to 84 in `skills.json`.

**Commits:**

- `4cbc0dc` — **sync: add 7 skills from aeon-agent** (PR #36 merged 14:32 UTC, +1964 / -2 across 11 files)
  - Added (SKILL.md + `aeon.yml` entry + `skills.json` manifest row each):
    - `auto-merge-agent-prs` (dev, +244 LoC) — auto-merge green agent-authored PRs
    - `fork-cohort` (productivity, +290 LoC) — weekly fork-activation cohort tracker
    - `operator-scorecard` (productivity, +278 LoC) — weekly "was this week worth it?" synthesis
    - `skill-freshness` (productivity, +286 LoC) — daily upstream-file-dependency staleness audit
    - `thread-formatter` (social, +190 LoC) — score today's events, format top as 5-tweet thread
    - `v4-readiness` (productivity, +289 LoC) — per-fork v4 upgrade checklist (workflow_dispatch)
    - `webhook-bridge` (productivity, +183 LoC) — external-event-to-skill bridge
  - **`.github/workflows/webhook.yml`** (+125, new): wiring required for `webhook-bridge`'s `repository_dispatch` handler — the skill description points at the workflow explicitly. Cross-syncs the skill delta between operator forks rather than letting them drift apart.
  - **`skills.json`** (+72 / -2): targeted append, not full regen — file was already ~55 entries behind the 110 dirs on disk; expanding scope here would balloon the diff. Total bumped 55 → 62.

- `7d46423` — **sync: pull 22 skills from aeon upstream** (PR #37 merged 14:45 UTC, +5696 / -14 across 27 files)
  - Added (every skill is SKILL.md + `aeon.yml` entry + `skills.json` row):
    - `ai-framework-watch` (dev, +307 LoC) — weekly competitive intelligence on 9 AI agent frameworks
    - `aixbt-pulse` (crypto, +185 LoC) — twice-daily AIXBT market pulse
    - `contributor-reward` (productivity, +254 LoC) — Monday tier-priced rewards from Sunday's leaderboard
    - `contributor-spotlight` (productivity, +288 LoC) — Sunday weekly POWER-fork human-moment post
    - `create-campaign` (social, +223 LoC + 99 LoC example config) — provision Meta ad campaigns via AdManage.ai (PAUSED)
    - `fleet-state` (productivity, +398 LoC) — Monday weekly fork-cohort + fork-release + spotlight synthesis
    - `fork-contributor-leaderboard` (productivity, +177 LoC) — Sunday cross-fork contributor ranking
    - `fork-release-tracker` (productivity, +252 LoC) — Sunday weekly fork release celebrator
    - `fork-skill-digest` (productivity, +357 LoC) — Sunday divergence digest (fleet vs upstream defaults)
    - `huggingface-trending` (research, +179 LoC) — daily curated HF models/datasets/spaces
    - `monitor-kalshi` (crypto, +190 LoC + 4 LoC watchlist) — daily Kalshi prediction-market mover scan
    - `onboard` (productivity, +130 LoC) — one-shot setup validator
    - `pr-triage` (dev, +248 LoC) — first-touch external-PR triage
    - `price-threshold-alert` (crypto, +266 LoC) — 30-min cron for ATH / ±20% / target crossings
    - `schedule-ads` (social, +186 LoC + 87 LoC example config) — daily AdManage.ai paid-ads scheduler (PAUSED by default)
    - `show-hn-draft` (productivity, +190 LoC) — one-shot Show HN + r/MachineLearning + r/selfhosted drafter
    - `skill-analytics` (productivity, +316 LoC) — Wednesday fleet-level skill-run analytics
    - `skill-graph` (productivity, +153 LoC) — Sunday skill dependency map regenerator
    - `smithery-manifest` (productivity, +281 LoC) — weekly Smithery manifest refresh (PR-on-diff)
    - `star-milestone` (dev, +168 LoC) — daily star-count milestone announcer
    - `star-momentum-alert` (dev, +280 LoC) — daily next-milestone projection on Tue/Wed/Thu HN window
    - `syndicate-article` (social, +220 LoC) — cross-post latest article to Dev.to
  - **`skills.json`** (+234 / -14): 22 new manifest rows plus em-dash normalization noise that covered the small "modified" delta.

**Impact:** miroshark-aeon's skill surface area roughly doubles in 13 minutes. The categories are interesting: 9 new productivity / fleet-state skills, 3 new dev skills (auto-merge, PR triage, framework watch), 3 new crypto skills (kalshi, aixbt, price-threshold), 2 new social skills (create-campaign, schedule-ads — both PAUSED by default for safety since they spend real money), 1 research skill (huggingface-trending), plus weekly retros (operator-scorecard, fleet-state) and onboarding helpers (onboard, v4-readiness, skill-graph). Notable: **two distinct "fleet" skills landed** (`fleet-state` Monday weekly + `fork-skill-digest` Sunday divergence) — first-class acknowledgment that miroshark-aeon now operates as one of multiple operator forks rather than a single-tenant agent.

### Theme 2: Selective Rollout — 6 Skills Enabled, 1 Immediately Reverted
**Summary:** PRs #38 + #39 are the rollout-control follow-up to the sync PRs above, landing 4 + 2 minutes after #37 merged. The pair demonstrates the operator's pre-flight check actually working: enable a coherent stack of comms + visibility skills, then immediately revert the one whose dependency isn't ready.

**Commits:**

- `dfb5e06` — **enable: launch comms + weekly visibility (6 skills)** (PR #38 merged 14:51 UTC, +6 / -6 in `aeon.yml`)
  - `star-milestone` (daily 15:15 UTC) — announce on star milestones
  - `star-momentum-alert` (daily 10:10 UTC) — projects next-milestone date in the Tue/Wed/Thu HN window
  - `thread-formatter` (daily 17:30 UTC) — score today's events, format top one as a 5-tweet thread; silent on quiet days
  - `contributor-spotlight` (Sun 20:00 UTC) — weekly POWER-fork recognition post
  - `operator-scorecard` (Mon 10:30 UTC) — weekly "was this week worth it?" digest
  - `ai-framework-watch` (Mon 08:30 UTC) — weekly competitive intel on 9 AI agent frameworks
  - Each enable is a single `enabled: false` → `enabled: true` flip (6 lines added, 6 deleted). All 6 silent on quiet days per their own SKILL.md contracts — no notification spam if there's nothing to report.

- `ee00289` — **disable: contributor-spotlight (dependency not enabled)** (PR #39 merged 14:53 UTC, +1 / -1 in `aeon.yml`)
  - `contributor-spotlight` runs every Sunday and picks from the latest `fork-cohort` run; but `fork-cohort` is still `enabled:false`. First Sunday firing would have nothing to pick from → reverted the enable until `fork-cohort` gets enabled. Companion change on `aeon-agent`.

**Impact:** Five new daily-or-weekly skills are now part of the live cron — three of them are explicitly built for launch comms (star-milestone, star-momentum-alert, thread-formatter), two are weekly visibility (operator-scorecard, ai-framework-watch). The fact that #39 landed 2 minutes after #38 (without any user-visible breakage) is the pre-flight check pattern working as intended — dependency cycle caught and reverted before the first scheduled firing. **Lesson encoded:** the sync PRs land with `enabled:false` precisely so this kind of dependency cycle can surface in a follow-up enable PR rather than at 3am on a Sunday.

### Theme 3: Self-Improve — Two Feature-Skill Hardening Fixes
**Summary:** Two prompt-level fixes to `skills/feature/SKILL.md` close out recurring failure modes flagged in earlier push-recaps. Both PRs merged today; both single-file or near-single-file diffs.

**Commits:**

- `70fe027` — **improve: stop feature skill from leaking scratch verifiers to repo root** (PR #34 merged 12:46 UTC, +280 / -96 across 7 files)
  - **`skills/feature/SKILL.md`** (+7): explicit "repo root is OFF-LIMITS" guidance pointing scratch scripts at `/tmp/`. Past leaks flagged in the 2026-05-11 push-recap: `sig_smoke.py`, `_smoke_webhook.py`, `.aeon-tmp-verify-trending.py`. The feature skill was running sanity-check scripts (HMAC verifiers, smoke tests, sys.path probes) in the agent repo cwd, and the workflow's blanket `git add -A` was auto-committing them to main as tech debt.
  - **`.gitignore`** (+8): hardens against the past leak shapes (e.g. `sig_smoke.py`, `_smoke_*.py`, `.aeon-tmp-*.py`).
  - **Removed:** `sig_smoke.py` (-31), `_smoke_webhook.py` (-0; zero-byte placeholder), `.aeon-tmp-verify-trending.py` (-58). The three actual leaks from the past three weeks, deleted in the same PR that prevents the next one.
  - `.outputs/self-improve.md` (+9 / -7) + `dashboard/outputs/self-improve-2026-05-12T13-20-40Z.json` (+256, new): scratch-output snapshot of the self-improve run that proposed this PR.

- `01c11a6` — **improve: feature skill grep existing routes before building** (PR #35 merged 13:30 UTC, +28 / -5 in `skills/feature/SKILL.md`)
  - Inserts a new step 6 "Verify the idea doesn't already exist" between codebase read (step 5) and implementation (now step 7). Concrete grep patterns for backend route decorators (Flask `@app.route`, FastAPI `@app.get`, Express `app.get`, Django `path()`, Rails `routes.rb`), SPA router config (Vue Router / React Router), OpenAPI paths, and `docs/FEATURES.md` / `docs/API.md` / `README.md`. If a route or documented surface already covers the same intent, the skill skips the idea and returns to step 2; if all candidates already exist, logs `FEATURE_SKIP: all candidates already implemented` and stops without sending a notification. Subsequent steps renumbered 7–11; in-step cross-reference updated 9 → 10.
  - **Why it landed today:** three of five 2026-05-12 repo-actions ideas were redundant (`/embed/:simulationId` and `/frame/<round_num>` already shipped pre-PR #57). The build cycle caught it — both got the codebase-read no-go — but the exploration cost was real. The grep is ~60 seconds upstream of implementation; each redundant feature-skill run that gets skipped saves a full skill-budget execution.

**Impact:** Both fixes are tiny diffs against high-leverage failure modes. PR #34 cleans up three months of intermittent scratch-file leaks AND prevents the next batch via .gitignore + explicit prompt guidance. PR #35 adds a 60-second grep ahead of every feature-skill run that will save full-skill-budget executions on every redundant idea going forward. Pattern: the self-improve skill is finding lessons in the daily logs and the push-recap article (rather than waiting for a human reviewer to notice them) and turning them into prompt-level fixes the same week the lesson surfaces.

---

## Developer Notes
- **New dependencies:** Zero. Streak holds at **20 consecutive zero-new-deps PRs** on MiroShark (#57 → #82). PR #36 + #37 on aeon don't add Python/Node deps either — they're SKILL.md prose plus YAML/JSON manifest entries.
- **Breaking changes:** None on either repo. PR #81 is strictly additive query knobs (unfiltered URLs unchanged); PR #82 is a new blueprint behind `ENABLE_SITEMAP=true` default (`false` makes both routes 404). The aeon sync PRs land skills with `enabled:false` so they don't perturb the existing cron.
- **Architecture shifts:** MiroShark — the `surface_stats_reader` callback pattern (helper takes a reader function, route plugs in the real implementation) propagates from PR #69 (gallery) into PR #81 (feed). Same shape as the "make the algorithm portable, plug in instance-specific I/O at the boundary" pattern in PR #75 / #79 / #80. aeon — the fleet-state / fork-skill-digest / fork-release-tracker / fork-contributor-leaderboard skills introduce first-class fleet-of-operator-forks vocabulary that previously didn't exist in this repo's skill catalog. miroshark-aeon is now structurally aware that it shares a cron cadence with other forks.
- **Tech debt:** Three leaked scratch files removed (PR #34). `skills.json` is still ~26 entries behind the 110 dirs on disk after PR #36 — targeted appends only; a full regen will land in a follow-up. The `contributor-spotlight` ↔ `fork-cohort` dependency was caught in #39 but other sync'd-skill dependency chains haven't been audited end-to-end yet.

## What's Next
- **MiroShark PRs to monitor:** none open. PR #82 closed out the May-12 batch. Today's `repo-actions` skill produced a fresh 2026-05-14 batch of 5 ideas (Discord+Slack rich notifications, director event timeline, shareable belief chart SVG, comparative run view, private share link) — the lazy-evaluator candidate is "Shareable Belief Chart SVG" since it's also pure-stdlib + already-existing dataset.
- **aeon PRs to monitor:** none open. All six PRs from today merged. Next likely PR is `fork-cohort` enable (would unblock `contributor-spotlight` re-enable). Watch for the first Sunday firing of `contributor-reward` — it depends on `fork-contributor-leaderboard`, also still `enabled:false`. Likely follow-up: a "weekly skills dependency audit" PR that flips the missing dependencies on, or explicitly disables the dependent skills until their inputs exist.
- **Cron health watch:** today is the first day the new daily skills (`star-milestone`, `star-momentum-alert`, `thread-formatter`) will fire — `star-momentum-alert` at 10:10 UTC tomorrow (Friday, NOT in the Tue/Wed/Thu HN window, so should be silent) and `star-milestone` at 15:15 UTC (silent unless a milestone is crossed; currently 1145 → 1200 is the next round-number milestone). `thread-formatter` at 17:30 UTC should attempt a scoring pass over today's events.
- **Streak watch:** zero-new-deps streak at 20 PRs (#57 → #82) on MiroShark. Tomorrow's `feature` skill candidate is "Shareable Belief Chart SVG" via stdlib `xml.etree.ElementTree` — would extend to 21.
