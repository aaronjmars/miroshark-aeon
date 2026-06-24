# Repo Actions — aaronjmars/MiroShark — 2026-06-24

**Top pick for tomorrow:** #1 — Add `stop` CLI subcommand to cancel a running simulation (DX/Feature, Small)
**Verdict:** Five implementable ideas this cycle, all anchored to verified live state; top pick wires the only missing CLI-to-API path — `/stop` has been live in `simulation.py` since the SimulationRunner was built but has no CLI entry point, leaving automation scripts unable to cancel a stuck run even when `wait` (just shipped as #215) detects a timeout.

## Actions

### 1. Add `stop` CLI subcommand to cancel a running simulation
**Priority:** HIGH
**Type:** DX / Feature
**Effort:** Small (hours)
**Anchor:** FILE:backend/cli.py (no `stop` subparser in `build_parser()`; `@simulation_bp.route('/stop', methods=['POST'])` confirmed in `backend/app/api/simulation.py`, takes `{"simulation_id": "sim_xxxx"}`, returns `{"success": true, "data": {"runner_status": "stopped"}}`)
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** `wait` (PR #215, merged today) blocks until a run ends but has no escape hatch — if a simulation hangs, exhausts its timeout, or is simply no longer needed, there is no CLI command to cancel it. The `/stop` endpoint already exists and terminates a running simulation. Adding `stop sim_id` completes the automation lifecycle: `python -m cli wait $SIM || python -m cli stop $SIM` cleanly kills a timed-out run. Every integrator running production pipelines (AntFleet, Capacitr, RevaultDrops) currently has to raw-curl `/api/simulation/stop` to cancel a run — the CLI has had `wait` for hours but still no `stop`.
**How:**
1. In `backend/cli.py`, add `cmd_stop(args)`: call `_api("POST", "/api/simulation/stop", body={"simulation_id": args.simulation_id})`. On success (`res.get("success")`), print `f"{args.simulation_id} stopped"`; on failure, `_die(res.get("error", "stop failed"))`. Add `--json` branch (`_print_json(res)`).
2. In `build_parser()`, add `p_stop = sub.add_parser("stop", help="Stop a running simulation.")`, `p_stop.add_argument("simulation_id")`, `p_stop.set_defaults(func=cmd_stop)`.
3. Update `docs/CLI.md` command table: add `stop <sim_id>` row. Add `## Stop` section showing the `wait || stop` recovery idiom: `python -m cli wait "$SIM" || python -m cli stop "$SIM"`.
4. Update `docs/CLI.zh-CN.md` with equivalent Chinese section.
5. Add `test_stop_subcommand_registered` to `backend/tests/test_unit_cli.py` confirming the subparser exists in the subcommand set (mirrors the existing subcommand-set test from #215).
6. Open as `feat/cli-stop-command` branch PR.
**Definition of done:** `python -m cli stop sim_id` POSTs `{"simulation_id": sim_id}` to `/api/simulation/stop` and exits 0 on stopped; `--json` prints the full response; `docs/CLI.md` documents the command with the `wait || stop` pattern; CI green.

---

### 2. Add LLM model fallback chain to survive OpenRouter deprecations without a restart
**Priority:** HIGH
**Type:** DX / Performance
**Effort:** Medium (1–2 days)
**Anchor:** FILE:backend/app/config.py (line: `LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME') or 'xiaomi/mimo-v2.5'` — single model name, no `LLM_MODEL_FALLBACKS` or fallback array; FILE:backend/app/utils/llm_client.py — no 404 / "model not found" retry path, confirmed via grep)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** The default model has broken clean-install first runs twice in 5 weeks: x-ai/grok-4.1-fast deprecated May 16 (#86), mimo-v2-flash deprecated June 22 (#207). Each event was fixed reactively — a new commit changing the default string, leaving anyone on the old version or a stale `.env` stuck on a model that returns 404 on the first LLM call. An `LLM_MODEL_FALLBACKS` env var (comma-separated model list) and a try-on-404 retry loop in `llm_client.py` means the next deprecation is a soft degradation rather than a crash: the run continues on the fallback model, and a warning goes to the log so the operator knows to update `LLM_MODEL_NAME`. For self-hosters who don't watch the repo closely, this converts a broken install into a working one.
**How:**
1. In `backend/app/config.py`, add `LLM_MODEL_FALLBACKS: list[str] = [m.strip() for m in os.environ.get('LLM_MODEL_FALLBACKS', '').split(',') if m.strip()]`.
2. In `backend/app/utils/llm_client.py`, in the main chat completion call method, wrap the `client.chat.completions.create(...)` call in a try/except for HTTP 404 / `openai.NotFoundError`. On catch, iterate `Config.LLM_MODEL_FALLBACKS`; for each, re-attempt the call with `model=fallback`; log `f"Model {model} returned 404 — falling back to {fallback}"` via `logger.warning`. If all fallbacks fail, re-raise the original error.
3. Add `test_unit_llm_fallback_on_404` to the backend test suite: mock the primary model raising `NotFoundError`, assert the client calls the fallback from `LLM_MODEL_FALLBACKS`, assert the warning is logged.
4. Update `docs/CONFIGURATION.md` with `LLM_MODEL_FALLBACKS` entry and an example: `LLM_MODEL_FALLBACKS=xiaomi/mimo-v2.5,openai/gpt-4o-mini`.
5. Open as `feat/llm-model-fallback-chain` branch PR.
**Definition of done:** With `LLM_MODEL_FALLBACKS=fallback-model` set and primary model returning 404, the engine completes the call using the fallback and logs a warning; test passes; `docs/CONFIGURATION.md` documents the env var; CI green.

---

### 3. Add `--lang` flag to `report` CLI for localized analytical reports
**Priority:** MED
**Type:** DX / Feature
**Effort:** Small (hours)
**Anchor:** FILE:backend/cli.py (`cmd_report` calls `_api("GET", f"/api/report/{args.simulation_id}")` with no locale header; `_api()` signature — `method, path, body=None, params=None, timeout=120.0` — has no `extra_headers` parameter; `backend/app/utils/i18n.py` `SUPPORTED = ("en", "zh-CN", "de", "fr")` with `X-MiroShark-Locale` as the preferred locale header)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** The server generates reports in all 4 supported locales — PR #194 wired the locale registry through the report-agent module. But the CLI sends no locale header, so every `python -m cli report sim_id` produces an English report regardless of the user's language. Chinese self-hosters (#189 DE, #186 FR, #194 EN/ZH prompts) who automate via CLI get English output only. Adding `report --lang zh-CN` and forwarding `X-MiroShark-Locale: zh-CN` to the API enables fully scripted non-English report pipelines — the server already does the work, the CLI just needs to ask.
**How:**
1. In `build_parser()`, add `p_report.add_argument("--lang", choices=["en", "zh-CN", "de", "fr"], default=None, help="Report language (default: server decides from Accept-Language).")`.
2. Update `_api()` helper: add `extra_headers: Optional[dict] = None` parameter. When `extra_headers` is set, merge into the request `headers` dict before constructing `urlrequest.Request`.
3. In `cmd_report`, when `args.lang` is set, call `_api("GET", ..., extra_headers={"X-MiroShark-Locale": args.lang})`.
4. Update `docs/CLI.md` `## Commands` table to note `--lang` on `report`, and add a usage example: `python -m cli report sim_id --lang zh-CN`.
5. Update `docs/CLI.zh-CN.md` equivalently.
6. Open as `feat/cli-report-lang` branch PR.
**Definition of done:** `python -m cli report sim_id --lang zh-CN` returns Chinese-language report text; `--lang de` returns German; no `--lang` flag leaves existing behavior unchanged; CI green.

---

### 4. Add Spanish (ES) locale across the full prompt system
**Priority:** MED
**Type:** Community / Growth
**Effort:** Medium (1–2 days)
**Anchor:** MISSING:backend/app/prompts/locales/es/ (all 4 existing locales — `en/`, `zh_CN/`, `de/`, `fr/` — have 8 prompt module files each; no `es/` directory exists; Spanish has 450M+ native speakers, more than DE+FR combined)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** DE shipped June 19 (#189), FR June 18 (#186) — both expanded the self-hosting audience in Europe. Spanish-speaking researchers in Latin America, Spain, and the US represent a larger addressable audience than DE and FR combined. A complete `es/` locale set (8 files mirroring `de/` structure) + `SUPPORTED` update in `i18n.py` + frontend `i18n.js` entry unlocks Spanish as a first-class simulation language. Pattern is fully established: `de/` is the closest template, with prompt-by-prompt translations across all 8 modules (`graph_tools`, `ner_extractor`, `ontology`, `profile_generator`, `report_agent`, `simulation_config`, `social_simulations`, `web_enrichment`).
**How:**
1. Create `backend/app/prompts/locales/es/__init__.py` (empty package marker, matching `de/__init__.py`).
2. Translate all 8 prompt modules into Spanish, following `de/` as a structural template (same module API, Spanish prompt strings). Use `en/` as the content source where `de/` prompts diverge from expected semantics.
3. Add `"es"` to `SUPPORTED = ("en", "zh-CN", "de", "fr", "es")` in `backend/app/utils/i18n.py`; add branch `if head_lc.startswith("es"): return "es"` in `normalize_locale()`.
4. Add an `es` entry to `frontend/src/i18n.js` for the frontend language selector (mirroring the existing `de` or `fr` entry).
5. Confirm `test_unit_i18n.py` passes with `normalize_locale("es-ES")` → `"es"` and `normalize_locale("es")` → `"es"`.
6. Open as `feat/locale-spanish` branch PR.
**Definition of done:** `X-MiroShark-Locale: es` header routes to Spanish prompts across all 8 modules; `normalize_locale("es-MX")` resolves to `"es"`; frontend shows Español language selector option; existing locale tests still pass; CI green.

---

### 5. Add `--limit N` and `--offset N` to `list` CLI + server-side pagination
**Priority:** MED
**Type:** DX
**Effort:** Medium (1–2 days)
**Anchor:** FILE:backend/cli.py (`cmd_list` calls `_api("GET", "/api/simulation/list")` with no params; FILE:backend/app/api/simulation.py `list_simulations()` route docstring lists only `project_id` query param, no `limit` / `offset`)
**Score:** L=3 C=3 N=5 (total 11/15)
**Impact:** Integrators running automated benchmarks (AntFleet `miroshark-bench`) or research pipelines accumulate hundreds of simulation runs. `python -m cli list` dumps every run with no cap — unwieldy for scripted workflows that need only the latest N or a specific page. Adding `--limit 10 --offset 20` enables standard cursor-paged iteration in scripts. The server-side change is additive: default behavior (`limit=None`) returns the full list unchanged; the CLI change requires no new HTTP surface.
**How:**
1. In `build_parser()`, add `p_list.add_argument("--limit", type=int, default=None, help="Max results to return.")` and `p_list.add_argument("--offset", type=int, default=None, help="Skip first N results.")`.
2. In `cmd_list`, build `params: dict = {}`, populate `params["limit"] = args.limit` and `params["offset"] = args.offset` when not None; pass as `_api("GET", "/api/simulation/list", params=params or None)`. Skip params on the `/api/graph/projects` fallback path (no pagination support there).
3. In `backend/app/api/simulation.py`, `list_simulations()`: read `limit = request.args.get("limit", type=int)` and `offset = request.args.get("offset", type=int)`. After building the result list, apply `items = items[(offset or 0):]`; if `limit` is not None, `items = items[:limit]`. Return the sliced list.
4. Update `docs/CLI.md` `## Commands` table to note `--limit` and `--offset` on `list`, with a script example.
5. Open as `feat/cli-list-pagination` branch PR.
**Definition of done:** `python -m cli list --limit 5` returns at most 5 results; `--offset 10` skips first 10; no flags returns full list (existing behavior); `docs/CLI.md` updated; CI green.

---

## Monitor
<!-- Ideas that failed the implementability gate. Max 3. -->

### A. PR #214 — `fix(interview): Persona-interviews hang prevention, error surfacing`
**Why not yet:** Authored by dan-and (opened 2026-06-23), requires maintainer review and merge decision. Dan-and has a strong track record (#198, #192, #188, #189 all merged cleanly), so this is a high-value unreviewed PR — the blocker is human code review, not implementation.
**Anchor:** PR:#214

### B. PR #213 — `fix(i18n): keep non-English locale in agent actions and report sections`
**Why not yet:** Authored by dan-and (opened 2026-06-23), requires maintainer review. Directly addresses the ongoing locale-drop pattern that has generated 4+ PRs since Jun 18 — if this fixes it, it closes a recurring regression. Blocker: maintainer merge.
**Anchor:** PR:#213

### C. PR #212 — `chore: performance and robustness tuning for local LLM usage`
**Why not yet:** Authored by dan-and (opened 2026-06-23), requires maintainer review. Complements dan-and's local-LLM self-hosting work (SearXNG/Firecrawl/Ollama PR #178) with runtime tuning. Blocker: maintainer merge.
**Anchor:** PR:#212

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** "Loosen `camel-ai==0.2.90` to `>=0.2.90,<0.3.0`" (06-22 top pick, not yet merged, in 14-day novelty window — re-eligible after 2026-07-06)

**Selection rationale:**
- Excluded (novelty — 06-22, in window): camel-ai pin loosen (#1), `wait` CLI (#2 — shipped #215 today), CITATION.cff (#3), `cost` CLI (#4 — shipped #208), FUNDING.yml (#5)
- Excluded (novelty — 06-20, in window): locale thread fix (#1 — shipped #198), README Node prereq (#2), thinking budget (#3 — PR #203 closed unmerged; #209 addressed differently), JA locale (#4), CHANGELOG.md (#5)
- Excluded (novelty — 06-18, in window): DE locale (#1 — shipped #189), PR template (#2), CI badge (#3), cost UI (#4 — shipped #190), camel smoke (#5 — shipped #196)
- Excluded (novelty — 06-16, in window): cost README callout (#1 — shipped), FR locale (#2 — shipped #186), vue-router audit (#3), Python 3.14 Docker (#4)
- Excluded (novelty — 06-14 and 06-12, in window): CODE_OF_CONDUCT.md, SECURITY.md, pip-audit/bandit, API Docs UI, ISSUE_TEMPLATE
- Excluded (implementability → Monitor): PR #212/213/214 — dan-and contributions, maintainer merge needed
- Excluded (Gate 3 uncertainty): EN locale missing `report_agent.py` — PR #194 likely kept EN hardcoded as the default path; cannot confirm the missing file causes failures without reading the locale registry loader; dropped to avoid false premise
- Candidates considered: 10 | Ideas clearing all gates: 5
- Anchor type diversity: FILE (3 distinct: backend/cli.py ×3, backend/app/config.py + llm_client.py, simulation.py), MISSING (1: es/) — ≥3 distinct anchor sources ✅
