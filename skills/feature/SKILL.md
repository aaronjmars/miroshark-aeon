---
name: feature
description: Build a feature for the watched repo — picks from yesterday's repo-actions ideas first
var: ""
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

6. **Implement the feature.** Write clean, complete code. No TODOs or placeholders.

7. **Create a branch and push** to the watched repo:
   ```bash
   cd /tmp/build-target
   git checkout -b feat/short-feature-name
   git add -A
   git commit -m "feat: description of what was built"
   git push -u origin feat/short-feature-name
   ```

8. **Open a PR** on the watched repo:
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

9. **Update memory** — log what was built to `memory/logs/${today}.md` and update `memory/MEMORY.md` Skills Built table.

10. **Send a DETAILED notification** via `./notify`. This is the most important part — the notification goes to a Telegram group and must be rich enough that readers understand exactly what was built, why it matters, and how it works WITHOUT clicking the PR link.

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
