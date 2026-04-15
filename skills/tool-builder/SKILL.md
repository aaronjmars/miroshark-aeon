---
name: Tool Builder
description: Build automation scripts from action-converter suggestions and recurring manual tasks
var: ""
tags: [dev, build]
depends_on: [action-converter]
---
> **${var}** — Specific tool or automation to build. If empty, finds opportunities from recent action-converter outputs and logs.

If `${var}` is set, build that specific tool instead of auto-selecting.

Today is ${today}. Your task is to identify a recurring manual task and build a script or tool that automates it.

## Steps

1. **Find automation opportunities.** If `${var}` is empty:
   - Read last 7 days of `memory/logs/` — look for action-converter outputs
   - Read recent articles matching `output/articles/prototype-*` or action-converter patterns
   - Read `memory/MEMORY.md` for tracked goals or recurring tasks
   - Read `output/skills/action-converter.md` if it exists (chain context)
   - Look for patterns:
     - Actions suggested more than once across different days
     - Actions that involve repetitive commands or API calls
     - "Check X", "Monitor Y", "Fetch Z" type tasks that could be automated
     - Manual data collection that could be scripted

2. **Design the tool.** Define:
   - What it does (one sentence)
   - Input: what does it take? (args, env vars, stdin)
   - Output: what does it produce? (stdout, file, notification)
   - Dependencies: what does it need? (curl, jq, node, python — prefer things already in the workflow)

3. **Build it.** Write the tool to `scripts/{tool-name}`:
   ```bash
   mkdir -p scripts
   ```
   Prefer bash scripts when possible — they run everywhere in the workflow with zero setup.
   For more complex tools, use Node.js (already available) or Python.

   Requirements:
   - Must be self-contained (no npm install, no pip install)
   - Must have a shebang line and be executable
   - Must handle errors gracefully (set -euo pipefail for bash)
   - Must include a usage comment at the top
   - Must work in both local and GitHub Actions environments

4. **Test it.** Run the tool and verify it works:
   ```bash
   chmod +x scripts/{tool-name}
   scripts/{tool-name} [test args]
   ```
   If it fails, fix it. If it needs an API key or secret that isn't available, note it as a requirement.

5. **Create a branch and PR:**
   ```bash
   git checkout -b feat/tool-{name}-${today}
   git add scripts/{tool-name}
   git commit -m "feat(scripts): add {tool-name} — [description]"
   ```
   Open a PR:
   ```bash
   gh pr create --title "feat(scripts): {tool-name}" \
     --body "## What\n[description]\n\n## Usage\n\`\`\`bash\n./scripts/{tool-name} [args]\n\`\`\`\n\n## Why\nAppeared in action-converter outputs on [dates] / identified from [source]"
   ```

6. **Notify.** Send via `./notify`:
   ```
   tool-builder: built scripts/{tool-name} — [one-line description]
   PR: [url]
   ```

7. **Log.** Append to `memory/logs/${today}.md`:
   ```
   ## Tool Builder
   - **Tool:** scripts/{tool-name}
   - **What:** [description]
   - **Source:** [what triggered this — action-converter output, recurring pattern, etc.]
   - **PR:** [url]
   ```

## Guidelines

- Build small, focused tools. One tool, one job.
- Bash first, Node.js second, Python third. Match the existing codebase.
- Tools should be useful standalone — not just wrappers around a single curl command (unless that curl is complex).
- Don't build tools that duplicate existing skills. Check `skills/` first.
- If the tool needs a new secret/API key, document it but don't block on it.
- Prefer tools that you can run locally with `./scripts/{name}`, not just CI-only.

## Sandbox note

The sandbox may block outbound curl. Built tools that need network access should include a **WebFetch** fallback or use the pre-fetch/post-process pattern (see CLAUDE.md).
