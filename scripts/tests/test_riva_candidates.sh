#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d -t riva-candidates.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT
printf '%s\n' '[{"file":"src/auth.ts","line":12,"severity":"high","category":"authz","claim":"attacker-controlled account id crosses owner boundary"}]' > "$TMP/good.json"
printf '%s\n' '[{"file":"src/auth.ts","line":0,"severity":"high","category":"authz","claim":"too short"}]' > "$TMP/bad.json"
"$ROOT/scripts/validate-riva-candidates.sh" "$TMP/good.json" >/dev/null
if "$ROOT/scripts/validate-riva-candidates.sh" "$TMP/bad.json" >/dev/null 2>&1; then
  echo "invalid Riva candidate accepted" >&2
  exit 1
fi
echo "ok - Riva candidate handoff validation is fail-closed"
