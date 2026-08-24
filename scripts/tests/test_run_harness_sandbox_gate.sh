#!/usr/bin/env bash
# Tests for run-harness's read-only OS-sandbox gate — the case statement at
# ~line 141 that decides which harnesses get the wrapper sandbox applied.
#
# This exact gate is what silently missed `fx` when it was added as a 7th
# harness (aeonfun/aeon#941 review): the adapter, resolve-harness.sh, and
# install-harness.sh were all wired correctly, but run-harness's own sandbox
# case statement still only listed the original six — so a read-only fx skill
# would have run completely unsandboxed, with not even the advisory warning,
# since the whole case block is a no-op for any name it doesn't match.
#
# No fake harness CLI needed: the sandbox message prints unconditionally when
# the case matches, BEFORE the adapter script (which is what actually checks
# `command -v <harness>`) ever runs — so this test only needs the harness name
# to reach the gate, not to successfully dispatch. Confirmed by reading
# run-harness itself: the only earlier existence check is
# `[ -f adapters/$HARNESS.sh ]`, not the CLI binary.
#
# Run: bash scripts/tests/test_run_harness_sandbox_gate.sh
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1
RH="$(pwd)/harness-adapter/run-harness"
fail=0
pass() { echo "ok   - $1"; }
bad()  { echo "FAIL - $1"; fail=1; }

[ -x "$RH" ] || { echo "FAIL - $RH not executable"; exit 1; }

# Every harness that HAS an adapter file must reach the sandbox gate in
# read-only mode. Derived from the real adapters/ directory, not hardcoded,
# so this test itself can't silently miss a newly added harness the way the
# gate it's testing once did.
# (plain read loop, not `mapfile` — bash 3.2, macOS's stock /bin/bash, has no
# mapfile builtin; this repo has already hit that class of portability gap
# once today)
HARNESSES=()
while IFS= read -r name; do HARNESSES+=("$name"); done < <(cd harness-adapter/adapters && ls *.sh | sed 's/\.sh$//' | sort)

if [ "${#HARNESSES[@]}" -eq 0 ]; then
  bad "no adapters found in harness-adapter/adapters/ — test setup is broken"
fi

for h in "${HARNESSES[@]}"; do
  # --timeout tiny: the underlying "harness CLI" won't exist on this machine,
  # so the adapter's own `command -v` check fails almost instantly — we only
  # care about what's on stderr before that point.
  out=$(echo "prompt" | bash "$RH" "$h" --mode read-only --timeout 5 2>&1 >/dev/null)
  if echo "$out" | grep -q "read-only: workspace write-locked via"; then
    pass "$h: reaches the sandbox gate (wrapper applied)"
  elif echo "$out" | grep -q "warning: no OS sandbox available — read-only is advisory for $h"; then
    pass "$h: reaches the sandbox gate (advisory fallback — no OS sandbox on this machine)"
  else
    bad "$h: did NOT reach the sandbox gate at all (this is exactly the missing-fx-arm bug class) — stderr: $out"
  fi
done

# A harness with no adapter file should fail at the existence check, well
# before ever reaching the sandbox gate — confirms the gate isn't somehow
# matching on an unrelated wildcard.
out=$(echo "prompt" | bash "$RH" totally-not-a-real-harness --mode read-only 2>&1 >/dev/null)
echo "$out" | grep -q "unknown harness" \
  && pass "an unregistered harness name fails at the existence check, not the sandbox gate" \
  || bad "unregistered harness name should fail with 'unknown harness' (got: $out)"

echo "---"
[ "$fail" = "0" ] && echo "ALL PASS" || echo "SOME FAILED"
exit "$fail"
