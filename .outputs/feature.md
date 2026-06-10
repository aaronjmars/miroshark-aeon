*Feature Built — 2026-06-10*

Chinese README (README.zh-CN.md)
MiroShark's root directory now has a dedicated Chinese-language README that mirrors the full English version. Chinese-speaking developers landing on the repo get a top-level native entry point instead of a buried, condensed `## 中文` anchor inside the English README. It's the same pattern Vue.js, Electron, pandas, and pytorch use to onboard CJK audiences — and the same pattern MiroShark already uses for every doc under `docs/` and for `CONTRIBUTING.zh-CN.md`. The root README was the lone holdout.

Why this matters:
A hyperstition set back in April targets either a Chinese-locale contributor PR or Chinese-language coverage by June 15 — that deadline is 5 days away. The coverage leg already landed (btcbabycow's "米罗莎要来了" tweet from May 16, plus the first JP coverage in mid-May), but the contributor leg is still open. The most active external contributor on the repo by a wide margin — 666ghj, 219 commits — plausibly already maps to that audience but has been navigating an English-first README the whole time. A standalone README.zh-CN.md is the conversion surface for that pipeline. It was also the only time-sensitive idea in the Jun-08 repo-actions batch; the other three unbuilt candidates (Trending Topics, MCP Tool Catalog JSON, Pre-Run Cost Estimator) are evergreen and can wait.

What was built:
- README.zh-CN.md (new, 154 lines): full Chinese README mirroring the English structure 1:1 — badges row, demo image, hero/tagline, sections for what-it-does / quick-start / interface-language / use-cases / features / documentation, license, Star History chart. Replaces the condensed embedded section that was ~60% the depth of the English one.
- README.md (-102 / +3 lines): language switcher changed from in-page anchor to cross-file link to README.zh-CN.md. Removed the embedded Chinese section. Removed the English-anchor H2 wrapper. License trimmed to English-only.

How it works:
Pure documentation PR — no backend route, no openapi changes, no surfaces_catalog.py entry, zero dependencies. The new file uses the same centered-badges-and-images pattern that README.md uses so the two root files render as visual siblings on GitHub. All 7 image paths and all 14 documentation links verified to resolve against the cloned repo before commit. The split also makes the English README shorter and more focused — 143 lines vs. the previous 242.

What's next:
Companion Japanese README from the Jun-02 batch is the natural follow-up. After that, the three remaining Jun-08 evergreen ideas — Trending Topics, MCP Tool Catalog JSON, Pre-Run Cost Estimator — slot into the discovery / analytics / integration gaps the catalog audit surfaced last batch.

PR: https://github.com/aaronjmars/MiroShark/pull/155
