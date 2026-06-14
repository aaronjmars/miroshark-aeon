# Repo Actions — aaronjmars/MiroShark — 2026-06-14

**Top pick for tomorrow:** #1 — Review and merge PR #159 (community: same-origin fix + neo4j v5.26) (Community/DX, Small)
**Verdict:** One 14/15 and two 13/15 ideas anchored to a live community PR, an active contributor issue, and a structural security gap — all HIGH or MED priority, all executable autonomously inside 1 day.

## Actions

### 1. Review and merge PR #159: same-origin API fix + neo4j v5.26 bump (community from dan-and)
**Priority:** HIGH
**Type:** Community / DX
**Effort:** Small (hours)
**Anchor:** PR:#159 "chore: allow same origin api calls and neo4j v5.26 bump" (open since 2026-06-13, community contributor dan-and)
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** Merging this unblocks cross-origin embedding use cases (MiroShark iframes / external integrator UIs can now call the API), keeps neo4j on v5.26 (2 minor versions behind current), and signals to dan-and — who also opened issue #160 and maintains a fork with websearch support — that contributions are welcome; momentum matters when a key community member is mid-build.
**How:**
1. Run `gh pr checkout 159` locally (or inspect the diff via `gh pr diff 159`) to verify the two changes are isolated: (a) CORS / same-origin header tweak in the Flask app or config and (b) `neo4j>=5.26` version floor in `pyproject.toml`/`requirements.txt`. Confirm no new runtime dependencies or breaking changes.
2. Check CI status via `gh pr checks 159` — if `tests.yml` is green, the unit suite passes. If red, note the failing step and fix or request a fix.
3. Merge via `gh pr merge 159 --squash --delete-branch`; use a short squash commit title that matches the existing `chore: …` commit convention.
4. Leave a closing comment thanking dan-and, and link to issue #160 to indicate websearch/webretrieval work is on the radar.
**Definition of done:** PR #159 shows status `merged` in GitHub; `GET /api/status` responds without CORS errors from an origin other than the backend's own host; `neo4j` floor in `pyproject.toml` reads `>=5.26.0`.

---

