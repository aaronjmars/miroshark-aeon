---
name: Deploy Prototype
description: Generate a small app or tool and deploy it live to Vercel via API
var: ""
tags: [dev, build]
---
> **${var}** — What to build and deploy. If empty, picks from recent signals (articles, skill outputs, ideas in memory).

If `${var}` is set, build that specific prototype instead of auto-selecting.

Today is ${today}. Your task is to build a small, self-contained prototype and prepare it for deployment to Vercel.

## Steps

1. **Read context.** Read `memory/MEMORY.md` and recent logs in `memory/logs/` for ideas.
   If running as part of a chain, check the chain context for upstream skill outputs to build from.

2. **Decide what to build.** Pick something small and shippable:
   - A single-page interactive tool or visualization
   - A tiny API endpoint that does something useful
   - A landing page or dashboard for a concept from recent research
   - A prototype of a startup idea or technical concept

   Keep scope tight — it must be deployable as static files or a single serverless function.

3. **Build it.** Write the files to `.pending-deploy/files/`:
   ```bash
   mkdir -p .pending-deploy/files
   ```
   Write all prototype source files into `.pending-deploy/files/`. This directory is the
   complete project root — everything here gets pushed to a new GitHub repo and deployed to Vercel.

   Write complete, working code. No placeholders. No TODO comments.

   For **static sites**: write HTML/CSS/JS files directly.
   For **API endpoints**: write files in `api/` directory (e.g. `api/index.js` exporting a handler).
   For **Next.js**: keep it minimal — `package.json`, `pages/index.js`, or `app/page.tsx`.

   Prefer static HTML + vanilla JS when possible — fewer build steps, faster deploys, less to break.

4. **Write deploy metadata.** Create `.pending-deploy/meta.json`:
   ```json
   {
     "name": "aeon-prototype-DESCRIPTIVE_SLUG",
     "description": "One-sentence description of what this does",
     "framework": null
   }
   ```
   - `name` becomes both the GitHub repo name and Vercel project name.
   - `framework`: set to `null` for static, or `"nextjs"`, `"svelte"`, etc. if using one.
   - Use descriptive slugs: `aeon-prototype-market-heatmap`, not `aeon-prototype-1`.

5. **Prepare Vercel deploy payload.** Build `.pending-deploy/payload.json` with all files inlined:
   ```json
   {
     "name": "aeon-prototype-DESCRIPTIVE_SLUG",
     "files": [
       { "file": "index.html", "data": "<!DOCTYPE html>...", "encoding": "utf-8" }
     ],
     "projectSettings": {
       "framework": null,
       "buildCommand": null,
       "outputDirectory": null
     },
     "target": "production"
   }
   ```

   For binary files use `"encoding": "base64"`.
   If using a framework, set `projectSettings.framework` and include `package.json`.

6. **Save the prototype record.** Write to `articles/prototype-${today}.md`:
   ```markdown
   # Prototype: [Name]

   **Built:** ${today}
   **What:** One-sentence description
   **Status:** Pending deploy

   ## Why
   What signal or idea triggered this.

   ## How
   Brief technical notes — stack, approach, interesting bits.

   ## Files
   - file list with brief descriptions

   ## Next
   What would make this a real product.
   ```

7. **Notify.** Send via `./notify`:
   ```
   built: [name] — [one-line description]. deploying to vercel...
   ```

8. **Log.** Append what you did to `memory/logs/${today}.md`.

## Environment Variables

- `VERCEL_TOKEN` — Required. Vercel API bearer token.
- `GH_GLOBAL` — Required. GitHub PAT with repo creation permission (used by post-run step).

## Guidelines

- Keep prototypes small. A single HTML file is ideal. Max ~5 files.
- Name deployments descriptively.
- Prefer zero-build static deploys over framework-heavy setups.
- Clean, minimal code. No npm install steps unless absolutely required.
- Do not hardcode any secrets into deployed files.
- Always include a README.md in `.pending-deploy/files/` with a brief description.
- The actual GitHub repo creation, push, and Vercel deploy happen in a post-run workflow step
  outside the sandbox. Your job is to write the files and metadata correctly.
