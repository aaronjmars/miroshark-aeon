---
name: Spawn Instance
description: Clone this Aeon agent into a new GitHub repo — fork, configure skills, register in fleet
var: ""
tags: [dev]
---
> **${var}** — Name and purpose of the new instance, e.g. `crypto-tracker: monitor DeFi protocols and token movements`. If empty, the skill will ask via notification what kind of instance to create and stop.

Today is ${today}. Create a new Aeon instance by forking this repo, configuring it for a specific purpose, and registering it in the fleet.

## Security Model

This skill creates the repo and configuration but does **NOT** propagate secrets.
The new instance is inert until the owner manually sets secrets (ANTHROPIC_API_KEY, etc.).
This is intentional — each instance should have its own API keys for billing isolation and blast-radius containment.

## Steps

1. **Parse the var** to extract instance name and purpose:
   - Format: `name: purpose` (e.g. `crypto-tracker: monitor DeFi protocols`)
   - If var is empty, log to `memory/logs/${today}.md` and send a notification asking the owner to re-run with a var, then **stop**.
   - Derive the repo name: `aeon-{name}` (e.g. `aeon-crypto-tracker`)
   - Sanitize: lowercase, hyphens only, max 40 chars

2. **Check the fleet registry** — read `memory/instances.json` (create if missing).
   If an instance with the same name already exists and is not archived, log a warning and **stop**.

   The registry format:
   ```json
   {
     "instances": [
       {
         "name": "crypto-tracker",
         "repo": "OWNER/aeon-crypto-tracker",
         "purpose": "monitor DeFi protocols and token movements",
         "created": "2026-04-08",
         "status": "pending_secrets",
         "skills_enabled": ["token-movers", "defi-monitor", "heartbeat"],
         "parent": "OWNER/aeon"
       }
     ]
   }
   ```

3. **Determine the owner** for the new repo:
   ```bash
   OWNER=$(gh api user --jq '.login')
   ```

4. **Fork the repo** into the owner's account with the custom name:
   ```bash
   PARENT_REPO=$(gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner) --jq '.parent.full_name // .full_name')
   gh repo fork "$PARENT_REPO" --fork-name "aeon-{name}" --clone=false
   ```
   If the fork already exists (gh returns an error), check if it's already registered. If not, proceed to configure it.

   Note: `gh repo fork` may not support `--fork-name` in all versions. If it fails, fall back to:
   ```bash
   gh api repos/${PARENT_REPO}/forks -X POST -f name="aeon-{name}"
   ```

5. **Wait for fork availability** — GitHub forks are async. Poll until ready:
   ```bash
   for i in 1 2 3 4 5; do
     gh api "repos/${OWNER}/aeon-{name}" --jq '.full_name' 2>/dev/null && break
     sleep 5
   done
   ```

6. **Select skills for the instance** based on its purpose. Analyze the purpose string and choose from the available skills. Use these heuristics:
   - **crypto/defi/token** purpose: enable `token-movers`, `token-alert`, `defi-monitor`, `wallet-digest`, `trending-coins`, `heartbeat`
   - **research/papers/academic** purpose: enable `paper-digest`, `paper-pick`, `research-brief`, `deep-research`, `heartbeat`
   - **social/twitter/x** purpose: enable `fetch-tweets`, `tweet-digest`, `write-tweet`, `reply-maker`, `heartbeat`
   - **news/digest** purpose: enable `morning-brief`, `rss-digest`, `hn-digest`, `reddit-digest`, `heartbeat`
   - **dev/code/github** purpose: enable `github-monitor`, `github-issues`, `pr-review`, `code-health`, `changelog`, `heartbeat`
   - **general** or unclear: enable `morning-brief`, `heartbeat`, `reflect`
   - Always include `heartbeat` for health monitoring.

7. **Clone the fork, configure it, and push**:
   ```bash
   # Clone into a temp directory
   TMPDIR=$(mktemp -d)
   gh repo clone "${OWNER}/aeon-{name}" "$TMPDIR/repo"
   cd "$TMPDIR/repo"
   git config user.name "aeonframework"
   git config user.email "aeonframework@proton.me"
   ```

   a. **Write a customized `aeon.yml`**: Read the parent's `aeon.yml` as a base. Enable only the selected skills. Keep all others disabled. Preserve the structure and comments.

   b. **Write `SETUP.md`** to the repo root:
   ```markdown
   # Aeon Instance Setup

   This is a managed Aeon instance spawned from [parent-repo].

   ## Purpose
   {purpose description}

   ## Activate This Instance

   Go to **Settings > Secrets and variables > Actions** and add these secrets:

   ### Required
   | Secret | Description |
   |--------|------------|
   | `ANTHROPIC_API_KEY` | Claude API key — get one at console.anthropic.com |

   ### Recommended
   | Secret | Description |
   |--------|------------|
   | `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications |
   | `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications |

   ### Optional (depends on enabled skills)
   | Secret | Description |
   |--------|------------|
   | `COINGECKO_API_KEY` | For crypto skills |
   | `XAI_API_KEY` | For X/Twitter skills |
   | `DISCORD_WEBHOOK_URL` | Discord notifications |
   | `SLACK_WEBHOOK_URL` | Slack notifications |

   ## Enabled Skills
   {list of enabled skills with descriptions}

   ## Fleet Parent
   This instance is managed by `{parent-repo}`.
   The parent can dispatch skills and monitor health via the `fleet-control` skill.

   ## Security Note
   This instance has NO access to the parent's secrets.
   Each instance maintains its own API keys and credentials.
   ```

   c. **Update the CLAUDE.md** to reference the parent:
   Add a line under the "About This Repo" section: `- Managed instance of {parent-repo}. Purpose: {purpose}.`

   d. **Clear the parent's memory** — reset `memory/MEMORY.md` to a fresh state for the child, remove `memory/logs/*` contents, clear `memory/cron-state.json` to `{}`. Keep `memory/topics/` empty. The child starts with a clean slate.

   e. **Commit and push**:
   ```bash
   git add -A
   git commit -m "chore: configure instance — {purpose}"
   git push origin main
   ```

   f. **Clean up**:
   ```bash
   rm -rf "$TMPDIR"
   ```

8. **Enable GitHub Actions** on the fork (forks have Actions disabled by default):
   ```bash
   gh api "repos/${OWNER}/aeon-{name}/actions/permissions" -X PUT -f enabled=true -f allowed_actions=all
   ```

9. **Register the instance** — update `memory/instances.json` in the parent repo:
   Add the new instance entry with `status: "pending_secrets"`.

10. **Log to memory** — append to `memory/logs/${today}.md`:
    ```
    ## spawn-instance
    - Created new instance: ${OWNER}/aeon-{name}
    - Purpose: {purpose}
    - Skills enabled: {list}
    - Status: pending_secrets (owner must add API keys)
    ```

11. **Send notification** via `./notify`:
    ```
    *New Aeon Instance Created*

    Repo: {OWNER}/aeon-{name}
    Purpose: {purpose}
    Skills: {comma-separated list of enabled skills}

    Status: PENDING SECRETS — instance is inert until you add API keys.

    Quick setup:
    1. Go to https://github.com/{OWNER}/aeon-{name}/settings/secrets/actions
    2. Add ANTHROPIC_API_KEY (required)
    3. Add TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID (recommended)

    See SETUP.md in the repo for full instructions.
    ```

Write complete, working code. No TODOs or placeholders.
