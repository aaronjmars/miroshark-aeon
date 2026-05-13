# Push Recap — 2026-05-13

## Overview

One substantive feature PR on MiroShark (PR #81, filtered RSS/Atom feed) and the usual daily cron in `miroshark-aeon`. Zero MiroShark merges to `main` in the 24h window — yesterday's PR #80 (Jupyter notebook export) landed at 12:35 UTC on 2026-05-12, just outside the cutoff. Today's work is pure *composition*: stack the gallery's filter knobs (PR #69) onto the feed surface (PR #60) and the syndication channel inherits the entire vocabulary for free.

**Stats:** 8 files changed, +1,280/-37 across the substantive surface (PR #81). 27 auto-commits in `miroshark-aeon` (most are scheduler heartbeats and cron-success markers; ~5 carry actual skill content).

**Window:** 2026-05-12T15:57Z → 2026-05-13T15:57Z.

---

## aaronjmars/MiroShark

### Filtered RSS/Atom Feed (PR #81, opened, not yet merged)

**Summary:** The `/api/feed.atom` and `/api/feed.rss` endpoints (shipped in PR #60) returned every public sim in date order — no way to scope. PR #81 grafts the gallery's existing filter helper (`gallery_filters.select_filtered_cards`, shipped in PR #69 with 33 unit tests) onto the feed surface so the same six query knobs work on syndication: `?q=`, `?consensus=`, `?quality=`, `?outcome=`, `?sort=`, `?limit=`. Filters AND together. Unknown values fall back to "no filter" for that knob (`?consensus=bullsih` returns the full feed) — same graceful-degradation contract the gallery uses.

**Commits:**

- `c83db46` (aaronjmars, 2026-05-13 11:28 UTC) — *feat: filter knobs on /api/feed.atom + /api/feed.rss (consensus / quality / sort / q / outcome / limit)*
  - `backend/app/services/feed.py` (+209/-15): `select_public_cards` gains six keyword args plus a `surface_stats_reader` callback for the trending-sort path; defaults preserve every prior contract. `render_feed` gains the same knobs plus a new `_filter_chip` helper that builds an EN/zh-CN summary of active filters and splices it into the channel title + subtitle ("MiroShark · Public Simulations · Bullish · Excellent · Filtered: …"). Unfiltered feeds keep the original title — no surprise change for existing subscribers. New `MAX_FEED_LIMIT = 50` constant — a smaller cap than the gallery's 100, because aggregators (Feedly, n8n, Zapier) re-fetch feeds aggressively and a 100-item feed is bandwidth waste.
  - `backend/app/api/feed.py` (+72/-11): Parses and normalises the new query params via the existing `gallery_filters.normalise_*` helpers, then plumbs them through to the renderer. Trending sort lazily injects `surface_stats.read_surface_stats` only when the operator opts in; every other sort key keeps the path read-free.
  - `backend/openapi.yaml` (+115/-6): Both `/api/feed.atom` and `/api/feed.rss` document every new param with its enum + default. New params hang off existing paths, so the openapi drift-detection test passes.
  - `backend/tests/test_unit_feed_filters.py` (+622, new): 16 offline tests covering the ±0.2 stance threshold parity for `consensus=` (bullish / bearish / neutral, near-tie exclusion), `quality=` first-word match against `"Good with caveats"`, the logical-AND intersection of `consensus + quality`, `surface_stats_reader` callback wiring on `sort=trending`, graceful fallback on unknown sort keys, case-insensitive `q=` substring, `limit` clamping at `MAX_FEED_LIMIT`, legacy-caller default-limit preservation, `verified_only` still calling the on-disk `outcome_reader` (no regression on PR #60), `render_feed` title/subtitle reflection of active filters, title preservation when no filters are active, `rel="self"` query-string preservation (Substack auto-discovery contract), and a source-side drift guard that the route reads every new query knob.
  - `frontend/src/api/simulation.js` (+38/-3): `getFeedUrl(...)` accepts the full filter set. Defaults / empty params are omitted from the query string so an unfiltered selection produces the same URL as before.
  - `frontend/src/components/EmbedDialog.vue` (+221, additive): New "Build a filtered feed" block beneath the existing Atom/RSS/verified-only callout — three dropdowns (consensus, quality, sort), a live URL preview, and a "Copy filtered feed URL" button wired to a reactive `feedFilters` map. EN + zh-CN strings included; styles use the existing `--color-orange` palette, no new deps.
  - `docs/FEATURES.md` (+3/-2): Extends the "Public Gallery Feeds (RSS / Atom)" section with the filtered-feed bullet, the title-reflection contract, and the Embed dialog filter-builder pointer.

**Notable design call:** The `verified_only` gate stays on the feed side rather than going through `gallery_filters`. Reason — the live gallery card builder doesn't always inline `outcome.json` into the card payload, so trusting an embedded field alone would silently drop legit verified sims. Instead, the on-disk `outcome_reader` callback (same one PR #60 wired) runs BEFORE the rest of the filter stack so trending / pagination math operates on the right corpus.

**Impact:** The feed URL becomes a structured signal source, not a firehose. A trading-signal operator pointing n8n at "bullish + excellent + trending" no longer has to fetch the full feed and filter client-side — the filter goes in the URL, and the channel title tells subscribers which slice they're on. Direct unlock for the Revault / CancerHawk integration class (live integrations named in @Mnosh06's 2026-05-11 deep-tech thread). PR opened by aaronjmars, single Aeon-authored commit; not yet merged at recap time.

---

## aaronjmars/miroshark-aeon

### Daily skill cron (steady-state)

**Summary:** 27 commits today, all from `aeonframework`. Most are scheduler / cron-success markers (`chore(scheduler): update cron state`, `chore(cron): xxx success`) carrying ≤4 lines of state JSON; the substance lives in the five skill content commits below.

**Commits:**

- `7240b78` (06:05 UTC) — *chore(cron): token-report 2026-05-13 — $0.000009780 (-21.6% 24h), FDV $978K, post-ATH retrace*
  - New file `articles/token-report-2026-05-13.md` (+53). Captures the post-ATH retrace: -21.6% 24h, FDV pulled back under the $1M milestone after yesterday's crossing, -38.9% from the May 12 intraday ATH of $0.0000160. Volume still 7-10× pre-ATH baseline ($431K/24h). Buy/sell ratio 1.68× — dip-buying intact.
  - Appends 13-line skill stanza to `memory/logs/2026-05-13.md`.

- `f3b170e` (07:28 UTC) — *chore(fetch-tweets): 4 new $MIROSHARK tweets 2026-05-13*
  - `memory/fetch-tweets-seen.txt` (+4): @cybercelos, @Concept_felipe (×2), @penguinxbt_.
  - `memory/logs/2026-05-13.md` (+11): records the @Concept_felipe NVIDIA/AWS/Azure verifiable-AI-infrastructure framing tweet (11L/7RT) and the @pmarca following sister $AEON signal.

- `d90e49e` (08:24 UTC) — *chore(tweet-allocator): auto-commit 2026-05-13*
  - New file `articles/tweet-allocator-2026-05-13.md` (+19): $10 budget distributed across 3 wallets — @Concept_felipe $6.53 (highest, that's the verifiable-AI-framing tweet), @cybercelos $1.84, @penguinxbt_ $1.63. All pending manual send.
  - New file `dashboard/outputs/tweet-allocator-2026-05-13T08-23-35Z.json` (+210): JSON-render spec for the dashboard.
  - Appends 11 lines to `memory/logs/2026-05-13.md`.

- `adabb38` (10:22 UTC) — *chore(repo-pulse): auto-commit 2026-05-13*
  - `.outputs/repo-pulse.md` (+7/-4): MiroShark now 1,143 stars / 226 forks. **+9 stars in 24h** (DonRuben, smsudip, FelipeDeveloperFullStack, baiyanwu, spontain112, vinayrkumar, DefiClickhouse, CASTvivian, CybrFarhvn06) and **+2 forks** (Eldocdou, Nodal-design). Strong growth despite the price retrace.
  - New file `dashboard/outputs/repo-pulse-2026-05-13T10-21-32Z.json` (+208).

- `ea8ac07` (11:32 UTC) — *chore(feature): auto-commit 2026-05-13*
  - `.outputs/feature.md` (+14/-13): records today's feature work — PR #81 filtered RSS/Atom feed.
  - `memory/MEMORY.md` (+3/-2): adds PR #81 row to the Skills Built table.
  - New file `dashboard/outputs/feature-2026-05-13T11-32-06Z.json` (+205).
  - `.build-target` rotated, token-usage row appended, log stanza appended.

**Impact:** Cron held steady through the second day of the post-ATH retrace. The token-report -21.6% 24h is the largest single-day drawdown in the dataset, but the on-chain narrative (1.68× buy/sell ratio, 7-10× pre-ATH volume baseline, +9 stars / +2 forks) and the social narrative (@pmarca following $AEON, @Concept_felipe NVIDIA-tier enterprise framing) both held the structure intact. The feature skill threaded its third straight clean run (no scratch-verifier leak — PR #34's fix is still pending but the prompt-level guard is preventing the failure mode).

### Aeon self-repair (PR #34, still open)

**Summary:** No new commits on `improve/feature-scratch-cleanup` today. Head is still `08491e4` from 2026-05-12 13:21 UTC. PR opened ~26 hours ago; this exceeds the 24-hour stalled-PR threshold the heartbeat skill flags.

**Impact:** None new today, but the prompt-level fix in `skills/feature/SKILL.md` is already merged into the branch and the feature skill ran cleanly today (no `.py` leak in the repo root — `git status` at recap time shows only `notify/` and `.notify-sent-hashes` as untracked). The `.gitignore` safety net would be belt-and-suspenders; not urgent.

---

## Developer Notes

- **New dependencies:** None. PR #81 is pure stdlib + existing helpers — extends the **19-PR zero-new-deps streak** (#57 → #81). The MIROSHARK repo has not pulled in a new package since 2026-04-17.
- **Breaking changes:** None. PR #81 is additive on both surfaces:
  - Backend: all six new query params are keyword-only with safe defaults. Unfiltered feed URL keeps the original title.
  - Frontend: `getFeedUrl(...)` omits empty params, so a default call produces the same URL as before.
- **Architecture shifts:**
  - PR #81 doubles down on the *composition-over-invention* pattern: the same `gallery_filters.select_filtered_cards` helper now serves both `/api/simulation/public` and `/api/feed.{atom,rss}`. Single source of truth for "which sims match this filter set" — no risk of the gallery and the feed answering the same question differently.
  - The `surface_stats_reader` callback pattern keeps `gallery_filters` Flask-free (the helper takes a reader function; the route plugs in `surface_stats.read_surface_stats`). Lets the 16 new tests run fully offline without spinning up the Flask test client.
- **Tech debt:** PR #34 (aeon self-repair) is now >24h old, but the underlying behavior (scratch verifier leaks) appears to have stopped — the prompt-level fix is doing the job. Consider closing the PR vs. landing the `.gitignore` safety net before it stales further.

## What's Next

- **Most likely next step:** PR #81 merge + repo-article framing the third-party syndication unlock. The PR is `mergeable: true` and the implementation is gated only on a human review — Aaron typically merges Aeon-authored PRs within the day.
- **Open threads:**
  - Per-round belief snapshot API (`GET /api/simulation/<id>/round/<n>`), interactive iframe embeds (`/embed/<id>`), and sitemap.xml for organic discoverability are all called out in PR #81's "What's next" — they're idea #4, #2, #5 from the 2026-05-12 `repo-actions` batch.
  - MiroShark Issue #70 (Cyril Private Impact mode + MiroResult collab) still unblocked; sits 11 days old.
- **Branches created but not merged:**
  - MiroShark `feat/filtered-rss-atom-feed` (PR #81, today, mergeable)
  - aeon `improve/feature-scratch-cleanup` (PR #34, 26h old, mergeable but possibly redundant)
