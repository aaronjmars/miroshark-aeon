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

### Webhook Delivery Log API
- **Signature keywords:** `webhook delivery log`, `webhook log api`, `webhook-log.jsonl`, `delivery history`, `/api/simulation/<id>/webhook-log`, `webhook log endpoint`
- **Lives at:** `GET /api/simulation/<simulation_id>/webhook-log` — admin-token gated, returns last 10 entries + total count from `<sim_dir>/webhook-log.jsonl`. Registered on `simulation_bp` at `backend/app/api/simulation.py:7044`. Service helpers (`webhook_log_path`, `read_webhook_log`) live in `backend/app/services/webhook_service.py:282,401`. Fully documented in `backend/openapi.yaml:3512` + `docs/API.md` Notifications section. Backed by `backend/tests/test_unit_webhook_log.py`.
- **Verified:** 2026-06-05 by `feature` skill grep (`memory/logs/2026-06-05.md`).
- **Suggestion history:** Jun-04 #1.

### Webhook Manual Retry
- **Signature keywords:** `webhook retry`, `webhook manual retry`, `re-fire webhook`, `replay webhook`, `/api/simulation/<id>/webhook-retry`, `re-deliver webhook`
- **Lives at:** `POST /api/simulation/<simulation_id>/webhook-retry` — admin-token gated, re-fires the completion webhook for a finished sim using the real payload + HMAC re-signing; appends a new entry to `webhook-log.jsonl`. Registered on `simulation_bp` at `backend/app/api/simulation.py:7083`. Documented in `backend/openapi.yaml:3556` + `docs/API.md`. Pairs with the Webhook Delivery Log endpoint above.
- **Verified:** 2026-06-05 by `feature` skill grep (`memory/logs/2026-06-05.md`).
- **Suggestion history:** Jun-04 #5.

