# Repo Actions — aaronjmars/MiroShark — 2026-06-20

**Top pick for tomorrow:** #1 — Fix graph_tools._fallback_interview locale drop across ThreadPoolExecutor (Bug Fix/i18n, Small)
**Verdict:** A freshly-filed bug today and a silent first-run friction mismatch lead the set — top pick (#1) closes the same ThreadPoolExecutor locale-drop class that PR #194 fixed in report_agent this morning, now confirmed in graph_tools by issue #195 filed hours later.

## Actions

### 1. Fix graph_tools._fallback_interview locale drop across ThreadPoolExecutor
**Priority:** HIGH
**Type:** Bug Fix / i18n
**Effort:** Small (hours)
**Anchor:** ISSUE:#195 "i18n: graph_tools._fallback_interview drops locale across ThreadPoolExecutor (same bug as #194)"
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** PR #194 (merged 2026-06-20) fixed the locale-drop bug in report_agent by threading locale explicitly through the locale registry. Issue #195 was filed the same day identifying graph_tools._fallback_interview as the next instance — non-English users (ZH/JA/FR/DE locale selections) receive English-language output from graph_tools steps, breaking the localization promise for ~4 of 5 active app locales in a core simulation component.
**How:**
1. Inspect the PR #194 diff — locate the fix that threads `locale` explicitly through report_agent calls crossing ThreadPoolExecutor boundaries. The pattern passes locale as an explicit argument rather than relying on thread-local state (Flask's `g` or a closure) that doesn't survive thread hops in `concurrent.futures.ThreadPoolExecutor`.
2. Find `graph_tools._fallback_interview` in `backend/app/` — apply the same fix: pass the current request locale as an explicit parameter to any function submitted via `ThreadPoolExecutor.submit()` or `asyncio.run_in_executor()`. Do not capture context-locals in a closure across executor boundaries.
3. Add a test to `backend/tests/` asserting that `_fallback_interview` returns locale-aware output when called with a non-English locale — mirror the locale parity test pattern from `test_unit_prompt_registry.py`.
4. Open as `fix/graph-tools-locale-threadpool` branch PR; body: `closes #195`.
**Definition of done:** `graph_tools._fallback_interview` returns locale-correct output for ZH/FR/DE/JA sessions; a test asserts this; PR body closes #195; CI green.

---

### 2. Fix README Node version prereq: says "Node 18+" but package.json requires ">=22.0.0"
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md#Quick-start ("Prereqs — Python 3.11+, Node 18+") vs FILE:package.json#engines (`"node": ">=22.0.0"`) — the documented prereq contradicts the engine constraint added when Vite 8 (PR #177) and concurrently 10 (PR #167) landed on 2026-06-16
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** A reader following "Node 18+" installs on Node 18, 19, 20, or 21, then silently or noisily fails when Vite 8.0.16 or concurrently 10 enforce the Node 22 floor. First-run failure is the worst outcome for the "$1 first simulation" north-star: it's the exact moment a star converts to an operator. Fixing this is a one-line README edit with zero risk.
**How:**
1. Confirm Vite 8 dropped Node 18/20 support (Vite 8 release notes state Node 22+ as the minimum). The `package.json` engines field `">=22.0.0"` was set correctly; the README was not updated when #177 and #167 merged.
2. Update `README.md` Quick start "Prereqs" from `Node 18+` to `Node 22+`.
3. Search `docs/INSTALL.md` for any mention of `Node 18`, `Node 16`, or `node >=18` — update those lines to `Node 22+` as well.
4. Open as `docs/fix-node-prereq` branch PR — documentation-only change, no code.
**Definition of done:** `README.md` Quick start Prereqs reads "Node 22+"; `docs/INSTALL.md` (if it mentions an older floor) is updated to match; no occurrence of "Node 18" or "Node 16" remains in current install-path docs; CI green.

---

### 3. Implement thinking token budget separation for reasoning-capable models
**Priority:** HIGH
**Type:** Feature / Performance
**Effort:** Medium (1–2 days)
**Anchor:** ISSUE:#193 "Discussion: separate thinking token budget from response token budget for reasoning-capable models"
**Score:** L=4 C=3 N=5 (total 12/15)
**Impact:** MiroShark's `suggest_scenarios` was already silently truncating at a token cap (issues #187/#188) — the same truncation class applies when reasoning models (Claude 4, claude-3-7-sonnet, o1, o3) are used with a single `max_tokens` pool covering both extended thinking and the final response. The "$1" cost promise breaks when users can't reason about the thinking/response budget split. A `THINKING_BUDGET_TOKENS` env var maps directly to Anthropic's `thinking.budget_tokens` and OpenAI's `reasoning_effort`, making cost predictable per model tier.
**How:**
1. Locate where MiroShark sets `max_tokens` in LLM API calls — likely in `backend/wonderwall/` (CAMEL-AI bridge) or `backend/app/services/`. Identify the per-call construction point.
2. Add a `THINKING_BUDGET_TOKENS` env var (int, default: None/unset). Add reasoning-model detection by model ID substring: match `claude-3-7`, `claude-4`, `o1`, `o3`, `o4` — when the active model matches AND `THINKING_BUDGET_TOKENS` is set, inject the appropriate API param: for Anthropic, `thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS}`; for OpenAI o-series, the appropriate `reasoning_effort` or budget param per their API spec.
3. Update `docs/CONFIGURATION.md` env-var table: add `THINKING_BUDGET_TOKENS | int | unset | Thinking token budget for reasoning-capable models (claude-3-7, claude-4, o1, o3); applied separately from max_tokens`.
4. Open as `feat/thinking-budget-tokens` branch PR; body: addresses #193.
**Definition of done:** Running MiroShark with a reasoning model and `THINKING_BUDGET_TOKENS=2000` sets the thinking budget in the API call without affecting `max_tokens` for the response; `docs/CONFIGURATION.md` documents the variable; CI green.

---

### 4. Wire Japanese (JA) through the full locale system: prompt modules + navbar entry
**Priority:** MED
**Type:** Community / i18n
**Effort:** Medium (1–2 days)
**Anchor:** FILE:README.md#Interface-language (Interface language section lists EN/ZH/DE/FR in the navbar switcher but omits Japanese, despite README language bar linking to `README.ja.md` and JP community interest confirmed via @m000_crypto coverage in May)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Japanese was MiroShark's first non-English/Chinese locale (README.ja.md predates FR and DE). After PRs #184→#186→#189→#194 built the full locale registry for EN/ZH/FR/DE, JA is the only language with a README and community evidence but no prompt locale modules and no navbar entry — JA sessions still run on English prompts. Closing this gap replicates the exact flywheel that the ZH-CN README seeded (community pickup, JP @m000_crypto coverage) and that DE/FR replicated.
**How:**
1. Follow PR #186 (FR prompt locale) and PR #189 (DE frontend/agent translations) as exact templates. Create `backend/app/prompts/locales/ja/` with all 7 prompt modules (web_enrichment, ner_extractor, ontology, profile_generator, simulation_config, graph_tools, social_simulations) — mirror the `locales/de/` structure, values translated to Japanese.
2. Add `test_ja_has_no_missing_keys_relative_to_en` + `test_get_prompt_returns_japanese_for_ja` to `backend/tests/test_unit_prompt_registry.py` — mirror the fr/de parity test pair added in prior PRs.
3. Add `ja` to the frontend locale switcher (create `frontend/src/locales/ja.json` if absent; wire `ja` into `normalize_locale` and the navbar locale picker alongside EN/ZH/DE/FR). Update the `Interface language` section in `README.md` to add Japanese.
4. Open as `feat/locale-ja` branch PR; body: "Adds full JA locale parity (prompt modules + navbar). README.ja.md already exists. Mirrors the FR (#186) and DE (#189) pattern."
**Definition of done:** `backend/app/prompts/locales/ja/` has all 7 modules; locale parity tests pass; navbar shows 日本語 as a selectable option; Interface language section in README.md lists Japanese; CI green.

---

### 5. Add CHANGELOG.md generated from merged PRs since v0.1.0
**Priority:** MED
**Type:** Community / DX
**Effort:** Medium (1–2 days)
**Anchor:** MISSING:CHANGELOG.md (196 PRs merged across 14 documented feature areas; no changelog exists despite active integrators — RevaultDrops, AntFleet, Capacitr — tracking changes to decide when to update their deployments)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Production integrators currently track MiroShark changes via `git log` or PR notifications. A CHANGELOG in keep-a-changelog format gives them a structured upgrade reference — and signals release maturity to evaluators who compare changelog presence when choosing a framework dependency. With PR #196 (camel smoke test), cost.json, locale registry, EmbedView cost pill, and websearch all shipping within the last week, this is the ideal moment to open the document.
**How:**
1. Create `CHANGELOG.md` at repo root in [keep-a-changelog](https://keepachangelog.com/) format with a `## [Unreleased]` section and a `## [0.1.0] - Initial release` baseline section.
2. Populate `[Unreleased]` by scanning the last 30 merged PRs (visible from `git log --oneline`), grouped by type prefix: `feat:` → **Added**, `fix:` → **Fixed**, `chore:` → **Changed**, `ci:` → **Changed**, `i18n:` / `docs:` → **Documentation**. Key entries: cost.json endpoint (#179), cost-on-embed (#190), locale registry FR/DE (#184/#186/#189/#194), suggest_scenarios JSON repair (#192), camel smoke test (#183/#196), alternative websearch (#178), agents.json surface (#137), thinking budget (if #3 is implemented).
3. Add a row to the README Documentation table: `Changelog | Notable changes per release` linking to `./CHANGELOG.md`.
4. Open as `docs/changelog` branch PR.
**Definition of done:** `CHANGELOG.md` exists at repo root in keep-a-changelog format; `[Unreleased]` has ≥10 entries spanning the last 30 merged PRs; `README.md` Documentation table links to it; CI green.

---

## Monitor
<!-- Ideas that failed the implementability gate. Surfaced for human decision. Max 3. -->

### A. SECURITY.md — responsible disclosure policy
**Why not yet:** Aeon opened PR #158 on 2026-06-13; maintainer closed it without merging the same day. Autonomous re-open would re-trigger the same rejection. Human decision needed: use GitHub's native "Private vulnerability reporting" (Settings → Security — no separate SECURITY.md required), or accept that the maintainer has chosen not to add a policy at this stage.
**Anchor:** MISSING:SECURITY.md (1,315 stars, AGPL-3.0, 3 confirmed production integrators — RevaultDrops, AntFleet, Capacitr)

### B. pip-audit + bandit security scan in `tests.yml`
**Why not yet:** Adding a job to `.github/workflows/tests.yml` requires pushing to `.github/workflows/` — the Aeon PAT lacks the `workflows` scope. Maintainer has merged CI workflow PRs opened by others (PR #180 frontend build, PR #183 camel smoke test), so the blocker is Aeon's push step only. Granting the PAT the `workflows` scope would unblock this and all future CI improvements.
**Anchor:** FILE:.github/workflows/tests.yml (no dependency-vulnerability or static-analysis scan; Dependabot bumps deps but no CVE gate in CI)

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** "Complete German (DE) locale: translate 7 prompt modules + add README.de.md" (2026-06-18 top pick) — substantially shipped via #189 (DE frontend/agent) and #194 (locale registry); README.de.md not yet added but idea is within 14-day novelty window.

**Selection rationale:**
- Excluded (novelty — 06-12, within 14-day window): SECURITY.md (#1), CONTRIBUTING.md (#2), pip-audit/bandit CI (#3), Redoc/docs (#4 — pre-existing), ISSUE_TEMPLATE (#5)
- Excluded (novelty — 06-14, within 14-day window): CODE_OF_CONDUCT.md (#4)
- Excluded (novelty — 06-16, within 14-day window): cost.json README callout (#1 — still unshipped, carried, but in window)
- Excluded (novelty — 06-18, within 14-day window): .github/pull_request_template.md (#2), tests.yml CI badge (#3), strengthen camel smoke test (#5 — open as PR #196)
- Excluded (implementability → Monitor): SECURITY.md (maintainer declined), pip-audit/bandit (PAT blocks workflow push)
- Excluded (novelty pass, score below threshold): ROADMAP.md (L=3 C=3 N=5 = 11/15 — C barely at floor; deprioritized vs higher-concreteness ideas at same total)
- Candidates considered: 10 | Ideas clearing all gates: 5
- Anchor type diversity: ISSUE (2: #195, #193), FILE (2: README.md/package.json, README.md/Interface-language), MISSING (1: CHANGELOG.md) — ≥3 distinct types ✅
