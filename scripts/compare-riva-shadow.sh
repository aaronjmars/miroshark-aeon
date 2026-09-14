#!/usr/bin/env bash
# Compare two private candidate artifacts without routing either to disclosure.
set -euo pipefail

usage() { echo "usage: $0 --legacy FILE --riva FILE --out FILE" >&2; exit 2; }
LEGACY=""; RIVA=""; OUT=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --legacy) LEGACY="${2:-}"; shift 2 ;;
    --riva) RIVA="${2:-}"; shift 2 ;;
    --out) OUT="${2:-}"; shift 2 ;;
    *) usage ;;
  esac
done
[ -f "$LEGACY" ] && [ -f "$RIVA" ] && [ -n "$OUT" ] || usage
command -v jq >/dev/null 2>&1 || { echo "RIVA_COMPARE_ERROR jq-missing" >&2; exit 3; }

normalise() {
  jq -c 'if type == "array" then . else (.candidates // []) end
    | map({file:(.file // ""),line:(.line // 0),category:(.category // ""),
           claim:(.claim // "")}) | unique_by([.file,.line,.category,.claim]) | sort_by([.file,.line,.category,.claim])' "$1"
}
legacy_json="$(normalise "$LEGACY")"
riva_json="$(normalise "$RIVA")"
mkdir -p "$(dirname "$OUT")"
jq -n --argjson legacy "$legacy_json" --argjson riva "$riva_json" \
  '{schema_version:1,legacy:$legacy,riva:$riva,
    only_legacy:[$legacy[] as $x | select(($riva | index($x)) == null)],
    only_riva:[$riva[] as $x | select(($legacy | index($x)) == null)],
    common:[$legacy[] as $x | select(($riva | index($x)) != null)],
    counts:{legacy:($legacy|length),riva:($riva|length),
      only_legacy:([$legacy[] as $x | select(($riva | index($x)) == null)]|length),
      only_riva:([$riva[] as $x | select(($legacy | index($x)) == null)]|length),
      common:([$legacy[] as $x | select(($riva | index($x)) != null)]|length)}}' > "$OUT"
echo "RIVA_COMPARE_OK out=$OUT"
