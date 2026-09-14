#!/usr/bin/env bash
# Source from the Aeon runner after SKILL_NAME and SKILL_VAR are exported.
# Resolves the capability tier before MCP or skill-secret setup. This file is
# sourced, so it must not change the caller's shell options.

SHADOW_MODE=0
case "${SKILL_NAME:-}:${SKILL_VAR:-}" in
vuln-scanner:shadow|vuln-scanner:shadow:*|vuln-scanner:compare|vuln-scanner:compare:*)
  SHADOW_MODE=1
  SKILL_MODE=read-only
  # Fail closed at the capability boundary, before MCP and declared-secret
  # setup. The workflow repeats this unset as defense in depth.
  unset ALL_SECRETS GH_GLOBAL GH_TOKEN GITHUB_TOKEN RESEND_API_KEY RESEND_FROM RESEND_REPLY_TO XAI_API_KEY
  echo "Riva shadow mode: forcing read-only capability tier"
  ;;
*)
  SKILL_MODE=$(bash scripts/skill_mode.sh mode "${SKILL_NAME:-}")
  ;;
esac
ALLOWED=$(bash scripts/skill_mode.sh allowed-tools "$SKILL_MODE")
export SHADOW_MODE SKILL_MODE ALLOWED
echo "SKILL_MODE=$SKILL_MODE" >> "${GITHUB_ENV:-/dev/null}"
echo "Capability mode: $SKILL_MODE"
