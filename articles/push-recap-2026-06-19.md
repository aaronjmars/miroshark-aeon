# Push Recap — 2026-06-19

## Verdict
> SHIPPING — German locale live and suggest_scenarios hardened for any language

**Shape:** 4 user-visible commits · 0 internal · 0 infra · ~30 bot-filtered (miroshark-aeon chores)
**Volume:** ~58 files changed, +3264/−2095 lines across 4 commits by 2 authors (aaronjmars, dan-and)
**Merged PRs:** 4 (#188 suggest-scenarios timeout+token, #189 German locale, #190 embed cost pill, #192 JSON salvage)

---

## Top impact today
1. `696f9ad` — German (de) locale: full translation across 8 backend prompt modules + 40+ frontend components. This was the last gap from the earlier fr/zh-CN rollout — DE was in the UI and README but prompts were stubs (`PROMPTS={}`), so sims ran on English internally. Also fixes locale propagation across `ThreadPoolExecutor` workers. (52 files, +2888/−1973)
2. `97e83fc` — JSON salvage for suggest_scenarios. A verbose model in any language can overflow the 1500-token cap, leaving a truncated JSON array that `json.loads` rejects — endpoint silently returned zero suggestions. New `json_repair.py` does two-tier best-effort recovery, also consolidating three copy-pasted salvage blocks in the profile and config generators. (6 files, +306/−119)
3. `09a60cf` — Cost pill on public embed widget. `~$X` appears in the embed meta row once a run completes, surfacing the cost.json figure (#179) exactly where strangers first encounter a MiroShark result. A 403/404 is swallowed so the pill never blocks the embed. (2 files, +68/−1)

---

## aaronjmars/MiroShark

### Full German locale — end-to-end localization complete

**What this is:** MiroShark now runs fully in German from UI through to LLM agent behavior. When a DE-locale user runs a sim, all prompts, profile generation, and sim configuration use German-language instructions. This closes community issue #161, which highlighted that DE was advertised but the prompt stubs were empty, so agents produced English output regardless of the selected locale. A thread-propagation bug where `ContextVar`-based locale got silently dropped across parallel `ThreadPoolExecutor` workers is also fixed — the same pattern was already applied in `wonderwall_profile_generator`; it's now consistent across `simulation_config_generator` too.

**Shipped to users**
- `a9366b2` — fix(simulation): raise suggest-scenarios timeout and token limit (#188)
  - `backend/app/api/simulation.py`: `max_tokens` 700→1500, timeout 20s→40s in `suggest_scenarios` — DE (and other verbose-language) responses were frequently getting truncated at the old cap (+2/−2)

- `696f9ad` — Translation de in Frontend and Agent-Description/Communication (#189)
  - `backend/app/prompts/locales/de/`: 8 modules filled with real German prompt text — `report_agent.py` +326, `social_simulations.py` +168, `graph_tools.py` +112, `ontology.py` +77, `simulation_config.py` +70, `ner_extractor.py` +39, `profile_generator.py` +21, `web_enrichment.py` +42; all were stub `PROMPTS={}` before this PR
  - `backend/app/utils/i18n.py`: `lang_block(locale, fields)` helper extracted, replacing four inline locale→directive dicts across `simulation.py` and `simulation_config_generator.py`; also adds locale restore per ThreadPoolExecutor worker (+31/−0)
  - `backend/app/services/simulation_config_generator.py`: captures `get_active_locale()` before thread fan-out, restores it per worker via `use_locale()` (+24/−11)
  - `backend/app/services/wonderwall_profile_generator.py`: same locale-propagation fix applied to parallel profile generation (+27/−7)
  - `backend/app/api/simulation.py`: `lang_block()` helper used; `WICHTIG: Schreibe…` phrasing for German directives instead of `Write…in German` (+3/−1)
  - `frontend/src/views/Home.vue`: German hero paragraph via `v-if="$isDe()"` / `v-else-if="$isZh()"` / `v-else` chain (+84/−75)
  - `frontend/src/components/`: 40+ components updated to DE string mappings; also fixes Vue template parse errors — curly-quote delimiters in Step2EnvSetup.vue, unterminated template in Step3Simulation.vue, escaped apostrophes in EmbedDialog.vue
  - `frontend/src/i18n.js`: `de` added to locale mapping (+10/−4)
  - `backend/tests/test_unit_prompt_registry.py`: `test_de_has_no_missing_keys_relative_to_en` added — mirrors zh-CN and fr coverage gate (+16/−0)

### Scenario suggestions hardened for any language

**What this is:** `suggest_scenarios` had two compounding failure modes for verbose or slow models — a token cap too tight for non-English output, and no recovery path when truncation left a half-written JSON array. Both are now closed. The salvage logic is implemented as a shared util, replacing three independently copy-pasted fixup blocks that had accumulated in the profile and config generators.

**Shipped to users**
- `97e83fc` — fix(simulation): salvage truncated suggest_scenarios JSON (#192)
  - `backend/app/utils/json_repair.py` (NEW): `close_truncated_json` appends a closing quote for an unterminated trailing string then closes unbalanced brackets; `repair_json` does two tiers — (1) re-close and parse, (2) trim to the last complete `}`/`]`, dropping only the partial trailing element, and retry. For a three-suggestion array clipped mid-third entry, both fully emitted suggestions survive.
  - `backend/app/utils/llm_client.py`: `chat_json(repair_truncated=True)` opt-in added; default strict-parse behavior unchanged (+15/−1)
  - `backend/app/api/simulation.py`: `suggest_scenarios` now calls `chat_json(..., repair_truncated=True)` (+6/−0)
  - `backend/app/services/simulation_config_generator.py`: `_fix_truncated_json` (49 lines) removed, `_try_fix_config_json` delegates to `repair_json` (+10/−49)
  - `backend/app/services/wonderwall_profile_generator.py`: `_fix_truncated_json` (43 lines) removed, `_try_fix_json` delegates to `repair_json` with fallback scraping for partial `bio`/`persona` fields (+25/−68)
  - `backend/tests/test_unit_json_repair.py` (NEW): 12 test cases — bracket/string closing, round-trip valid input, clean-boundary recovery, mid-element trim keeping 2 of 3 suggestions, raw-newline tolerance, garbage/non-string raises `ValueError`, and `chat_json(repair_truncated=True)` opt-in vs. strict-by-default (+130/−0)

### Cost transparency on public embeds

**What this is:** Every public embed now shows the dollar cost of the sim it displays. The cost.json endpoint (PR #179) had been producing data since 2026-06-16 with no UI surface a stranger would ever see. The embed widget is the right place — it's public by definition (publish gate already satisfied), so 403s can't happen there, and it's the first place a non-user encounters a MiroShark result.

**Shipped to users**
- `09a60cf` — feat: show estimated run cost on public simulation embeds (#190)
  - `frontend/src/api/simulation.js`: new `getSimulationCost(simulationId)` fetches the cost.json share-surface blob; rejects on 403 (not published) / 404 (no LLM calls) (+22/−0)
  - `frontend/src/views/EmbedView.vue`: cost fetched after summary loads, only for completed runs; `costLabel` computed as `~$X.XX` for estimates, `<$0.01` for sub-cent runs, empty string suppresses the pill; new `.embed-pill.cost` in meta row with i18n tooltip in EN and 中文 noting it's a lower-bound estimate (+46/−1)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none
- **New public surface:** `backend/app/utils/json_repair.py` (internal import; `close_truncated_json`, `repair_json`); `chat_json(repair_truncated=True)` opt-in parameter (additive, default unchanged); `getSimulationCost(simulationId)` in `frontend/src/api/simulation.js`; `lang_block(locale, fields)` in `backend/app/utils/i18n.py`; DE locale in `frontend/src/i18n.js`
- **Tech debt added:** none — three copy-pasted salvage blocks in profile/config generators were removed and replaced with calls to the shared util
- **Note:** `EmbedView.vue` was touched by both #189 (i18n string refactor, +26/−26) and #190 (cost pill, +46/−1); both merged cleanly to main within the same 90-minute window

## Open threads
- No open PRs on aaronjmars/MiroShark as of run time
- `#192` PR body notes the original truncation bug was misdiagnosed in #187 as "Chinese-specific" — it affects any verbose model in any language; the fix is language-agnostic

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (30 bot-filtered aeonframework chore commits; PR #68 treasury fix was already in 2026-06-18 push-recap and is not re-reported here)
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: ~30 (miroshark-aeon aeonframework chores)
- diff-truncated: 0
