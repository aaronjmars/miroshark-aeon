#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"

cat > "$TMP/bin/agent" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$AGENT_ARGS"
printf '%s\n' '{"result":"ok","usage":{},"session_id":"cursor-test"}'
SH
chmod +x "$TMP/bin/agent"
printf 'inspect this workspace' > "$TMP/prompt"

run_adapter() {
  local mode=$1
  AGENT_ARGS="$TMP/$mode.args" \
    PATH="$TMP/bin:$PATH" \
    RH_LIB="$ROOT/harness-adapter/lib" \
    RH_TMPDIR="$TMP/$mode-tmp" \
    RH_PROMPT_FILE="$TMP/prompt" \
    RH_MODE="$mode" \
    bash "$ROOT/harness-adapter/adapters/cursor.sh" >/dev/null
}

mkdir -p "$TMP/read-only-tmp" "$TMP/write-tmp"
run_adapter read-only
if ! grep -qx -- '--trust' "$TMP/read-only.args"; then
  echo 'read-only cursor run omitted --trust' >&2
  exit 1
fi
if grep -qx -- '--force' "$TMP/read-only.args"; then
  echo 'read-only cursor run unexpectedly received --force' >&2
  exit 1
fi

run_adapter write
grep -qx -- '--trust' "$TMP/write.args" || { echo 'write cursor run omitted --trust' >&2; exit 1; }
grep -qx -- '--force' "$TMP/write.args" || { echo 'write cursor run omitted --force' >&2; exit 1; }

echo 'cursor adapter trust tests passed'