### 2. Draft websearch integration spec on ISSUE #160 to unblock dan-and's SearXNG + Firecrawl fork
**Priority:** HIGH
**Type:** Integration / Community
**Effort:** Small (hours)
**Anchor:** ISSUE:#160 "FYI: Building support for Websearch and Webretrieval" (open 2026-06-13, author dan-and; fork branch `alternative_websearch` at `dan-and/MiroShark`)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Web search support directly addresses the gap between MiroShark's "$1 to simulate anything" promise and local-LLM operators who run models without built-in web search (Ollama, LM Studio, self-hosted deployments). Formalising the ENV-var contract now means dan-and's PR will land with the right interface the first time, avoiding back-and-forth that stalls community PRs.
**How:**
1. Post a response comment on ISSUE:#160 that lays out the expected integration contract: `SEARXNG_URL` (base URL of a SearXNG instance, empty = disabled), `FIRECRAWL_URL` + `FIRECRAWL_API_KEY` (empty = disabled), and a precedence rule (SearXNG checked first; Firecrawl as fallback). State that the integration hook should live in `backend/app/services/` as a `web_search_service.py` returning a `List[SearchResult]` that the simulation oracle/agent-step can call before making LLM calls when a scenario requires external knowledge.
2. Add the `ai-build` label to the issue (create it on the repo if it doesn't exist: `gh label create ai-build --color 0075ca --description "Suitable for autonomous implementation"`) and the `enhancement` label.
3. Link from the comment to the existing `backend/app/services/` pattern (e.g., `signal_service.py` as a reference shape for a service that fetches external data) so the contributor can model their PR structure against it.
**Definition of done:** Issue #160 has a maintainer comment outlining the `SEARXNG_URL` / `FIRECRAWL_*` ENV-var interface and the `web_search_service.py` hook location; the `ai-build` label is attached; dan-and can proceed to open a PR without architecture clarification.

---

### 3. Add `.github/dependabot.yml` to automate weekly Python and npm dependency updates
**Priority:** MED
**Type:** Security
**Effort:** Small (hours)
**Anchor:** MISSING:.github/dependabot.yml (`camel-ai==0.2.78` is pinned to an exact version in `backend/requirements.txt`; no automated dep-update tooling exists in the repo)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** An exact pin on `camel-ai==0.2.78` (a large ML framework with frequent releases) means security patches in any later version never flow in. Dependabot opens a weekly PR when it detects a version behind the declared floor — the repo catches CVEs passively instead of waiting for a manual audit. Also covers `npm` devDependencies in root `package.json` (currently `concurrently@^9.1.2`).
**How:**
1. Create `.github/dependabot.yml` at repo root:
   ```yaml
   version: 2
   updates:
     - package-ecosystem: pip
       directory: "/backend"
       schedule:
         interval: weekly
       open-pull-requests-limit: 5
     - package-ecosystem: npm
       directory: "/"
       schedule:
         interval: weekly
       open-pull-requests-limit: 3
   ```
2. Open a PR (`feat/add-dependabot`) targeting `main`; no code changes required beyond this one file. Include a short PR body explaining that `camel-ai==0.2.78` is currently pinned and the first dependabot run may immediately surface an update PR.
3. After merging, verify GitHub's dependency graph shows both ecosystems under the repo's "Insights → Dependency graph" tab.
**Definition of done:** `.github/dependabot.yml` exists in `main`; GitHub shows "Dependabot enabled" on the Security tab; at least one ecosystem (pip or npm) appears in the dependency graph.

---

### 4. Add `CODE_OF_CONDUCT.md` using Contributor Covenant v2.1
**Priority:** MED
**Type:** Community
**Effort:** Small (hours)
**Anchor:** MISSING:CODE_OF_CONDUCT.md (14 public ecosystem integrators and 1,270 stars; no community governance document exists)
**Score:** L=3 C=5 N=4 (total 12/15)
**Impact:** With 14 named integrators (AntFleet, Capacitr, Blue Agent, Crucible Sim, Echo Oracle, HivemindOS, Noelclaw, RootAI, Signa, Sparkleware, SyntheticsAI, Xerg, ZER0, Monitor), MiroShark has a real multi-org contributor community. A CoC sets the expected interaction norm before the first dispute rather than after — and unlocks the GitHub "Community profile" completeness badge which shows in repository discovery.
**How:**
1. Create `CODE_OF_CONDUCT.md` at repo root using the Contributor Covenant v2.1 template (publicly available under CC-BY-4.0 — no license conflict with AGPL-3.0). Fill in `[INSERT CONTACT METHOD]` with either a GitHub Discussions link or the same contact path being added in SECURITY.md (PR #158).
2. Add a one-line entry to `README.md` in the contributing/community section: `[Code of Conduct](CODE_OF_CONDUCT.md)` alongside the existing `[Contributing](CONTRIBUTING.md)` link.
3. Open as a single PR (`docs/code-of-conduct`) alongside or separately from the other pending docs PRs.
**Definition of done:** `CODE_OF_CONDUCT.md` exists in `main` under the Contributor Covenant v2.1 header; GitHub's Community profile checklist shows "Code of conduct" ticked; `README.md` links to it.

---

### 5. Loosen `camel-ai==0.2.78` exact pin to `>=0.2.78` in `backend/requirements.txt` and `backend/pyproject.toml`
**Priority:** MED
**Type:** Security
**Effort:** Small (hours)
**Anchor:** DEP:camel-ai==0.2.78 (exact pin in both `backend/requirements.txt` line 20 and `backend/pyproject.toml` `[project.dependencies]`; every other major dep uses `>=`)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** An exact version pin on a large ML framework (camel-ai) means the runtime never benefits from upstream bug fixes or security patches without a manual pin bump. The pattern in this repo is consistently `>=` for all other deps (`flask>=3.0.0`, `openai>=1.0.0`, `neo4j>=5.15.0`). Aligning camel-ai to the same convention removes the inconsistency and allows Dependabot (idea #3) to detect and auto-PR updates as they land.
**How:**
1. In `backend/requirements.txt`, change `camel-ai==0.2.78` to `camel-ai>=0.2.78`.
2. In `backend/pyproject.toml` under `[project.dependencies]`, change `"camel-ai==0.2.78"` to `"camel-ai>=0.2.78"`.
3. Verify `uv sync` resolves cleanly (it should, since 0.2.78 is the floor — any installed version ≥0.2.78 satisfies the constraint). Open a PR (`fix/loosen-camel-ai-pin`); CI `tests.yml` runs pytest which doesn't import camel-ai directly (wonderwall is bundled), so the tests should pass green.
**Definition of done:** `camel-ai` appears as `>=0.2.78` in both `requirements.txt` and `pyproject.toml`; `uv.lock` updated; CI green on the PR.

---

## Monitor

### A. Frontend build/lint step in CI
**Why not yet:** Adding a job to `.github/workflows/tests.yml` requires pushing to `.github/workflows/` — and the Aeon PAT lacks the `workflows` scope. Same blocker that stopped idea #3 (pip-audit/bandit) on 2026-06-12. A repo admin with a `workflow`-scoped PAT can add a `frontend-build` job that runs `npm run build` in the `frontend/` directory; the current CI only exercises the Python backend.
**Anchor:** FILE:.github/workflows/tests.yml (no frontend build/lint step; `frontend/` has ~100+ Vue/TS components untested in CI)

### B. `.github/ISSUE_TEMPLATE` bug-report and feature-request templates
**Why not yet:** Novelty-gated — was idea #5 on 2026-06-12 (2 days ago, within the 14-day corpus window). Still missing from the repo; carry forward past 2026-06-26 if not shipped.
**Anchor:** MISSING:.github/ISSUE_TEMPLATE

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** "Add SECURITY.md with responsible disclosure policy" (2026-06-12 top pick — PR #158 opened 2026-06-13, still open and unmerged)

**Selection rationale:**
- Excluded (pre-existing): Interactive API Docs UI (`/api/docs` — Swagger UI, `docs.py` already in `backend/app/api/`; was incorrectly suggested as Redoc in Jun-12 idea #4 — verified pre-existing by Jun-13 feature run)
- Excluded (novelty — in 14-day corpus): SECURITY.md, CONTRIBUTING.md expansion, pip-audit/bandit CI, ISSUE_TEMPLATE — all from 2026-06-12 article
- Excluded (novelty gate pass, but below score threshold): README CI badge (L=2 < 3 — fails single-dimension floor)
- Dropped (PAT blocks → Monitor): Frontend build step in CI
- Dropped (pre-existing check): ecosystem.json API (listed in ECOSYSTEM.md: `GET /api/ecosystem.json`)
- Candidates considered: 10 | Ideas clearing all gates: 5
