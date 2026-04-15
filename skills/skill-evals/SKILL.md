---
name: Skill Evals
description: Evaluate skill output quality against assertion manifests — detects regressions before users notice
var: ""
tags: [meta]
---

> **${var}** — Skill name to evaluate. If empty, evaluates all skills in evals.json.

Today is ${today}. Your task is to evaluate skill output quality by validating recent outputs against assertions defined in `skills/skill-evals/evals.json`.

## Steps

1. **Read the assertion manifest** — read `skills/skill-evals/evals.json`.

2. **Read `aeon.yml`** to get the full registered skill list.

3. **Read `memory/cron-state.json`** — contains `total_runs`, `success_rate`, `last_quality_score` per skill.

4. **Determine which skills to evaluate**:
   - If `${var}` is set, evaluate only that skill.
   - Otherwise evaluate all skills listed in evals.json.

5. **For each skill being evaluated**, run the following checks:

   a. **Find the most recent output file** using the glob pattern from evals.json (`output_pattern`).
      - Use Glob to find all matching files.
      - Sort by filename descending to get the most recent.
      - If no matching file exists → mark as **NO COVERAGE**.

   b. **Word count check**: count words in the file. Fail if below `min_words`.

   c. **Required pattern check**: for each pattern in `required_patterns`, search the file content.
      - Patterns are pipe-separated alternatives (e.g. `"stars|forks"` — either must appear).
      - Fail if any required pattern is not found.

   d. **Forbidden pattern check**: for each pattern in `forbidden_patterns`, search the file.
      - Fail if any forbidden pattern IS found.

   e. **Numeric checks** (if `numeric_checks` is defined): for each entry:
      - Extract the first number matching the regex `pattern` from the file.
      - Fail if the extracted value is outside [`min`, `max`].
      - If no match found and the field is expected (skip if not found is not specified), flag as WARN.

   f. **Quality score cross-check**: read `memory/skill-health/{skill}.json` if it exists.
      - If `avg_score` < 2.5 → flag as **QUALITY_DEGRADED** even if assertions pass.
      - If `avg_score` >= 2.5 → note the score in the report.

6. **Classify each skill**:
   - **PASS** — all assertions pass, quality score >= 2.5 (or no health data yet)
   - **FAIL** — one or more assertions failed (word count, required pattern, forbidden pattern, or numeric check)
   - **QUALITY_DEGRADED** — assertions pass but avg quality score < 2.5
   - **NO COVERAGE** — no output file found matching the pattern

7. **Detect coverage gaps** — skills that have cron-state entries with `total_runs > 0` but are NOT in evals.json.
   These are skills running in production without any eval spec.

8. **Write the report** to `articles/skill-evals-${today}.md`:

   ```markdown
   # Skill Evals — ${today}

   ## Results

   | Skill | Status | Details |
   |-------|--------|---------|
   | heartbeat | PASS | 52 words, all patterns matched |
   | repo-pulse | FAIL | Missing pattern: "stars" |
   | token-report | NO COVERAGE | No output file found |

   ## Summary
   - Evaluated: N skills (from evals.json)
   - Passing: N
   - Failing: N
   - Quality degraded: N
   - No coverage: N

   ## Coverage Gaps (running in production but not in evals.json)
   - skill-name: N runs (success_rate: X%)

   ## Recommendations
   [List specific fixes for failing skills and skills to add to evals.json]
   ```

9. **Send notification** via `./notify` if any skills are FAILING or QUALITY_DEGRADED. Include the full results table in the message.
   If all skills pass or have no coverage issues, send a brief summary: "Skill Evals PASS — N/N skills healthy."

10. **Log to `memory/logs/${today}.md`**:
    ```
    ## Skill Evals — ${today}
    - Evaluated N skills from evals.json
    - PASS: X, FAIL: Y, NO_COVERAGE: Z
    - Coverage gaps: [list skill names]
    ```

Write complete output with no placeholders.
