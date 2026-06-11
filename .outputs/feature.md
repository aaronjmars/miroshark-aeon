*Feature Built — 2026-06-11*

Japanese README (README.ja.md)
MiroShark now has a Japanese-language landing page. A native-Japanese reader hitting the GitHub repo can click 日本語 in the language strip and see the project described — the simulate-anything pitch, the Quick Start, the use cases, the full documentation index — without ever touching the English version. It's the second alternate-language root README, following yesterday's Chinese one (PR #155).

Why this matters:
The root README had one language until 24 hours ago, then two. Twelve docs files already had Chinese siblings, but zero `.ja.md` files existed anywhere in the repo. The Japanese audience has been visible since `@m000_crypto`'s Japanese-language coverage on May 17 — the gap was real and the precedent was fresh. This was idea #1 in the Jun-10 repo-actions batch and it was the only candidate where yesterday's just-merged PR provided a mechanically reproducible pattern to mirror.

What was built:
- `README.ja.md` (new, 143 lines): Full Japanese mirror of the English README. Hero tagline rendered as `あらゆるシナリオをシミュレート、$1 以下・10 分未満で`. Feature table, use cases, image alt text, and section headings translated to natural Japanese. Code blocks, env var names, image paths, and endpoint paths remain in English by convention — matches the treatment in `README.zh-CN.md`.
- `README.md` language switcher: `<b>English</b> · 中文` becomes `<b>English</b> · 中文 · 日本語`.
- `README.zh-CN.md` language switcher: `English · <b>中文</b>` becomes `English · <b>中文</b> · 日本語`.

How it works:
The translation strategy was conservative: every image src kept as-is, every CLI command kept verbatim, every docs/ link pointed at the English `docs/*.md` because no `docs/*.ja.md` files exist yet (same fallback pattern the Chinese README already uses for DKG and WAYBACKCLAW). The 中 / EN UI toggle section honestly describes the in-app locale toggle as English / Chinese only — no Japanese UI is wired in the frontend, so the README doesn't promise one. Language switcher edits are one line per file: no layout disruption, no markdown restructuring. Three files changed, 145 insertions, 2 deletions, zero new dependencies, zero backend touches, zero openapi/catalog changes — 44-PR zero-dep streak intact.

What's next:
The `README.ja.md` is the anchor file; `docs/*.ja.md` translations (INSTALL.ja.md, FEATURES.ja.md, CONFIGURATION.ja.md) are the natural follow-ups, same way the Chinese localization unfolded. The Korean and French gaps remain — French has open issue #95 — but the i18n dict-form refactor blocks the in-app side; the README path is unblocked and could ship in parallel.

PR: https://github.com/aaronjmars/MiroShark/pull/156
