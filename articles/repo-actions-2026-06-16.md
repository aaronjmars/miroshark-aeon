# Repo Actions — aaronjmars/MiroShark — 2026-06-16

**Top pick for tomorrow:** #1 — Wire the cost.json endpoint callout into README Quickstart to prove the "$1" claim (Content/DX, Small)
**Verdict:** A uniquely active day — three PRs merged before noon (websearch, frontend CI, cost.json) — leaving a clean proof gap in the README and four open major-version Dependabot PRs that each need a human eye before merging.

## Actions

### 1. Wire the new cost.json endpoint callout into README Quickstart
**Priority:** HIGH
**Type:** Content / DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md#Quick-start + PR:#179 (merged 2026-06-16T13:31: "feat: GET /api/simulation/<id>/cost.json — per-sim cost breakdown")
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** The README tagline reads "Simulate anything, for $1 & less than 10 min" — the headline claim — but the Quick start section has no pointer to verifying it. PR #179 (merged hours ago) added exactly that proof: a queryable JSON endpoint returning per-step token and dollar cost. A single callout sentence in Quick start converts an assertion into an observable fact that any skeptic can check in under 30 seconds.
**How:**
1. In `README.md`, after the `./miroshark` launcher block and before the "The launcher checks dependencies…" sentence, insert: `After the first run finishes, `GET http://localhost:5001/api/simulation/<id>/cost.json` returns a per-step token and dollar breakdown — typical total is around $1.`
2. In `docs/API.md`, confirm `GET /api/simulation/<id>/cost.json` appears in the endpoint table under the Simulation section (PR #179 updated this file; verify it's present and the response schema matches the `CostResponse` / `CostBreakdownRow` types added in the PR).
3. Open as a `docs/cost-proof-callout` branch PR — no code changes, pure documentation edit.
**Definition of done:** `README.md` Quick start section contains a sentence with a copy-pasteable `cost.json` URL pattern; `docs/API.md` lists the endpoint with its response shape; CI green on the PR.

---

### 2. Add French locale — README.fr.md + frontend i18n to close issue #161
**Priority:** HIGH
**Type:** Community / Content
**Effort:** Medium (1–2 days)
**Anchor:** ISSUE:#161 "Additional translations" (open 2026-06-13, 2 comments, last updated 2026-06-14; closed ISSUE:#95 "Would you accept a French (fr) locale PR?" confirms demand — closed 2026-06-11 only because Japanese was added first)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** French is the highest-demand unimplemented locale — the only one that got an explicit "would you accept?" issue before it was passed over. The zh-CN README added Jun 10 directly seeded the "米罗莎要来了" CN tweet coverage that satisfied the Chinese-locale hyperstition. French replicates that pattern for FR/BE/CA communities, feeding the ecosystem growth metric through the same localization flywheel.
**How:**
1. Create `README.fr.md` by translating `README.md` — follow the bilingual link structure in `README.zh-CN.md` and `README.ja.md`. Add `<a href="./README.fr.md">Français</a>` to the language link row in `README.md` (currently `<b>English</b> · <a href="./README.zh-CN.md">中文</a> · <a href="./README.ja.md">日本語</a>`).
2. Locate frontend i18n JSON files — likely `frontend/src/locales/zh-CN.json` (or equivalent path from the zh-CN PR #155 pattern). Create `frontend/src/locales/fr.json` with the same keys, French-translated values. Add `fr` to the locale switcher array in whichever component manages the **中 / EN** toggle.
3. In `backend/app/i18n/` (check `normalize_locale`, `get_locale`, `apply_i18n` functions that cover `zh-CN` and `ja` per test coverage added in PR #163/#165): create `fr.json` backend locale file and wire `fr` into `normalize_locale` alongside the existing locales.
4. Open as `feat/locale-fr` branch PR; body: `closes #161`.
**Definition of done:** `README.fr.md` exists at repo root; `README.md` language row links to it; `http://localhost:3000` shows "Français" in the locale switcher; gallery titles and descriptions render in French when selected; CI green.

---

### 3. Audit and resolve Dependabot PR #175: vue-router 4.6.3 → 5.1.0 (MAJOR version)
**Priority:** MED
**Type:** DX / Security
**Effort:** Small (hours)
**Anchor:** PR:#175 "chore: bump vue-router from 4.6.3 to 5.1.0 in /frontend" (open 2026-06-15, Dependabot, MAJOR version jump)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Vue Router 5 introduces breaking changes: `RouterLink`'s `v-slot custom` API changed, `<keep-alive>` scoped-slot syntax with `<router-view>` was reworked, and `createWebHistory` base behavior shifted. The frontend CI step (PR #180, merged today) now builds the frontend on every PR — catching compilation failures — but not runtime navigation regressions. A broken merge that compiles green but 404s on navigation is the failure mode here.
**How:**
1. Read the PR diff via `gh pr diff 175`. Confirm it changes only `"vue-router": "^4.6.3"` → `"^5.1.0"` in `frontend/package.json` (and updates `package-lock.json`/`pnpm-lock.yaml`). No source changes expected from Dependabot.
2. Check `frontend/package.json` for the current Vue version — vue-router 5 requires Vue 3.5+. If Vue < 3.5, hold PR #175 with a comment: `"vue-router v5 requires Vue 3.5+; current package.json pins Vue X.Y.Z — upgrade Vue first."` If Vue ≥ 3.5, proceed.
3. Grep `frontend/src/` for `RouterLink` with `v-slot` + `custom`, `<keep-alive>` wrapping `<router-view>`, and `import.*from 'vue-router/composables'` — these are the most common v4→v5 break sites. If no hits and CI passes: merge `gh pr merge 175 --squash --delete-branch`. If hits found: leave a blocking review comment listing exact file:line occurrences.
**Definition of done:** PR #175 is merged (CI green, no breaking usages) OR has a blocking review comment listing the specific `frontend/src` file:line occurrences requiring migration before merge.

---

### 4. Audit Dependabot PR #168: python 3.11 → 3.14 Docker image (three-version jump)
**Priority:** MED
**Type:** Security / DX
**Effort:** Small (hours)
**Anchor:** PR:#168 "chore: bump python from 3.11 to 3.14" (open 2026-06-15, Dependabot; skips Python 3.12 and 3.13)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Python 3.14 is a very recent release; native extension packages may lack 3.14 wheels on PyPI, causing either a Docker build failure or silent fallback to slower source builds. Key packages at risk: `camel-ai` (large ML framework, pinned 0.2.78, being bumped to 0.2.90 by PR #176), `pywebpush` (just updated to >=2.3.0 in PR #173), `nashpy` (just updated to >=0.0.43 in PR #172), and the `neo4j` Python driver. A three-version Docker jump that breaks the container image at build time takes down the one-click deploy paths (Railway, Render) the README promotes.
**How:**
1. Read PR #168 diff via `gh pr diff 168` — confirm it changes only `FROM python:3.11` → `FROM python:3.14` (or `python:3.11-slim` → `python:3.14-slim`) in `backend/Dockerfile`. Note if any `pip install` steps change.
2. Spot-check wheel availability for the top 4 packages: use WebFetch on `https://pypi.org/pypi/camel-ai/json`, `https://pypi.org/pypi/pywebpush/json`, `https://pypi.org/pypi/nashpy/json`, `https://pypi.org/pypi/neo4j/json` — look for `"python_version": "cp314"` or `"cp314"` in the `releases` dict's file list. If any package has no cp314 wheels: leave a blocking review on PR #168 recommending `python:3.13` instead, and open a follow-up PR `fix/python-3-13-docker` targeting 3.13 (which all these packages support).
3. If all four packages have cp314 wheels: approve PR #168 with a comment noting the wheel check passed for the top packages.
**Definition of done:** PR #168 has a review comment with explicit cp314 wheel-check findings for camel-ai, pywebpush, nashpy, and neo4j driver; the PR is either approved or has a blocking review with a `fix/python-3-13-docker` follow-up PR linked.

---

### 5. Close issue #160 and document the merged websearch env-var interface
**Priority:** MED
**Type:** Community / DX
**Effort:** Small (hours)
**Anchor:** ISSUE:#160 "FYI: Building support for Websearch and Webretrieval" (open since 2026-06-13, still open as of this run; PR:#178 "Alternative websearch/scrape via SearXNG / Firecrawl for non-websearch capable LLMs" merged 2026-06-16T14:25)
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** PR #178 implemented dan-and's feature and was merged hours ago — but issue #160 is still open. Any integrator who finds the issue via search thinks the feature is pending. Closing with an env-var callout converts the issue into a setup reference, acknowledges the contributor, and removes a stale open signal from the repo's issue count.
**How:**
1. Post a closing comment on ISSUE:#160 via `gh issue comment 160 --body "Implemented in PR #178 (merged 2026-06-16). To enable websearch: set \`SEARXNG_URL\` to your SearXNG instance base URL, or set \`FIRECRAWL_URL\` + \`FIRECRAWL_API_KEY\` for Firecrawl. Both are optional — the engine uses the LLM's native capabilities if neither is set. Thanks @dan-and for building this!"`.
2. Close the issue: `gh issue close 160 --reason completed`.
3. Open `docs/CONFIGURATION.md` (linked from README docs table) and add `SEARXNG_URL`, `FIRECRAWL_URL`, and `FIRECRAWL_API_KEY` to the env-var table, with descriptions matching the comment above. Open a `docs/websearch-env-vars` PR if not already covered by PR #178's diff.
**Definition of done:** Issue #160 status is `closed (completed)`; the closing comment is present with the three env-var names; `docs/CONFIGURATION.md` lists all three variables with descriptions; `@dan-and` is acknowledged.

---

## Monitor

### A. SECURITY.md — responsible disclosure policy
**Why not yet:** Aeon opened PR #158 on 2026-06-13; maintainer closed it without merging the same day. Autonomous re-open would re-trigger the same rejection. Human decision needed: re-approach via GitHub's native "Private vulnerability reporting" UI (no separate SECURITY.md required — enables directly in repo Settings → Security → Private vulnerability reporting), or accept that the maintainer has actively chosen not to add a security policy at this stage.
**Anchor:** MISSING:SECURITY.md (GitHub Security tab shows "Security policy not configured"; 1,284 stars, AGPL-3.0, 3+ named production integrators)

### B. pip-audit + bandit security scan in `tests.yml`
**Why not yet:** Adding a job to `.github/workflows/tests.yml` requires the PAT to have the `workflows` scope — which it currently lacks. However, PR #180 ("ci: build the frontend on every PR") was merged today via maintainer action, confirming the maintainer actively reviews and merges CI workflow PRs opened on branches. Aeon can open the branch and PR; the PAT blocks only the *push* to `.github/workflows/`. Granting the PAT the `workflows` scope would unblock this class of CI improvements (frontend CI, dep scanning, bandit) without manual maintainer intervention.
**Anchor:** FILE:.github/workflows/tests.yml (no dependency-vulnerability or static-analysis scan; camel-ai is being bumped via Dependabot PR #176 but no CVE gate exists in CI)

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** — (2026-06-14 top pick — PR #159 — merged 2026-06-14; no carry-forward)

**Selection rationale:**
- Excluded (novelty — in 14-day corpus): SECURITY.md (Jun 12), CONTRIBUTING.md expansion (Jun 12, merged), pip-audit/bandit CI (Jun 12), Redoc/docs at /api/docs (Jun 12, already shipped per README), ISSUE_TEMPLATE (Jun 12 + Jun 14 Monitor), CODE_OF_CONDUCT.md (Jun 14), camel-ai pin loosen (Jun 14, superseded by Dependabot PR #176), dependabot.yml (Jun 14, merged Jun 15), websearch integration spec (Jun 14, superseded by merged PR #178)
- Excluded (already shipped today): PR #178 (websearch, merged), PR #179 (cost.json, merged), PR #180 (frontend CI build, merged)
- Dropped (implementability → Monitor): SECURITY.md (maintainer declined), pip-audit/bandit (PAT workflows scope)
- Candidates considered: ~9 | Ideas clearing all gates: 5
