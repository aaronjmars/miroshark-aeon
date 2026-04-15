---
name: Repo Scanner
description: Catalog all GitHub repos for a user or org
var: ""
tags: [dev, meta]
---
> **${var}** — GitHub username or org to scan. Required — set in aeon.yml var field.

Today is ${today}. Your task is to catalog all GitHub repos into a structured reference file that other skills can use.

## Steps

1. **Resolve username.** If `${var}` is empty, check `memory/MEMORY.md` for a GitHub username. If none found, log 'repo-scanner: no username configured' and exit.

2. **Fetch all repos.**
   ```bash
   gh repo list ${var} --limit 100 --json name,description,pushedAt,primaryLanguage,isArchived,isFork,stargazerCount,url,defaultBranchRef \
     --jq '.[] | select(.isArchived == false)'
   ```

3. **For each active (non-archived) repo**, gather a quick profile:
   - Clone shallow: `gh repo clone owner/repo /tmp/repo-scan --depth 1`
   - Read README.md (first 50 lines) to understand what it does
   - Check what's in the root: `ls /tmp/repo-scan`
   - Identify the stack from config files:
     - `package.json` → Node/JS/TS (check framework: next, react, express, etc.)
     - `Cargo.toml` → Rust
     - `pyproject.toml` / `requirements.txt` → Python
     - `go.mod` → Go
     - `foundry.toml` / `hardhat.config.*` → Solidity/smart contracts
   - Count open issues: `gh issue list --repo owner/repo --state open --json number --jq length`
   - Count open PRs: `gh pr list --repo owner/repo --state open --json number --jq length`
   - Check last commit date from the clone: `git -C /tmp/repo-scan log -1 --format=%as`
   - Clean up: `rm -rf /tmp/repo-scan`

4. **Categorize each repo** into one of:
   - **active** — pushed to in last 30 days
   - **maintained** — pushed to in last 90 days
   - **stale** — no pushes in 90+ days
   - **fork** — is a fork (note: can still be active)

5. **Write the catalog** to `memory/topics/repos.md`:
   ```markdown
   # GitHub Repos — ${today}

   ## Active
   | Repo | What | Stack | Issues | Last Push |
   |------|------|-------|--------|-----------|
   | [name](url) | one-line description | lang/framework | N open | YYYY-MM-DD |

   ## Maintained
   | Repo | What | Stack | Issues | Last Push |
   ...

   ## Stale
   ...

   ## Forks
   ...

   ---

   ### Repo Details

   #### repo-name
   **What:** 2-3 sentence explanation based on README
   **Stack:** language, framework, key dependencies
   **Status:** active/maintained/stale
   **Issues:** N open, notable ones: [brief]
   **Opportunities:** What could be improved (TODOs, missing tests, features, etc.)
   ```

6. **Update memory index.** If `memory/MEMORY.md` doesn't already link to `topics/repos.md`, add a pointer under an appropriate section.

7. **Update watched-repos.** Write `memory/watched-repos.md` with all active + maintained repos:
   ```markdown
   - ${var}/repo-name
   - ${var}/other-repo
   ```

8. **Notify.** Send via `./notify`:
   ```
   repo-scanner: cataloged N repos (A active, M maintained, S stale, F forks)
   saved to memory/topics/repos.md
   ```

9. **Log.** Append to `memory/logs/${today}.md`.

## Guidelines

- Skip archived repos entirely.
- Keep descriptions tight — 1-2 sentences per repo max in the table.
- The "Opportunities" field is key — this is what external-feature reads to decide what to work on.
- Don't clone repos that are clearly empty or config-only (0 stars, no README, <3 files).
- If a repo has a CLAUDE.md, mention it — it means the repo is AI-ready.
