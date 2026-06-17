# Push Recap — 2026-06-17

## Verdict
> SHIPPING — German/French i18n foundation + French README live; run-end logs stop reporting 0 actions.

**Shape:** 3 user-visible commits · 0 internal-only · 0 infra-only · 5 bot-filtered (dependabot, already recapped 06-16)
**Volume:** 29 files changed, +507/−56 lines across 3 new merged PRs by 1 author (aaronjmars)
**Merged PRs (new since last recap):** 3 — #184 i18n locale generalization, #185 French README, #183 total_actions fix + camel smoke test

> **Window note:** the 24h window (06-16 15:13 → 06-17 15:13 UTC) also re-spans #181, #182 and the dependabot sweep #167/#168/#175/#176/#177 — all already covered in `push-recap-2026-06-16.md` (cutoff #182). They're excluded from the body below and accounted for in Sources.

---

## aaronjmars/MiroShark

### Internationalization — German & French go from zero to wired

**What this is:** MiroShark had a two-language (`en`/`zh-CN`) i18n layer hardcoded throughout. This window generalizes that layer to N locales, lands German and French as the first additions, and ships the French entry point (README + language selector). A French- or German-speaking visitor now lands on a localized README and can flip the UI to their language; backend prompt locales exist as stubs ready to be filled.

**Shipped to users**

- `b5df64f` — feat(i18n): generalize locale helpers + add German/French foundation (#161, #95) — PR #184 (+230/−49, 22 files)
  - `backend/app/utils/i18n.py`: `SUPPORTED` grows from `("en","zh-CN")` to include `"de"` and `"fr"`; `normalize_locale` gains `de`/`fr` branches; the `t()` helper is rewritten from a binary `if zh` to a keyword-override map `{"zh-CN": zh, "de": de, "fr": fr}` that falls back to English when an override is empty — so untranslated call sites stay English under any locale instead of breaking (+17/−7).
  - `frontend/src/i18n.js`: `SUPPORTED` mirrors the backend list; the old binary `toggleLocale()` becomes a cycle through all four locales; `tr(en, zh, extra)` takes an optional per-locale map (`{ de, fr }`); new `LOCALE_LABELS` (`EN`/`中`/`DE`/`FR`) sizes the nav pill (+17/−4).
  - `frontend/src/components/LocaleToggle.vue`: reworked from a two-state toggle into a full selector rendering all supported locales (+45/−36).
  - `backend/app/prompts/locales/de/` and `…/fr/`: 16 new prompt-module stubs (graph_tools, ner_extractor, ontology, profile_generator, report_agent, simulation_config, social_simulations, web_enrichment) — scaffolding for localized agent prompts, English-fallback for now (+8 each).
  - `backend/tests/test_unit_i18n.py`: extended to assert `de`/`fr` normalization and override behavior (+23/−2).
- `82196bf` — docs(i18n): add French README and wire FR into language switcher (#185) — PR #185 (+147/−4, 4 files)
  - `README.fr.md`: new, full French translation of the project README.
  - `README.md`: adds the FR link to the language row and rewrites the "Interface language" section from a stale EN/中 toggle description into a 4-locale selector.
  - `README.zh-CN.md`, `README.ja.md`: each gains the FR cross-link so every localized README points at the new one.
  - *(This was Aeon's own feature PR for the day — see the 06-17 feature log; it closes the gap #184 left, which added the FR foundation but no French entry point. Addresses open #161, demand from closed #95.)*

### Observability — the run-end log stops lying about action counts

**What this is:** A small but pointed honesty fix in the simulation runner, plus a CI guard. After the camel-ai 0.2.90 episode (where the agent loop silently produced **zero** actions, recapped 06-16), the runner had a second, independent reason to mislead: it hardcoded `total_actions=0` in its end-of-run log regardless of what actually happened.

**Shipped to users / operators**

- `fe6efc3` — fix+ci: correct total_actions reporting + add camel agent smoke test (#181 follow-ups) — PR #183 (+130/−3, 3 files)
  - `backend/scripts/run_parallel_simulation.py`: `log_simulation_end(total_rounds, 0)` was emitting a literal `0` for every platform (Twitter/Reddit/Polymarket) even on fully successful runs; it now threads each platform's real `result.total_actions` into the log. Before this, a perfectly healthy run and a totally dead agent loop logged the same `total_actions=0` — masking the exact failure the camel-ai break produced (+13/−3).
  - **Under the hood:** `backend/tests/test_smoke_camel_agent.py` (new, +78) — a smoke test asserting a camel agent actually produces actions, so a future dependency bump that zeroes the loop fails CI instead of shipping silently.
  - **Infra:** `.github/workflows/tests.yml` (+39) — wires the new smoke test into the CI job.

---

## aaronjmars/miroshark-aeon *(agent repo — internal-only, not featured per STRATEGY #5)*

Two agent-tooling PRs merged, both fixing the `tweet-digest` skill flagged in the 06-16 heartbeat (never-run, no data):

- `6ce2cb0` — feat(tweet-digest): track our own X account daily (@miroshark_) (#66, +7/−1)
- `6bb5bcc` — fix(tweet-digest): add missing prefetch case so the skill can fetch in sandbox (#67, +32/−1)

~28 `aeonframework` cron/auto-commit chores filtered. Out of lane (framework is aeon-agent); noted, not analyzed.

---

## Developer notes
- **New dependencies:** none (all dependabot bumps in the window were already merged & recapped 06-16).
- **Breaking changes:** none. The i18n generalization is backward-compatible by design — `t(en, zh)` and `tr(en, zh)` two-arg call sites keep working; new locales fall back to English until strings are added.
- **New public surface:** two new UI/API locales (`de`, `fr`) in `SUPPORTED` on both backend (`i18n.py`) and frontend (`i18n.js`); `README.fr.md`; `LOCALE_LABELS` export; 16 backend prompt-locale module paths under `app/prompts/locales/{de,fr}/`.
- **Tech debt added:** the `de`/`fr` prompt-locale modules are English-fallback stubs — real translations are deferred. Honest scaffolding, but the locales advertise support the agent prompts don't yet deliver (same EN-only-end-to-end caveat noted for zh-CN/JP in prior recaps).

## Open threads
- No open PRs on aaronjmars/MiroShark at fetch time. The DE/FR prompt-locale stubs are the visible "incomplete by design" surface — each waits on translated strings.
- Engine note: `simulation_runner.py` / `simulation_manager.py` core untouched again. `run_parallel_simulation.py` (the orchestration script) saw its first product-facing edit in a while via the total_actions fix, but the simulation engine proper remains frozen — now a 4th consecutive window.

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (internal-only)
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 5 (dependabot #167/#168/#175/#176/#177 — already recapped 06-16) + ~28 aeonframework chores
- already-recapped-in-window (excluded from body): #181, #182 (cutoff of push-recap-2026-06-16.md)
- diff-truncated: 0
