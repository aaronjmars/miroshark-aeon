# Push Recap — 2026-04-24

## Overview
Two repos, two substantive PRs in the same ~2-hour window — both merged by Aaron Mars with Aeon as co-author. **aaronjmars/MiroShark** shipped PR #44 *AI Integration · MCP Onboarding*: the bundled `mcp_server.py` is now discoverable from inside the app itself, with copy-paste config snippets for four MCP clients plus a live Neo4j health probe. **aaronjmars/miroshark-aeon** shipped PR #23 *dedup fetch-tweets by tweet ID, not URL*, closing a latent re-notify bug before it could fire. The day's other 31 aeon commits are skill-run bookkeeping (scheduler state updates, cron-success markers, per-skill auto-commits of logs + articles).

**Stats:** 15 files changed, +1,382 / −32 across 2 substantive commits. Plus ~31 automation commits on miroshark-aeon (logs, articles, dashboard outputs, scheduler/cron state).

---

## aaronjmars/MiroShark

### Theme 1: AI Integration · MCP Onboarding (PR #44)

**Summary:** The graph-memory + MCP stack landed on Apr 21 as a direct-push commit (`b20f955`, 17 files, 8 stdio tools) and has been sitting there invisibly ever since — there was no in-app path to wire it into a client. PR #44 closes that gap: a new Settings panel section surfaces the full tool catalog, stamps out per-client JSON snippets using the user's own backend paths, and pings Neo4j so the UI can show "Ready / Neo4j down / Server file missing" at a glance. Positions MiroShark as MCP-native at a moment when Claude Desktop, Cursor, Windsurf, and Continue have all shipped MCP support inside the last six months.

**Commits:**

