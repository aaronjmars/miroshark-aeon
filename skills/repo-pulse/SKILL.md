---
name: repo-pulse
description: Daily report on new stars, forks, and traffic for watched repos
var: ""
tags: [dev]
---
> **${var}** — Repo (owner/repo) to check. If empty, checks all watched repos.

## Config

This skill reads repos from `memory/watched-repos.md` but **skips agent/monitoring repos** (repos that contain "aeon-agent" or "miroshark-aeon" in their name). Only track the actual project repos — not the agent repos that run the skills.

---

Read memory/MEMORY.md and the last 3 days of memory/logs/ for previous star/fork counts to calculate deltas.
Read memory/watched-repos.md for the list of repos to track. Skip any repo whose name ends with "-aeon" or contains "aeon-agent" — those are agent repos, not project repos.

## Steps

1. **Fetch repo stats** for each watched repo:
   ```bash
   gh api repos/owner/repo --jq '{stargazers_count, forks_count, watchers_count, open_issues_count, subscribers_count}'
   ```

2. **Compute the 24h cutoff timestamp** FIRST — this is critical:
   ```bash
   CUTOFF=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)
   ```
   Use this `$CUTOFF` for ALL time filtering below. Do NOT use "today's date" — use exactly 24 hours ago from now.

3. **Fetch the most recent stargazers** — efficiently, without downloading all pages:
   ```bash
   # Calculate the last page (100 per page) to avoid fetching all stargazers
   STARS=$(gh api repos/owner/repo --jq '.stargazers_count')
   LAST_PAGE=$(( (STARS + 99) / 100 ))
   # Fetch only the last 2 pages (covers up to 200 most recent stars)
   PREV_PAGE=$(( LAST_PAGE > 1 ? LAST_PAGE - 1 : 1 ))
   gh api "repos/owner/repo/stargazers?per_page=100&page=$PREV_PAGE" -H "Accept: application/vnd.github.star+json" --jq '.[] | {user: .user.login, starred_at: .starred_at}'
   gh api "repos/owner/repo/stargazers?per_page=100&page=$LAST_PAGE" -H "Accept: application/vnd.github.star+json" --jq '.[] | {user: .user.login, starred_at: .starred_at}'
   ```
   Combine the results from both pages, deduplicate by user, and keep only entries where `starred_at` >= `$CUTOFF` (24 hours ago). NOT "since midnight today" — since exactly 24 hours ago.

   **Why not `--paginate`?** The stargazers API returns oldest-first. Using `--paginate` fetches ALL pages (O(N) API calls as stars grow). Fetching only the last 2 pages is O(1) and covers up to 200 recent stars — more than enough for 24h changes.

4. **Fetch recent forks** (sorted by newest):
   ```bash
   gh api "repos/owner/repo/forks?sort=newest&per_page=10" --jq '.[] | {owner: .owner.login, created_at: .created_at, full_name: .full_name}'
   ```
   Keep only forks where `created_at` >= `$CUTOFF`.

5. **Determine if there's activity to report.** Check BOTH:
   - **New stargazers from step 3**: any with `starred_at` >= the 24h cutoff
   - **New forks from step 4**: any with `created_at` >= the 24h cutoff

   **Send a notification if ANY of these are true:**
   - At least 1 new stargazer in the last 24h (unstars don't cancel this out)
   - At least 1 new fork in the last 24h
   - First run (no previous data in logs)

   Only log "REPO_PULSE_QUIET" and skip notification if ZERO new stargazers AND ZERO new forks since the 24h cutoff.

6. **Send notification** via `./notify`:
   ```
   *Repo Pulse — ${today}*
   [owner/repo]

   Stars: X total (+N new)
   Forks: Y total (+N new)

   New stargazers:
   github.com/user1 | github.com/user2 | github.com/user3

   New forks:
   github.com/user1/repo | github.com/user2/repo
   ```

   Format rules:
   - List stargazers on one line separated by ` | ` (not one per line)
   - Same for forks
   - Omit "New stargazers" section entirely if there are none
   - Omit "New forks" section entirely if there are none
   - Do NOT include traffic data, watchers, or open issues

7. **Log** to `memory/logs/${today}.md` — ALWAYS include the exact current counts so the next run can calculate deltas:
   ```
   ## Repo Pulse
   - **aaronjmars/repo**: stargazers_count=X, forks_count=Y
   - **New stars (24h):** N
   - **New forks (24h):** N
   - **Notification sent:** yes/no
   ```
