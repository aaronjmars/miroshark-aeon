---
name: repo-article
description: Write an article about the current state, progress, and vision of the watched repo
var: ""
tags: [dev, content]
---
> **${var}** — Angle or topic to focus on (e.g. "architecture", "recent progress", "roadmap"). If empty, auto-selects the most compelling angle.

## Config

This skill reads repos from `memory/watched-repos.md`.

---

Read memory/MEMORY.md and the last 7 days of memory/logs/ for context on recent activity.
Read memory/watched-repos.md for the repo to cover.

## Steps

1. **Gather repo context** — for each watched repo:
   ```bash
   # Repo metadata
   gh api repos/owner/repo --jq '{name, description, language, stargazers_count, forks_count, open_issues_count, topics, created_at, updated_at}'

   # Recent commits (last 7 days)
   gh api repos/owner/repo/commits -X GET -f since="$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)" --jq '.[] | {sha: .sha[0:7], message: .commit.message | split("\n")[0], author: .commit.author.name, date: .commit.author.date}' --paginate

   # Open PRs
   gh api repos/owner/repo/pulls --jq '.[] | {number, title, user: .user.login, created_at, labels: [.labels[].name]}'

   # Recent releases
   gh api repos/owner/repo/releases --jq '.[0:3] | .[] | {tag_name, name, published_at, body}'

   # README
   gh api repos/owner/repo/readme --jq '.content' | base64 -d
   ```

2. **Read key source files** to understand the project's architecture and current state. Look at:
   - Main entry points, config files, package.json
   - Any CHANGELOG, ROADMAP, or similar docs
   - The most recently changed files (from commit history)

3. **Choose the article angle** based on what's most compelling:
   - If `${var}` is set, use that angle
   - Otherwise pick from: recent shipping velocity, architectural decisions, community growth, technical deep-dive on a feature, project vision and where it's heading, comparison with similar projects

4. **Search the web** for external context:
   - Mentions of the project on Twitter, HN, Reddit
   - Similar projects for comparison/positioning
   - Industry trends that make this project relevant

5. **Write a 600-900 word article** in markdown:
   ```markdown
   # [Compelling title about the repo]

   [Hook — why should someone care about this project right now?]

   ## [Section 1 — Current State]
   [What the project does, key metrics, recent activity]

   ## [Section 2 — What's Been Shipping]
   [Recent commits, PRs, releases — explained in plain language]

   ## [Section 3 — Technical Depth or Vision]
   [Architecture insight, design decisions, or where it's heading]

   ## [Section 4 — Why It Matters]
   [Context: market fit, community, ecosystem position]

   ---
   *Sources: [links]*
   ```

6. **Save** to `articles/repo-article-${today}.md`

7. **Log** to `memory/logs/${today}.md` (title, angle chosen, word count) and update `memory/MEMORY.md` Recent Articles table. **Do this before sending the notification.**

8. **Send notification** via `./notify`:
   ```
   *New Article: [title]*

   [2-3 sentence summary of the article]

   Read: [link to articles/repo-article-${today}.md in THIS repo — get the repo name from `git remote get-url origin`, not the watched repo]
   ```
