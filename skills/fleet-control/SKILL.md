---
name: Fleet Control
description: Monitor managed Aeon instances — check health, dispatch skills, aggregate status
var: ""
tags: [dev]
cron: "0 9,15 * * *"
---
> **${var}** — Command to execute. Format: `dispatch <instance> <skill>` to run a skill on a child, `status` for fleet overview, or empty for default health check. Examples: `dispatch crypto-tracker token-movers`, `status`.

Today is ${today}. Monitor and manage the fleet of Aeon instances registered in `memory/instances.json`.

## Steps

### 0. Load the fleet registry

Read `memory/instances.json`. If it doesn't exist or has no instances, log `FLEET_EMPTY: no managed instances` to `memory/logs/${today}.md` and **stop — do NOT send a notification**.

Parse the var to determine the command:
- If var starts with `dispatch`: extract instance name and skill, go to **Dispatch Mode**
- If var is `status`: go to **Status Mode**
- If var is empty or anything else: go to **Health Check Mode** (default)

---

### Health Check Mode (default)

1. **For each registered instance**, check its health:

   a. **Repo exists and is accessible**:
   ```bash
   gh api "repos/${REPO}" --jq '.full_name' 2>/dev/null
   ```

   b. **GitHub Actions status** — check if workflows are running:
   ```bash
   gh api "repos/${REPO}/actions/runs?per_page=5" --jq '[.workflow_runs[] | {name: .name, status: .status, conclusion: .conclusion, created_at: .created_at}]'
   ```

   c. **Last activity** — check the most recent push:
   ```bash
   gh api "repos/${REPO}" --jq '.pushed_at'
   ```

   d. **Read the child's cron-state** (if accessible):
   ```bash
   gh api "repos/${REPO}/contents/memory/cron-state.json" --jq '.content' | base64 -d | jq '.'
   ```

   e. **Classify instance health**:
   - **healthy**: Actions running, recent pushes, no failed skills in cron-state
   - **pending_secrets**: No workflow runs at all (instance is inert)
   - **degraded**: Some skills failing in cron-state
   - **stale**: No push in 7+ days but was previously active
   - **unreachable**: API calls fail (repo deleted or permissions changed)

2. **Update the registry** — write back updated status for each instance to `memory/instances.json`. Add a `last_checked` timestamp and `health` field.

3. **Check for instances that need attention**:
   - Any `pending_secrets` older than 7 days — nudge the owner
   - Any `degraded` instances — list which skills are failing
   - Any `stale` instances — flag for review
   - Any `unreachable` instances — mark for cleanup

4. **Log to memory** — append to `memory/logs/${today}.md`:
   ```
   ## fleet-control (health check)
   - Fleet size: N instances
   - Healthy: N | Pending: N | Degraded: N | Stale: N | Unreachable: N
   - Issues: [list any problems found]
   ```

5. **Send notification** via `./notify` (only if there are issues OR this is the first check of the day):
   ```
   *Fleet Status — ${today}*

   Instances: N total
   [For each instance, one line]:
   - {name} ({repo}): {status} — last active {date}, {N} skills running
   
   [If issues exist]:
   Issues:
   - {instance}: {problem description}
   ```

   If all instances are healthy and this is not the first check today, skip the notification.

---

### Dispatch Mode

Parse var: `dispatch <instance-name> <skill-name>`

1. **Look up the instance** in `memory/instances.json` by name.
   If not found, send an error notification and stop.

2. **Check the instance is active** (status is `healthy` or `degraded`).
   If `pending_secrets`, notify: "Cannot dispatch — instance needs secrets configured first."

3. **Dispatch the skill** on the child repo:
   ```bash
   gh workflow run aeon.yml --repo "${REPO}" -f skill="${SKILL_NAME}"
   ```

4. **Log the dispatch** to `memory/logs/${today}.md`:
   ```
   ## fleet-control (dispatch)
   - Dispatched skill '${SKILL_NAME}' on instance '${INSTANCE_NAME}' (${REPO})
   ```

5. **Notify** via `./notify`:
   ```
   *Fleet Dispatch*
   Dispatched '${SKILL_NAME}' on ${INSTANCE_NAME} (${REPO})
   ```

---

### Status Mode

Generate a comprehensive fleet report.

1. **For each instance**, gather:
   - Repo metadata (stars, forks, open issues)
   - Last 10 workflow runs with outcomes
   - Full cron-state.json
   - List of enabled skills (read their aeon.yml)
   - Recent commits (last 5)

2. **Read each child's aeon.yml** to see what skills are enabled:
   ```bash
   gh api "repos/${REPO}/contents/aeon.yml" --jq '.content' | base64 -d
   ```

3. **Write a fleet status article** to `articles/fleet-status-${today}.md`:
   ```markdown
   # Fleet Status Report — ${today}

   ## Overview
   Parent: ${PARENT_REPO}
   Managed instances: N
   Total skills running across fleet: N

   ---

   ## Instance: {name}
   **Repo:** {owner/repo}
   **Purpose:** {purpose}
   **Status:** {health status}
   **Created:** {date}
   **Last active:** {pushed_at}
   **Skills enabled:** {list}
   **Recent runs:**
   | Skill | Status | When |
   |-------|--------|------|
   | ... | ... | ... |

   ---
   [repeat for each instance]

   ## Fleet Health Summary
   | Metric | Value |
   |--------|-------|
   | Total instances | N |
   | Healthy | N |
   | Degraded | N |
   | Pending setup | N |
   | Total skills across fleet | N |
   | Total runs today | N |
   ```

4. **Log and notify** with a summary.

Write complete, working code. No TODOs or placeholders.
