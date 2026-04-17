---
name: Issue Triage
description: Label and prioritize new GitHub issues on watched repos
var: ""
tags: [dev]
---
> **${var}** — Repo (owner/repo) to triage. If empty, triages all watched repos.

If `${var}` is set, only triage that repo (owner/repo format).


## Config

This skill reads repos from `memory/watched-repos.md`. If the file doesn't exist yet, create it or skip this skill.

```markdown
# memory/watched-repos.md
- owner/repo
- another-owner/another-repo
```

---

Read memory/MEMORY.md and memory/watched-repos.md for repos to triage.
Read the last 2 days of memory/logs/ to avoid re-triaging.

Steps:
1. For each repo in watched-repos.md, list issues created in the last 48h:
   ```bash
   gh issue list -R owner/repo --state open --json number,title,body,labels,createdAt --limit 20
   ```
2. For each new issue without labels:
   - Read the issue body and classify:
     - **bug** — something broken
     - **feature** — new capability request
     - **question** — needs clarification
     - **urgent** — security, data loss, or blocking
     - **good-first-issue** — well-scoped, self-contained
   - Apply appropriate labels:
     ```bash
     gh issue edit NUMBER -R owner/repo --add-label "label"
     ```
   - If labeled `urgent`, also post a comment acknowledging it:
     ```bash
     gh issue comment NUMBER -R owner/repo --body "Triaged as urgent — flagging for immediate attention."
     ```
3. Send a summary via `./notify` if any urgent issues found.
4. Log what you triaged to memory/logs/${today}.md.
If no new issues, log "ISSUE_TRIAGE_OK" and end.
