---
name: Changelog
description: Generate a changelog from recent commits across watched repos
var: ""
tags: [dev]
---
> **${var}** — Repo (owner/repo) to scan. If empty, scans all watched repos.

If `${var}` is set, only scan that repo (owner/repo format).


## Config

This skill reads repos from `memory/watched-repos.md`. If the file doesn't exist yet, create it or skip this skill.

```markdown
# memory/watched-repos.md
- owner/repo
- another-owner/another-repo
```

---

Read memory/MEMORY.md and memory/watched-repos.md for repos to scan.
Read the last 7 days of memory/logs/ for context.

Steps:
1. For each repo in watched-repos.md, get commits from the last 7 days:
   ```bash
   gh api repos/owner/repo/commits --jq '.[] | {sha: .sha[0:7], message: .commit.message, author: .commit.author.name, date: .commit.author.date}' --paginate -X GET -f since="$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)"
   ```
2. Group commits by type using conventional commit prefixes:
   - **Features** (feat:)
   - **Fixes** (fix:)
   - **Docs** (docs:)
   - **Chores** (chore:, ci:, build:)
   - **Other** (everything else)
3. Write a clean changelog and save to articles/changelog-${today}.md:
   ```markdown
   # Changelog — Week of ${today}

   ## repo-name
   ### Features
   - description (sha)

   ### Fixes
   - description (sha)
   ```
4. Send an abbreviated version via `./notify`.
5. Log what you did to memory/logs/${today}.md.
