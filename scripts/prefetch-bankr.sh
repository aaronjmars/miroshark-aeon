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

mkdir -p .bankr-cache

# Defensive crash sidecar — if the script exits with a non-zero status before
# reaching one of the write_status calls below, the EXIT trap stamps a "crashed"
# status so the skill can distinguish "script never ran" (workflow
# misconfiguration → file truly absent) from "script ran but bailed early"
# (e.g. set -e on an unexpected jq/grep failure → file present with exit_code).
# Triggered on TWEET_ALLOCATOR_ERROR drift observed 2026-05-24 where
# prefetch-status.json was missing and the cause was unrecoverable from logs.
trap 'PREFETCH_EXIT_CODE=$?
  if [ "$PREFETCH_EXIT_CODE" -ne 0 ] && [ -d .bankr-cache ] && [ ! -s .bankr-cache/prefetch-status.json ]; then
    jq -n \
      --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      --argjson code "$PREFETCH_EXIT_CODE" \
      "{status: \"crashed\",
        note: (\"prefetch-bankr.sh exited with code \" + (\$code|tostring) + \" before completing — see workflow logs\"),
        timestamp: \$ts,
        candidate_count: 0,
        lookup_attempted: 0,
        curl_failed: 0,
        verified_count: 0,
        null_count: 0,
        timed_out: 0,
        exit_code: \$code}" \
      > .bankr-cache/prefetch-status.json 2>/dev/null || true
  fi' EXIT

# Status sidecar — written at every exit point so the skill can tell what
# actually happened (no-api-key vs no-candidates vs lookups-failed vs ok)
# instead of guessing from an empty verified-handles.json.
write_status() {
  local status="$1"
  local note="${2:-}"
  local candidate_count="${3:-0}"
  local lookup_attempted="${4:-0}"
  local curl_failed="${5:-0}"
  local verified_count="${6:-0}"
  local null_count="${7:-0}"
  local timed_out="${8:-0}"
  jq -n \
    --arg status "$status" \
    --arg note "$note" \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --argjson candidate_count "$candidate_count" \
    --argjson lookup_attempted "$lookup_attempted" \
    --argjson curl_failed "$curl_failed" \
    --argjson verified_count "$verified_count" \
    --argjson null_count "$null_count" \
    --argjson timed_out "$timed_out" \
    '{status: $status, note: $note, timestamp: $ts,
      candidate_count: $candidate_count,
      lookup_attempted: $lookup_attempted,
      curl_failed: $curl_failed,
      verified_count: $verified_count,
      null_count: $null_count,
      timed_out: $timed_out}' \
    > .bankr-cache/prefetch-status.json
}

if [ -z "${BANKR_API_KEY:-}" ]; then
  echo "::warning::bankr-prefetch: BANKR_API_KEY not set — skipping Bankr lookups (tweet-allocator will mark all handles unverified)"
  echo "{}" > .bankr-cache/verified-handles.json
  write_status "no-api-key" "BANKR_API_KEY env var not set in workflow"
  exit 0
fi

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

# Exclude project-owned accounts (never allocate to these) and X.com reserved
# paths that are NOT user handles. `i` is the big one — XAI annotation citations
# surface as `x.com/i/status/<id>` URLs (3–4/day in recent fetch-tweets runs),
# and the path-level grep above slurps `i` in as if it were a handle. Without
# this filter, every prefetch wastes one Bankr Agent Max-Mode call (~16–112s
# polling budget) on `@i`, which Bankr cheerfully reports has no wallet.
# Reserved paths cover the broader x.com URL surface so any other non-handle
# path that lands in a log via a future content type is also skipped.
RESERVED_X_PATHS='^(i|home|explore|notifications|messages|compose|intent|settings|search|hashtag|share|lists|bookmarks|topics|moments|analytics|following|followers|jobs|verified-orgs|tos|privacy|about|login|signup|logout|account|help)$'
HANDLES=$(echo "$HANDLES" \
  | grep -viE '^(aaronjmars|miroshark_)$' \
  | grep -viE "$RESERVED_X_PATHS" \
  | grep -v '^$' \
  | head -25)

if [ -z "$HANDLES" ]; then
  echo "bankr-prefetch: no candidate handles found in .xai-cache/ or memory/logs/${TODAY}.md — nothing to verify"
  # Write an empty cache so the skill knows the prefetch ran
  echo "{}" > .bankr-cache/verified-handles.json
  write_status "no-candidates" "no candidate handles found in .xai-cache/ or today's log"
  exit 0
fi

COUNT=$(echo "$HANDLES" | wc -l | tr -d ' ')
echo "bankr-prefetch: looking up $COUNT handles on Bankr Agent API..."

# Start from an empty map (overwrite any stale cache)
echo "{}" > .bankr-cache/verified-handles.json

