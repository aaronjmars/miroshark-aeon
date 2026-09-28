#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
FILTER="$ROOT/scripts/hunter-22-filter.mjs"
NOW=2026-09-22T12:00:00Z
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

cat > "$TMP/matches.json" <<'JSON'
{
  "count": 4,
  "demo": false,
  "matches": [
    {"id":"expired","title":"Expired","rewardUsd":20,"expiresAt":"2026-06-14T23:17:58.513+00:00"},
    {"id":"boundary","title":"Boundary","rewardUsd":30,"expiresAt":"2026-09-22T12:00:00Z"},
    {"id":"future","title":"Future","rewardUsd":40,"expiresAt":"2026-09-23T12:00:00Z"},
    {"id":"no-deadline","title":"No deadline","rewardUsd":50,"expiresAt":null,"poolLeftPct":14}
  ]
}
JSON

node "$FILTER" --now "$NOW" < "$TMP/matches.json" > "$TMP/filtered.json"
jq -e '
  .count == 2 and
  ([.matches[].id] == ["future", "no-deadline"]) and
  .gate.inputCount == 4 and
  .gate.keptCount == 2 and
  .gate.rejectedCount == 2 and
  ([.gate.rejected[] | [.id, .reason]] == [["expired", "expired"], ["boundary", "expired"]]) and
  ([.gate.seen[].id] == ["expired", "boundary", "future", "no-deadline"])
' "$TMP/filtered.json" >/dev/null
echo 'ok - expired and boundary deadlines are removed before triage'

printf '%s\n' '{"matches":[{"id":"bad-date","expiresAt":"not-a-date"}]}' \
  | node "$FILTER" --now "$NOW" > "$TMP/invalid-date.json"
jq -e '.matches == [] and .gate.rejected == [{"id":"bad-date","reason":"invalid-expiration"}]' \
  "$TMP/invalid-date.json" >/dev/null
echo 'ok - malformed deadlines fail closed'

if printf '%s\n' '{"count":1}' | node "$FILTER" --now "$NOW" > "$TMP/malformed.out" 2> "$TMP/malformed.err"; then
  echo 'FAIL - a response without matches passed the gate' >&2
  exit 1
fi
grep -q '^HUNTER22_GATE_ERROR:' "$TMP/malformed.err"
echo 'ok - malformed API responses fail closed'

echo 'ALL PASS'
