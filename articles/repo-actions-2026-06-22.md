# Repo Actions — aaronjmars/MiroShark — 2026-06-22

**Top pick for tomorrow:** #1 — Loosen `camel-ai==0.2.90` to `>=0.2.90,<0.3.0` (Security/DX, Small)
**Verdict:** Five implementable ideas this cycle, all anchored to verified live state; top pick closes the one remaining exact-pinned dep and lets the camel smoke test (#196) do its job — automatically validating every future patch bump before it reaches main.

## Actions

### 1. Loosen `camel-ai==0.2.90` to `>=0.2.90,<0.3.0` — smoke test guards regressions now
**Priority:** HIGH
**Type:** Security / DX
**Effort:** Small (hours)
**Anchor:** FILE:backend/pyproject.toml (`"camel-ai==0.2.90"` — only exact-pinned dep in the backend dependency list)
**Score:** L=4 C=5 N=5 (total 14/15)
**Impact:** camel-ai is the engine's core agent library — 850+ calls per run, and the 0.2.90 bump (PR #176, Jun 16) broke the agent loop and required two same-day hotfixes (#181, #182). The exact pin `==0.2.90` blocks security patches in 0.2.91+ from flowing in automatically and prevents Dependabot from proposing patch-release bumps (a new release would require a full major-version PR to propose anything). With the camel agent smoke test now in CI (#196), a bad camel-ai version fails the smoke gate before it reaches main — exactly the defense-in-depth the incident showed was missing. Loosening to `>=0.2.90,<0.3.0` lets Dependabot send 0.2.91+ patch PRs that the smoke test validates automatically.
**How:**
1. In `backend/pyproject.toml`, change `"camel-ai==0.2.90"` to `"camel-ai>=0.2.90,<0.3.0"`.
2. Run `cd backend && uv lock` — uv resolves the range and updates `uv.lock`. If 0.2.90 is still the latest patch, the lock file stays identical for now; the change only unlocks future Dependabot bumps within the 0.2.x line.
3. Run `pytest -m "not integration"` (unit suite) and `pytest tests/test_smoke_camel_agent.py` (camel smoke test) locally to confirm no regression.
4. Open as `chore/loosen-camel-ai-pin` branch PR; body: "Loosens camel-ai from an exact pin to `>=0.2.90,<0.3.0`. The camel agent smoke test (#196) now guards against regression on any future patch bump, making Dependabot-managed updates safe to receive and review."
**Definition of done:** `backend/pyproject.toml` pins `"camel-ai>=0.2.90,<0.3.0"`; `uv.lock` updated; camel smoke test passes on the PR branch; CI green.

---

### 2. Add `wait` subcommand to `miroshark-cli` for one-line automation pipelines
**Priority:** MED
**Type:** DX / Feature
**Effort:** Small (hours)
**Anchor:** FILE:backend/cli.py (subcommands: ask, list, status, report, publish — no blocking poll/wait command; `docs/CLI.md` documents these five only)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Automation scripts and ecosystem pipelines (AntFleet `miroshark-bench`, SyntheticsAI synthetic-user runs) currently implement their own polling loop around `python -m cli status sim_id` to detect completion. A `wait sim_id` command that blocks until `status == "completed"` or `"failed"`, then exits 0/1, enables a one-liner: `SIM=$(python -m cli ask "Will the EU AI Act hold?" | jq -r .sim_id) && python -m cli wait $SIM && python -m cli report $SIM`. With 14 ecosystem integrators running production pipelines, removing the boilerplate polling is a DX gap that blocks scripted workflows.
**How:**
1. In `backend/cli.py`, add a `wait` subparser under the main argument parser. Arguments: `sim_id` (positional), `--interval` (float, default 5.0s poll frequency), `--timeout` (float, default 600s maximum wait).
2. Implement `_cmd_wait`: call `GET /api/simulation/{sim_id}` repeatedly via the existing `_api("GET", ...)` pattern. On `"completed"` → print final status JSON, exit 0. On `"failed"` → print status JSON to stderr, exit 1. On elapsed timeout → print a timeout error to stderr, exit 2. Print each status check to stderr so the caller can see progress without polluting stdout.
3. Update `docs/CLI.md` to add the `wait` command: usage, `--interval`, `--timeout`, exit codes (0=completed, 1=failed, 2=timeout), and the one-liner `ask → wait → report` automation example.
4. Open as `feat/cli-wait-command` branch PR.
**Definition of done:** `python -m cli wait sim_id` polls and exits 0 on completed, 1 on failed, 2 on timeout; `--interval` and `--timeout` flags work; `docs/CLI.md` documents the command with exit codes; CI green.

---

### 3. Add `CITATION.cff` — one-click academic citation via GitHub's "Cite this repository"
**Priority:** MED
**Type:** Community / Growth
**Effort:** Small (hours)
**Anchor:** MISSING:CITATION.cff (Crucible Sim at Tianjin Normal University — `wshuyi/crucible-sim` in ECOSYSTEM.md — confirms active academic use; no `CITATION.cff` means researchers must cite manually or skip the citation entirely)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** With 14 ecosystem integrators and at least one academic research project (Crucible Sim), MiroShark is increasingly simulation infrastructure for research. A `CITATION.cff` at repo root activates GitHub's "Cite this repository" button in the right-side panel — one click exports a correctly formatted BibTeX, APA, MLA, or Chicago citation. Academic papers citing MiroShark drive discovery: researchers find the repo via related-work searches, evaluate it as infrastructure, and become contributors or integrators. The file is set-once, zero-maintenance after the first commit.
**How:**
1. Create `CITATION.cff` at repo root in [Citation File Format v1.2.0](https://citation-file-format.github.io/) syntax:
   ```yaml
   cff-version: "1.2.0"
   message: "If you use MiroShark in your research, please cite it as below."
   title: "MiroShark — Universal Swarm Intelligence Engine"
   version: "0.1.0"
   license: AGPL-3.0
   url: "https://github.com/aaronjmars/MiroShark"
   date-released: "2026-03-01"
   authors:
     - family-names: Mars
       given-names: Aaron J.
       alias: aaronjmars
   ```
2. Validate the syntax at [citation-file-format.github.io/cff-initializer-javascript/](https://citation-file-format.github.io/cff-initializer-javascript/) or confirm GitHub renders the "Cite this repository" button after the PR merges.
3. Open as `docs/citation-cff` branch PR — single file addition.
**Definition of done:** `CITATION.cff` exists at repo root; GitHub renders a "Cite this repository" button in the repo's right-side panel; the button exports valid BibTeX; CI green.

---

### 4. Add `cost` subcommand to `miroshark-cli` — "$1 promise" visible from the command line
**Priority:** MED
**Type:** DX / Feature
**Effort:** Small (hours)
**Anchor:** FILE:backend/cli.py (subcommands: ask, list, status, report, publish — no `cost` command; `GET /api/simulation/<id>/cost.json` has shipped since PR #179; exposed in EmbedView UI via PR #190 but never surfaced in the CLI)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** The embed UI shows `~$0.92` after a sim (PR #190). Automation pipelines and CLI users have no cost visibility — the "$1 to simulate anything" claim is unverifiable from a script. A `python -m cli cost sim_id` call printing `total_usd`, `total_tokens`, and the `is_estimate` flag (prefixed `~` when true) gives every integrator a one-line cost audit after any run. With 14 ecosystem integrators running production pipelines, cost observability is table stakes for budget tracking and the north-star "$1" claim.
**How:**
1. In `backend/cli.py`, add `cost` under the subparsers block. Argument: `sim_id` (positional).
2. Implement `_cmd_cost`: call `GET /api/simulation/{sim_id}/cost.json` via `_api("GET", ...)`. Print: `"~${total_usd:.4f} (estimated, {total_tokens:,} tokens)"` when `is_estimate` is true, or `"${total_usd:.4f} ({total_tokens:,} tokens)"` when exact. Print any `per_step` breakdown if present. On 404 → print `"cost not yet available (simulation still running?)"` to stderr, exit 1.
3. Update `docs/CLI.md` to document the `cost sim_id` command.
4. Open as `feat/cli-cost-command` branch PR.
**Definition of done:** `python -m cli cost sim_id` prints formatted cost with `~` prefix when estimated; returns non-zero on HTTP error; `docs/CLI.md` documents it; CI green.

---

### 5. Add `.github/FUNDING.yml` linking to Bankr $MIROSHARK page
**Priority:** MED
**Type:** Growth
**Effort:** Small (hours)
**Anchor:** MISSING:.github/FUNDING.yml (README footer has ETH address `0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3` and a Bankr badge in the header, but no GitHub "Sponsor" button — 1,322 stars with no funding CTA above the fold in the right-side panel)
**Score:** L=3 C=5 N=5 (total 13/15)
**Impact:** GitHub shows a prominent heart "Sponsor" button above the "About" section when `.github/FUNDING.yml` exists. For a 1,322-star repo, that button converts repo visitors browsing the landing page into $MIROSHARK token holders — the shortest conversion path from GitHub traffic to token liquidity. The `custom` key in `FUNDING.yml` accepts any URL; pointing it to the Bankr discover page for the $MIROSHARK contract makes the repo→token conversion path explicit and one-click for every visitor.
**How:**
1. Create `.github/FUNDING.yml`:
   ```yaml
   custom:
     - https://bankr.bot/discover/0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3
   ```
2. No other files need changing — GitHub reads `.github/FUNDING.yml` automatically after push.
3. Verify the "Sponsor" heart button appears in the right-side panel of the repo landing page after the PR merges and the Bankr URL resolves correctly.
4. Open as `docs/funding-yml` branch PR.
**Definition of done:** `.github/FUNDING.yml` exists with a valid `custom` entry pointing to the Bankr $MIROSHARK page; GitHub's repo right-side panel shows a "Sponsor" heart button; CI green.

---

## Monitor
<!-- Ideas that failed the implementability gate. Max 3. -->

### A. ROADMAP.md
**Why not yet:** A `ROADMAP.md` requires the maintainer to decide on planned milestones, version targets, and feature priorities — autonomous agents can't substitute editorial decisions about project direction. With 14 ecosystem integrators tracking upgrades, a public roadmap would help them plan but the content is the operator's call.
**Anchor:** MISSING:ROADMAP.md

### B. tests.yml unit job — replace manual `pip install` with `uv sync`
**Why not yet:** The CI unit job installs deps via a manual `pip install` block (hardcoding `neo4j>=5.26.0`, `pillow>=12.0.0`, etc.) instead of `uv sync`, creating version drift from the locked `uv.lock`. Fixing this requires pushing to `.github/workflows/tests.yml` — the Aeon PAT lacks the `workflows` scope. The maintainer has merged CI workflow PRs opened on branches (#180, #183, #196), so the blocker is Aeon's push step only.
**Anchor:** FILE:.github/workflows/tests.yml (unit job: manual pip install with hardcoded versions, not `uv sync --group dev`)

### C. SECURITY.md — responsible disclosure policy
**Why not yet:** Aeon opened PR #158 (2026-06-13); maintainer closed it the same day. Autonomous re-open would re-trigger the rejection. Human decision: enable GitHub's native Private vulnerability reporting (Settings → Security → Enable private vulnerability reporting) which requires no separate file.
**Anchor:** MISSING:SECURITY.md

---

## Fleet follow-ons
<!-- aaronjmars/miroshark-aeon is the agent repo — skipped per skill rules. -->

---

**Source status:** gh=ok code_search=rate_limited memory_topics=missing articles_dir=ok watched_repos=2 parsed (1 active, 1 skipped — `-aeon`)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** — (2026-06-20 top pick "Fix graph_tools._fallback_interview locale drop" shipped as PR #198 on 2026-06-21)

**Selection rationale:**
- Excluded (novelty — 06-12, in 14-day window): SECURITY.md (#1 → Monitor), CONTRIBUTING.md expansion (#2 — shipped), pip-audit/bandit CI (#3 → Monitor), API Docs UI (#4), ISSUE_TEMPLATE (#5)
- Excluded (novelty — 06-14, in window): CODE_OF_CONDUCT.md (#4)
- Excluded (novelty — 06-16, in window): cost.json README callout (#1 — shipped as EmbedView PR #190), FR locale (#2 — shipped), vue-router audit (#3), Python 3.14 Docker (#4)
- Excluded (novelty — 06-18, in window): DE locale top pick (partial ship), PR template (#2), CI badge (#3), show cost in UI (#4 — shipped EmbedView #190), strengthen camel smoke (#5 — shipped #196)
- Excluded (novelty — 06-20, in window): locale fix (#1 — shipped #198), Fix README Node prereq (#2), thinking budget (#3 — PR #203 open), JA locale (#4), CHANGELOG.md (#5)
- Excluded (novelty risk — launcher Node check): `./miroshark` L128 `if [[ $nodemaj -ge 18 ]]` is a confirmed live bug (passes Node 18-21, then Vite 8 fails), but the underlying "fix node version" concept fuzzy-matches the 06-20 #2 title — dropped to avoid false novelty pass
- Excluded (implementability → Monitor): ROADMAP.md (owner decides content), tests.yml pip→uv (PAT blocks .github/workflows/), SECURITY.md (maintainer declined)
- Candidates considered: 10 | Ideas clearing all gates: 5
- Anchor type diversity: FILE (2 distinct: backend/pyproject.toml, backend/cli.py), MISSING (2 distinct: CITATION.cff, .github/FUNDING.yml) — ≥3 distinct anchor sources ✅