# Per-handle outcome counters surfaced into the status sidecar so the skill
# can distinguish "all curl calls failed" from "Bankr returned null for all"
# from "the LLM-backed Agent job did not complete in time."
LOOKUP_ATTEMPTED=0
CURL_FAILED=0
TIMED_OUT=0

bankr_lookup() {
  local handle="$1"
  LOOKUP_ATTEMPTED=$((LOOKUP_ATTEMPTED + 1))

  local payload
  payload=$(jq -n --arg h "$handle" \
    '{prompt: ("what is the wallet address for @" + $h + " on base? just tell me the 0x address or say no wallet"),
      maxMode: {enabled: true, model: "claude-sonnet-4.6"}}')

  local submit_response
  submit_response=$(curl -s --max-time 45 -X POST "https://api.bankr.bot/agent/prompt" \
    -H "X-API-Key: $BANKR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    echo "bankr-prefetch: @$handle — submit failed (curl error)"
    CURL_FAILED=$((CURL_FAILED + 1))
    return 1
  }

  local job_id
  job_id=$(echo "$submit_response" | jq -r '.jobId // .job_id // empty' 2>/dev/null)
  if [ -z "$job_id" ]; then
    echo "bankr-prefetch: @$handle — no jobId in response: $(echo "$submit_response" | head -c 200)"
    CURL_FAILED=$((CURL_FAILED + 1))
    return 1
  fi

  # Poll up to 14 × 8s = 112s. Max-Mode Agent calls (claude-sonnet-4.6) can
  # chain multiple tool calls inside Bankr; the previous 64s window timed out
  # for handles that were verifiable on slower-tier days (May 18–20 drift).
  local result=""
  local status=""
  for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
    result=$(curl -s --max-time 15 "https://api.bankr.bot/agent/job/$job_id" \
      -H "X-API-Key: $BANKR_API_KEY" 2>/dev/null) || break
    status=$(echo "$result" | jq -r '.status // ""' 2>/dev/null)
    [ "$status" = "completed" ] && break
    [ "$status" = "failed" ] && break
    sleep 8
  done

  # If the job never reached a terminal state, treat as a transient timeout
  # rather than "no wallet" — the agent might have answered eventually. Leave
  # the handle out of verified-handles.json entirely (same downstream effect
  # as null for this run, but surfaced separately in prefetch-status.json so
  # the skill can distinguish "Bankr genuinely doesn't know" from "we didn't
  # wait long enough for an LLM response").
  if [ "$status" != "completed" ] && [ "$status" != "failed" ]; then
    TIMED_OUT=$((TIMED_OUT + 1))
    echo "bankr-prefetch: @$handle → job timed out (last status=\"${status:-empty}\")"
    return 0
  fi

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
NULL_COUNT=$((TOTAL - VERIFIED))
echo "bankr-prefetch: done — $VERIFIED/$TOTAL handles have Bankr wallets ($CURL_FAILED curl failures + $TIMED_OUT job timeouts across $LOOKUP_ATTEMPTED attempts)"

if [ "$LOOKUP_ATTEMPTED" -gt 0 ] && [ "$CURL_FAILED" -eq "$LOOKUP_ATTEMPTED" ]; then
  STATUS_NOTE="all $LOOKUP_ATTEMPTED Bankr lookups failed at curl/jobId step (API down, key invalid, or rate-limited)"
  STATUS="lookups-failed"
elif [ "$VERIFIED" -eq 0 ] && [ "$TIMED_OUT" -gt 0 ] && [ "$TIMED_OUT" -ge "$NULL_COUNT" ]; then
  # Distinct from "completed-no-wallets" — the LLM-backed Agent jobs did not
  # finish in our polling window. Treated as a transient outage by the skill.
  STATUS_NOTE="$LOOKUP_ATTEMPTED handles checked, 0 verified — $TIMED_OUT Agent jobs did not complete within 112s ($NULL_COUNT returned no wallet, $CURL_FAILED curl failed)"
  STATUS="agent-timeout"
elif [ "$VERIFIED" -eq 0 ] && [ "$LOOKUP_ATTEMPTED" -gt 0 ]; then
  STATUS_NOTE="$LOOKUP_ATTEMPTED handles checked, 0 verified ($CURL_FAILED curl failed, $NULL_COUNT returned null, $TIMED_OUT timed out)"
  STATUS="completed-no-wallets"
else
  STATUS_NOTE="$VERIFIED/$LOOKUP_ATTEMPTED handles have Bankr wallets ($TIMED_OUT timed out)"
  STATUS="completed"
fi
write_status "$STATUS" "$STATUS_NOTE" "$COUNT" "$LOOKUP_ATTEMPTED" "$CURL_FAILED" "$VERIFIED" "$NULL_COUNT" "$TIMED_OUT"
ls -la .bankr-cache/ 2>/dev/null || true
