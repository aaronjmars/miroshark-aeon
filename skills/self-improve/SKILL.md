---
name: self-improve
description: Improve the agent itself — better skills, prompts, workflows, and config based on recent performance
var: ""
tags: [meta]
---
> **${var}** — Specific area to improve (e.g. "push-recap notification", "token-report formatting", "add error handling to notify"). If empty, analyzes recent logs to find what needs fixing.

Today is ${today}. Your task is to improve **this agent repo** — the skills, workflows, config, prompts, or dashboard. NOT the watched repos.

## Steps

1. **Assess what needs improving** (in this priority order):
   a. If `${var}` is set, work on that specific improvement.
   b. Check `memory/logs/` from the last 24 hours — look for:
      - Skills that logged errors or produced empty/low-quality output
      - Notifications that were truncated or failed (Markdown parse errors)
      - Skills that ran but didn't send notifications when they should have
      - Patterns in the logs that suggest a skill needs tweaking
   c. Check `articles/repo-actions-*.md` for ideas that target the agent itself (not the watched project repos).
   d. Read the current skills in `skills/` — look for:
      - Prompts that are vague or produce inconsistent results
      - Missing error handling or edge cases
      - Skills that could be more useful with small tweaks
      - Notification formats that could be clearer or richer
   e. Check `aeon.yml` and `.github/workflows/` for workflow improvements.
   f. If nothing needs improving, log "SELF_IMPROVE_SKIP: agent is healthy" and **do NOT send any notification. Stop here.**

2. **Pick ONE improvement** — the most impactful, smallest-effort fix. Don't try to do everything at once.

3. **Implement the improvement** directly in this repo. You have full access to:
   - `skills/*/SKILL.md` — skill prompts and instructions
   - `aeon.yml` — skill config, schedules, vars
   - `.github/workflows/` — workflow files
   - `CLAUDE.md` — agent instructions
   - `dashboard/` — dashboard code
   - `memory/` — memory files
   - `notify` script template in workflows

4. **Create a branch, commit, and push**:
   ```bash
   git checkout -b improve/short-description
   git add -A
   git commit -m "improve: description of what was changed"
   git push -u origin improve/short-description
   ```

5. **Open a PR** on this repo:
   ```bash
   gh pr create \
     --title "improve: short description" \
     --body "## What
   Description of the improvement.

   ## Why
   What triggered this — a log entry, a failed skill, a pattern noticed.

   ## Changes
   - file1: what changed
   - file2: what changed

   ---
   *Self-improved by Aeon*"
   ```

6. **Update memory** — log to `memory/logs/${today}.md` and update `memory/MEMORY.md` Skills Built table.

7. **Send a DETAILED notification** via `./notify`:
   ```
   *Agent Self-Improvement — ${today}*

   [What was improved]
   [2-3 sentences explaining the change in plain language]

   Why: [What triggered this — a specific log entry, error pattern, or quality issue observed over the last week]

   What changed:
   - [file 1]: [what was modified and why]
   - [file 2]: [what was modified and why]

   Impact: [How this makes the agent better — more reliable notifications? Better skill output? Fewer errors?]

   PR: [url]
   ```

   **Important:** If no improvement was needed, do NOT send any notification.
