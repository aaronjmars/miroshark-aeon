# Push Recap — 2026-06-10

## Overview
One substantive shipping event on `aaronjmars/MiroShark`: the PR #155 merge landed the Chinese README as a standalone file, completing the README-internationalisation pattern the rest of the docs tree had already adopted. The agent repo (`aaronjmars/miroshark-aeon`) saw 26 cron / auto-commit churn entries from `aeonframework` — excluded as noise per the May-31 convention encoded in step 5 of this skill — plus three skill-output commits (yesterday's `project-lens` article and a manual self-improve log entry for aeon PR #56). Today's main thrust: shipping the Chinese-locale front door 5 days ahead of the Jun-15 hyperstition deadline, then immediately encoding the deadline-tiebreaker reasoning that picked it.

**Stats:** 5 files changed, +201/-108 lines across 4 substantive commits (26 agent-repo cron auto-commits excluded as noise per the May-31 convention).

---

## aaronjmars/MiroShark

### New Chinese-Locale Front Door (`README.zh-CN.md`)

**Summary:** PR #155 promoted the embedded `## 中文` section out of `README.md` into a dedicated `README.zh-CN.md` file, mirroring the per-file `.zh-CN.md` convention already used by `CONTRIBUTING.zh-CN.md` and 12 `docs/*.zh-CN.md` files. The merged result also restructured the English `README.md` — removing the manual `<a id="english">` / `## English` H2 wrapper and promoting the orphaned H3 subsections (`What it does`, `Quick start`, `Interface language`, `Use cases`, `Features`, `Documentation`) to H2 so the file reads as a single-language README instead of a two-language anchor scaffold. The language switcher near the top now cross-links to the sibling file (`./README.zh-CN.md`) instead of an in-page `#中文` anchor.

**Commits:**
- `4f691c8` — `docs: add README.zh-CN.md and link from main README (#155)`
  - New file `README.zh-CN.md` (+142 lines): full Chinese mirror of the English README — badges row (stars / forks / X / Bankr), hero + demo image embeds, sections 它做什么 / 快速开始 / 界面语言 / 应用场景 / 主要功能 / 文档, license block, Star History chart. Uses the localized overview image `miroshark-overview-cn-v2.jpg` (not the English variant) and points the **其他路径** anchor list at section-specific deep-links into `docs/INSTALL.zh-CN.md` (`#一键云部署`, `#方案-b-docker--本地-ollama`, `#方案-c-手动--本地-ollama`, `#方案-d-claude-code无需-api-密钥`) rather than the bare `INSTALL.zh-CN.md` URL.
  - Modified `README.md` (+9 / −108 lines, net −99): removed the entire embedded `## 中文` block (the section that previously lived inside the English file), dropped the `<a id="english">` anchor and the `## English` H2, promoted the six orphaned H3s to H2, trimmed the bilingual License section to English-only, and changed the switcher chip from `<a href="#中文">中文</a>` to `<a href="./README.zh-CN.md">中文</a>` (with the active "English" side now rendered as bold text rather than a self-link).
  - The merged PR contained two follow-up review commits (also visible in the merge message): one fixing three mis-slugged anchor deep-links into `docs/INSTALL.zh-CN.md`, swapping the overview image to the `-cn-v2` variant, and promoting the orphaned H3s; and one phrasing fix replacing 把 with 个 for API-key quantity and removing a literal 一个 before 预测市场. Co-authors on the merge: `aaronjmars` (final reviewer), `aeonframework` (PR author), `Claude Fable 5` (review commits).

**Impact:** This is the first MiroShark commit that directly addresses the **Jun-15 Chinese-locale hyperstition** ("MiroShark PR from Chinese-locale contributor OR Chinese-language coverage", set 2026-04-18). The Chinese-coverage half of the OR already resolved via btcbabycow's "米罗莎要来了" tweet (May 16); a Chinese-locale contributor PR is still open as a resolution path, and the GitHub-native `README.zh-CN.md` pattern (used by Vue.js, Electron, pandas, pytorch) lowers the friction for 666ghj-class external contributors to land docs PRs in their own locale. The README.md restructure is a quiet secondary win: removing the manual `<a id="english">` / `## English` scaffold means the English README now reads like every other GitHub README — not like a bilingual anchor manifest — which is the larger documentation hygiene wedge the per-file pattern unlocks. Zero deps, no openapi or catalog change, no auth-guard touch. Catalog stays at 35 on `main`.

---

## aaronjmars/miroshark-aeon

The agent repo received 29 commits in the last 24 hours, 26 of which were `aeonframework` cron auto-commits (scheduler state churn, per-skill cron success markers, per-skill auto-commit payloads). Per the May-31 convention encoded in step 5 of this skill, those 26 are excluded as noise — each is already covered in the originating skill's own `## <skill>` section in today's daily log (`memory/logs/2026-06-10.md`) and `memory/logs/2026-06-09.md`. Filtered noise breakdown: 8× `chore(scheduler): update cron state`, 9× `chore(cron): <skill> success` (repo-actions, self-improve, feature, star-momentum-alert, repo-pulse, token-report, heartbeat, thread-formatter, project-lens, repo-article), 9× `chore(<skill>): auto-commit YYYY-MM-DD` (matching the same nine skills).

What remains is three skill-output commits that don't match the strict noise patterns (so the filter keeps them) — surfaced here for completeness:

### Project-Lens Article — Polling vs Webhooks (yesterday, 2026-06-09)

