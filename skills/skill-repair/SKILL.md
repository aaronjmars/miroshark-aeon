---
name: Skill Repair
description: Diagnose and fix failing or degraded skills automatically
var: ""
tags: [meta, dev]
depends_on: [skill-health]
---
> **${var}** — Skill name to repair. If empty, finds the worst-performing skill automatically.

If `${var}` is set, repair that specific skill instead of auto-selecting.

Today is ${today}. Your task is to diagnose and fix a failing or degraded skill.

## Steps

1. **Identify the target skill.** If `${var}` is empty:
   - Read `memory/issues/INDEX.md` for open issues — prioritize by severity (critical > high > medium > low).
   - Also read `memory/cron-state.json` and find skills with:
     - `consecutive_failures >= 2`, OR
     - `success_rate < 0.5` (with at least 3 total runs), OR
     - `last_error` set from a recent failure
   - Prefer skills that have an open issue (already diagnosed) over raw cron-state signals.
   - Skip issues with category `permanent-limitation` — these can't be fixed by prompt changes.
   - Sort by severity: critical issues first, then consecutive failures, then lowest success rate.
   - Pick the worst fixable one. If everything is healthy, log "all skills healthy" and exit.

2. **Gather diagnostic context:**
   - Read the skill file: `skills/{name}/SKILL.md`
   - Read `memory/cron-state.json` entry for the skill (last_error, success_rate, run counts)
   - Read last 3 days of `memory/logs/` and search for the skill name — look for error patterns
   - Check recent GitHub Actions runs for the skill:
     ```bash
     gh run list --workflow=aeon.yml --limit 5 --json status,conclusion,name,createdAt \
       | jq '[.[] | select(.name | contains("SKILL_NAME"))]'
     ```
   - If the run failed, check its logs:
     ```bash
     RUN_ID=$(gh run list --workflow=aeon.yml --limit 5 --json databaseId,name \
       | jq -r '[.[] | select(.name | contains("SKILL_NAME"))][0].databaseId')
     gh run view "$RUN_ID" --log 2>&1 | grep -iE "error|fail|missing|denied|timeout" | tail -20
     ```

3. **Diagnose the root cause.** Common failure modes:
   - **Missing secret** — skill references an env var that isn't set
   - **API change** — external API changed format, URL, or auth
   - **Bad prompt** — skill instructions are ambiguous or reference stale data
   - **Rate limiting** — skill hits an API too frequently
   - **Timeout** — skill takes too long (>30 min)
   - **Output format** — skill produces output that fails quality scoring

4. **Fix it.** Based on diagnosis:
   - Edit `skills/{name}/SKILL.md` to fix the prompt, update API usage, clarify instructions
   - If a secret is missing, note it in the notification (you can't set secrets)
   - If an API changed, update the skill to use the new format
   - If the skill is fundamentally broken beyond a prompt fix, disable it in `aeon.yml` and note why

5. **Create a branch and PR:**
   ```bash
   git checkout -b fix/skill-repair-{name}-${today}
   git add skills/{name}/SKILL.md aeon.yml  # if changed
   git commit -m "fix({name}): [description of fix]"
   ```
   Open a PR with diagnosis and fix details:
   ```bash
   gh pr create --title "fix({name}): [short description]" \
     --body "## Diagnosis\n[what was wrong]\n\n## Fix\n[what was changed]\n\n## Evidence\n- success_rate: X\n- consecutive_failures: Y\n- last_error: Z"
   ```

6. **Notify.** Send via `./notify`:
   ```
   skill-repair: fixed {name} — [one-line description of fix]
   diagnosis: [root cause]
   PR: [url]
   ```

7. **Update issue tracker** (`memory/issues/`):
   - Read `memory/issues/INDEX.md` — find if there's an open issue for this skill.
   - If an issue exists:
     - If the fix was applied: update the issue file — set `status: resolved`, `resolved_at: ${today}`, `fix_pr: [PR url]`. Move the row from Open to Resolved in INDEX.md.
     - If you couldn't fix it: add a `## Repair Attempt` section to the issue file with the date, diagnosis, and why the fix failed.
   - If no issue exists but you found and fixed a real problem: create a new issue file with status already set to `resolved`.

8. **Log.** Append to `memory/logs/${today}.md`:
   ```
   ## Skill Repair
   - **Target:** {name}
   - **Diagnosis:** [root cause]
   - **Fix:** [what was changed]
   - **PR:** [url or "disabled"]
   - **Issue:** [ISS-NNN resolved/updated/created]
   ```

## Guidelines

- Only fix one skill per run. Pick the worst offender.
- Don't rewrite skills from scratch — make minimal, targeted fixes.
- If you can't determine the root cause, log the diagnostic info and notify. Don't guess.
- If a skill has been failing for 7+ days with no clear fix, disable it and recommend manual review.
- Never modify secrets or workflow files — only skill files and aeon.yml.