- `d42fade` — *feat: AI Integration · MCP onboarding panel (Settings + docs) (#44)*
  - **New `backend/app/api/mcp.py`** (+291 lines): `GET /api/mcp/status` endpoint. Ships the 8-tool catalog inline (`list_graphs`, `search_graph`, `browse_clusters`, `search_communities`, `get_community`, `list_reports`, `list_report_sections`, `get_reasoning_trace`) — a deliberate design choice, since the catalog lives in both the API and `mcp_server.py` and is kept honest by a regex-based drift test. `_resolve_paths()` returns absolute on-disk paths (`backend_dir`, `mcp_script`, `python_executable`) so the rendered snippet is copy-paste-ready on the user's machine. `_build_config_snippets()` pre-renders `mcpServers` blocks for Claude Desktop / Cursor / Windsurf (all the same shape) and the distinct `experimental.modelContextProtocolServers` shape for Continue, plus a `fallback_direct` interpreter form. A Neo4j liveness probe is wrapped in a defensive try/except so the panel renders even if the DB is down.
  - **`backend/app/__init__.py` + `backend/app/api/__init__.py`** (+4/−1): register `mcp_bp` at `/api/mcp`.
  - **New `frontend/src/api/mcp.js`** (+24 lines): `getMcpStatus()` wrapper.
  - **`frontend/src/components/SettingsPanel.vue`** (+445/−1): new "AI Integration · MCP" section — health badge, summary grid, client tabs, dark `<pre>` snippet block + copy button with both a clipboard API path and an `execCommand` fallback for non-secure contexts, per-client config-file path, collapsed tool catalog (`▸ 8 tools available`), docs link.
  - **New `backend/tests/test_unit_mcp_api.py`** (+203 lines): 9 offline tests covering tool-catalog drift detection (regex over `mcp_server.py`), payload shape, real-on-disk paths, per-client snippet validity, `mcpServers` wrapper consistency, Continue's distinct config shape, fallback interpreter wiring, and defensive defaults when Neo4j is down.
  - **`docs/MCP.md`** (+144/−17): expanded from Claude-Desktop-only to cover Cursor (`.cursor/mcp.json`), Windsurf (`~/.codeium/windsurf/mcp_config.json`), Continue (`experimental.modelContextProtocolServers`), plus a 5-row troubleshooting matrix; pointer at the new Settings panel.
  - **`README.md`** (+1/−1): MCP row in the docs index now mentions in-app integration.

**Impact:** The on-disk graph + MCP substrate has been shipping since Apr 21 but was completely invisible to users. After PR #44 every operator who opens Settings sees a wired-up MCP panel for their own machine, one copy-click away from having MiroShark's knowledge graph queryable from inside Claude, Cursor, Windsurf, or Continue. This is a direct-lever feature for the 1K-stars-by-Apr-30 sprint (repo-actions Apr 22 idea #3) — MCP discoverability turns every existing MiroShark install into an "add this to your favourite AI editor" pitch.

---

## aaronjmars/miroshark-aeon

### Theme 1: Fetch-tweets dedup hardening (PR #23)

**Summary:** A defensive fix for a latent re-notify bug, picked up by the `self-improve` skill and shipped the same day. Grok returns the same tweet under two different URL shapes across runs — `x.com/<handle>/status/<id>` when it has the full text and `x.com/i/status/<id>` when the tweet is only cited via `content.annotations[]` (the annotation-harvest path introduced by PR #20). 54 of the 115 historical seen URLs (47%) are in the `i/status` form. No duplicate had fired yet, but the URL-matching dedup in `fetch-tweets` was one crossover away from re-notifying the same tweet under two different shapes.

**Commits:**

- `3c469c7` — *improve: dedup fetch-tweets by tweet ID, not URL (#23)*
  - **`skills/fetch-tweets/SKILL.md`** (+7/−5):
    - Step 1 now builds a `SEEN_IDS` set (of numeric tweet IDs) by regex-extracting `/status/(\d+)` from the persistent seen-file (`memory/fetch-tweets-seen.txt`) and the last 3 days of logs — not full URLs.
    - Step 5 matches candidates by ID instead of URL: `x.com/TheGodfath13541/status/2047375217715032115` and `x.com/i/status/2047375217715032115` now collapse to the same entry.
    - A new paragraph documents *why* the dedup is ID-based — tying it explicitly to `scripts/filter-xai-tweets.py`'s existing in-run ID dedup, so the invariant is stated in one place.
    - Seen-file write path is unchanged (step 6b still appends full URLs); extraction happens on read only.
  - **`memory/MEMORY.md`** (+1): "Fetch-Tweets ID-Based Dedup — 2026-04-24" entry added to the Skills Built table.
  - **`memory/logs/2026-04-24.md`** (+8): self-improve section documenting trigger, fix, impact.
  - **`.outputs/self-improve.md`** (+8/−7): rewritten from Apr 22 token-report entry to the new fetch-tweets entry.
  - **New `dashboard/outputs/self-improve-2026-04-24T13-14-11Z.json`** (+245): json-render dashboard spec.
  - **`memory/token-usage.csv`** (+1): self-improve run cost row.

**Impact:** Prevents a future duplicate-notification regression before it lands, and reconciles two dedup models (skill-level + `filter-xai-tweets.py`) under the same ID-matching contract. Zero new deps, zero file moves. Matches the pattern from the PR #21 "XAI Cache Query Validation" + PR #22 "Token-Report XAI Prefetch" run — self-improve picking up fragile-but-not-yet-broken invariants and tightening them before they fail.

### Theme 2: Automation bookkeeping (non-substantive)

~31 commits by `aeonframework` across the window: per-skill `chore(<skill>): auto-commit` pairs plus `chore(cron): <skill> success` markers plus `chore(scheduler): update cron state` updates plus one `log(feature)` entry. These are the byproducts of the day's skill runs — `token-report`, `fetch-tweets`, `tweet-allocator`, `repo-pulse`, `feature` (MCP PR #44), `self-improve` (fetch-tweets PR #23), `repo-actions`, plus the previous evening's `heartbeat` / `project-lens` / `repo-article`. Listed here for completeness; no codebase change.

---

## Developer Notes

- **New dependencies:** None on either repo.
- **New Flask blueprint on MiroShark:** `mcp_bp` at `/api/mcp`; single endpoint (`/status`). Follows the existing `api/__init__.py` registration pattern.
- **Tool-catalog duplication on MiroShark:** the 8-tool list in `backend/app/api/mcp.py` and the actual tool definitions in `backend/mcp_server.py` are deliberately separate. A regex-based unit test in `test_unit_mcp_api.py` scans `mcp_server.py` for `@mcp.tool()` decorators and fails CI if the two drift. This is a pragmatic choice — re-importing the MCP server module into the web API would pull in stdio-only dependencies at Flask boot time.
- **Continue config shape is genuinely different:** Claude Desktop / Cursor / Windsurf all use `{"mcpServers": {"miroshark": {...}}}`. Continue uses `{"experimental": {"modelContextProtocolServers": [{"transport": {"type": "stdio", ...}}]}}`. The new `_build_config_snippets()` handles both.
- **Dedup invariant on aeon:** `SEEN_IDS` now runs over (persistent seen-file ∪ last 3 days of logs). If a tweet ID ever leaves the 3-day log window *and* its URL gets dropped from the seen-file, it would become re-notifiable — but the seen-file is append-only, so this only happens if the seen-file is manually edited. Acceptable trade-off.
- **Breaking changes:** None on either repo.
- **Architecture shifts:** MiroShark adds a first-class "integration discoverability" surface — the pattern is the same one PR #43 (public gallery) used for *published* sims and PR #42 (share card) used for *shared* sims. The user-facing surface keeps catching up with the capability layer underneath.

## What's Next

- **MiroShark open PRs:** 0 on the main branch after PR #44 merged at 13:20 UTC. 798 stars / 149 forks / PR #44 MCP Onboarding merged today. The repo-actions Apr 24 run generated 5 new candidate ideas: Live Simulation Streaming (SSE), Simulation Engagement Leaderboard, Webhook Notification on Completion, "Post to Discord/Slack" Share Button, OpenAPI / Swagger Documentation — all tagged "Small". The 1K-stars-by-Apr-30 sprint needs ~34/day with 6 days left; today added 10 stars.
- **miroshark-aeon open PRs:** 0 after PR #23 merged at 13:20 UTC. Next self-improve candidates are still latent — nothing screaming failure in today's logs.
- **Likely next feature beat on MiroShark:** one of the Apr 24 repo-actions Small picks. The "Post to Discord/Slack" share button and the Webhook Notification on Completion both feed the same distribution loop that share-card + public gallery + MCP onboarding have been laying down all week — each PR adds one more surface where a simulation becomes shareable or addressable from outside the app.
- **Open threads:** Graph-memory stack (direct-pushed Apr 21) now has a user-facing entry point via PR #44; the next expansion would be exposing graph contents *inside* the MiroShark UI itself rather than only through external MCP clients.
