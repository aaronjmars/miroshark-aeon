---
name: push-recap
description: Daily deep-dive recap of all pushes — reads diffs, explains what changed and why
var: ""
---
> **${var}** — Repo (owner/repo) to recap. If empty, recaps all watched repos.

If `${var}` is set, only recap that repo (owner/repo format).

## Config

This skill reads repos from `memory/watched-repos.md`. If the file doesn't exist yet, create it or skip this skill.

---

Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.
Read memory/watched-repos.md for the list of repos to scan.

## Steps

1. **Fetch push events** for each watched repo from the last 24 hours:
   ```bash
   gh api repos/owner/repo/events --jq '[.[] | select(.type == "PushEvent") | {actor: .actor.login, created_at: .created_at, ref: .payload.ref, commits: [.payload.commits[] | {sha: .sha[0:7], message: .message, author: .author.name}]}]' --paginate
   ```

2. **Fetch commits** directly as a supplement (catches force-pushes, rebases, etc.):
   ```bash
   gh api repos/owner/repo/commits -X GET -f since="$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)" --jq '.[] | {sha: .sha[0:7], full_sha: .sha, message: .commit.message, author: .commit.author.name, date: .commit.author.date}' --paginate
   ```

3. **If no commits found** across all watched repos: log "PUSH_RECAP_QUIET" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

4. **Deduplicate** commits by SHA across both sources.

5. **Read the actual diffs** for each commit to understand what changed:
   ```bash
   gh api repos/owner/repo/commits/FULL_SHA --jq '{files: [.files[] | {filename: .filename, status: .status, additions: .additions, deletions: .deletions, patch: .patch}]}'
   ```
   Read ALL commits in detail. If there are more than 15, read the 15 most significant (by lines changed) and summarize the rest.

6. **Analyze and explain** each commit thoroughly:
   - Read the actual patch content — don't just repeat the commit message
   - What files were changed and what the diff actually shows
   - What feature, fix, or improvement this represents in plain language
   - How it fits into the broader project direction
   - Any notable patterns (new dependencies, architecture changes, refactors, new APIs)
   - If a commit touches multiple areas, break it down by area

7. **Group commits by theme** — don't just list them chronologically. Cluster related commits together under descriptive headings (e.g. "New token tracking system", "Dashboard UX overhaul", "CI/CD improvements").

8. **Write a deep recap** to `articles/push-recap-${today}.md`:
   ```markdown
   # Push Recap — ${today}

   ## Overview
   [2-3 sentence summary: X commits by Y authors. What was the main thrust of today's work? What moved forward?]

   **Stats:** X files changed, +Y/-Z lines across N commits

   ---

   ## owner/repo

   ### [Theme 1: e.g. "New Feature: Token Price Tracking"]
   **Summary:** [2-3 sentences explaining what this group of changes accomplishes]

   **Commits:**
   - `abc1234` — [commit message]
     - Changed `src/token.ts`: Added new `fetchPrice()` function that calls GeckoTerminal API, parses OHLCV response, and caches results (+85 lines)
     - Changed `src/config.ts`: Added `tokenContract` and `chain` fields to the config schema (+12 lines)
     - New file `src/types/token.ts`: Type definitions for price data, pool info, and trade history (+45 lines)

   - `def5678` — [commit message]
     - Changed `src/notify.ts`: Extended notification template to include price formatting with delta arrows (+23, -4 lines)

   **Impact:** [What does this enable? What's the user-facing or developer-facing outcome?]

   ### [Theme 2: e.g. "Bug Fixes & Hardening"]
   **Summary:** [...]

   **Commits:**
   - `ghi9012` — [commit message]
     - Changed `src/worker.ts`: Fixed race condition in concurrent skill execution — added mutex lock around memory file writes (+18, -3 lines)
     - The bug was causing corrupted log entries when two skills ran in the same cron window

   **Impact:** [...]

   ### [Theme 3 if applicable]
   ...

   ---

   ## Developer Notes
   - **New dependencies:** [any added packages, with versions]
   - **Breaking changes:** [any API or config changes that affect other parts]
   - **Architecture shifts:** [any structural changes worth noting]
   - **Tech debt:** [any TODOs introduced or shortcuts taken]

   ## What's Next
   - [Based on today's commits, what's the likely next step?]
   - [Any open threads or incomplete work visible in the diffs?]
   - [Branches created but not merged?]
   ```

9. **Log** to `memory/logs/${today}.md` (repos covered, commit count, article path). **Do this before sending the notification.**

10. **Send a detailed notification** via `./notify`:
   ```
   *Push Recap — ${today}*
   [repo] — X commits by Y authors

   [Theme 1]: [2-sentence explanation of what changed and why it matters]

   [Theme 2]: [2-sentence explanation]

   [Theme 3 if applicable]: [2-sentence explanation]

   Key changes:
   - [most impactful file/feature change with specific detail]
   - [second most impactful]
   - [third most impactful]

   Stats: X files changed, +Y/-Z lines
   Full recap: [link to articles/push-recap-${today}.md in THIS repo — get the repo name from `git remote get-url origin`, not the watched repo]
   ```
   The notification should give someone a full picture without needing to click through. Include actual substance — what was built, what was fixed, what it means — not just commit message summaries.
