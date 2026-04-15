---
name: Skill Security Scan
description: Audit imported skills for shell injection, secret exfiltration, path traversal, and prompt injection before they run
var: ""
tags: [dev]
---
> **${var}** — Path to a SKILL.md file or skill directory to scan. If empty, scans all skills in `skills/`.

If `${var}` is set, scan only that path. Otherwise, scan all skill directories.

Today is ${today}. Your task is to audit skill files for security vulnerabilities before they can be executed.

## Threat Model

Imported skills are markdown files that instruct Claude Code to take actions. A malicious skill could:
- **Shell injection**: Execute arbitrary commands via unquoted variables, `eval`, backticks, or `$(...)` in bash blocks
- **Secret exfiltration**: Send environment variables, tokens, or file contents to external URLs via curl/wget/fetch
- **Path traversal**: Access files outside the repo using `../` or absolute paths
- **Prompt injection**: Override CLAUDE.md safety rules with embedded instructions ("ignore previous instructions", "you are now...")
- **Destructive commands**: Run `rm -rf`, `git push --force`, or other irreversible operations

## Steps

1. **Determine scan scope**:
   - If `${var}` is a file path, scan that file only.
   - If `${var}` is a skill name, scan `skills/${var}/SKILL.md`.
   - If empty, scan all `skills/*/SKILL.md` files.

2. **Run the scanner** on each skill file using `./skills/skill-security-scan/scan.sh`:
   ```bash
   ./skills/skill-security-scan/scan.sh <path-to-SKILL.md>
   ```
   The scanner checks for the threat categories above and outputs findings with severity levels (HIGH, MEDIUM, LOW).

3. **Check trusted sources**: Read `skills/security/trusted-sources.txt`. Skills from trusted sources get a reduced scan (format validation only, skip content analysis). The source is determined by checking git remote or the skill's frontmatter for an origin field.

4. **Generate report**: For each scanned skill, produce:
   ```
   [PASS/WARN/FAIL] skill-name
     HIGH: description (if any)
     MEDIUM: description (if any)
     LOW: description (if any)
   ```
   - FAIL = any HIGH severity finding
   - WARN = MEDIUM findings only
   - PASS = no findings or LOW only

5. **Save report** to `articles/security-scan-${today}.md` with full details.

## Sandbox note

This skill reads local files only — no network access needed. If `scripts/scan.sh` is not available, perform the audit inline using grep and file reads.

6. **Notify** via `./notify` if any skills FAIL:
   ```
   *Security Scan — ${today}*
   Scanned N skills: X passed, Y warnings, Z failed.
   Failed: skill1 (reason), skill2 (reason)
   ```
   If all pass, log "SECURITY_SCAN_OK" and skip notification.

7. **Log** results to `memory/logs/${today}.md`.
