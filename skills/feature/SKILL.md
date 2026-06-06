---
name: feature
description: Build a feature for the watched repo — picks from yesterday's repo-actions ideas first
var: ""
tags: [dev]
---
> **${var}** — Feature to build. If empty, picks from repo-actions output or GitHub issues.

If `${var}` is set, build that specific feature.

Today is ${today}. Your task is to build a new feature for the **watched repo** (not this agent repo).

## Steps

1. **Identify the target repo** — read `memory/watched-repos.md` to get the repo (owner/repo format).

2. **Pick what to build** (in this priority order):
   a. If `${var}` is set, build that.
   b. Check yesterday's `repo-actions` output in `articles/repo-actions-*.md` (most recent file). Pick the highest-impact idea that is scoped for autonomous implementation.
   c. Check open GitHub issues labelled "ai-build" on the watched repo: `gh issue list -R owner/repo --label ai-build`.
   d. Check `memory/MEMORY.md` for planned features or next priorities.
   e. If none of the above yields anything, log "FEATURE_SKIP: no suitable feature found" and **do NOT send any notification. Stop here.**

3. **Check for existing open PRs** on the watched repo to avoid building something that's already pending:
   ```bash
   gh pr list -R owner/repo --state open --json title,body,headRefBranch --limit 20
   ```
   Compare your chosen idea against the open PR titles and descriptions. If an open PR already covers the same feature (even partially), **skip that idea and pick the next best one from step 2**. If ALL candidate ideas overlap with open PRs, log "FEATURE_SKIP: all candidates have open PRs" and stop.

4. **Clone the watched repo** into a temp directory and work from there:
   ```bash
   gh repo clone owner/repo /tmp/build-target
   cd /tmp/build-target
   ```

5. **Read the codebase** — understand the project structure, README, package.json/config files, and the area you'll be modifying.

