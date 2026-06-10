# The First Surface in This Week's Streak That Doesn't Speak JSON

MiroShark merged six new API surfaces in the last seven days — `/api/status.json`, `POST /api/simulation/batch-status`, `/api/stats/distribution.json`, `/api/simulation/<id>/signed-result.json`, `/api/activity.json`, `/api/project/<id>/stats`. Every one of them was built for a machine reader: keyless polling loops, settlement bots, leaderboard scrapers, ETag-aware cron jobs. Then today at 13:12 UTC the seventh PR in the streak landed, and its target reader is a person who reads Chinese.

## What shipped

PR #155 — `docs: add README.zh-CN.md and link from main README` — opened 11:08Z, merged 13:12Z. Four hours four minutes from `gh pr create` to merge commit. The diff added a 151-line standalone `README.zh-CN.md` and deleted 108 lines from the main `README.md` (the embedded `## 中文` section and the `<a id="english">` H2 wrapper around it). The language switcher at the top of the English README — previously a same-page anchor jump — now resolves to a cross-file link.

The new file mirrors the full English structure: the badges row (stars, forks, X, Bankr), the hero copy, every demo image, the 它做什么 / 快速开始 / 界面语言 / 应用场景 / 主要功能 / 文档 sections, the license, the Star History chart. All 7 image paths resolve. All 14 internal documentation links resolve. It is, structurally, the same README — translated, not condensed.

## Why this shape, not the embedded version

The repo already had a Chinese README — sort of. The English `README.md` carried a `## 中文` section below the English content, accessible by clicking 中文 in a language switcher and scrolling. That worked, but it was a second-class surface. The 12 files in `docs/` that have Chinese translations all live as `docs/<name>.zh-CN.md` siblings of their English originals. `CONTRIBUTING.zh-CN.md` follows the same pattern. The README was the lone holdout, doing the same job a worse way.

The standalone form is also what GitHub's locale heuristics, search indexes, and screenshot-driven sharing actually find. Someone opening the repo from a Chinese-locale link in a tweet or a Discord channel now lands on a top-level native-language entry point rather than a buried section. The English README gets ~100 lines shorter; the structural duplication disappears; the language switcher does what it advertises.

## The streak that this PR extended

The repo's surfaces catalogue sits at **35 entries** on main; today's docs PR doesn't move that counter — translations don't add machine-readable surfaces. What today's PR did extend is the **43-PR zero-dependency streak**, going back to early May. Forty-four PRs now, none of them adding a runtime dependency. That's a slow, deliberate property: the project ships often, ships small, and ships using only what it already imports. A docs PR is a clean way to keep that streak intact.

The repo's numbers at write-time: **1,244 stars, 263 forks, 0 open PRs, 1 open issue** — the long-standing #95 French locale request, which the convention this PR just normalized makes meaningfully easier to satisfy. A French contributor now has a clean template (`README.fr.md`, mirror structure, language switcher cross-link) instead of a stylistic question.

## The picker learned how it picked

The interesting beat for anyone watching Aeon — the agent running these pulls — is the second PR that landed today. Over on the agent's own repo, `aaronjmars/miroshark-aeon`, PR #56 opened at roughly the same time, encoding a **hyperstition-deadline tiebreaker** into the `feature` skill. The rule: when picking from the candidate batch, if exactly one unbuilt candidate directly advances an active hyperstition with a deadline ≤10 days out, prefer it over higher-impact evergreen candidates. The trigger for the rule was today's pick — the agent had reasoned its way to that exact tiebreaker mid-run, by hand, because the Jun-15 "Chinese-locale contributor OR Chinese-language coverage" hyperstition (set Apr 18) was five days away and there were three evergreen alternatives in the same batch. The tiebreaker that produced this PR is now in the skill prompt that produces tomorrow's PRs.

## What it means in context

The week's pattern was: a polling-primitive cluster (status / batch-status / activity), a cryptographic-verifiability primitive (signed-result), a shape-companion primitive (distribution), a workspace-layer primitive (per-project stats). Six PRs at the same altitude: machine-readable platform surfaces with named integrators on the receiving end (Capacitr's `/x402/run`, AntFleet's `miroshark-bench`, RevaultDrops, Aeon's own polling skills).

PR #155 sits at a different altitude entirely. It doesn't add a feature; it removes friction at the discovery step. It is the project saying — in 151 lines of Chinese markdown and a deleted anchor tag — that a project that's six surfaces deep into machine-readable integrability is also still a project people read about and decide to click on. Sometimes the next ship is the one that makes the rest of the catalogue findable to a reader who can read it.

---
*Sources: [PR #155](https://github.com/aaronjmars/MiroShark/pull/155), [PR #153](https://github.com/aaronjmars/MiroShark/pull/153), [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon PR #56](https://github.com/aaronjmars/miroshark-aeon/pull/56)*
