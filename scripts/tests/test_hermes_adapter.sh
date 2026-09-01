#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
printf 'score this output' > "$TMP/prompt"

cat > "$TMP/bin/hermes" <<'SH'
#!/usr/bin/env bash
if [ "${HERMES_STUB_MODE:-ok}" = api-error ]; then
  printf '%s\n' 'HTTP 400: modelCode: does not exist'
  exit 0
fi
printf '%s\n' 'usable hermes result'
SH
chmod +x "$TMP/bin/hermes"

run_adapter() {
  local mode=$1
  mkdir -p "$TMP/$mode"
  HERMES_STUB_MODE="$mode" \
    PATH="$TMP/bin:$PATH" \
    RH_LIB="$ROOT/harness-adapter/lib" \
    RH_TMPDIR="$TMP/$mode" \
    RH_PROMPT_FILE="$TMP/prompt" \
    RH_MODE=read-only \
    bash "$ROOT/harness-adapter/adapters/hermes.sh"
}

normal=$(run_adapter ok)
[ "$(jq -r '.result' <<<"$normal")" = 'usable hermes result' ] || {
  echo 'normal hermes output was not preserved' >&2
  exit 1
}

set +e
error=$(run_adapter api-error 2>&1)
rc=$?
set -e
[ "$rc" -eq 1 ] || { echo "hermes HTTP error returned rc=$rc, want 1" >&2; exit 1; }
grep -Fq 'hermes API error: HTTP 400: modelCode: does not exist' <<<"$error" || {
  echo "hermes HTTP error diagnostic missing: $error" >&2
  exit 1
}

echo 'hermes adapter error tests passed'
