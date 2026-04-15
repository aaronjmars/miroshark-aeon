---
name: Vuln Scanner
description: Fork trending repos, audit for security vulnerabilities, and PR fixes
var: ""
tags: [dev, security]
depends_on: [github-trending]
---
> **${var}** — Target repo in `owner/repo` format. If empty, picks from recent github-trending output or trending repos.

If `${var}` is set, audit that specific repo. Otherwise auto-select.

Today is ${today}. Your task is to find a trending GitHub repo, audit it for security vulnerabilities, and submit a fix PR if you find something real.

## Steps

1. **Pick a target repo.**

   If `${var}` is set, use that repo directly.

   If empty:
   - Read `output/skills/github-trending.md` if it exists (chain context from github-trending skill)
   - Otherwise fetch trending repos using `gh api` (handles auth automatically, works in sandbox):
     ```bash
     gh api "search/repositories?q=created:>$(date -u -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)&sort=stars&order=desc&per_page=20" \
       --jq '.items[] | {full_name, language, stargazers_count, description}'
     ```
   - Pick a repo that:
     - Is written in a language you can audit well (JS/TS, Python, Go, Rust, Solidity)
     - Has 50+ stars (real project, not a toy)
     - Is not a fork itself
     - Handles user input, auth, crypto, or network calls (higher vuln surface)
   - Read `memory/logs/` from last 14 days — skip repos already scanned

2. **Fork and clone.**
   ```bash
   REPO="owner/repo"
   # Fork it under your account
   gh repo fork "$REPO" --clone --default-branch-only -- --depth 100
   cd "$(basename "$REPO")"
   ```

3. **Audit the codebase.** Look for real, exploitable vulnerabilities — not style issues. Scan for:

   **Injection vulnerabilities:**
   - SQL injection: raw string interpolation in queries, no parameterized queries
   - Command injection: user input passed to `exec`, `spawn`, `os.system`, `subprocess`
   - XSS: unescaped user input rendered in HTML, `dangerouslySetInnerHTML` with user data
   - Template injection: user input in template strings evaluated server-side
   - Path traversal: user input in file paths without sanitization (`../../../etc/passwd`)

   **Auth & crypto issues:**
   - Hardcoded secrets, API keys, private keys in source code
   - Weak crypto: MD5/SHA1 for passwords, ECB mode, predictable IVs
   - Missing auth checks on sensitive endpoints
   - JWT issues: `none` algorithm accepted, secret in source, no expiry validation
   - CORS misconfiguration: wildcard origins with credentials

   **Dependency issues:**
   ```bash
   # Check for known CVEs in dependencies
   # Node.js
   [ -f package-lock.json ] && npm audit --json 2>/dev/null | jq '.vulnerabilities | to_entries[] | select(.value.severity == "critical" or .value.severity == "high")' || true
   # Python
   [ -f requirements.txt ] && pip-audit -r requirements.txt --format json 2>/dev/null || true
   ```

   **Smart contract vulnerabilities** (if Solidity):
   - Reentrancy patterns (external calls before state changes)
   - Unchecked return values on `transfer`/`send`
   - Integer overflow (pre-0.8.0 without SafeMath)
   - Access control: missing `onlyOwner` or role checks
   - Front-running susceptibility

   **Other:**
   - SSRF: user-controlled URLs in server-side fetch/requests
   - Insecure deserialization: `pickle.loads`, `yaml.load` without SafeLoader
   - Race conditions in financial/state-changing operations
   - Missing rate limiting on auth endpoints
   - Debug/dev mode enabled in production configs

   Use grep to scan efficiently:
   ```bash
   # Examples
   grep -rn "exec\|spawn\|system\|popen" --include="*.js" --include="*.ts" --include="*.py" . | grep -v node_modules | grep -v test
   grep -rn "innerHTML\|dangerouslySetInnerHTML\|v-html" --include="*.js" --include="*.ts" --include="*.vue" --include="*.jsx" --include="*.tsx" . | grep -v node_modules
   grep -rn "password\|secret\|api_key\|private_key" --include="*.env*" --include="*.json" --include="*.yml" --include="*.yaml" . | grep -v node_modules | grep -v "\.example"
   ```

4. **Assess findings.** For each potential vulnerability:
   - Is it actually exploitable? (not just a pattern match — read the surrounding code)
   - What's the severity? (critical / high / medium)
   - Can you fix it without breaking functionality?
   - Only proceed with confirmed, real vulnerabilities — not false positives

   If no real vulnerabilities found, log "clean audit" and exit. Don't force findings.

5. **Fix the vulnerability.** For each confirmed finding:
   - Write the minimal fix that resolves the issue
   - Don't refactor surrounding code
   - Add a comment only if the fix isn't self-evident
   - If it's a dependency issue, update the lockfile if possible

6. **Create a branch and commit.**
   ```bash
   git checkout -b security/fix-VULN-TYPE
   git add -A
   git commit -m "fix(security): [description of vulnerability and fix]

   Vulnerability: [type — e.g. SQL injection, XSS, hardcoded secret]
   Severity: [critical/high/medium]
   Location: [file:line]
   Impact: [what an attacker could do]"
   ```

7. **Push and open a PR to the original repo.**
   ```bash
   git push -u origin security/fix-VULN-TYPE
   gh pr create --repo "$REPO" \
     --title "fix(security): [short description]" \
     --body "## Security Vulnerability Report

   **Type:** [vulnerability type]
   **Severity:** [critical/high/medium]
   **Location:** \`file:line\`

   ### Description
   [Clear explanation of the vulnerability and how it could be exploited]

   ### Fix
   [What this PR changes and why it resolves the issue]

   ### Impact
   [What an attacker could do without this fix]

   ---
   Found by [Aeon](https://github.com/aeonframework/aeon) — automated security scanner"
   ```

8. **Write a report.** Save to `output/articles/vuln-scan-${today}.md`:
   ```markdown
   # Vulnerability Scan — ${today}

   **Repo:** owner/repo (stars, language)
   **Findings:** N vulnerabilities

   ## Finding 1: [Type]
   - **Severity:** critical/high/medium
   - **File:** path:line
   - **Description:** what's wrong
   - **Fix:** what was changed
   - **PR:** url
   ```

9. **Notify.** Send via `./notify`:
   ```
   vuln-scanner: [repo] — found [N] vulnerabilities ([severity])
   PR: [url]
   ```

10. **Log.** Append to `memory/logs/${today}.md`.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables

- `GH_TOKEN` / `GITHUB_TOKEN` — Required. Needs fork + PR permissions.

## Guidelines

- Only report REAL vulnerabilities. False positives damage credibility.
- Read the code context around each finding — a grep match isn't proof.
- Be respectful in PR descriptions. You're helping, not shaming.
- One PR per repo per run. Bundle related fixes into a single PR.
- Skip repos that are clearly abandoned (no commits in 1+ year).
- Skip repos that are security research / intentionally vulnerable (e.g. DVWA, juice-shop).
- If you're not confident a finding is real, don't file a PR. Log it and move on.
- Never disclose vulnerabilities publicly — PRs are the responsible disclosure path.
- Don't scan the same repo twice in 30 days (check logs).
