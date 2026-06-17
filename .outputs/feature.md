*Feature Built — 2026-06-17 — aaronjmars/MiroShark*

French README + FR language switcher

MiroShark now speaks French. Added README.fr.md — a full French translation of the project README — and wired Français into the language switcher across every README. A French-speaking builder landing on the repo now reads the whole pitch, quickstart, and docs map in their own language, and the in-app selector already had FR live from last week.

Why this matters:
French was the most-requested locale nobody had built — issue #95 asked "would you accept a French PR?" and got closed only because Japanese shipped first; #161 still tracks the ask. PR #184 quietly added the fr/de i18n plumbing two days ago but left no front door: no README.fr.md, no language-row link, and a README still telling people to click an "EN/中 toggle" that's now a four-language selector. The zh-CN README seeded real Chinese coverage. This opens the same door for FR/BE/CA.

What was built:
- README.fr.md (new): complete French translation — same images, code blocks, and doc links as the English README; prose and image alt-text translated. Language row marks Français current, links the other three.
- README.md: added the Français link and rewrote the stale "Interface language" section to describe the real four-locale selector (English / 中文 / DE / FR).
- README.zh-CN.md + README.ja.md: added the Français link so the locale is discoverable from every README.

How it works:
Pure docs — no code touched. The fr locale was already wired and tested via #184 (backend SUPPORTED tuple, frontend i18n.js, LocaleToggle.vue), so this just builds the human-facing entry point on top of plumbing that already exists. Structure mirrors README.ja.md exactly so the four READMEs stay parallel; every doc link reuses the already-passing English links, so CI has nothing new to break.

What's next:
German (README.de.md) is the obvious next locale — de is already in SUPPORTED. And the zh/ja "Interface language" sections still describe the old EN/中 toggle, worth a follow-up sync.

PR: https://github.com/aaronjmars/MiroShark/pull/185
