#!/usr/bin/env bash
# Validate Riva's candidate handoff without promoting or disclosing anything.
set -euo pipefail
FILE="${1:-}"
[ -f "$FILE" ] || { echo "usage: $0 FILE" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || exit 3
jq -e '
  (if type == "array" then . else (.candidates // error("missing candidates")) end)
  | all(.[];
      (.file | type == "string" and length > 0) and
      (.line | type == "number" and . >= 1) and
      (.severity | type == "string" and (ascii_downcase == "low" or ascii_downcase == "medium" or ascii_downcase == "high" or ascii_downcase == "critical")) and
      (.category | type == "string" and length > 0) and
      (.claim | type == "string" and length >= 20))
' "$FILE" >/dev/null
echo "RIVA_CANDIDATES_OK file=$FILE"
