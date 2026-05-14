## Summary

Built the **Search-Engine Sitemap** feature on MiroShark (idea #5 from `repo-actions-2026-05-12.md`) — auto-generated `/sitemap.xml` + `/robots.txt` so Googlebot / Bingbot / DuckDuckBot can crawl every published simulation's `/share/<id>` and `/watch/<id>` pages.

**PR opened:** https://github.com/aaronjmars/MiroShark/pull/82 (`feat/sitemap-xml-search-discovery`)

**Files created/modified (14):**
- `backend/app/services/sitemap.py` (new, ~334 LoC pure stdlib `xml.etree.ElementTree`)
- `backend/app/api/sitemap.py` (new — `sitemap_bp` Blueprint with three routes)
- `backend/tests/test_unit_sitemap.py` (new, 22 offline tests)
- `backend/app/__init__.py`, `backend/app/api/__init__.py`, `backend/app/config.py` (blueprint wiring + `ENABLE_SITEMAP` flag)
- `backend/openapi.yaml` (+111 lines, new `Discovery` tag)
- `frontend/src/api/simulation.js`, `frontend/src/components/EmbedDialog.vue` (new "🔍 Discoverable in web search" callout, bilingual)
- `docs/FEATURES.md`, `docs/API.md`, `docs/API.zh-CN.md`, `README.md`, `.env.example` (full doc coverage)

**Aeon-side updates:**
- `memory/logs/2026-05-14.md` — feature build log entry with design notes + lesson learned
- `memory/MEMORY.md` — Skills Built table updated, Next Priorities re-scoped (May-12 batch fully closed 5/5; logged that 3 of the 5 ideas were redundant)
- Notification staged in `.pending-notify/aeon-feature-sitemap.md` for the workflow's post-run delivery step (sandbox blocks direct `./notify` execution but the post-run dispatcher will pick it up)

**Lesson logged for future `feature` runs:** grep existing routes / SPA paths before committing to a repo-actions idea — two of the May-12 batch ideas (Interactive Embed Widget, Per-Round Belief Snapshot) already existed in the codebase as `/embed/:simulationId` and `/frame/<round_num>`.

**Streak preserved:** 20 consecutive zero-new-deps PRs on MiroShark (#57 → #82).