### Simulation Consensus Timeline / Round-by-Round Summary
- **Signature keywords:** `consensus timeline`, `round-by-round`, `round timeline`, `belief timeline`, `per-round consensus`, `round summary json`, `/timeline`
- **Lives at:** `GET /api/simulation/<simulation_id>/timeline` — returns `{rounds_count, timeline: [...]}` (summary per round); frontend progress bar / round timeline view. Supports `start_round` and `end_round` query params.
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md` — found at simulation.py:3609).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Simulation Quality Breakdown
- **Signature keywords:** `quality breakdown`, `quality details`, `quality endpoint`, `/quality`, `quality surface`, `quality analysis api`
- **Lives at:** `GET /api/simulation/<simulation_id>/quality` — quality breakdown surface (registered on `simulation_bp` at simulation.py:4208).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Belief Drift Analysis
- **Signature keywords:** `belief drift`, `belief-drift`, `drift analysis`, `belief drift surface`, `/belief-drift`
- **Lives at:** `GET /api/simulation/<simulation_id>/belief-drift` — belief drift analytics surface (simulation.py:3822).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Agent Interaction / Influence Network
- **Signature keywords:** `interaction network`, `influence network`, `agent network graph`, `/interaction-network`, `agent influence graph`, `network graph json`
- **Lives at:** `GET /api/simulation/<simulation_id>/interaction-network` — directed interaction graph between agents (simulation.py:10255).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Simulation Transcript Export (Markdown + JSON)
- **Signature keywords:** `transcript export`, `transcript json`, `transcript markdown`, `/transcript`, `simulation transcript`, `debate transcript`
- **Lives at:** `GET /api/simulation/<simulation_id>/transcript.md` + `GET /api/simulation/<simulation_id>/transcript.json` — narrative rendering of the simulation debate (simulation.py:5298,5314). Turns trajectory + quality + resolution artifacts into a readable transcript in both formats.
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Thread / Tweet Thread Export
- **Signature keywords:** `tweet thread`, `twitter thread`, `thread export`, `/thread.txt`, `/thread.json`, `tweetable thread`, `thread surface`
- **Lives at:** `GET /api/simulation/<simulation_id>/thread.txt` + `GET /api/simulation/<simulation_id>/thread.json` — tweet-thread export of simulation outcome (simulation.py:6609,6631).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### BibTeX / Academic Citation Export
- **Signature keywords:** `bibtex`, `cite.bib`, `academic citation`, `latex citation`, `citation export`, `zotero export`, `/cite.bib`
- **Lives at:** `GET /api/simulation/<simulation_id>/cite.bib` — BibTeX `@misc{}` citation entry with stable key, reproduce.json SHA-256, and DKG asset locator (simulation.py:6260).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Jupyter Notebook Export
- **Signature keywords:** `jupyter notebook`, `notebook export`, `ipynb`, `/notebook.ipynb`, `data science export`, `notebook surface`
- **Lives at:** `GET /api/simulation/<simulation_id>/notebook.ipynb` — Jupyter notebook export for trajectory analysis (simulation.py:6814).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Simulation Templates List
- **Signature keywords:** `templates list`, `simulation templates`, `preset templates`, `/api/templates`, `templates api`, `/templates/list`, `template catalog`, `template gallery`
- **Lives at:** `GET /api/templates/list` — returns template summaries (id/name/category/description/icon/difficulty/estimated_agents) with i18n support. `GET /api/templates/capabilities` — returns oracle_seed and MCP tool feature flags. Defined in `backend/app/api/templates.py`.
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery — was going to be idea #3 before audit).

### Per-Agent Activity Statistics
- **Signature keywords:** `agent stats`, `agent activity stats`, `agent activity ranking`, `/agent-stats`, `per-agent stats`, `agent action distribution`
- **Lives at:** `GET /api/simulation/<simulation_id>/agent-stats` — agent activity ranking and action distribution (simulation.py:3649).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Per-Round Frame Snapshot
- **Signature keywords:** `frame snapshot`, `round frame`, `frame metadata`, `/frame/`, `per-round frame`, `round snapshot json`
- **Lives at:** `GET /api/simulation/<simulation_id>/frame/<round_num>` — per-round frame metadata (simulation.py:4413). Separate from `/<id>/frame-metadata` (top-level list).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Simulation Demographics Export
- **Signature keywords:** `demographics export`, `demographics json`, `demographic breakdown`, `/demographics`, `agent demographics api`
- **Lives at:** `GET /api/simulation/<simulation_id>/demographics` — demographic composition of the agent cohort (simulation.py:10758).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Simulation Lineage
- **Signature keywords:** `simulation lineage`, `lineage api`, `sim lineage`, `/lineage`, `fork lineage`, `branch lineage`
- **Lives at:** `GET /api/simulation/<simulation_id>/lineage` — fork/branch lineage graph for a sim (simulation.py:6922).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Counterfactual Analysis
- **Signature keywords:** `counterfactual`, `what-if analysis`, `/counterfactual`, `counterfactual api`, `counterfactual endpoint`
- **Lives at:** `GET /api/simulation/<simulation_id>/counterfactual` — counterfactual scenario analysis (simulation.py:4024).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Reproduce JSON
- **Signature keywords:** `reproduce json`, `reproducibility export`, `/reproduce.json`, `simulation reproducibility`, `parameter snapshot`
- **Lives at:** `GET /api/simulation/<simulation_id>/reproduce.json` — all parameters needed to reproduce the simulation (simulation.py:6724).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Archive / Full Sim Export ZIP
- **Signature keywords:** `archive zip`, `sim archive`, `/archive.zip`, `export zip`, `full sim export`, `simulation download`
- **Lives at:** `GET /api/simulation/<simulation_id>/archive.zip` — full simulation archive (simulation.py:6396).
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).

### Per-Agent Interview Transcripts
- **Signature keywords:** `interview transcript`, `agent interview`, `/interviews/`, `per-agent interview`, `interview export`, `agent interview history`
- **Lives at:** `GET /api/simulation/<simulation_id>/interviews/<agent_name>` — per-agent interview transcript (simulation.py:9916). Batch at `POST /api/simulation/interview/batch`. History at `POST /api/simulation/interview/history`.
- **Verified:** 2026-06-06 by `repo-actions` skill deep audit (`memory/logs/2026-06-06.md`).
- **Suggestion history:** Jun-06 (excluded from batch after discovery).
