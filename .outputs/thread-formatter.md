*Thread Draft — 2026-06-17*
Topic: MiroShark i18n expansion — EN/中 → EN/中/DE/FR (PRs #184 + #185)

1/ MiroShark has shipped in two languages since launch. today that became four. EN, 中, DE, FR — the i18n layer went from a binary toggle to a proper N-locale system.

2/ the original i18n code was a two-state switch: zh or en. every call site returned one of two strings. no map, no fallback table. adding German meant touching every if-branch in both backend and frontend.

3/ PR #184 replaced the if-else with a keyword-override map. SUPPORTED grows from 2 locales to 4. LocaleToggle.vue goes from a flip to a full selector. adding a new language now means one map entry, not 50 call site edits.

4/ if you're simulating Twitter opinion dynamics and your agent fleet only speaks English and Mandarin, you're not simulating the internet. you're simulating a subset of it. PR #184 is the first step toward changing that.

5/ PR #185 — French README + 4-locale language switcher. https://github.com/aaronjmars/MiroShark/pull/185 🦈

(article: articles/thread-2026-06-17.md)
