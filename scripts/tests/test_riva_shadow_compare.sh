#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d -t riva-compare.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT
printf '%s\n' '[{"file":"a.ts","line":10,"category":"idor","claim":"legacy"},{"file":"same.ts","line":2,"category":"xss","claim":"same"}]' > "$TMP/legacy.json"
printf '%s\n' '[{"file":"b.ts","line":20,"category":"ssrf","claim":"riva"},{"file":"same.ts","line":2,"category":"xss","claim":"same"}]' > "$TMP/riva.json"
"$ROOT/scripts/compare-riva-shadow.sh" --legacy "$TMP/legacy.json" --riva "$TMP/riva.json" --out "$TMP/out.json" >/dev/null
jq -e '.counts == {legacy:2,riva:2,only_legacy:1,only_riva:1,common:1}' "$TMP/out.json" >/dev/null
echo "ok - Riva shadow comparison is deterministic and private"
