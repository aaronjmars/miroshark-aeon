# Push Recap — 2026-05-01

## Overview

Seven substantive commits on `aaronjmars/MiroShark` between 2026-04-30 15:26 UTC and 2026-05-01 13:44 UTC, all by Aaron with `Claude Opus 4.7 (1M context)` co-author signatures. Two themes: **Chinese (zh-CN) localization completes its three-tier rollout** (PR #61 → #62 → #65, plus README polish #63/#64 and a screenshot direct-push) and **the sixth quantitative export surface ships** as PR #66 belief trajectory CSV / JSONL. On the aeon side, the day was scheduled-skill auto-commits only — no substantive work.

**Stats:** ~95 distinct files changed (counting overlap), +7,908 / −2,423 net across 7 substantive commits on MiroShark; miroshark-aeon recorded only auto-commit churn.

---

## aaronjmars/MiroShark

### Theme 1: Chinese (zh-CN) localization completes its three-tier rollout

**Summary:** PR #61 yesterday (Apr 30 15:26 UTC, just after yesterday's recap window closed at 15:16 UTC) shipped the Tier-1 SPA toggle + bilingual README and explicitly carved out two layers as out of scope: backend error strings (Tier 2) and simulation prompts (Tier 3). Both fell within the next five hours. PR #62 closed Tier 2 (138 backend error sites + 10 bilingual `docs/*.md` siblings + locale-aware RSS feed). PR #65 closed Tier 3 — the originally-deferred agent / report-writer prompts — via a new pluggable `app/prompts/locales/<code>/` registry that propagates locale all the way through Flask → ThreadPoolExecutor → simulation subprocess via `MIROSHARK_LOCALE` env var, with a one-time `ZhWarningBanner.vue` flagging the simulation-prompt path as experimental. PRs #63/#64 cleaned up README ordering after #61 had Chinese first; the `11b647a` direct push added the Chinese-UI screenshot the zh-CN README section was referencing.

**Commits:**

- `0034053` — feat: Chinese (zh-CN) UI toggle + localized templates + bilingual README (#61)
  - **NEW** `frontend/src/i18n.js` (+54): locale ref + `tr(en, zh)` helper + global `$tr`, persisted to `localStorage`, surfaced via Vue `app.config.globalProperties`.
  - **NEW** `frontend/src/components/LocaleToggle.vue` (+63): navbar `中 / EN` button, also reused inside SettingsPanel + Home + Explore + the 5-step pipeline header + 6 other views.
  - 30 `.vue` files wrapped: ~1,300 user-visible strings flipped to `$tr(en, zh)` calls. The big ones — `Step2EnvSetup.vue` (+184/−183), `Step3Simulation.vue` (+149/−148), `Step4Report.vue` (+148/−139), `SettingsPanel.vue` (+121/−114), `HistoryDatabase.vue` (+110/−98) — show line counts on the same order as their existing length, i.e. nearly every visible string changed.
  - `frontend/src/api/index.js` (+8/−1): Axios interceptor sends `X-MiroShark-Locale` and `Accept-Language` on every API call.
  - **NEW** `backend/app/utils/i18n.py` (+122): `get_locale(request)` resolution chain (`?lang=` → `X-MiroShark-Locale` → `Accept-Language` → default), `apply_i18n(payload, locale)` walker, `t(en, zh, locale)` fallback helper.
  - `backend/app/preset_templates/*.json` (×6, +96 across all): each of the six preset templates (`campus_controversy`, `corporate_crisis`, `crypto_launch`, `historical_whatif`, `political_debate`, `product_announcement`) gained an embedded `i18n["zh-CN"]` block carrying name / category / description / tags / counterfactual labels — gallery cards swap on the fly via `apply_i18n` at render time, no template fork.
  - `backend/app/api/templates.py` (+21/−15): `/api/templates/list` and `/<id>` apply the locale; error messages localized.
  - `README.md` (+129/−10): a `## 中文` block sits at the top right after the badges with full quick-start, feature table, use cases, docs index. English version follows. Top-of-page `English · 中文` switcher.

- `2d9f823` — feat(i18n): localize backend errors + bilingual docs (#62)
  - `backend/app/api/simulation.py` (+516/−143): the largest single backend touch — the bulk is wrapping every user-facing API error message through `_t(en, zh, locale)`. ~58 distinct error-message sites in this file alone.
  - `backend/app/api/graph.py` (+51/−24), `report.py` (+56/−22), `share.py` (+7/−1), `feed.py` (+3/−0): the other 80 of the 138 error-site touches.
  - `backend/app/services/feed.py` (+35/−12): `render_feed()` gains a `locale` kwarg. `/api/feed.atom?lang=zh-CN` now serves a Chinese channel title + description; `/verified` maps to "MiroShark · 已验证预言"; RSS `<language>` tag flips. Same surface added two days ago in PR #60 just gained a second audience.
  - 10 new `docs/*.zh-CN.md` siblings: ARCHITECTURE (+127), API (+134), CLI (+33), CONFIGURATION (+198), FEATURES (+199), INSTALL (+332), MCP (+183), MODELS (+82), OBSERVABILITY (+59), WEBHOOKS (+183), plus root CONTRIBUTING.zh-CN.md (+30). Each English source also gained a 1-line `<sup>English · [中文](*.zh-CN.md)</sup>` switcher under the H1 (+2 each).
  - INSTALL.zh-CN.md and CONFIGURATION.zh-CN.md given the most attention — the two priority files for a real Chinese onboarding path.
  - Cross-doc links inside the Chinese set rewritten to point at Chinese siblings — the localized docs are internally self-consistent.
  - All 214 backend unit tests pass; `npm run build` clean.

- `441ba54` — docs(readme): put English section above Chinese (#63)
  - `README.md` (+110/−109): mechanical reorder. The top-of-page `English · 中文` switcher and both anchor IDs (`#english`, `#中文`) are unchanged so existing deep links still resolve.

- `28e3123` — docs(readme): move License + Star History below the Chinese section (#64)
  - `README.md` (+8/−12): both belong to the project as a whole, not either language section, so they shouldn't render twice or sit between the two language blocks. Single bilingual `License · 许可证` header at the very bottom.

- `4c2e470` — feat(i18n): Chinese-mode simulation prompts + experimental warning (#65)
  - **NEW** `backend/app/prompts/registry.py` (+159): pluggable prompt registry with `get(key, locale)` dispatch + English fallback.
  - **NEW** `backend/app/prompts/locales/en/{graph_tools,ner_extractor,ontology,profile_generator,simulation_config,social_simulations,web_enrichment}.py` (+522 across 7 files): English source-of-truth extracted from where it was previously hardcoded in `services/*.py`.
  - **NEW** `backend/app/prompts/locales/zh_CN/{graph_tools,ner_extractor,ontology,profile_generator,simulation_config,social_simulations,web_enrichment,report_agent}.py` (+849 across 8 files): full Chinese translations of the 20 prompt sites that previously hardcoded English. `report_agent.py` alone is +330 because the report-writer's prompt set is the longest in the codebase.
  - `backend/app/services/{graph_tools,ontology_generator,report_agent,simulation_config_generator,web_enrichment,wonderwall_profile_generator}.py` (+234/−291 net): hardcoded prompts deleted; calls now route through the registry.
  - `backend/app/storage/ner_extractor.py` (+5/−38), `backend/wonderwall/simulations/{polymarket,social_media}/prompts.py` (+85/−241): prompt-removal cleanup against the registry.
  - `backend/app/utils/i18n.py` (+54/−2): adds `use_locale` context manager so background threads (ThreadPoolExecutor) inherit the request locale.
  - `backend/scripts/run_{parallel,reddit,twitter}_simulation.py` (+10–11 each): each subprocess bootstrap reads `MIROSHARK_LOCALE` and applies it before any prompt is fetched.
  - `backend/app/services/simulation_runner.py` (+12): `start_simulation()` forwards `Config.<resolved locale>` into the subprocess `env` so a Settings UI flip applies on the next run without Flask restart — same pattern PR #59 (Apr 29) used for `WONDERWALL_API_KEY`.
  - **NEW** `frontend/src/components/ZhWarningBanner.vue` (+230): one-time UI banner that surfaces the first time a user toggles to Chinese, explaining that simulation prompts are experimental and structured-output quality may vary by configured LLM. Dismissal persists.
  - `frontend/src/App.vue` (+2): mount the banner.
  - **NEW** `backend/tests/test_unit_prompt_registry.py` (+90): gates zh-CN coverage so future EN additions don't silently regress (any new English prompt key without a Chinese sibling fails the test).

- `11b647a` — docs(readme): add Chinese UI screenshot to zh-CN section
  - `README.md` (+4): inserts the screenshot under the zh-CN section.
  - **NEW** `docs/images/miroshark-cn.jpg`: the actual screenshot. Direct push, no PR.

**Impact:** PR #61 was explicit about Tier 3 (agent prompts, report-writer prompts, simulation content) being out of scope. PR #65 closed it three hours later — Aaron came back the same evening to walk back the carve-out. Net effect: a Chinese-speaking operator now drives the **entire** stack in Chinese — UI, backend errors, docs, simulation agent prompts, report writer, RSS feed metadata — gated behind a single locale toggle that propagates Flask → thread → subprocess. The registry pattern (`app/prompts/locales/<code>/`) is the contribution surface for additional languages: drop a folder mirroring `en/`, missing keys silently fall back to English, and `test_unit_prompt_registry.py` enforces parity. The bilingual docs hit is meaningful operationally — INSTALL.zh-CN.md and CONFIGURATION.zh-CN.md are the two onboarding files a Chinese operator actually reads, and PR #62 prioritized them.

### Theme 2: Sixth quantitative export surface — Belief Trajectory CSV / JSONL

**Summary:** PR #66 ships the row-per-round table for Pandas / Excel / Tableau / R / Observable analysts. Continues the now-canonical `_serve_transcript` pattern (PR #57, Apr 29) — pure stdlib, all data on disk, publish-gated, 60-second cache, ±0.2 stance threshold matches every other surface. The previous five surfaces (share-card / replay GIF / transcript.md / transcript.json / RSS feed) cover the qualitative read of a simulation; trajectory CSV/JSONL is the first surface aimed squarely at the **quantitative** read — variance, autocorrelation, replicate comparison.

**Commits:**

- `3a31d77` — feat: belief trajectory CSV / JSONL export (#66)
  - **NEW** `backend/app/services/trajectory_export.py` (+297, pure stdlib `csv` + `io` + `json`): `compute_stance_split()` with strict-inequality boundary bucketing (exactly ±0.2 ⇒ neutral); `build_rows()` reads `trajectory.json` + `quality.json` and emits one analyst row per snapshot with defensive chronological sort + corrupt-JSON graceful degradation; `_participating_agents()` falls back to `active_agent_count` when `viral_posts` is empty; `render_csv` uses `csv.DictWriter` + `QUOTE_MINIMAL` so numeric columns stay unquoted (`pd.read_csv()` dtype inference works); `render_jsonl` filters output through `CSV_COLUMNS` so upstream changes can't leak unstable keys into JSONL.
  - `backend/app/api/simulation.py` (+93): `_serve_trajectory()` shared body + two route decorators (`@simulation_bp.route('/<simulation_id>/trajectory.csv')` + `.jsonl`), mirroring `_serve_transcript`. Same `_build_embed_summary_payload()` for the publish gate.
  - `backend/openapi.yaml` (+107): both paths under **Publish & Embed** + new `SimulationTrajectoryRow` schema. The OpenAPI drift-detection test (PR #45 contract) passes against the new routes on the first run.
  - **NEW** `backend/tests/test_unit_trajectory.py` (+402, 17 offline tests): STANCE_THRESHOLD parity, strict-inequality boundary bucketing, empty/None/non-numeric input → all-zero split, full 3-snapshot pipeline, chronological reordering on out-of-order on-disk snapshots, missing/corrupt/unparseable-`round_num` graceful degradation, missing-`quality.json` → empty-string fallback, `participating_agents` fallback to `active_agent_count`, locked CSV header column order (10 fields), header emitted on empty input, `csv.DictReader` round-trip (RFC 4180 compliance), `QUOTE_MINIMAL` keeps numeric columns unquoted, JSONL one-object-per-line + field-key order matches `CSV_COLUMNS`, `render_jsonl([])` zero bytes, route-decorator presence guard.
  - `frontend/src/api/simulation.js` (+35): `getTrajectoryCsvUrl` + `getTrajectoryJsonlUrl` helpers.
  - `frontend/src/components/EmbedDialog.vue` (+92): "📊 Export trajectory data" section beneath the transcript row — Download `.csv` + `.jsonl` buttons (publish-gated empty-state copy "Publish the simulation to enable the trajectory export."), copyable CSV URL with Copy URL button, `pd.read_csv("<url>")` quickstart styled as a one-line code block.
  - `README.md` (+1) + `docs/FEATURES.md` (+11) + `docs/API.md` (+29): Features row, dedicated "Belief Trajectory Export (CSV / JSONL)" section, "Analyst quickstart" with Pandas + DuckDB snippets.

**Impact:** Six surfaces, one ±0.2 stance threshold, one folder. The five prior surfaces all serve the qualitative path — preview cards, motion replays, prose transcripts, syndication feeds. Trajectory CSV/JSONL is the first surface targeted at the **research-credibility** path: a quant pastes the URL into `pd.read_csv()` and lands a chronologically-sorted, dtype-inferable, 10-column table. Picked over the four other Apr 30 repo-actions ideas because it's pure stdlib, all data already on disk, and follows the just-shipped `_serve_transcript` pattern — smallest-effort autonomous pick.

---

## aaronjmars/miroshark-aeon

No substantive commits in the recap window. The 25–30 `aeonframework` auto-commits visible in `git log` are scheduled-skill output (`token-report`, `fetch-tweets`, `tweet-allocator`, `repo-pulse`, `feature`, `repo-article`, `project-lens`, `heartbeat`, `push-recap`) plus their `chore(scheduler): update cron state` and `chore(cron): <skill> success` companions. These are runtime artifacts of the schedule itself, not code changes.

---

## Developer Notes

- **New deps:** zero. PR #66 (CSV/JSONL) is pure stdlib; PR #65 (locale prompts) is pure stdlib; PRs #61/#62 are pure JS/Python plus existing `vue-i18n`-style helpers Aaron rolled by hand (`tr(en, zh)`) rather than pulling `vue-i18n`. The README screenshot adds one JPG file. The "zero new deps" streak now spans seven consecutive PRs (PRs #57 transcript, #58 CI, #60 RSS, #61–#66 zh-CN + trajectory).
- **Breaking changes:** none for English users (all locale resolution defaults to English with explicit fallback). For backend consumers: `services/feed.py:render_feed()` gained a `locale` kwarg (positional callers unaffected); `app/api/templates.py` `/api/templates/list` and `/<id>` responses are now locale-applied (English remains identical).
- **Architecture shifts:** new top-level package `backend/app/prompts/` with the locale registry — every hardcoded English prompt previously living in `services/*.py` was extracted into `prompts/locales/en/<topic>.py` and re-imported through the registry. This is a structural change (services no longer own their prompts) but the diff shows it cleanly: each service file shed ~20–80 lines of prompt strings as the registry imports were added.
- **Tech debt:** the agent prompts and report-writer prompts inherited the experimental-grade flag in PR #65's banner. The opt-in path is real (locale flips agent prompt set) but the structured-output quality is LLM-dependent, and there is no eval harness yet — the warning banner is the operator-facing acknowledgment that the eval set lives in a future PR.
- **Test coverage:** PR #62 reports 214 backend unit tests pass. PR #65 adds the prompt-registry parity test (zh-CN coverage gates future EN additions). PR #66 adds 17 trajectory tests on top of the OpenAPI drift-detection test (PR #45 contract) which silently passes against the new endpoints. Net additions today: ~20 unit tests.
- **Pattern consistency:** PR #66 is the third clean reuse of the `_serve_transcript` shared-body pattern (PR #57 Apr 29 introduced it; PR #60 Apr 30 RSS used a sibling `_serve_feed`; PR #66 today is `_serve_trajectory`). The pattern is durable.

## What's Next

- **Localization eval harness for Tier-3 simulation prompts.** PR #65's `ZhWarningBanner.vue` is the user-visible acknowledgment that simulation-prompt quality varies by LLM in Chinese mode. The natural follow-on is an automated eval: fixture set of Chinese prompts × N model presets → structured-output validity rate per (prompt, model) pair. The `test_unit_prompt_registry.py` parity test is the structural floor; the eval is the quality floor.
- **Belief trajectory analytics on top of PR #66.** With CSV / JSONL on disk, downstream surfaces become cheap: variance / autocorrelation badges on gallery cards, divergence-from-replicate comparison, "consensus stability" score on the share card. Repo-actions Apr 30 idea #3 (Batch Rerun / Reproducibility Badge) is the most natural next step — a 3× run with the new trajectory format collapses into a clean reproducibility metric.
- **Apr 30 repo-actions queue resolves by date.** Today's PR #66 closes idea #4. Four Apr 30 ideas remain: #1 Historical Simulation Mode, #2 LLM-as-Judge Audit Panel, #3 Batch Rerun / Reproducibility Badge, #5 Spectator Watch Page. From earlier queues: Apr 28 #1 (Langfuse Cost Breakdown Panel), #4 (Scenario Template Library), #5 (Comparative Run View); Apr 26 #3 / #4 / #5; Apr 24 #1 / #2 / #4; Apr 22 #4 — the backlog of unbuilt ideas is now wider than any single day's pick will close.
- **Open PRs:** none on either repo as of recap time. PR #66 merged 13:44 UTC same-day. Net: 0 open PRs across both watched repos.
