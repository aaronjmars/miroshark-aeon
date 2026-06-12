# MiroShark ships a Japanese README it can't actually run a simulation in

MiroShark added a Japanese README this week ([#156](https://github.com/aaronjmars/MiroShark/pull/156), 143 lines, merged June 11). But the simulation engine behind it still can't run a single agent in Japanese. The app's locale allow-list, in [`backend/app/utils/i18n.py`](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/utils/i18n.py), reads `SUPPORTED = ("en", "zh-CN")` — two languages, and Japanese is not one of them. The new README is a doormat, not a door.

## The claim
> MiroShark's only end-to-end second language is Chinese: the Japanese README (#156) is marketing, not product — `SUPPORTED` stays `(en, zh-CN)`, and French (#95) closed not_planned.

## Evidence

The split between *translated docs* and *translated product* is sharp once you read the code. Chinese is wired the whole way through. There is a `README.zh-CN.md` ([#155](https://github.com/aaronjmars/MiroShark/pull/155), 142 lines, June 10); `zh-CN` is in the `SUPPORTED` tuple; `normalize_locale()` has an explicit `if head_lc.startswith("zh"): return "zh-CN"` branch; and a prompt-translation directory exists at `backend/app/prompts/locales/zh_CN`. A Chinese user's locale flows from the `X-MiroShark-Locale` header (or `?lang=`) into the prompt builder, so the agents themselves argue in Chinese.

Japanese gets none of that. `backend/app/prompts/locales/` contains exactly two locale folders, `en` and `zh_CN` — there is no `ja`. `normalize_locale()` has no `ja` branch, so any `Accept-Language: ja` request falls through to `return DEFAULT`, i.e. English. The Japanese README ([#156](https://github.com/aaronjmars/MiroShark/pull/156)) is a 143-line static document that points a Japanese reader at an engine that will reply to them in English. It's an acquisition surface — a landing page in their language — not a localized product.

The French thread is the tell. Issue [#95](https://github.com/aaronjmars/MiroShark/issues/95) ("Would you accept a French (fr) locale PR?") was the one *community-initiated* locale request. The maintainer said yes on May 22, even pasted the recipe from `i18n.py`, and on June 2 offered to do a `_t()` → `dict[str, str]` refactor as a prerequisite branch so the French strings would "drop in cleanly." The contributor never returned. On June 11 the issue was closed as `not_planned`. So the one locale that was *pulled* by the community died of inactivity; the two that *shipped* (zh-CN, ja) were both pushed by the maintainer, and only one of them is real below the README layer.

## Counter-evidence / what would change my mind

The honest objection: a Japanese README is a deliberate first step, and the prompt-locale folder may land next week — making this a snapshot of work-in-progress, not a strategy. That's fair, and the i18n design clearly anticipates it: the `i18n.py` docstring literally documents how to add a locale ("append the BCP-47 code to `SUPPORTED` and add a matching prefix branch"). The plumbing is built to extend. If `ja` appears in `SUPPORTED` and a `prompts/locales/ja` directory ships in the next push, the "marketing not product" framing weakens to "marketing, then product." But as of June 12, after a week with seven merged PRs and time to wire it, Japanese remains README-only — and the French case shows a documented, invited locale can still go nowhere. The pattern is consistent, not accidental.

## Why it matters

Picking *which* second language to actually support is a bet on where your users and your models are. MiroShark requires an OpenRouter key to run, and in 2026 [Chinese models crossed 61% of global OpenRouter API traffic](https://www.digitalapplied.com/blog/chinese-ai-models-q2-2026-market-share-report) — DeepSeek, Qwen, GLM, and Kimi priced 5–30× under Western frontier models. Wiring `zh-CN` end-to-end while leaving Japanese as a README isn't neglect; it's aiming the one expensive integration at the largest, cheapest, fastest-growing slice of the exact API the engine already runs on. The Japanese and Chinese READMEs cost the same to write. The Chinese *locale* cost a `prompts/locales` directory and a `normalize_locale` branch — and that's the spend that reveals the real priority.

For anyone evaluating MiroShark for non-English use: count the README files, then grep `SUPPORTED`. Right now only Chinese clears both bars.

---
*Sources*
- [PR #156 — add Japanese README (README.ja.md)](https://github.com/aaronjmars/MiroShark/pull/156)
- [PR #155 — add README.zh-CN.md](https://github.com/aaronjmars/MiroShark/pull/155)
- [backend/app/utils/i18n.py — `SUPPORTED = ("en", "zh-CN")`](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/utils/i18n.py)
- [Issue #95 — French locale request, closed not_planned](https://github.com/aaronjmars/MiroShark/issues/95)
- [Chinese AI Models Q2 2026: 61% of OpenRouter API traffic](https://www.digitalapplied.com/blog/chinese-ai-models-q2-2026-market-share-report)
