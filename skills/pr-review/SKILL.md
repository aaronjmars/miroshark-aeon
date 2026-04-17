---
name: PR Review
description: Auto-review open PRs on watched repos and post summary comments
var: ""
tags: [dev]
---
> **${var}** — Repo (owner/repo) to review. If empty, reviews all watched repos.

If `${var}` is set, only review PRs on that repo (owner/repo format).


## Config

This skill reads repos from `memory/watched-repos.md`. If the file doesn't exist yet, create it or skip this skill.

```markdown
# memory/watched-repos.md
- owner/repo
- another-owner/another-repo
```

---

Read memory/MEMORY.md and memory/watched-repos.md for repos to review.
Read the last 2 days of memory/logs/ to avoid reviewing the same PR twice.

Steps:
1. For each repo in watched-repos.md, list open PRs:
   ```bash
   gh pr list -R owner/repo --state open --json number,title,author,createdAt,updatedAt,body,additions,deletions,changedFiles
   ```
2. For each PR not already reviewed in recent logs:
   - Fetch the diff: `gh pr diff NUMBER -R owner/repo`
   - Review for:
     - Logic errors or bugs
     - Security concerns (injection, exposed secrets, unsafe operations)
     - Code quality (naming, structure, duplication)
     - Missing tests or edge cases
   - Keep feedback concise and actionable — no nitpicks
3. Post a review comment on the PR:
   ```bash
   gh pr review NUMBER -R owner/repo --comment --body "review text"
   ```
4. Send a summary via `./notify`:
   ```
   *PR Review — ${today}*
   Reviewed N PRs across M repos.
   - owner/repo#123: summary of findings
   ```
5. Log what you reviewed to memory/logs/${today}.md.
If no open PRs found, log "PR_REVIEW_OK" and end.
