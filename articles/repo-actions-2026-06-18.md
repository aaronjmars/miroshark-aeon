# Repo Actions — aaronjmars/MiroShark — 2026-06-18

**Top pick for tomorrow:** #1 — Complete German (DE) locale: prompt translations + README.de.md (Community/i18n, Medium)
**Verdict:** One 14/15 idea and four 12–13/15 ideas today, all HIGH or MED priority; top pick closes the last UI-exposed locale gap (DE is visible in the navbar switcher but has no prompt translations and no README.de.md), following the exact same pattern that shipped FR in 48 hours this week (#184 → #185 → #186).

## Actions

### 1. Complete German (DE) locale: translate 7 prompt modules + add README.de.md
**Priority:** HIGH
**Type:** Community / i18n
**Effort:** Medium (1–2 days)
**Anchor:** ISSUE:#161 "Additional translations" (open, 3 comments, last updated 2026-06-16) + FILE:backend/app/prompts/locales/de/ (stubs from PR:#184 "generalize locale helpers + add German/French foundation") + FILE:README.md (language bar shows EN · 中文 · 日本語 · Français — no Deutsch link despite DE appearing in the navbar)
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** German is the only UI-exposed locale with incomplete parity: the navbar shows "DE" as a selectable option (wired in PR:#184) but German-locale sims run on English prompts and no README.de.md exists. FR had the same gap and was closed in two commits (#185 + #186) merged Jun 17–18. Closing DE creates the same flywheel that the ZH-CN README seeded: a localized README surfaces in German-language search and community channels, driving non-English stars the same way "米罗莎要来了" did for the CN community.
**How:**
1. Follow PR:#186 as exact template. Create `backend/app/prompts/locales/de/{web_enrichment,ner_extractor,ontology,profile_generator,simulation_config,graph_tools,social_simulations}.py` — each file exports a `PROMPTS` dict with German-translated strings for every key present in the `en/` equivalents. The `fr/` files from #186 are the structural reference; the pattern is identical.
2. Add DE coverage tests to `backend/tests/test_unit_prompt_registry.py`: `test_de_has_no_missing_keys_relative_to_en` + `test_get_prompt_returns_german_for_de` — mirror the fr test pair added in #186 exactly.
3. Create `README.de.md` at repo root (translate `README.md` into German). Add `<a href="./README.de.md">Deutsch</a>` to the language bar in `README.md` after the Français link.
4. Open as `feat/locale-de` branch PR; body: `closes #161` (or notes partial close if more locales remain requested in the thread).
**Definition of done:** `README.de.md` exists at repo root; `README.md` language bar links to it; `backend/app/prompts/locales/de/` has all 7 translated modules with no missing keys relative to `en/`; `test_unit_prompt_registry.py` de parity gate passes; CI green on the PR.

---

### 2. Add `.github/pull_request_template.md` to standardize PR body format
**Priority:** MED
**Type:** Community / DX
**Effort:** Small (hours)
**Anchor:** MISSING:.github/pull_request_template.md (186 PRs merged; `CONTRIBUTING.md` defines `feat:`, `fix:`, `docs:`, `chore:` conventions and an endpoint PR pattern, but no template enforces a body structure when contributors open PRs)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** Community contributors (dan-and, AntFleet, Capacitr, and the next wave from 1,309 stars) open PRs into a blank text area. CONTRIBUTING.md defines conventions but isn't shown at PR-open time. A template surfaces the checklist — PR type, linked issue, how-to-test, openapi.yaml flag, i18n flag — exactly when it's needed, reducing review round-trips and ensuring `closes #N` issue links appear consistently. With active locale PRs (#184, #185, #186 all merged this week), the i18n checklist item alone would have flagged whether prompt files were complete before review.
**How:**
1. Create `.github/pull_request_template.md`:
   ```markdown
   ## Type
   - [ ] `feat:` — new feature
   - [ ] `fix:` — bug fix
   - [ ] `docs:` — documentation only
   - [ ] `chore:` — dependency / CI / tooling

   ## Summary
   <!-- 1–2 sentences: what changed and why -->

   ## Linked issue
   closes #

   ## How to test
   <!-- Steps for the reviewer to verify the change works -->

   ## Checklist
   - [ ] CI passes
   - [ ] `backend/openapi.yaml` updated if any API endpoint changed
   - [ ] locale prompt files updated if i18n changes were made
   ```
2. Open as `docs/pr-template` branch PR. Single file addition — no code changes.
3. Add a one-line note to `CONTRIBUTING.md` under the "Submitting a PR" section: "GitHub pre-fills the PR body from `.github/pull_request_template.md` — fill in every section before requesting review."
**Definition of done:** `.github/pull_request_template.md` exists; opening a new PR via GitHub UI shows the template pre-filled; `CONTRIBUTING.md` references it; CI green on the PR.

---

### 3. Add `tests.yml` CI status badge to the README shield row
**Priority:** MED
**Type:** Growth / DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md (shield row has GitHub stars, forks, X follow, Bankr — no CI/tests status badge) + FILE:.github/workflows/tests.yml (exists; now includes camel agent smoke test from PR:#183 and frontend build from PR:#180)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** After PR:#183 added the first real agent-loop smoke test and PR:#180 added frontend build CI, the test suite is meaningful — a green run now asserts that agents produce non-zero actions and the frontend compiles. That signal doesn't reach a repo visitor who sees stars and forks but no CI indicator. A `tests.yml` badge above the fold converts "I hope this works" into "CI passed on this commit" for every integrator and potential contributor evaluating the repo, directly supporting the ecosystem growth metric.
**How:**
1. In `README.md`, in the `<p align="center">` shields block, add after the Bankr badge:
   `<a href="https://github.com/aaronjmars/MiroShark/actions/workflows/tests.yml"><img src="https://github.com/aaronjmars/MiroShark/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>`
2. Verify the badge resolves green on `main` (CI should pass after #183 + #186 both landed cleanly today).
3. Open as `docs/ci-badge` branch PR — single-line diff in `README.md`.
**Definition of done:** `README.md` shield row shows a green "passing" tests badge that links to the `tests.yml` workflow run history; badge is visible above the fold on the GitHub repo landing page.

---

### 4. Display simulation cost from cost.json in the frontend completion UI
**Priority:** HIGH
**Type:** DX / Feature
**Effort:** Small (hours)
**Anchor:** PR:#179 (merged 2026-06-16: "feat: GET /api/simulation/<id>/cost.json — per-sim cost breakdown") + FILE:frontend/src/ (no cost display in the simulation result or gallery card per current README Quick start section — endpoint exists but frontend never calls it)
**Score:** L=4 C=3 N=5 (total 12/15)
**Impact:** "Simulate anything, for $1" is the entire product promise — but the UI never shows a user what their simulation cost. PR:#179 built the proof: a queryable JSON endpoint returning per-step token and dollar cost. The gap between API (cost.json) and UI (no display) means users have to know to `curl` the endpoint to verify the "$1" claim. Closing this converts a marketing assertion into an inline observable that appears automatically after every run — the single strongest credibility move for the north-star promise without touching the simulation engine.
**How:**
1. Locate the simulation completion/result view — search `frontend/src/` for components that render `status === 'completed'` or display a finished simulation header. Likely `SimulationView.vue`, `SimulationResult.vue`, or a status-handling section in the main sim view.
2. After sim completion, fetch `GET /api/simulation/<id>/cost.json`. Display `total_usd` as a small inline chip near the simulation header (e.g., `Cost: ~$0.87`). If the response has `is_estimate: true` (the endpoint's lower-bound flag per PR:#179's design), prefix with `~`; if `is_estimate: false`, display exact amount.
3. Fetch once on completion (not polling) — store in component state. Handle 404 gracefully (cost.json only exists for completed sims).
4. Open as `feat/show-cost-in-ui` branch PR.
**Definition of done:** After a simulation completes, the UI shows the total USD cost inline; `is_estimate=true` triggers the `~` prefix; the component fetches cost.json once on completion and doesn't re-poll; network tab shows a single `GET .../cost.json` request after sim status flips to completed.

---

### 5. Strengthen the camel smoke test to catch silent engine output failures
**Priority:** HIGH
**Type:** DX / Quality
**Effort:** Small (hours)
**Anchor:** FILE:backend/tests/test_smoke_camel_agent.py (added in PR:#183 "fix+ci: correct total_actions reporting + add camel agent smoke test"; fixed the camel-ai 0.2.90 regression where total_actions was hardcoded to 0 for two months undetected)
**Score:** L=4 C=3 N=5 (total 12/15)
**Impact:** The camel-ai 0.2.90 breakage (PRs #181, #182) slipped past CI for ~2 months because `total_actions=0` read as healthy. PR:#183 added the first smoke test and fixed the reporting — but a subtly-broken agent (non-zero count, empty or malformed messages) would still pass the current assertion. The next camel-ai bump or `_aget_model_response` signature change could silently produce agents that execute 0-length turns. Strengthening the test to assert real content in messages closes the remaining blind spot before the next dependency bump opens it.
**How:**
1. Open `backend/tests/test_smoke_camel_agent.py`. Inspect the current assertion — likely `result.total_actions > 0` or `result is not None`.
2. Add assertions: `assert result.total_actions >= 2` (a real agent exchange produces at minimum an opening and a reply); `assert len(result.messages) >= 1`; `assert all(len(m.content.strip()) > 10 for m in result.messages[:3])` (messages contain real text, not empty strings or whitespace from a silent failure).
3. If the test uses a mock LLM (likely, to avoid real API cost in CI), verify the mock returns strings of ≥ 10 characters — update the fixture if it currently returns empty or single-character stubs that would pass today's assertions but mask the failure mode being guarded.
4. Open as `test/strengthen-camel-smoke` branch PR.
**Definition of done:** `test_smoke_camel_agent.py` asserts `total_actions >= 2`, `len(messages) >= 1`, and non-empty message content; the test passes on `main`; a contrived `total_actions=0` patch causes the new assertions to fail; CI green on the PR.

---

## Monitor

### A. SECURITY.md — responsible disclosure policy
**Why not yet:** Aeon opened PR #158 on 2026-06-13; maintainer closed it without merging the same day. Autonomous re-open would re-trigger the same rejection. Human decision needed: re-approach via GitHub's native "Private vulnerability reporting" UI (Settings → Security → Private vulnerability reporting) — this requires no separate `SECURITY.md` file and works out of the box — or accept that the maintainer has actively chosen not to add a policy at this stage.
**Anchor:** MISSING:SECURITY.md (1,309 stars, AGPL-3.0, 3+ named production integrators — RevaultDrops, AntFleet, Capacitr)

### B. pip-audit + bandit security scan in `tests.yml`
**Why not yet:** Adding a CI job to `.github/workflows/tests.yml` requires pushing to `.github/workflows/` — which the Aeon PAT lacks (`workflows` scope not granted). Maintainer has merged CI workflow PRs opened on branches (PR:#180 frontend build, PR:#183 camel smoke test), so the blocker is Aeon's push step, not maintainer willingness. Granting the PAT the `workflows` scope would unblock this class of CI improvements.
**Anchor:** FILE:.github/workflows/tests.yml (no dependency-vulnerability or static-analysis scan; camel-ai was bumped via Dependabot PR #176 but no CVE gate exists in CI)

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** "Wire the cost.json endpoint callout into README Quickstart" (2026-06-16 top pick — not merged; README Quick start section has no cost.json mention as of 2026-06-18)

**Selection rationale:**
- Excluded (corpus — Jun-12, in 14-day window): SECURITY.md (#1), CONTRIBUTING.md expansion (#2), pip-audit/bandit CI (#3), API Docs UI (#4 — pre-existing as Swagger), issue templates (#5)
- Excluded (corpus — Jun-14): CODE_OF_CONDUCT.md (#4), dependabot.yml (#3 — merged Jun-15), camel-ai pin loosen (#5 — superseded by Dependabot PR #176 merge)
- Excluded (corpus — Jun-16): cost.json README callout (#1 — not yet merged, carried over), French locale (#2 — merged #184/#185/#186), vue-router audit (#3 — merged #175), Python 3.14 Docker (#4 — merged #168), close issue #160 (#5 — done Jun 16)
- Excluded (implementability → Monitor): SECURITY.md (maintainer declined), pip-audit/bandit (PAT blocks workflow push)
- Excluded (pre-existing — blocked-features.md): Operator Profile (no `operator`/`created_by` field on SimulationState)
- Candidates considered: 8 | Ideas clearing all gates: 5
- Anchor type diversity: ISSUE (1), MISSING (1), FILE (3) — ≥3 distinct types ✅
