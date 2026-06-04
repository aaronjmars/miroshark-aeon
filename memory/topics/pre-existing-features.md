# Pre-Existing Features

Ideas that the `repo-actions` skill should NOT regenerate because they have been verified as **already shipped** on the watched repo (under a different name, path, or surface). Sibling registry to `blocked-features.md` — that one is for architecturally-blocked ideas; this one is for ideas where the work is already done.

## Why this list exists

Across May-20 through Jun-01 `repo-actions` batches, at least 8 distinct ideas have been re-suggested after the watched repo already shipped them. The `feature` skill catches these in step 6 (60-second grep upstream) and pivots — but the cost is real:

- Idea slots wasted in `repo-actions` (a 5-of-5 batch can degrade to 1 net-new idea when 4 are pre-existing).
- Operator confusion when notifications surface ideas the repo already has.
- Article clutter and dedup churn (the 7-day in-article dedup ages out and the same idea reappears).

## How this list is used

- **`repo-actions` step 4** reads this file (alongside `blocked-features.md`). For every candidate idea, do a case-insensitive substring match against each entry's signature keywords. If a match hits, exclude the idea from the batch and append a one-line `Excluded (pre-existing): <title> — lives at <path>` note to the article's Selection Rationale section so the operator sees what was filtered.
- **`feature` step 6** also reads this file. If the picked idea matches a pre-existing entry, the feature skill skips it and falls through to the next candidate (same path as a grep hit).
- **No auto-removal.** Unlike `blocked-features.md` (which auto-unblocks when upstream changes lift the constraint), pre-existing entries are permanent — once a feature is shipped, it stays shipped. Entries are only removed if the upstream feature is *deleted* (extremely rare).

## Entry schema

Each entry includes: signature keywords (for exclusion matching), the live path/surface where it exists, the verifying log entry, and the suggestion history that motivated adding it.

## Entries

### Gallery JSON / Public Simulation List
- **Signature keywords:** `gallery json`, `gallery api`, `public simulation list`, `simulation gallery api`, `/api/simulation/public`, `published simulations endpoint`, `list simulations api`
- **Lives at:** `GET /api/simulation/public` — full filter set (consensus / quality / sort / verified), publish-gated, surface_stats counters wired.
- **Verified:** 2026-05-28 by `feature` skill grep (`memory/logs/2026-05-28.md`); re-verified 2026-05-30.
- **Suggestion history:** May-20 #5, May-28 #1.

### Gallery Trending Sort
- **Signature keywords:** `gallery trending`, `trending gallery`, `simulation trending`, `sort by trending`, `?sort=trending`, `trending simulations`
- **Lives at:** `GET /api/simulation/public?sort=trending` — pre-existing query param on the gallery endpoint.
- **Verified:** 2026-06-02 by `feature` skill grep (`memory/logs/2026-06-02.md`).
- **Suggestion history:** Jun-01 #4.

### Compare API
- **Signature keywords:** `compare api`, `comparison api`, `simulation compare`, `compare simulations`, `/api/simulation/compare`, `comparison endpoint`
- **Lives at:** `GET /api/simulation/compare` — paired against `clone.json` (PR #131).
- **Verified:** 2026-05-28 by `feature` skill grep (`memory/logs/2026-05-28.md`).
- **Suggestion history:** May-28 #2.

### Compare UI View
- **Signature keywords:** `compare ui`, `comparison ui`, `comparison view`, `/compare/:id`, `comparisonview.vue`, `compare page`, `comparison page`
- **Lives at:** Frontend route `/compare/:id1?/:id2?` → `ComparisonView.vue` (lazy-loaded view component).
- **Verified:** 2026-06-01 by `feature` skill grep (`memory/logs/2026-06-01.md`).
- **Suggestion history:** May-30 #5.

### RSS / Atom Feed
- **Signature keywords:** `rss feed`, `atom feed`, `simulation rss`, `/api/feed.rss`, `/api/feed.atom`, `rss/atom subscription`, `feed endpoint`
- **Lives at:** `GET /api/feed.rss` + `GET /api/feed.atom` — full filter knobs (consensus / quality / sort / verified), publish-gated, surface_stats counters wired.
- **Verified:** 2026-05-31 by `feature` skill grep (`memory/logs/2026-05-31.md`).
- **Suggestion history:** May-30 #3.

### Per-Sim Surface Engagement
- **Signature keywords:** `per-sim surface engagement`, `surface engagement`, `surface views per sim`, `/surface-stats`, `surface-stats`, `engagement stats per simulation`
- **Lives at:** `GET /api/simulation/<id>/surface-stats` — per-sim engagement counters across surfaces.
- **Verified:** 2026-06-02 by `feature` skill grep (`memory/logs/2026-06-02.md`).
- **Suggestion history:** May-22 #5, Jun-01 #5.

### Webhook Test Ping
- **Signature keywords:** `webhook test ping`, `test webhook`, `webhook ping`, `test-webhook`, `/api/settings/test-webhook`, `verify webhook delivery`
- **Lives at:** `POST /api/settings/test-webhook` + UI button in `SettingsPanel.vue`.
- **Verified:** 2026-05-30 by `feature` skill grep (`memory/logs/2026-05-30.md`).
- **Suggestion history:** May-20 #4, May-28 #4.

### Simulation Search JSON API
- **Signature keywords:** `simulation search api`, `search simulations`, `search json api`, `/api/simulation/search`, `simulation search endpoint`
- **Lives at:** Functionally redundant with `/api/simulation/public` filter set (which already supports filtering by consensus, quality, sort, verified, etc.). A separate `/search` endpoint would duplicate functionality.
- **Verified:** 2026-06-02 by `feature` skill (`memory/logs/2026-06-02.md` — assessed as redundant).
- **Suggestion history:** May-24 #5, Jun-01 #3.
