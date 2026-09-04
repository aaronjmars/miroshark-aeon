#!/usr/bin/env bash
# Regression test for chain-runner's "Update cron state" step: a chain rejected
# before any skill ran (CHAIN_STATUS=invalid-dispatch, set by the dev-loop target
# guard) must skip cron-state bookkeeping entirely, while a real failure/success
# must still fall through to it unchanged.
set -uo pipefail

WORKFLOW="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/.github/workflows/chain-runner.yml"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Extract the guard verbatim from the "Update cron state" step: from the env-bound
# chain-name re-derivation up to (excluding) the real cron-state.json write. Real
# git/state-file work is intentionally out of scope here — see test_chain_runner.sh
# for the sibling dispatch_skill() extraction using the same anchored-sed pattern.
awk '
  /^          # env-bound \+ allowlisted, same as the Run chain step\./ { on=1 }
  on && /^          STATE_FILE="memory\/cron-state\.json"$/ { exit }
  on { print }
' "$WORKFLOW" | sed 's/^          //' > "$TMP/guard.sh"
# Sanity: the extraction must have found both the chain-name guard and the
# invalid-dispatch guard — a rename/reflow of the source step would otherwise
# silently extract nothing (or half) and the test would pass on a stub script.
grep -q "Invalid chain name" "$TMP/guard.sh" && grep -q 'CHAIN_STATUS' "$TMP/guard.sh" \
  || { echo "FAIL: extraction anchor drifted — expected content missing from extracted guard" >&2; cat "$TMP/guard.sh" >&2; exit 1; }
printf 'echo REACHED_STATE_WRITE\n' >> "$TMP/guard.sh"

run_guard() {
  ( _INPUT_CHAIN="dev-loop" CHAIN_STATUS="${1:-}" bash "$TMP/guard.sh" )
}

fail=0
pass() { echo "ok   - $1"; }
bad() { echo "FAIL - $1"; fail=1; }

# CHAIN_STATUS=invalid-dispatch → skip the write, exit 0, no sentinel reached.
out=$(run_guard invalid-dispatch); rc=$?
[ "$rc" -eq 0 ] && pass "invalid-dispatch exits 0" || bad "invalid-dispatch should exit 0 (got $rc)"
echo "$out" | grep -q "REACHED_STATE_WRITE" && bad "invalid-dispatch must not reach the state write" || pass "invalid-dispatch skips the cron-state write"
echo "$out" | grep -q "rejected before any skill ran" && pass "invalid-dispatch logs why it's skipping" || bad "missing explanatory log line"

# CHAIN_STATUS unset (the CHAIN_STATUS:-failed default, a genuine failure) → falls
# through to the write path unchanged.
out=$(run_guard ""); rc=$?
[ "$rc" -eq 0 ] && echo "$out" | grep -q "REACHED_STATE_WRITE" \
  && pass "a real failure (CHAIN_STATUS unset) still reaches the state write" \
  || bad "a real failure must still reach the state write (rc=$rc)"

# CHAIN_STATUS=success (the normal happy path) → also falls through unchanged.
out=$(run_guard success); rc=$?
[ "$rc" -eq 0 ] && echo "$out" | grep -q "REACHED_STATE_WRITE" \
  && pass "a real success still reaches the state write" \
  || bad "a real success must still reach the state write (rc=$rc)"

echo "---"
[ "$fail" -eq 0 ] && echo "ALL PASS" || echo "SOME FAILED"
exit "$fail"
