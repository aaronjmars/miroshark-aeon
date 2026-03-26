---
name: repo-pulse
description: Daily report on new stars, forks, and traffic for watched repos
var: ""
---
> **${var}** — Repo (owner/repo) to check. If empty, checks all watched repos.

## Config

This skill reads repos from `memory/watched-repos.md`.

---

Read memory/MEMORY.md and the last 3 days of memory/logs/ for previous star/fork counts to calculate deltas.
Read memory/watched-repos.md for the list of repos to track.

## Steps

1. **Fetch repo stats** for each watched repo:
   ```bash
   gh api repos/owner/repo --jq '{stargazers_count, forks_count, watchers_count, open_issues_count, subscribers_count}'
   ```

2. **Fetch the most recent stargazers** — use `--paginate` and grab the last page to get the newest stars:
   ```bash
   # Get the last 20 stargazers (most recent) with timestamps
   gh api repos/owner/repo/stargazers -H "Accept: application/vnd.github.star+json" --paginate --jq '.[] | {user: .user.login, starred_at: .starred_at}' | tail -20
   ```
   Filter these to only show stargazers from the last 24 hours.

3. **Fetch recent forks** (sorted by newest):
   ```bash
   gh api "repos/owner/repo/forks?sort=newest&per_page=10" --jq '.[] | {owner: .owner.login, created_at: .created_at, full_name: .full_name}'
   ```
   Filter to only show forks from the last 24 hours.

4. **Fetch traffic data** (requires push access to the repo):
   ```bash
   gh api repos/owner/repo/traffic/views --jq '{count, uniques}'
   gh api repos/owner/repo/traffic/clones --jq '{count, uniques}'
   gh api repos/owner/repo/traffic/popular/referrers --jq '.[0:5]'
   ```
   If traffic endpoints return 403, skip traffic data and note it.

5. **Determine if there's activity to report.** There are TWO signals — check BOTH:
   - **New stargazers from step 2**: filter the list to only those with `starred_at` in the last 24 hours. If there are ANY, that counts as activity.
   - **New forks from step 3**: filter to forks with `created_at` in the last 24 hours.

   **Send a notification if ANY of these are true:**
   - There is at least 1 new stargazer in the last 24h (regardless of net total change — unstars don't cancel this out)
   - There is at least 1 new fork in the last 24h
   - This is the first run (no previous data in logs)

   Only log "REPO_PULSE_QUIET" and skip notification if there are truly ZERO new stargazers AND ZERO new forks in the last 24h.

7. **Send notification** via `./notify`:
   ```
   *Repo Pulse — ${today}*
   [owner/repo]

   Stars: X (+N new today)
   Forks: Y (+N new today)
   Watchers: Z

   New stargazers today:
   - github.com/user1
   - github.com/user2
   - github.com/user3
   [list all stargazers from the last 24h]

   New forks today:
   - github.com/user/fork-name
   [list all forks from the last 24h]

   Traffic (14d): X views (Y unique) | Z clones
   Top referrers: [list top 3]
   ```

   If there are many new stars (5+), lead with an excited tone. If it's just 1-2, keep it factual.

8. **Log** to `memory/logs/${today}.md` — ALWAYS include the exact current counts in this format so the next run can calculate deltas:
   ```
   ## Repo Pulse
   - **aaronjmars/repo**: stargazers_count=X, forks_count=Y
   - **New stars today:** N
   - **New forks today:** N
   - **Notification sent:** yes/no
   ```
