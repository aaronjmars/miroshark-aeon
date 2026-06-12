# Repo Actions — aaronjmars/MiroShark — 2026-06-12

**Top pick for tomorrow:** #1 — Add SECURITY.md with a responsible disclosure policy (Security, Small)
**Verdict:** Five HIGH/MED ideas today — all anchored to real structural gaps; top pick closes the most embarrassing hole (no disclosure policy on a security-affected AGPL project with 1,266 stars and 3+ named integrators).

## Actions

### 1. Add SECURITY.md with responsible disclosure policy
**Priority:** HIGH
**Type:** Security
**Effort:** Small (hours)
**Anchor:** MISSING:SECURITY.md
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** Operators and integrators running MiroShark in production (RevaultDrops, AntFleet, Capacitr) gain a clear private-report path; eliminates the pattern seen in issue #88 (hardcoded Neo4j password discovered and disclosed publicly before a private channel existed).
**How:**
1. Create `SECURITY.md` at repo root with: supported versions table (current `0.1.0`), a "Report a vulnerability" section pointing to a private contact (GitHub's private-vulnerability-reporting or an email), expected response SLA (e.g., 7 days), and a reference to prior fix example (issue #88 → resolved).
2. Add a `security-policy` link in `README.md` under the contributing/community badge row so it surfaces in the GitHub Security tab automatically.
3. Open a PR; no code changes required — this is a pure markdown addition.
**Definition of done:** `SECURITY.md` exists at repo root, GitHub Security tab shows "Security policy" as configured, and the file passes `markdownlint` (no broken links).

---

### 2. Expand CONTRIBUTING.md from test-only stub to full contributor guide
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:CONTRIBUTING.md (856 bytes — currently covers only the pytest suite, nothing else)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Contributors landing from 1,266 stars can set up a working dev environment and submit a well-formed PR without filing a "how do I run this?" issue — removing the onboarding friction that currently requires reading README + pyproject + CI in parallel.
**How:**
1. Add a **Development setup** section: `git clone` → `npm run setup:all` (pulls both frontend npm deps and backend uv deps) → `docker compose up neo4j` → `npm run dev` — copy-pasteable steps anchored to the `scripts` block in `package.json`.
2. Add a **Submitting a PR** section: branch naming (`feat/`, `fix/`, `docs/`), the required PR title prefix format used in all recent merges (e.g., `feat: …`, `fix: …`), note that `tests.yml` runs the unit suite on every PR.
3. Add an **Adding an API endpoint** paragraph referencing `backend/openapi.yaml` drift test and the existing endpoint PR pattern (register on a `_bp`, update `openapi.yaml`, add a unit test under `backend/tests/`).
**Definition of done:** `CONTRIBUTING.md` ≥ 2,000 bytes with setup + PR + API-endpoint sections; `npm run setup:all` command in the file exactly matches the `package.json` scripts block.

---

### 3. Add pip-audit + bandit security scan step to `.github/workflows/tests.yml`
**Priority:** HIGH
**Type:** Security
**Effort:** Small (hours)
**Anchor:** FILE:.github/workflows/tests.yml (currently runs unit tests only — no dependency vulnerability or static-analysis scan)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Catches vulnerable transitive dependencies (e.g., a CVE in `camel-ai==0.2.78`, which is pinned to an exact version) and Python code-level security anti-patterns (hardcoded credentials, unsafe deserialization) before they land in `main` — directly addressing the class of bug from issue #88.
**How:**
1. Add a new job `security` in `tests.yml` that installs `pip-audit` and `bandit` (`pip install pip-audit bandit`), then runs `pip-audit --require-hashes -r backend/requirements.txt` (or against `backend/pyproject.toml`) and `bandit -r backend/app/ -ll` (high/medium severity only, to avoid noise).
2. Set `continue-on-error: false` so a HIGH-severity CVE blocks merge; add a `// bandit: noqa` escape hatch comment convention in the CONTRIBUTING.md for known false positives.
3. The job should run on `push` + `pull_request` to `main`, same triggers as the existing `unit` job.
**Definition of done:** `tests.yml` has a `security` job; a test PR with a known-vulnerable dep (e.g., pinning an old `requests`) shows the job failing; the current `main` branch passes clean.

---

### 4. Serve Redoc UI at `GET /api/docs` from the existing `backend/openapi.yaml`
**Priority:** HIGH
**Type:** DX
**Effort:** Medium (1–2 days)
**Anchor:** FILE:backend/openapi.yaml (actively maintained ~1,200-line spec; no browser-accessible UI endpoint exists)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** The 3 named integrators (RevaultDrops, AntFleet, Capacitr) and any new API consumer can navigate 30+ endpoints — including the recently added `/api/surfaces.json?type=`, `/api/activity.json`, `/api/stats/distribution.json` — in a browser without pulling the repo, accelerating integration time.
**How:**
1. Add a `docs_bp` Blueprint in `backend/app/api/docs.py`: one route `GET /api/docs` that serves a minimal HTML page loading Redoc from the jsDelivr CDN (`<redoc spec-url='/api/openapi.yaml'></redoc>`), and a companion route `GET /api/openapi.yaml` that reads and returns `openapi.yaml` with `Content-Type: application/yaml`.
2. Register `docs_bp` in `backend/app/__init__.py` alongside the existing blueprints; add a `DOCS_ENABLED` env-var guard (default `true`) so operators can disable it in locked-down deployments.
3. Add a one-line entry to `README.md` under the API section: "`GET /api/docs` — interactive API reference (Redoc)".
**Definition of done:** `GET /api/docs` returns a 200 HTML page that renders all routes from `openapi.yaml` in a browser; `GET /api/openapi.yaml` returns the raw spec; `DOCS_ENABLED=false` returns 404 for both routes.

---

### 5. Add `.github/ISSUE_TEMPLATE` with bug-report and feature-request templates
**Priority:** MED
**Type:** Community
**Effort:** Small (hours)
**Anchor:** MISSING:.github/ISSUE_TEMPLATE (no templates exist — the 0 current open issues is a honeymoon period, not a sign this won't be needed)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** The next wave of community issues (from 1,266-star users) arrives with structured reproduction steps, environment info, and clear feature framing — reducing triage time and the back-and-forth seen in prior issues like #8 (polling bug filed with no repro steps).
**How:**
1. Create `.github/ISSUE_TEMPLATE/bug_report.yml`: fields for `description`, `steps_to_reproduce` (textarea), `expected` vs `actual` (textareas), `environment` (Node version, Python version, Docker vs local), and `sim_id` (optional, for backend issues).
2. Create `.github/ISSUE_TEMPLATE/feature_request.yml`: fields for `problem` (what you can't do today), `proposed_solution`, `alternatives_considered`, and an `ai-build` checkbox label for ideas suitable for autonomous implementation.
3. Create `.github/ISSUE_TEMPLATE/config.yml` with `blank_issues_enabled: false` and a link to `CONTRIBUTING.md` so free-form issues are funneled through templates.
**Definition of done:** New issues on the repo show a template picker with Bug Report and Feature Request options; `blank_issues_enabled: false` is confirmed in `config.yml`; the `ai-build` label exists on the repo.

---

## Monitor
<!-- Ideas that failed the implementability gate. Surfaced for human decision. Max 3. Omit section entirely if empty. -->

### A. CODE_OF_CONDUCT.md
**Why not yet:** Not blocked on autonomy — trivially addable. Deferred from the main 5 only by score (12/15 vs the four 13/15 ideas above). Carry forward if any of ideas 2–5 ship this cycle and a slot opens.
**Anchor:** MISSING:CODE_OF_CONDUCT.md

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=rate_limited memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** — (no prior repo-actions articles)

**Selection rationale:**
- Excluded (blocked): Operator Profile — no `operator`/`created_by` field on `SimulationState` (see `memory/topics/blocked-features.md`)
- Excluded (pre-existing): Gallery JSON API, Compare API, RSS Feed, Webhook Delivery Log, Webhook Retry, and 20+ others (see `memory/topics/pre-existing-features.md`)
- Dropped (novelty): 0 (no prior articles in novelty corpus)
- Dropped (specificity): 0
- Dropped (score <10): 0
