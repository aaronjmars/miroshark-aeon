---
name: feature
description: Build new features from GitHub issues or improve the agent
var: ""
---
> **${var}** — Feature to build. If empty, picks from GitHub issues or memory.

If `${var}` is set, build that feature instead of picking from issues.


Today is ${today}. Your task is to build a new feature for this repository.

## Steps

1. Read `memory/MEMORY.md` for context.
2. Check open GitHub issues labelled "ai-build" using `gh issue list --label ai-build`.
   If there are none, check memory for planned features, or pick a reasonable
   improvement (e.g. a new skill, better prompts).
3. Read the relevant existing files to understand the codebase.
4. Implement the feature. Write clean code.
5. Create a branch, commit, and open a PR with a clear title and description.
6. Update memory/MEMORY.md to record what was built.
7. Log what you did to memory/logs/${today}.md.

8. **Send a detailed notification** via `./notify` that explains what was built and why:
   ```
   *Feature Built — ${today}*

   [Feature name]: [1-2 sentence description of what it does]

   Why: [What problem does this solve? What triggered building this — an issue, a gap in functionality, a pattern noticed in logs?]

   What changed:
   - [file/component 1]: [what was added/modified and why]
   - [file/component 2]: [what was added/modified and why]
   - [file/component 3 if applicable]

   How it works: [2-3 sentences explaining the implementation — what approach was taken, key design decisions, how it integrates with existing code]

   Next steps: [anything left to do, or how this connects to future work]

   PR: [url]
   ```

   The notification should give someone a complete understanding of the feature without needing to read the PR. Include the reasoning behind implementation choices, not just what files changed.

   **Important:** If no suitable feature was found to build (no issues, no planned features, nothing useful to add), log "FEATURE_SKIP: no suitable feature found" and **do NOT send any notification**.

Write complete, working code. No TODOs or placeholders.
