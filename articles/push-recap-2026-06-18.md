# Push Recap — 2026-06-18

## Verdict
> SHIPPING — French (fr) prompt locale complete; sims no longer fall back to English

**Shape:** 1 user-visible · 0 internal · 4 infra · 34 bot-filtered
**Volume:** ~14 files, +735/−135 lines across 5 commits by 1 author
**Merged PRs:** 2 (#186 feat(i18n): translate French (fr) prompt locale + CI coverage gate; #68 fix: token-report treasury fetch)

---

## aaronjmars/MiroShark

### FR prompt locale — from stubs to real

**What this is:** PR #186 fills in the 7 empty `PROMPTS = {}` stubs that #184 shipped two days ago. French-locale sims were silently falling back to English for every agent call — the locale switcher, README, and backend `SUPPORTED` tuple all said `fr` was live, but the prompt registry had nothing to serve. Now it does: all 7 modules translated, a CI coverage gate added so it can't regress.

**Shipped to users**
- `5643802` — feat(i18n): translate French (fr) prompt locale + CI coverage gate (#186)
  - `backend/app/prompts/locales/fr/social_simulations.py`: 9 keys for Twitter/Reddit/Polymarket agent system prompts + persona fragments translated — the social-sim pipeline now instructs agents in French when locale is `fr` (+168/−5)
  - `backend/app/prompts/locales/fr/graph_tools.py`: 14 keys covering sub-query decomposition + full interview pipeline (select/question-gen/summary) in French (+112/−6)
  - `backend/app/prompts/locales/fr/ontology.py`: knowledge-graph ontology designer prompts — 5 keys — now serve French system prompts to the Neo4j graph builder (+77/−6)
  - `backend/app/prompts/locales/fr/simulation_config.py`: 7 keys for timing/event/market/agent-behavior architect prompts in French (+67/−5)
  - `backend/app/prompts/locales/fr/web_enrichment.py`: research-assistant system prompts translated — web-enrichment phase now runs in French (+42/−6)
  - `backend/app/prompts/locales/fr/ner_extractor.py`: NER/relation-extraction system + user prompts in French; adds a French-source rule (mirrors zh-CN rule #8), JSON keys kept in English (+40/−6)
  - `backend/app/prompts/locales/fr/profile_generator.py`: individual + institutional persona-writer system prompts — persona generation now runs in French (+21/−7)
  - `backend/tests/test_unit_prompt_registry.py`: adds `test_fr_has_no_missing_keys_relative_to_en` CI gate (mirrors existing zh-CN gate) + `test_get_prompt_returns_french_for_fr`; any future EN key without a FR sibling now fails CI (+29/−1)

---

## aaronjmars/miroshark-aeon

### Internal: Agent infrastructure — model tier reset + treasury fix

**What this is:** Three consecutive commits by Aaron on 06-17 reset the model configuration — Sonnet 4-6 is now the default for all skills (was Opus 4.8), with Opus 4.8 pinned explicitly on deep-reasoning skills. A follow-up PR (#68) fixes the `treasury=fetch_fail` that broke token-report since 06-16 when BaseScan deprecated its V1 API.

**Infra**
- `d5033d8` — Switch default model to claude-sonnet-4-6: changes root-level `model: claude-opus-4-8` → `model: claude-sonnet-4-6` in aeon.yml; all skills inherit Sonnet unless explicitly overridden (+1/−1)
- `7ee81cc` — Remove redundant per-skill model pins: strips 78 lines of `model: claude-sonnet-4-6` overrides that were duplicating what is now the default; single source of truth (+78/−78)
- `3b3cbd8` — Pin Opus 4.8 on high-reasoning enabled skills: re-adds `model: claude-opus-4-8` to `repo-article` and other skills whose output quality depends on deep reasoning; routine monitoring/ops skills stay on Sonnet (+3/−3)
- `24fe74c` (#68) — Fix token-report treasury fetch: replaces deprecated BaseScan V1 (`api.basescan.org/api?...action=balance` → returns `NOTOK` since 2026-06) with Base public RPC (`https://mainnet.base.org`, `eth_getBalance`, no key). Alchemy stays secondary, WebFetch tertiary. Adds do-not-use notes for both dead endpoints (+97/−11)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** aeon default model changed from `claude-opus-4-8` to `claude-sonnet-4-6` — skills not explicitly pinned now run on Sonnet; only deep-reasoning skills keep Opus 4.8
- **New public surface:** `fr` locale works end-to-end in MiroShark — prompt registry serves real French for all 7 modules; `test_fr_has_no_missing_keys_relative_to_en` enforces it in CI going forward
- **Tech debt added:** none

## Open threads
- German (DE) locale: `de` directory has empty stubs (same state `fr` was in before #186); repo-actions flagged as top pick for 2026-06-19
- Wire cost.json into README Quickstart: carried over from repo-actions for 2+ days, still unmerged

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 34 (aeonframework operational scheduler/cron chores)
- diff-truncated: 0
