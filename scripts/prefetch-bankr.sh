#!/usr/bin/env bash
# Pre-fetch Bankr wallet verifications OUTSIDE the Claude sandbox.
# Called by the workflow before Claude runs. Saves results to .bankr-cache/
# so skills (tweet-allocator, distribute-tokens, etc.) can read cached wallet
# mappings instead of calling the Bankr Agent API from inside the sandbox —
# where curl with BANKR_API_KEY in headers fails due to env var expansion blocks.
#
# Usage: scripts/prefetch-bankr.sh <skill-name> [var]
# Runs automatically via the `for script in scripts/prefetch-*.sh` loop in aeon.yml.
set -euo pipefail

SKILL="${1:-}"
VAR="${2:-}"

if [ -z "$SKILL" ]; then
  echo "bankr-prefetch: no skill arg, skipping"
  exit 0
fi

# Only run for skills that consume the Bankr wallet cache
case "$SKILL" in
  tweet-allocator|distribute-tokens) ;;
  *)
    echo "bankr-prefetch: nothing to do for skill '$SKILL'"
    exit 0
    ;;
esac

if [ -z "${BANKR_API_KEY:-}" ]; then
  echo "::warning::bankr-prefetch: BANKR_API_KEY not set — skipping Bankr lookups (tweet-allocator will mark all handles unverified)"
  exit 0
fi

mkdir -p .bankr-cache

# Collect candidate handles from multiple sources (in freshness order):
# 1. .xai-cache/fetch-tweets.json (if prefetch-xai.sh just ran)
# 2. memory/logs/${today}.md (if fetch-tweets ran earlier and logged handles)
TODAY=$(date -u +%Y-%m-%d)
HANDLES=""

if [ -f ".xai-cache/fetch-tweets.json" ]; then
  FROM_CACHE=$(jq -r '.output[]? | select(.type == "message") | .content[]? | select(.type == "output_text") | .text' \
    .xai-cache/fetch-tweets.json 2>/dev/null \
    | grep -oE '@[A-Za-z0-9_]{1,15}' \
    | sed 's/^@//' \
    | sort -u)
  HANDLES="$FROM_CACHE"
fi

if [ -f "memory/logs/${TODAY}.md" ]; then
  FROM_LOG=$(grep -oE 'x\.com/[A-Za-z0-9_]{1,15}' "memory/logs/${TODAY}.md" 2>/dev/null \
    | sed 's|x\.com/||' \
    | sort -u)
  HANDLES=$(printf "%s\n%s\n" "$HANDLES" "$FROM_LOG" | sort -u)
fi

# Exclude project-owned accounts (never allocate to these)
HANDLES=$(echo "$HANDLES" | grep -viE '^(aaronjmars|miroshark_)$' | grep -v '^$' | head -25)

if [ -z "$HANDLES" ]; then
  echo "bankr-prefetch: no candidate handles found in .xai-cache/ or memory/logs/${TODAY}.md — nothing to verify"
  # Write an empty cache so the skill knows the prefetch ran
  echo "{}" > .bankr-cache/verified-handles.json
  exit 0
fi

COUNT=$(echo "$HANDLES" | wc -l | tr -d ' ')
echo "bankr-prefetch: looking up $COUNT handles on Bankr Agent API..."

# Start from an empty map (overwrite any stale cache)
echo "{}" > .bankr-cache/verified-handles.json

bankr_lookup() {
  local handle="$1"

  local payload
  payload=$(jq -n --arg h "$handle" \
    '{prompt: ("what is the wallet address for @" + $h + " on base? just tell me the 0x address or say no wallet")}')

  local submit_response
  submit_response=$(curl -s --max-time 30 -X POST "https://api.bankr.bot/agent/prompt" \
    -H "X-API-Key: $BANKR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    echo "bankr-prefetch: @$handle — submit failed (curl error)"
    return 1
  }

  local job_id
  job_id=$(echo "$submit_response" | jq -r '.jobId // .job_id // empty' 2>/dev/null)
  if [ -z "$job_id" ]; then
    echo "bankr-prefetch: @$handle — no jobId in response: $(echo "$submit_response" | head -c 200)"
    return 1
  fi

  local result=""
  local status=""
  for _ in 1 2 3 4 5 6 7 8; do
    result=$(curl -s --max-time 15 "https://api.bankr.bot/agent/job/$job_id" \
      -H "X-API-Key: $BANKR_API_KEY" 2>/dev/null) || break
    status=$(echo "$result" | jq -r '.status // ""' 2>/dev/null)
    [ "$status" = "completed" ] && break
    [ "$status" = "failed" ] && break
    sleep 8
  done

  # Try several common response shapes; grab the first 0x address we can find
  local text wallet
  text=$(echo "$result" | jq -r '.result // .output // .response // .data.response // .messages[-1].content // ""' 2>/dev/null)
  wallet=$(echo "$text" | grep -oE '0x[a-fA-F0-9]{40}' | head -1)

  local tmpfile=".bankr-cache/tmp.$$.json"
  if [ -n "$wallet" ]; then
    jq --arg h "$handle" --arg w "$wallet" '. + {($h): $w}' .bankr-cache/verified-handles.json > "$tmpfile" \
      && mv "$tmpfile" .bankr-cache/verified-handles.json
    echo "bankr-prefetch: @$handle → $wallet"
  else
    jq --arg h "$handle" '. + {($h): null}' .bankr-cache/verified-handles.json > "$tmpfile" \
      && mv "$tmpfile" .bankr-cache/verified-handles.json
    echo "bankr-prefetch: @$handle → no wallet"
  fi
}

while IFS= read -r HANDLE; do
  [ -z "$HANDLE" ] && continue
  bankr_lookup "$HANDLE" || true
done <<< "$HANDLES"

VERIFIED=$(jq -r 'to_entries | map(select(.value != null)) | length' .bankr-cache/verified-handles.json 2>/dev/null || echo 0)
TOTAL=$(jq -r 'to_entries | length' .bankr-cache/verified-handles.json 2>/dev/null || echo 0)
echo "bankr-prefetch: done — $VERIFIED/$TOTAL handles have Bankr wallets"
ls -la .bankr-cache/ 2>/dev/null || true
