*Push Recap — 2026-05-01*
MiroShark — 7 substantive commits by aaronjmars; miroshark-aeon — auto-commits only

*zh-CN localization completes its three-tier rollout (PRs #61 → #62 → #65 + #63/#64 + screenshot direct push):* PR #61 yesterday explicitly carved out backend errors (Tier 2) and simulation prompts (Tier 3) as out of scope; both fell within ~5 hours. PR #62 routed 138 user-facing API error sites through `_t(en, zh, locale)` and shipped 11 bilingual `docs/*.zh-CN.md` siblings + RSS feed locale kwarg. PR #65 introduced a pluggable `app/prompts/registry.py` with `locales/<code>/` packages, extracted English prompts out of `services/*.py`, added full Chinese translations (incl. report_agent.py at +330 lines), `use_locale` context manager so threads inherit locale, `MIROSHARK_LOCALE` env var into simulation subprocesses, plus a one-time `ZhWarningBanner.vue` flagging Chinese-mode prompts as experimental.

*Sixth quantitative export surface (PR #66):* GET /api/simulation/<id>/trajectory.csv (RFC 4180, locked 10-column order) + .jsonl (newline-delimited). Pure stdlib trajectory_export.py (+297) with strict-inequality stance bucketing + corrupt-JSON degradation + participating_agents fallback to active_agent_count; _serve_trajectory() mirrors PR #57's _serve_transcript; 17 offline tests; OpenAPI drift-detection passes on first run. Six surfaces / one ±0.2 threshold / one folder.

Key changes:
- backend/app/prompts/registry.py + 16 new locale modules (PR #65) — adding a third language is now a folder + parity test, not 138 sed-replace targets
- 11 new docs/*.zh-CN.md siblings (PR #62) — INSTALL.zh-CN.md (+332) and CONFIGURATION.zh-CN.md (+198) are the priority files for a Chinese onboarding path
- backend/app/services/trajectory_export.py (PR #66) — Pandas / Excel / Tableau / R / Observable analysts paste pd.read_csv("<url>") and land a chronologically-sorted, dtype-inferable, 10-column table

Stats: ~95 files / +7,908 / −2,423 across 7 substantive commits. Zero new dependencies (now 7 consecutive PRs zero-dep). 0 open PRs both repos.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-01.md