6. **Verify the idea doesn't already exist.** Before writing any code, check `memory/topics/pre-existing-features.md` for a case-insensitive signature-keyword match against the picked idea. If a match hits, skip this idea and return to step 2 to pick the next candidate (treat it the same as a positive grep result below). Then, regardless of the registry result, grep the cloned repo to confirm the chosen idea isn't already shipped under a different name / path / surface. Past misses (May-12 repo-actions batch): "Interactive Embed Widget" already existed as SPA route `/embed/:simulationId`; "Per-Round Belief Snapshot" already existed as `/frame/<round_num>`. Three of five ideas that day were redundant — the build cycle catches it, but the exploration cost is real. A 60-second grep upstream is cheaper. **If the grep surfaces a pre-existing surface that's not yet in the registry, add an entry to `memory/topics/pre-existing-features.md` in this same run** so future `repo-actions` batches don't re-suggest it.

   Cast a wide net across at least these surfaces (skip ones that don't apply to the cloned repo):
   ```bash
   cd /tmp/build-target

   # Backend API routes (Flask / FastAPI / Express / Django / Rails patterns)
   grep -rEn "@(app|blueprint|router|bp)\.(route|get|post|put|delete|patch)|app\.(get|post|put|delete|patch)\(|router\.(get|post|put|delete|patch)\(" \
     backend/ src/ app/ 2>/dev/null | head -80

   # SPA routes (Vue Router / React Router patterns)
   grep -rEn "path:\s*['\"]|<Route\s+path=|createBrowserRouter|RouterModule" \
     frontend/ src/router/ src/routes/ 2>/dev/null | head -50

   # Documented surfaces (features index, API index, README)
   grep -in -E "$KEYWORD1|$KEYWORD2|$KEYWORD3" \
     docs/FEATURES.md docs/API.md README.md openapi.yaml 2>/dev/null
   ```

   Pick 2–4 keywords from the idea's name and intended functionality (e.g. "embed widget" → `embed`, `iframe`, `widget`; "per-round snapshot" → `round`, `snapshot`, `frame`). If a route, SPA path, OpenAPI entry, or documented feature already covers the same intent, **skip this idea and return to step 2 to pick the next candidate.** If ALL candidates from step 2 already exist, log `FEATURE_SKIP: all candidates already implemented` and stop — do not send a notification.

   Brief evidence of the grep (what you searched, what you found) goes in the log entry from step 10.

7. **Decide auth posture UPFRONT — before writing any code.** Most repos default new endpoints behind auth by inheriting the wiring of their sibling endpoints (in MiroShark: `internal_auth_guard` auto-applies to all `/api/*` unless the route is in an explicit allow-list). That default is correct for write/mutation/private-read endpoints but wrong for *public-by-design* surfaces (status probes, capability catalogs, status-page body-matchers, integrator polling endpoints, discoverability registries). Past miss — **PR #149** (`/api/status.json`, 2026-06-05) shipped with default auth-guarded posture, drift-test caught the docs/code disagreement on CI, third squash review-commit had to actively *remove* `internal_auth_guard` from the route. The rewrite was free in retrospect but cost one CI cycle and one review-commit that should have been the initial design.

   Ask three questions before picking a posture:
   1. **Does the picked idea's description, the openapi spec for sibling endpoints, or the PR-body audience name a public-by-design consumer?** Signals to look for: "status page" / "uptime monitor" / "integrator" / "discovery" / "machine-readable" / "polling" / "third-party". If yes → public-without-auth.
   2. **Does the route expose data that would let an anonymous caller infer private state?** (e.g. unknown-id 404 vs private-id 403 lets a caller probe for private existence.) If yes → either keep behind auth, OR design a byte-identical envelope so private + unknown are indistinguishable to the caller (PR #150 `/api/simulation/batch-status` pattern: `{found: false, ...nulls}` for both).
   3. **What do sibling endpoints in `openapi.yaml` say their auth posture is?** `grep -nE "security:|x-internal:|x-public:" backend/openapi.yaml` then read the path entries near the new one. If the sibling family is split (some public, some private), the openapi spec is the source of truth, not the blueprint default.

   Then make the wiring decision *now*, alongside the route handler:
   - **Public** → add the new path to the auth-exemption allow-list in the same commit that adds the route. In MiroShark this lives at `backend/app/__init__.py` in `internal_auth_guard`. The openapi `security: []` (or absence of `security:`) entry on the path must agree.
   - **Private** → no allow-list change; rely on the blueprint default. The openapi path needs a `security:` block matching the project's convention.
   - **Mixed** (e.g. write requires auth but read is public) → handle per-method in the route, allow-list only the public method paths.

   Add a one-line "Auth posture: public / private / mixed — reason" comment near the route handler so reviewers see the decision was deliberate. Include the same line in the PR body's Design notes section.

8. **Implement the feature.** Write clean, complete code. No TODOs or placeholders.

   **Scratch / verifier scripts — repo root is OFF-LIMITS.**
   Any throwaway script you use to sanity-check the build (HMAC verifiers, smoke tests, `sys.path.insert(0, '/tmp/build-target/...')` probes, etc.) MUST live under `/tmp/` — never in the agent repo working directory. The workflow runs `git add -A` after this skill, so any `.py` you leave at the agent repo root gets auto-committed to `main` as tech debt. Past leaks: `sig_smoke.py`, `_smoke_webhook.py`, `.aeon-tmp-verify-trending.py` — flagged in 2026-05-11 push-recap.
   - **DO**: write verifier scripts to `/tmp/verify-${feature}.py` and run them from there.
   - **DON'T**: write `*.py` files in the agent repo cwd, even with leading dot or underscore.
   - Before finishing this step, run `ls *.py .*-tmp-* _smoke_*.py sig_smoke.py 2>/dev/null` in the agent repo root and delete anything that appears. If nothing prints, you're clean.
   - All file-edit tools should target paths under `/tmp/build-target/` (the watched-repo clone) — never paths relative to the agent repo cwd.

9. **Create a branch and push** to the watched repo:
   ```bash
   cd /tmp/build-target
   git checkout -b feat/short-feature-name
   git add -A
   git commit -m "feat: description of what was built"
   git push -u origin feat/short-feature-name
   ```

10. **Open a PR** on the watched repo:
   ```bash
   gh pr create -R owner/repo \
     --title "feat: short description" \
     --body "## What
   Description of the feature.

   ## Why
   What triggered this — repo-actions idea, issue, or gap identified.

   ## Changes
   - file1: what changed
   - file2: what changed

   ---
   *Built autonomously by Aeon*"
   ```

11. **Update memory** — log what was built to `memory/logs/${today}.md` and update `memory/MEMORY.md` Skills Built table.

12. **Send a DETAILED notification** via `./notify`. This is the most important part — the notification goes to a Telegram group and must be rich enough that readers understand exactly what was built, why it matters, and how it works WITHOUT clicking the PR link.

   DO NOT compress this into 1-2 lines. Every section below is REQUIRED:

   ```
   *Feature Built — ${today}*

   [Feature name]
   [2-3 sentence description of what the feature does in plain language. Explain it like you're telling a non-technical person in the community what just got added to the project.]

   Why this matters:
   [2-3 sentences on why this feature is relevant to the project RIGHT NOW. What problem did users/developers have before? What triggered building this — a repo-actions idea, a GitHub issue, a gap noticed in the codebase? How does it move the project forward?]

   What was built:
   - [file/component 1]: [what was added/modified — be specific about the functionality, not just "added endpoint"]
   - [file/component 2]: [same level of detail]
   - [file/component 3 if applicable]
   - [file/component 4 if applicable]

   How it works:
   [3-4 sentences explaining the technical implementation. What approach was chosen and why? What libraries/APIs does it use? How does it integrate with existing code? Any interesting design decisions?]

   What's next:
   [1-2 sentences on follow-up work, potential improvements, or how this connects to the broader roadmap]

   PR: [url]
   ```

   BAD example (too short — DO NOT do this):
   "Feature Built: Simulation Data Export. Users can download results as JSON/CSV. PR: url"

   GOOD example (this is the level of detail expected):
   "Feature Built — 2026-03-25

   Simulation Data Export
   MiroShark simulations now have a one-click export feature. Users can download their full simulation results — including all agent states, interaction logs, and performance metrics — as either JSON (for programmatic use) or CSV (for spreadsheets and analysis).

   Why this matters:
   Until now, simulation data was trapped in the browser. Researchers and developers running MiroShark swarms had no way to extract results for external analysis, comparison across runs, or sharing with collaborators. This was the #2 most requested feature in repo-actions and directly supports the project's goal of being a serious research tool, not just a demo.

   What was built:
   - api/export/route.ts: New API endpoint that serializes simulation state to JSON or CSV based on Accept header. Handles large datasets with streaming response to avoid memory issues.
   - components/ExportButton.tsx: Download buttons added to the simulation results panel. JSON and CSV options with proper MIME types and generated filenames.
   - lib/serializer.ts: Conversion logic that flattens nested agent state trees into tabular CSV format while preserving full structure in JSON output.

   How it works:
   The export endpoint reads the simulation ID from the request, pulls the full state tree from the in-memory store, and streams it as either application/json or text/csv. The CSV serializer walks the nested agent hierarchy depth-first and flattens each agent's state into a row with dot-notation column headers (e.g. agent.memory.shortTerm). The frontend buttons trigger a fetch with the appropriate Accept header and use the download attribute for a clean save-as experience.

   What's next:
   Could add PDF report generation with charts, or a shareable link that hosts the export temporarily for collaboration.

   PR: https://github.com/aaronjmars/MiroShark/pull/1"

Write complete, working code. No TODOs or placeholders.
