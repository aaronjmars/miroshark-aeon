#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WF="$ROOT/.github/workflows/aeon.yml"
SKILL="$ROOT/skills/vuln-scanner/SKILL.md"
CAPS="$ROOT/scripts/resolve-riva-capabilities.sh"

run_resolver() {
  local selector="$1" envfile
  envfile="$(mktemp -t riva-shadow-env.XXXXXX)"
  (
    cd "$ROOT"
    set +u
    SKILL_NAME=vuln-scanner
    SKILL_VAR="$selector"
    GITHUB_ENV="$envfile"
    ALL_SECRETS=secret GH_GLOBAL=secret GH_TOKEN=secret GITHUB_TOKEN=secret
    RESEND_API_KEY=secret RESEND_FROM=secret RESEND_REPLY_TO=secret XAI_API_KEY=secret
    source "$CAPS"
    [ "$SHADOW_MODE" = 1 ]
    [ "$SKILL_MODE" = read-only ]
    [[ "$-" != *u* ]]
    for key in ALL_SECRETS GH_GLOBAL GH_TOKEN GITHUB_TOKEN RESEND_API_KEY RESEND_FROM RESEND_REPLY_TO XAI_API_KEY; do
      ! declare -p "$key" >/dev/null 2>&1 || exit 22
    done
    ! grep -q '^RIVA_SHADOW_MODE=' "$envfile"
    grep -q '^SKILL_MODE=read-only$' "$envfile"
  ) || { rm -f "$envfile"; return 1; }
  rm -f "$envfile"
}

for selector in shadow compare shadow:owner/repo compare:owner/repo; do
  run_resolver "$selector"
done

# A normal scan must retain its configured capability tier and credentials.
(
  cd "$ROOT"
  SKILL_NAME=vuln-scanner
  SKILL_VAR=owner/repo
  GH_TOKEN=kept
  GITHUB_ENV=/dev/null
  source "$CAPS"
  [ "$SHADOW_MODE" = 0 ]
  [ -n "${GH_TOKEN:-}" ]
)

grep -q 'resolve-riva-capabilities.sh' "$WF"
grep -q 'SHADOW_MODE.*!=.*1' "$WF"
grep -q 'If `KERNEL=shadow`' "$SKILL"
grep -q 'do not execute A5' "$SKILL"
echo "ok - Riva shadow mode is workflow-isolated and comparison-only"
