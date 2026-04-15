---
name: skill-update-check
description: Check imported skills for upstream changes and security regressions since the version in skills.lock
var: ""
tags: [dev, security]
cron: "0 19 * * 0"
---
> **${var}** — Skill name to check. If empty, checks all skills tracked in `skills.lock`.

Today is ${today}. Your task is to audit imported skills for upstream changes since they were installed, detect security regressions in changed content, and report what has drifted.

## Steps

1. **Read `skills.lock`** at the repo root. If the file does not exist or is empty, log "SKILL_UPDATE_CHECK_SKIP: skills.lock not found — no imported skills tracked" to `memory/logs/${today}.md` and stop. Do NOT send a notification.

   Each entry in `skills.lock` has the shape:
   ```json
   {
     "skill_name": "bankr",
     "source_repo": "BankrBot/skills",
     "source_path": "skills/bankr/SKILL.md",
     "branch": "main",
     "commit_sha": "abc1234...",
     "imported_at": "2026-04-01T12:00:00Z"
   }
   ```

2. **Filter entries** — if `${var}` is set, only process the entry whose `skill_name` matches `${var}`.

3. **For each tracked skill**, fetch the latest commit SHA for that file path:
   ```bash
   gh api repos/{source_repo}/commits \
     -f path={source_path} \
     --jq '.[0] | {sha: .sha, message: .commit.message, date: .commit.author.date, author: .commit.author.name}'
   ```
   If the API call fails (repo deleted, private, rate limited), mark the skill as `UNREACHABLE` and continue.

4. **Compare SHAs** — if the latest SHA matches the locked SHA, the skill is up-to-date. If they differ, the skill has changed upstream.

5. **For each changed skill**, fetch the diff between the locked SHA and the current HEAD:
   ```bash
   gh api repos/{source_repo}/compare/{locked_sha}...{current_sha} \
     --jq '{ahead_by: .ahead_by, files: [.files[] | {filename, status, patch}]}'
   ```
   Extract the diff for the SKILL.md file specifically.

6. **Security check each changed skill** — pass the diff to the skill security scanner by reading the updated SKILL.md content:
   ```bash
   gh api repos/{source_repo}/contents/{source_path} \
     -f ref={current_sha} --jq '.content' | base64 -d > /tmp/updated-skill.md
   ./skills/skill-security-scan/scan.sh /tmp/updated-skill.md
   ```
   If the scanner is not present, skip the security check and note it in the report.

7. **Build the results table** with one row per tracked skill:

   | Skill | Source | Status | Last Changed | SHA (locked → current) | Security |
   |-------|--------|--------|--------------|------------------------|----------|
   | bankr | BankrBot/skills | CHANGED | 2026-04-10 | abc1234 → def5678 | PASS |
   | hydrex | BankrBot/skills | UP-TO-DATE | — | abc1234 | — |
   | custom | unknown/repo | UNREACHABLE | — | abc1234 | — |

   Status values:
   - `UP-TO-DATE` — SHA matches, no action needed
   - `CHANGED` — upstream has new commits for this file
   - `UNREACHABLE` — could not contact source repo

8. **Write the report** to `articles/skill-update-check-${today}.md`:
   ```markdown
   # Skill Update Check — ${today}

   Checked N imported skills against their upstream sources.

   ## Summary
   - Up-to-date: N
   - Changed: N
   - Unreachable: N

   ## Results

   [results table from step 7]

   ## Changed Skills — Diffs

   ### skill-name
   **Source:** owner/repo at path/to/SKILL.md
   **Locked SHA:** abc1234 (imported YYYY-MM-DD)
   **Current SHA:** def5678 (committed YYYY-MM-DD by Author — "commit message")
   **Security verdict:** PASS / WARN (details) / FAIL (details)

   **Diff summary:**
   [describe what changed in plain language based on the patch — what instructions were added, removed, or modified]

   **Recommendation:** Safe to update — run `./add-skill <source_repo> <skill-name>` to accept / Review before updating / Do NOT update (security risk)
   ```

9. **Update `last_checked` only — do NOT advance the locked SHA.** For every entry (including UP-TO-DATE ones), set a `last_checked` timestamp so the next run knows when each was last verified:
   ```bash
   jq --arg at "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
     '[.[] | .last_checked = $at]' \
     skills.lock > skills.lock.tmp && mv skills.lock.tmp skills.lock
   ```
   **Never auto-advance `commit_sha` in `skills.lock`**, even when the security verdict is PASS. Advancing the lock is a supply-chain trust decision that requires explicit human approval. The notification in step 10 will tell the operator how to advance manually.

10. **Send notification** only if at least one skill has CHANGED status. Format:
    ```
    *Skill Update Check — ${today}*

    Checked N imported skills. X changed upstream, Y up-to-date, Z unreachable.

    Changed skills:
    - skill-name (owner/repo): [1-sentence summary of what changed] — Security: PASS/WARN/FAIL
    - skill-name2 ...

    [If any FAIL]: ⚠ Security regression detected in [skill-name] — do NOT run until reviewed.
    [If any WARN]: Review recommended for [skill-name] before next execution.
    [If any PASS]: To accept the update and advance the lock, re-run:
      ./add-skill <source_repo> <skill-name>

    Full report: articles/skill-update-check-${today}.md
    ```
    If all skills are up-to-date or unreachable, do NOT send a notification — log "SKILL_UPDATE_CHECK_OK: N skills current" to `memory/logs/${today}.md` only.

11. **Log to `memory/logs/${today}.md`**:
    ```
    ## skill-update-check
    - Checked N skills from skills.lock
    - Up-to-date: N, Changed: N, Unreachable: N
    - [Changed: skill-name — old_sha → new_sha — security: PASS]
    - Report: articles/skill-update-check-${today}.md
    ```

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

Write the complete report. No TODOs or placeholders.
