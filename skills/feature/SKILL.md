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

3. **Clone the watched repo** into a temp directory and work from there:
   ```bash
   gh repo clone owner/repo /tmp/build-target
   cd /tmp/build-target
   ```

4. **Read the codebase** — understand the project structure, README, package.json/config files, and the area you'll be modifying.

5. **Implement the feature.** Write clean, complete code. No TODOs or placeholders.

6. **Create a branch and push** to the watched repo:
   ```bash
   cd /tmp/build-target
   git checkout -b feat/short-feature-name
   git add -A
   git commit -m "feat: description of what was built"
   git push -u origin feat/short-feature-name
   ```

7. **Open a PR** on the watched repo:
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

8. **Update memory** — log what was built to `memory/logs/${today}.md` and update `memory/MEMORY.md` Skills Built table.

9. **Send a detailed notification** via `./notify`:
   ```
   *Feature Built — ${today}*

   [Feature name]: [1-2 sentence description of what it does]

   Why: [What triggered this — which repo-actions idea, which issue, or what gap?]

   What changed:
   - [file/component 1]: [what was added/modified and why]
   - [file/component 2]: [what was added/modified and why]

   How it works: [2-3 sentences on the implementation approach and key decisions]

   Next steps: [anything left to do, or follow-up work]

   PR: [url]
   ```

   The notification should give someone a complete understanding of the feature without needing to read the PR.

Write complete, working code. No TODOs or placeholders.
