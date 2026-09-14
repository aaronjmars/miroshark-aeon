#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$(mktemp -t riva-context.XXXXXX.json)"
trap 'rm -f "$OUT"' EXIT

"$ROOT/scripts/build-vuln-context.sh" --repo "$ROOT" --out "$OUT" >/dev/null
jq -e '
  .schema_version == 1 and
  (.repo | type == "string" and length > 0) and
  (.commit | test("^[0-9a-f]{40}$")) and
  (.code_files | type == "number") and
  (.languages | type == "array") and
  (.security_docs | type == "array") and
  (.likely_entrypoint_files | type == "array") and
  (.research_fields.assets | type == "array") and
  (.research_fields.invariants | type == "array")
' "$OUT" >/dev/null
echo "ok - Riva dossier schema is valid"

