# Push Recap — 2026-06-15

## Verdict
> REFACTORING — round-2 DRY/dead-code cleanup dominates; one community same-origin deploy fix ships alongside.

**Shape:** 1 user-visible commit · 3 internal · 0 infra-only · 25 bot-filtered
**Volume:** 1,561 additions / 567 deletions across 4 commits by 2 authors (aaronjmars, dan-and)
**Merged PRs:** 4 (#159 same-origin API + neo4j bump; #163 round-2 code-quality cleanup; #164 dedup shared helpers; #165 fix LLM-key test)

> Caveat on volume: ~1,200 of the 1,561 added lines are markdown audit reports under `docs/cleanup/` from PR #163. Net source-code change is small and subtractive (more lines deleted than added in real `.py` files).

---

## Top impact today

1. `1a35ba2` — round-2 code-quality cleanup (#163). Extracts a single `safe_load_json` artifact reader that was copy-pasted across 11 read-only services into `backend/app/utils/json_io.py`; consolidates four byte-identical notify test-payload dicts onto one factory; strengthens weak types and removes dead imports. No behavior change — a future hardening of the artifact-read path now lives in one place instead of eleven. (44 files, +1,368/−317, of which ~1,200/+0 are docs)
2. `e01e495` — same-origin API + neo4j 5.26 bump (#159). The frontend now defaults its API base to same-origin `/api` (empty `baseURL`) instead of hardcoded `http://localhost:5001`, so the UI works behind LAN hostnames and reverse proxies; also surfaces server `error`/`message` fields as the rejected promise's message. **First-time external contributor dan-and.** (9 files, +97/−39)
3. `20aa674` — dedup shared helpers (#164). Hoists `utc_iso8601`, `avg_position`, and the public-base-url logic into `utils/timeutils.py`, `utils/belief.py`, `utils/base_url.py`; drops a dead settings import. Pure refactor, −209/+90. (19 files, +90/−209)

---

## aaronjmars/MiroShark

### [Code-quality cleanup — round 2]

**What this is:** A second sweep of internal hygiene across the backend — deduplication, type strengthening, dead-code removal, and a test fix. None of it changes product behavior; it lowers the cost of the *next* change by collapsing copy-pasted logic into shared helpers. The simulation engine (`simulation_runner` / `simulation_manager`) was not touched — a third consecutive engine-frozen week.

**Under the hood**
- `1a35ba2` — round-2 code-quality cleanup (#163)
  - `backend/app/utils/json_io.py`: new 37-line module holding the one `safe_load_json` reader that 11 services (`trajectory_export`, `thread_formatter`, `transcript`, `agent_export`, `project_stats`, `activity_feed`, `platform_status`, `platform_stats`, `outcome_distribution`, `agent_sparklines_service`, `batch_status`) previously each carried inline (+37/−0)
  - `backend/app/services/webhook_service.py`: new `build_test_payload()` factory replaces the byte-identical 13-key test payload dicts in the slack/discord/telegram/email notify modules (+32/−0)
  - `docs/cleanup/round2-*.md`: nine audit reports (DRY, types, unused, cycles, weak-types, defensive, legacy, slop, summary) documenting what was changed and what was deliberately kept (+1,198/−0)
  - Notable honesty in the legacy sweep: the audit concludes the tree is genuinely clean of removable legacy — the only two provably-dead micro-items are author-documented intentional keeps and were left alone to avoid hot-file conflicts
- `20aa674` — dedup shared helpers (#164)
  - `backend/app/utils/timeutils.py`, `utils/belief.py`, `utils/base_url.py`: new homes for `utc_iso8601`, `avg_position`, and public-base-url resolution, previously duplicated across API and service modules (+69/−0 across three new files)
  - `backend/app/services/transcript.py`: `_avg_position` removed and re-imported from `belief.py`; `app/api/settings.py` dead namespace import dropped
- `6c5f0e7` — fix LLM-key test (#165)
  - `backend/tests/test_unit_demographic_grounding.py`: stubs `create_llm_client` in the two generator-wiring tests so they no longer raise `LLM_API_KEY is not configured` in keyless CI (these were failing on `main`); suite back to 1,372 passing (+6/−2)

### [Self-hosting & deployment]

**What this is:** A community PR that makes the app deployable outside a developer's localhost. A self-hoster who opens the UI via a LAN hostname or behind a reverse proxy now gets working API calls without editing source, and API errors surface a readable message instead of a generic axios error.

**Shipped to users**
- `e01e495` — same-origin API calls + neo4j 5.26 bump (#159), by external contributor **dan-and**
  - `frontend/src/api/index.js`: default `baseURL` changed from `http://localhost:5001` to `''` (same-origin `/api`), relying on Vite's dev proxy / a reverse proxy; the response interceptor now extracts `body.error`/`body.message` and rejects with that as the `Error` message (+16/−5)
  - `frontend/vite.config.js`: proxy configuration reworked to route `/api` to the backend (+66/−27)
  - `docker-compose.yml` + `backend/requirements.txt` + `docs/INSTALL*.md`: Neo4j server image bumped 5.15 → 5.26-community and the Python driver floor + install docs aligned to 5.26 for indexing reliability (+~5 across files)
  - `.env.example`: documents the `VITE_API_BASE_URL` knob for production / direct backend access (+7/−0)

---

## Developer notes
- **New dependencies:** none added; Neo4j bumped 5.15 → 5.26-community (server image + Python driver floor) via #159.
- **Breaking changes:** Frontend default `baseURL` is now same-origin (`''`) instead of `http://localhost:5001` (#159). Developers running the frontend separately from the backend must rely on the Vite dev proxy or set `VITE_API_BASE_URL` explicitly — a silent behavior change for anyone who depended on the old hardcoded default.
- **New public surface:** `VITE_API_BASE_URL` env var is now the documented production knob (`.env.example`). New backend internal helper modules (`utils/json_io.py`, `utils/timeutils.py`, `utils/belief.py`, `utils/base_url.py`) — internal, not public API.
- **Tech debt added:** none observed; net debt reduced. Two provably-dead items (`settings.py` redundant import addressed in #164; `frame_metadata.py:235` placeholder) flagged but deliberately deferred per #163's audit.

## Open threads
- `d83131a` — `fix(sync): use GH_GLOBAL + skip dead branches on no-op merge (#62)` merged on **aaronjmars/miroshark-aeon** (the agent repo, author @aaronjmars). Real fix, but out of lane per STRATEGY #5 (framework work belongs to aeon-agent) — noted, not featured.
- Engine still frozen: no commits touched `simulation_runner.py` / `simulation_manager.py` / swarm-agent core. Third consecutive week the merge log served periphery (cleanup, deployment, tests) rather than the simulation engine.
- No open PRs left on aaronjmars/MiroShark after this batch (#159 was yesterday's carried-over top pick, now merged).

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (25 chore auto-commits + 1 out-of-lane fix PR #62)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 25 (aeonframework `chore(...)` cron auto-commits on the agent repo)
- diff-truncated: 0
