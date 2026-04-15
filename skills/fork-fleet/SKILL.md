---
name: fork-fleet
description: Inventory active Aeon forks, detect diverged work, surface upstream contribution candidates
var: ""
tags: [dev]
cron: "0 10 * * 1"
---
> **${var}** — Optional owner/repo to analyze a single fork. If empty, scans all active forks.

Today is ${today}. Track Aeon's fork fleet: discover active forks, analyze divergence, surface the most innovative work for potential upstream contribution.

## Steps

0. **Load managed instance registry** — read `memory/instances.json` (if it exists).
   Build a set of repo full_names that are managed instances (e.g. `owner/aeon-crypto-tracker`).
   These will be tagged differently from organic community forks in the report.

1. **Fetch all forks** of this repo (determine the repo from `git remote get-url origin`):
   ```bash
   PARENT_REPO=$(gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner) --jq '.parent.full_name // .full_name')
   gh api repos/${PARENT_REPO}/forks --paginate --jq '[.[] | {owner: .owner.login, full_name: .full_name, pushed_at, stargazers_count, open_issues_count, forks_count, description}]'
   ```

2. **Filter for active forks** — keep only forks with a `pushed_at` within the last 30 days. If no active forks exist, log `FORK_FLEET_QUIET: no active forks` to `memory/logs/${today}.md` and **stop — do NOT send any notification**.

3. **For each active fork**, analyze divergence by comparing commits against upstream:
   ```bash
   # Get fork's commits not in upstream (diverged work)
   gh api repos/FORK_OWNER/aeon/commits --paginate --jq '[.[] | {sha: .sha[0:7], message: .commit.message, author: .commit.author.name, date: .commit.author.date}]' -X GET -f since="$(date -u -d '90 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-90d +%Y-%m-%dT%H:%M:%SZ)"
   ```
   Then check which of those SHAs exist in upstream:
   ```bash
   gh api repos/${PARENT_REPO}/commits --paginate --jq '[.[].sha]' -X GET -f since="$(date -u -d '90 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-90d +%Y-%m-%dT%H:%M:%SZ)"
   ```
   Commits in the fork but NOT in upstream are **unique fork commits**.

4. **Classify divergence** for each fork using the unique commits. Check which areas were modified by fetching the file tree comparison:
   ```bash
   gh api repos/FORK_OWNER/aeon/compare/${PARENT_REPO##*/}:main...FORK_OWNER:main --jq '{ahead_by: .ahead_by, behind_by: .behind_by, files: [.files[] | {filename, status, additions, deletions}]}'
   ```
   Classify each fork into divergence signals:
   - **New skills**: files added under `skills/` not present in upstream
   - **Custom schedule**: modifications to `aeon.yml` (different cron times, new skill entries)
   - **Modified dashboard**: changes to `dashboard/` directory
   - **Custom notify**: changes to `notify` or `notify-jsonrender` scripts
   - **New articles/content**: files added to `articles/` or `memory/`
   - **Config changes**: changes to `CLAUDE.md`, `.github/`, or root scripts

5. **Score each fork** by divergence:
   - +3 points per new skill file
   - +2 points per unique commit (up to 10)
   - +1 point per modified core file (aeon.yml, dashboard, notify)
   - +1 point per star
   Rank forks by score descending. Flag forks with 5+ unique commits as "high-divergence — potential upstream contribution".

6. **Deep-read top 3 forks**: for each of the top 3 by score, read the actual content of their unique skill files:
   ```bash
   gh api repos/FORK_OWNER/aeon/contents/skills/SKILL_NAME/SKILL.md --jq '.content' | base64 -d
   ```
   Summarize what each unique skill does in 1-2 sentences.

7. **Write the article** to `articles/fork-fleet-${today}.md`:
   ```markdown
   # Fork Fleet Report — ${today}

   ## Overview
   Aeon has N total forks. X are active (pushed within 30 days). Summary of divergence landscape.

   ---

   ## Active Forks — Ranked by Divergence

   ### 1. owner/aeon — Score: N [MANAGED INSTANCE | COMMUNITY FORK]
   **Type:** Managed instance (spawned {date}, purpose: {purpose}) | Community fork
   **Activity:** Last pushed YYYY-MM-DD | Stars: N | Unique commits: N
   **Divergence signals:** [list of signals: "3 new skills", "custom schedule", "modified dashboard"]
   **Unique skills:** [list skill names and 1-sentence descriptions if found]
   **Upstream potential:** [Yes — N new skills worth reviewing / No — schedule changes only]

   ### 2. owner/aeon — Score: N [MANAGED INSTANCE | COMMUNITY FORK]
   ...

   ---

   ## Top Upstream Contribution Candidate
   **Fork:** owner/aeon
   **Why:** [What makes this fork's work most valuable to merge upstream]
   **Suggested action:** [Open a PR from fork's branch, or reach out to fork owner]

   ---

   ## Fleet vs Community
   | Category | Count |
   |----------|-------|
   | Managed instances | N |
   | Community forks | N |
   | Inactive (30+ days) | N |

   ## Coverage Gaps
   Forks not analyzed (inactive for 30+ days): [list]
   ```

8. **Save to memory** — append to `memory/logs/${today}.md`:
   ```
   ## fork-fleet
   - Analyzed N active forks out of M total
   - Top fork: owner/aeon (score: N, N unique commits, N new skills)
   - Article: articles/fork-fleet-${today}.md
   ```

9. **Send a detailed notification** via `./notify`:
   ```
   *Fork Fleet Report — ${today}*

   Aeon has [N] active forks (out of [M] total). [1-2 sentence overview of what the fleet looks like — are they mostly dormant clones, or are people actually building?]

   Top fork: [owner/aeon]
   [2-3 sentences: what makes this fork stand out. How many unique commits? What did they build? Any new skills not in upstream?]

   Divergence signals across fleet:
   - [N] forks with new skills not in upstream
   - [N] forks with custom schedules
   - [N] forks with modified dashboards
   - [N] high-divergence forks (5+ unique commits)

   Upstream contribution candidate: [owner/aeon]
   [1-2 sentences on what this fork built that could be merged back and why it's valuable]

   Full report: articles/fork-fleet-${today}.md
   ```

Write the full article. No TODOs or placeholders.
