---
name: Vercel Projects
description: Catalog all Vercel projects with deployment status, domains, and framework info
var: ""
tags: [dev, meta]
---
> **${var}** — Vercel team slug or ID. If empty, lists projects for the token owner's personal account.

Today is ${today}. Your task is to catalog all Vercel projects into a structured reference file.

## Steps

1. **Fetch all projects.**

   **Primary — WebFetch** (works reliably in sandbox):
   Use WebFetch to fetch `https://api.vercel.com/v9/projects?limit=100` with header `Authorization: Bearer $VERCEL_TOKEN`.

   If WebFetch doesn't support auth headers, try curl:
   ```bash
   curl -s "https://api.vercel.com/v9/projects?limit=100" \
     -H "Authorization: Bearer $VERCEL_TOKEN" | jq '.'
   ```
   If `${var}` is set (team slug), add `&teamId=${var}` to the URL.

   **If both fail** (sandbox blocks auth curl and WebFetch can't add headers): check if `.xai-cache/vercel-projects.json` exists (pre-fetched by workflow) and read from there.

2. **For each project**, extract:
   - Name and ID
   - Framework (Next.js, static, etc.)
   - Git repo link (if connected)
   - Production domain(s)
   - Latest deployment status and date
   - Environment: production / preview URLs

   For latest deployment info, use WebFetch or curl:
   ```bash
   curl -s "https://api.vercel.com/v6/deployments?projectId=PROJECT_ID&limit=1&target=production" \
     -H "Authorization: Bearer $VERCEL_TOKEN" | jq '.deployments[0] | {url, readyState, createdAt}'
   ```

3. **Categorize each project:**
   - **live** — has a successful production deployment in last 30 days
   - **idle** — last deploy 30-90 days ago
   - **stale** — no deploys in 90+ days
   - **errored** — latest deployment is in ERROR state

4. **Write the catalog** to `memory/topics/vercel.md`:
   ```markdown
   # Vercel Projects — ${today}

   ## Live
   | Project | Framework | Domain | Last Deploy | Repo |
   |---------|-----------|--------|-------------|------|
   | name | nextjs | example.vercel.app | YYYY-MM-DD | owner/repo |

   ## Idle
   ...

   ## Stale
   ...

   ## Errored
   ...

   ---

   ### Project Details

   #### project-name
   **URL:** https://domain.vercel.app
   **Framework:** Next.js / static / etc.
   **Repo:** linked repo or "not connected"
   **Last Deploy:** date, status
   **Domains:** list of custom domains if any
   ```

5. **Cross-reference with repos.** If `memory/topics/repos.md` exists, note which GitHub repos
   have Vercel projects and which don't (potential candidates for deploy-prototype).

6. **Update memory index.** Add a pointer in `memory/MEMORY.md` if not already there.

7. **Notify.** Send via `./notify`:
   ```
   vercel-projects: cataloged N projects (L live, I idle, S stale, E errored)
   saved to memory/topics/vercel.md
   ```

8. **Log.** Append to `memory/logs/${today}.md`.

## Environment Variables

- `VERCEL_TOKEN` — Required. Vercel API bearer token.

## Sandbox note

The sandbox may block curl with auth headers (env var expansion fails). Fallback chain:
1. WebFetch with auth header (may work)
2. curl with `$VERCEL_TOKEN` header (may be blocked)
3. `.xai-cache/vercel-projects.json` (pre-fetched by workflow if available)

## Guidelines

- Use the Vercel REST API — prefer WebFetch, fall back to curl.
- Handle pagination: if the response has a `pagination.next` field, fetch the next page.
- Keep descriptions tight. The catalog should be scannable at a glance.
- Note any projects with custom domains — these are likely production apps.
- If a project has no deployments at all, categorize as "empty" and skip the detail section.
