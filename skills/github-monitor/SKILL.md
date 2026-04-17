---
name: GitHub Monitor
description: Watch repos for stale PRs, new issues, and new releases
var: ""
tags: [dev]
---
> **${var}** — Repo (owner/repo) to monitor. If empty, monitors all watched repos.

If `${var}` is set, only monitor that repo (owner/repo format).


## Config

This skill reads repos from `memory/watched-repos.md`. If the file doesn't exist yet, create it or skip this skill.

```markdown
# memory/watched-repos.md
- owner/repo
- another-owner/another-repo
```

---

Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.
Read memory/watched-repos.md for the list of repos to monitor.

For each watched repo, check:
1. Open PRs not updated in >48h: `gh pr list -R owner/repo --json number,title,updatedAt`
2. Issues opened in the last 24h: `gh issue list -R owner/repo --json number,title,createdAt`
3. Latest release: `gh release list -R owner/repo --limit 1 --json tagName,publishedAt,name`

Compare findings against the last 48h of memory/logs/ — never alert on the same item twice.

If anything is noteworthy, send a single consolidated notification via `./notify` with format:
```
*GitHub Monitor*
[repo] 2 stale PRs: #12 title, #15 title
[repo] New issue: #20 title
[repo] New release: v1.2.0
```

Log findings to memory/logs/${today}.md.
If nothing new, log "GITHUB_MONITOR_OK" and end.
