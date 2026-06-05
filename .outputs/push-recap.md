*Push Recap — 2026-06-05*
aaronjmars/MiroShark — 2 substantive commits (both Aaron-merged 12:43Z + 13:01Z, 17m apart); aaronjmars/miroshark-aeon — cron churn only.

*Platform-surface family completes — the third leg:* PR #149 ships `GET /api/status.json` as the health-probe sibling to `/api/stats` (corpus shape) and `/api/surfaces.json` (capability catalog). First `/api/*` endpoint deliberately public-without-auth — third review-commit had to actively remove default `internal_auth_guard` to align code to openapi docs, and filter `total_sims` to public+completed so anonymous callers can't infer private/in-flight counts. Catalog 31→32. Built by Aeon.

*Locale-helper contract lockdown — French-locale prep:* PR #148 lands 343 lines of unit tests across 5 i18n helpers (`normalize_locale`, `get_locale`, `t`, `apply_i18n`, `_strip_i18n`, `use_locale`) with zero production-code changes, freezing behaviour ahead of the `dict[str,str]`-form `_t()` refactor that issue #95 (French) needs as prerequisite — refactor touches 195 call sites. Built by a different Aeon instance (`aeon-aaron`), the second non-miroshark-aeon Aeon to ship a MiroShark PR this week.

Key changes:
- `backend/app/services/platform_status.py` new +271 LoC stdlib scanner + envelope builder; tolerant of corrupt `state.json` and dotfile dirs; `ok: true` is a literal anchor for status-page body-matchers, not a derived value
- `backend/tests/test_unit_platform_status.py` new +428 LoC, 28 offline tests including the drift guard for blueprint wiring and OpenAPI coverage
- `backend/tests/test_unit_i18n.py` new +343 LoC, 26 tests including the `t()` "unknown-locale fallback" path that `fr` will exercise on day one

Stats: ~13 files changed, +1,463/-1 lines across 2 commits. PR #149 = 40th consecutive zero-deps PR on MiroShark.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-05.md
