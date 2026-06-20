# Push Recap — 2026-06-20

## Verdict
> SHIPPING — report-agent now generates multilingual sections without reverting to English mid-run

**Shape:** 1 user-visible commit · 0 internal · 0 infra · ~30 bot-filtered  
**Volume:** 1 file changed, +10/−8 lines across 1 commit by 1 author  
**Merged PRs:** 1 (#194 i18n(report-agent): wire language aware prompts through locale registry with English)

---

## aaronjmars/MiroShark

### Locale inheritance fix — report-agent parallel threads

**What this is:** The report generator runs sections in parallel via `ThreadPoolExecutor`. Python's `ContextVar` (which carries the active locale) does not propagate into worker threads automatically — so every section spawned in parallel was silently reverting to English regardless of the simulation's language setting. This commit captures the active locale before the thread pool starts and explicitly restores it inside each worker via `with use_locale(...)`.

**Shipped to users**
- `3e054f4` — i18n(report-agent): wire language aware prompts through locale registry with English constant fallback (#194) — *author: Daniel Andersen (dan-and)*
  - `backend/app/services/report_agent.py`: adds `use_locale` import; captures `get_active_locale()` before the `ThreadPoolExecutor` runs, then wraps `_generate_section_react()` in `with use_locale(_active_report_locale):` inside `_generate_one()`. Without this, parallel report sections lost their locale ContextVar and generated in English even for German/French/etc. simulations. (+10/−8)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none — the `use_locale` context manager is already in `backend/app/utils/i18n.py`; this is a usage-site fix
- **New public surface:** none
- **Tech debt added:** none

## Open threads
- PR #196 open (`test/strengthen-camel-smoke`, by aaronjmars): adds assertions that the camel smoke test returns non-empty message content — not just a non-None response. +21/−0 on `backend/tests/test_smoke_camel_agent.py`. CI running; not yet merged.

---

## aaronjmars/miroshark-aeon

~30 commits by `aeonframework` (cron state updates, skill auto-commits). All match `chore(*)` bot-filter pattern. No user-visible or significant internal work. Skipped.

---

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (30 bot-filtered)
- gh api events: ok (MiroShark events API returned null for PushEvent slice; commits API used directly)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: ~30 (miroshark-aeon chore commits by aeonframework)
- diff-truncated: 0