**Summary:** The contrarian project-lens skill committed its 5th essay directly to `main` rather than going through the auto-commit pipeline. The article re-frames PR #153's `activity.json` (the polling-shape endpoint merged Jun 09) against the 2026 agentic-API best-practice creed of webhook-driven + MCP-discoverable.

**Commits:**
- `c7ca1ab` — `project-lens 2026-06-09: Webhooks Won the Argument. Polling Won the Integration. (contrarian #5)`
  - New file `articles/project-lens-2026-06-09.md` (+50 lines). Argues that webhooks are right per-call-efficiency-wise (~90% reduction in wasted polls) and that Anthropic's MCP donation to the Linux Foundation in Dec 2025 + OpenAI's mid-2026 Assistants API sunset in favor of MCP make this the "correct" stack — but that every external integrator that actually wired into MiroShark this spring (Capacitr `/x402/run`, AntFleet `miroshark-bench`, the aeon agent itself) polled. Reasoning: webhooks are great for one consumer with infrastructure, bad for N-unknown consumers where each integration is a bespoke project; polling is the same `curl` + `sleep` every time. Closes by pointing to the 2026 RSS revival and the `feed-mcp` project as parallel evidence, and positions `activity.json` as the 35th surface — discovery-cluster sibling to `feed_atom` and `feed_rss`.
- `3873aeb` — `log: project-lens 2026-06-09 (contrarian #5)` (+12 lines to `memory/logs/2026-06-09.md`)

**Impact:** Operator-voice content artifact; ships under the project-lens cadence, not a code change. No PR, no review, lands straight on `main` like the other content skills.

### Self-Improve Log Entry — Feature Skill Hyperstition Tiebreaker

**Summary:** `aeonframework` committed an additional log entry to `memory/logs/2026-06-10.md` documenting today's self-improve action (aeon PR #56). The PR itself was opened by the self-improve skill earlier; this commit is the log-and-MEMORY-bookkeeping pass that landed alongside the skill's auto-commit but with a distinct commit message.

**Commits:**
- `49bbf96` — `chore(self-improve): log feature-skill hyperstition-tiebreaker improvement` (+16 lines to `memory/logs/2026-06-10.md`, +2 lines to `memory/MEMORY.md`)
  - The log entry captures: trigger (today's feature-skill picked Chinese README #5 over evergreen #2/#3/#4 by reasoning about the Jun-15 deadline in-flight), what changed (new paragraph at bottom of step 2 in `skills/feature/SKILL.md` scoped to step 2.b — reads `Active Targets` in MEMORY.md, finds unresolved hyperstitions with ≤10-day deadline, picks the matching unbuilt candidate over higher-raw-impact evergreen alternatives, multi-match falls back to highest-impact among matched, no-match proceeds unchanged), and the four alternatives the skill considered and rejected (move to repo-actions / widen the 10-day window / hyperstition-weight in step 2.d / hard override). PR #56 (`improve/feature-hyperstition-tiebreaker`) is linked but not yet merged.

**Impact:** Closes the feedback loop on today's feature-skill judgment — yesterday's "lesson" (deadline-aware pick) is encoded mechanically into `skills/feature/SKILL.md` so future runs make the same call without re-deriving it in-flight. Sibling to PR #55 (push-recap noise-exclusion, merged Jun 08) and PR #53 (feature auth-posture, merged Jun 06) — three SKILL.md tightenings in 4 days, all triggered by the operator noticing the agent making the same call repeatedly without it being encoded.

---

## Developer Notes

- **New dependencies:** None. MiroShark zero-deps streak holds at 43 PRs.
- **Breaking changes:** None. README.md restructure removed the `#english` / `#中文` in-page anchors that the language-switcher chip used; any external links to `README.md#english` or `README.md#中文` now 404 to the anchor, though they still resolve to the top of the file. The `[中文](README.md#中文)` link from `README.zh-CN.md`'s language switcher correctly points at the new sibling file (not at the old anchor).
- **Architecture shifts:** MiroShark's README now follows the per-file i18n pattern the rest of the docs tree already used — a small but cumulative documentation-hygiene win. The aeon repo continues to commit skill outputs directly to `main` via two parallel paths (cron auto-commit pipeline + manual content commits), which today produced 29 commits without any merge events.
- **Tech debt:** None introduced. The README.md and README.zh-CN.md license sections diverged in the merge: README.md now carries the English-only license block, README.zh-CN.md carries a Chinese-only version. If a future contributor adds a 3rd-language README (e.g. `README.ja.md`, currently in the Jun-02 unbuilt batch), the per-file pattern means each gets its own localized license block rather than a single bilingual one.

## What's Next

- **PR #155 is merged**, so the immediate Chinese-locale wedge is in main. The Jun-15 hyperstition's contributor-half is still the open resolution path; a Chinese-locale external contributor PR within the next 5 days would close it definitively.
- **PR #56 (miroshark-aeon)** is open — feature-skill hyperstition-tiebreaker — awaiting merge. Once merged, future feature-skill runs will mechanically apply the deadline check.
- **PR #53 (miroshark-aeon)** also still open from Jun-06 — feature auth-posture check.
- **Tomorrow's eligible feature-skill candidates** (per today's repo-actions batch): Japanese README, Scenario Clone Button, Simulation Batch Create API, Simulation Percentile Rank, Platform Performance Metrics. Of these, only the Japanese README would touch a hyperstition — but there's no active JP-locale hyperstition deadline, so the new tiebreaker (once merged) would proceed with the highest-impact pick unchanged. Most likely next ship: one of the three new analytics/integration surfaces.
- **No branches created but not merged today** beyond the ones already noted. PR #154 (polymarket) was closed prior to this window.
