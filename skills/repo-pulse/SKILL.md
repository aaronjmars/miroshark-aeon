---
name: repo-pulse
description: Daily report on new stars, forks, and traffic for watched repos — enriched with each new starrer/forker's profile (name, company, bio, location, followers)
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

   **Idempotency check:** After fetching, scan `memory/logs/${today}.md` for any prior `## Repo Pulse` section. If a prior section for this same repo already recorded identical `stargazers_count` AND identical `forks_count`, log `REPO_PULSE_DUPLICATE — same counts (stars=X, forks=Y) already reported earlier today` and **skip this repo** (do NOT send a notification). This prevents duplicate notifications when repo-pulse is re-triggered (by heartbeat, manual dispatch, or workflow retry) within the same UTC day with no new activity. If counts differ from any prior run today, continue normally — the delta from the true 24h cutoff is still the right thing to report.

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

5b. **Enrich new stargazers and forkers (profile lookup).** Before formatting the notification and article, look up *who* each new account is — a bare handle (`github.com/xyz123`) tells the operator nothing; `@ Vercel · 2.3k followers` tells them a launch is landing. For each new stargazer handle and each new fork owner from the 24h window, make one read-only call:

   ```bash
   gh api users/$LOGIN --jq '{login, name, company, bio, location, blog, twitter_username, followers, public_repos, hireable, created_at}'
   ```

   Rules:
   - **Cap at 25 new accounts per run** (stargazers + forkers combined). If there are more, enrich the first 25 in `starred_at` / `created_at` order and append a final `…and N more` entry un-enriched. Bounds both API calls and message length.
   - **Skip empty fields** — most accounts have `null` company/bio/location. Omit a segment rather than printing a blank.
   - **One-line summary per account**, joining the present fields with ` · ` in this order:
     `${name or login} · @ ${company} · ${location} · ${followers}f · ${public_repos} repos · "${bio trimmed to ~80 chars}"`
     Drop any segment whose source field is empty (e.g. no company → no `@ …` segment). Use `${twitter_username}` / `${blog}` only in the article, not the notification, to keep messages short.
   - **Low-signal flag** — if `followers <= 2` AND `public_repos == 0` AND `created_at` is within the last 30 days, append ` ⚠ new/low-signal`. A soft fake-star tell that complements `star-milestone`'s burst check; annotate, don't suppress.
   - **Sandbox note** — `gh api users/$LOGIN` is read-only and the `gh` CLI handles auth internally (no curl, no env-var headers), so it works in the Actions sandbox. If a lookup fails (deleted/renamed account), fall back to the bare handle for that entry and continue.

6. **Send notification** via `./notify`:
   ```
   *Repo Pulse — ${today}*
   [owner/repo]

   Stars: X total (+N new)
   Forks: Y total (+N new)

   New stargazers:
   - github.com/alice — Alice Chen · @ Vercel · San Francisco · 2.3k followers · 87 repos · "building dev tools"
   - github.com/bob — @ Stripe · 480 followers
   - github.com/carol — 4 followers · joined 6d ago ⚠ new/low-signal

   New forks:
   - github.com/dave/repo — Dave Kim · @ Acme · 1.1k followers
   ```

   Format rules:
   - **One enriched line per stargazer/forker** (from step 5b): `- github.com/${handle} — ${summary}`. The `github.com/${handle}` prefix MUST stay first; the profile summary follows after ` — `.
   - If step 5b produced no summary for an account (all fields empty or lookup failed), fall back to the bare `- github.com/${handle}` line.
   - Omit "New stargazers" section entirely if there are none
   - Omit "New forks" section entirely if there are none
   - Do NOT include traffic data, watchers, or open issues

7. **Write the article** to `articles/repo-pulse-${today}.md` — this is the canonical structured artifact that downstream consumers (`operator-scorecard`, `thread-formatter`, `star-momentum-alert`, `show-hn-draft`, `skill-freshness`) read. Always write the file when at least one repo was fetched in this run, even when there are zero new stars and zero new forks — consumers need the counts row to verify "no activity" vs "no run". Overwrite on same-day reruns so the file always reflects the latest counts.

   Format (one `##` block per non-skipped repo, in the order they were processed):

   ```markdown
   # Repo Pulse — ${today}

   ## aaronjmars/repo

   - **stargazers_count:** X
   - **forks_count:** Y
   - **New stars (24h):** N
   - **New forks (24h):** M
   - **Notification sent:** yes/no

   **New stargazers:**
   - github.com/user1 — Alice Chen · @ Vercel · San Francisco · 2.3k followers · 87 repos · twitter.com/alice · "building dev tools"
   - github.com/user2 — @ Stripe · 480 followers

   **New forks:**
   - github.com/user1/repo — Dave Kim · @ Acme · 1.1k followers
   ```

   Format rules:
   - The two key fields `stargazers_count` and `forks_count` MUST use the exact `**stargazers_count:** N` / `**forks_count:** N` markup (matches `operator-scorecard` step 3a parser).
   - Each `**New stargazers:**` / `**New forks:**` bullet is `- github.com/${handle} — ${profile summary}` from step 5b (the fuller form including `twitter`/`blog`, with empty fields dropped and ` ⚠ new/low-signal` appended for low-signal accounts). The bare `github.com/${handle}` prefix MUST stay first so the handle is still parseable; if step 5b produced no summary, emit the bare handle line. Cap at the 25 enriched accounts; if more, append a final `- …and N more` bullet.
   - The two delta fields `New stars (24h)` and `New forks (24h)` MUST use the exact `**New stars (24h):** N` / `**New forks (24h):** N` markup (same parser).
   - Omit the `**New stargazers:**` block entirely if N == 0. Same for forks.
   - For multi-repo runs, emit one `##` block per repo in fetch order; do not interleave fields across repos.
   - Repos that were skipped via the step-1 idempotency gate (`REPO_PULSE_DUPLICATE`) appear in the article as a single-line `- **Status:** REPO_PULSE_DUPLICATE` row under the repo header — keep the counts on the same row as a courtesy for the parser, but omit the `New stargazers` / `New forks` lists (the earlier same-day run already covered them).
   - If ALL repos in the run hit the idempotency gate, still write the file (overwrite) so the article date suffix advances and consumers can find today's file — the body is just the per-repo `REPO_PULSE_DUPLICATE` rows.

8. **Log** to `memory/logs/${today}.md` — ALWAYS include the exact current counts so the next run can calculate deltas:
   ```
   ## Repo Pulse
   - **aaronjmars/repo**: stargazers_count=X, forks_count=Y
   - **New stars (24h):** N
   - **New forks (24h):** N
   - **Article:** articles/repo-pulse-${today}.md
   - **Notification sent:** yes/no
   ```

   If step 1's idempotency check skipped the repo, still log a short entry so the skip is visible in the record:
   ```
   ## Repo Pulse
   - **aaronjmars/repo**: stargazers_count=X, forks_count=Y
   - **Status:** REPO_PULSE_DUPLICATE (same counts as earlier run today — skipped notification)
   ```
