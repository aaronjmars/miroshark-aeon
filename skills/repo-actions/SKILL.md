---
name: repo-actions
description: Generate actionable ideas to improve the repo — features, integrations, community, and growth
var: ""
---
> **${var}** — Focus area (e.g. "features", "community", "integrations", "security"). If empty, covers all areas.

## Config

This skill reads repos from `memory/watched-repos.md`.

---

Read memory/MEMORY.md and the last 7 days of memory/logs/ for context.
Read memory/watched-repos.md for the repo to analyze.

## Steps

1. **Assess current repo state**:
   ```bash
   # Repo info
   gh api repos/owner/repo --jq '{name, description, language, stargazers_count, forks_count, open_issues_count, topics}'

   # Open issues (potential feature requests, bugs)
   gh api repos/owner/repo/issues --jq '[.[] | select(.pull_request == null) | {number, title, labels: [.labels[].name], created_at, comments}] | .[0:20]'

   # Recent commits (what's the current development direction?)
   gh api repos/owner/repo/commits -X GET -f since="$(date -u -d '14 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-14d +%Y-%m-%dT%H:%M:%SZ)" --jq '.[] | {sha: .sha[0:7], message: .commit.message | split("\n")[0]}' --paginate

   # Contributors
   gh api repos/owner/repo/contributors --jq '.[0:10] | .[] | {login, contributions}'
   ```

2. **Read the codebase** — look at the README, main source files, package.json/Cargo.toml/etc., and any TODO/ROADMAP files to understand what the project does and where it's heading.

3. **Search for ecosystem context**:
   - What are similar projects doing?
   - What's trending in this project's domain?
   - What integrations would make sense?

4. **Check open PRs** to avoid suggesting ideas that are already in progress:
   ```bash
   gh pr list -R owner/repo --state open --json title,body,headRefBranch --limit 20
   ```
   Also check the last 7 days of `articles/repo-actions-*.md` for previously suggested ideas. Do NOT regenerate ideas that overlap with open PRs or were already suggested in the past 7 days.

5. **Generate 5 action ideas** — concrete, implementable suggestions that the `feature` skill can autonomously build tomorrow. Each should be:
   - Specific enough to be a GitHub issue
   - Scoped so an AI agent can implement it autonomously (clear inputs/outputs, no ambiguous design decisions, no external approvals needed)
   - Feasible within 1-3 days of focused work
   - Valuable for the project's growth, quality, or community

   Categories to draw from (pick whichever 5 are most relevant):
   - **Feature** — new capability that users would want
   - **Integration** — connect with another tool, API, or ecosystem
   - **DX improvement** — better docs, setup, error messages, onboarding
   - **Performance** — optimization, caching, reducing overhead
   - **Community** — contributor guide, examples, templates, showcase
   - **Security** — audit, dependency updates, access control
   - **Content** — blog post, tutorial, demo, tweet thread
   - **Growth** — listing on directories, partnerships, ecosystem plays

6. **Format each idea**:
   ```
   ### [N]. [Idea Title]
   **Type:** [Feature/Integration/DX/Performance/Community/Security/Content/Growth]
   **Effort:** [Small (hours) / Medium (1-2 days) / Large (3+ days)]
   **Impact:** [Why this moves the needle — specific outcome]
   **How:** [2-3 concrete steps to implement]
   ```

7. **Write** to `articles/repo-actions-${today}.md`

8. **Send notification** via `./notify`:
   ```
   *Repo Action Ideas — ${today}*
   Generated from analysis of the current project — these are ideas that could be autonomously built by the feature skill tomorrow.

   1. [idea title] ([type], [effort])
      [1-sentence description of what it does and why]

   2. [idea title] ([type], [effort])
      [1-sentence description]

   3. [idea title] ([type], [effort])
      [1-sentence description]

   4. [idea title] ([type], [effort])
      [1-sentence description]

   5. [idea title] ([type], [effort])
      [1-sentence description]

   Full details: [link to articles/repo-actions-${today}.md in THIS repo — get the repo name from `git remote get-url origin`, not the watched repo]
   ```

9. **Log** to `memory/logs/${today}.md`.
