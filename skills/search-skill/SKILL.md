---
name: Search Skills
description: Search the open agent skills ecosystem for useful skills to install
var: ""
tags: [meta]
---
> **${var}** — Capability to search for. If empty, searches based on current gaps.


Read `memory/MEMORY.md` for context on current goals and capability gaps.

Steps:
1. Determine what to search for:
   - If `${var}` is set, use that.
   - Otherwise, look at recent logs and memory for capability gaps, failed skills, or requested features that could be solved by an existing skill.
2. Search for skills using the CLI:
   ```bash
   npx skills find "${query}"
   ```
3. If no results or you want to browse a specific repo, list available skills:
   ```bash
   npx skills add vercel-labs/agent-skills --list
   ```
4. For any interesting skill found, evaluate:
   - Does it fill a gap we don't already cover in `skills/`?
   - Is it compatible with Claude Code?
   - Would it be useful given our current goals?
5. If a skill is worth installing, install it globally for Claude Code:
   ```bash
   npx skills add <source> --skill "<skill-name>" -a claude-code -g -y
   ```
6. Send a notification via `./notify` with what was found:
   ```
   Skill Search: searched for "${query}"
   - Found: skill1 — description
   - Found: skill2 — description
   - Installed: skill1 (reason)
   ```
   If nothing useful was found, notify with a brief summary of what was searched.
7. Log results to `memory/logs/${today}.md`.
