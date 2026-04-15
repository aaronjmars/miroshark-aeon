#!/usr/bin/env bash
set -euo pipefail

# sync-upstream.sh — Update skills from upstream aaronjmars/aeon
#
# Usage:
#   ./scripts/sync-upstream.sh              Interactive sync
#   ./scripts/sync-upstream.sh --auto       Auto-update all outdated skills
#   ./scripts/sync-upstream.sh --dry-run    Show what would be updated
#   ./scripts/sync-upstream.sh --missing    Also install missing skills

UPSTREAM="${UPSTREAM_REPO:-aaronjmars/aeon}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AUTO=false
DRY_RUN=false
INCLUDE_MISSING=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --auto)     AUTO=true; shift ;;
    --dry-run)  DRY_RUN=true; shift ;;
    --missing)  INCLUDE_MISSING=true; shift ;;
    --upstream) UPSTREAM="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: ./scripts/sync-upstream.sh [--auto] [--dry-run] [--missing] [--upstream owner/repo]"
      exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if ! command -v jq &>/dev/null; then
  echo "jq is required. Install with: brew install jq / apt-get install jq" >&2
  exit 1
fi

LOCAL_JSON="$ROOT/skills.json"
if [[ ! -f "$LOCAL_JSON" ]]; then
  echo "Local skills.json not found. Run ./generate-skills-json first." >&2
  exit 1
fi

echo "Checking against upstream: $UPSTREAM"
echo ""

# Fetch upstream skills.json
UPSTREAM_TMP=$(mktemp)
trap 'rm -f "$UPSTREAM_TMP"' EXIT

if ! gh api "repos/$UPSTREAM/contents/skills.json" --jq '.content' | base64 -d > "$UPSTREAM_TMP" 2>/dev/null; then
  echo "Failed to fetch upstream skills.json from $UPSTREAM" >&2
  exit 1
fi

# Find outdated skills (SHA mismatch)
OUTDATED_SLUGS=()
OUTDATED_INFO=()
while IFS=$'\t' read -r slug local_sha upstream_sha updated; do
  [[ -z "$slug" ]] && continue
  if [[ -n "$local_sha" && -n "$upstream_sha" && "$local_sha" != "$upstream_sha" ]]; then
    OUTDATED_SLUGS+=("$slug")
    OUTDATED_INFO+=("$slug (local: $local_sha → upstream: $upstream_sha, updated: $updated)")
  fi
done < <(
  jq -r --slurpfile local "$LOCAL_JSON" '
    .skills[] |
    . as $up |
    ($local[0].skills // [] | map(select(.slug == $up.slug)) | first) as $loc |
    if $loc != null and ($up.sha // "") != "" and ($loc.sha // "") != "" then
      [$up.slug, ($loc.sha // ""), ($up.sha // ""), ($up.updated // "")] | @tsv
    else empty end
  ' "$UPSTREAM_TMP"
)

# Find missing skills
MISSING_SLUGS=()
while IFS=$'\t' read -r slug name; do
  [[ -z "$slug" ]] && continue
  MISSING_SLUGS+=("$slug")
done < <(
  jq -r --slurpfile local "$LOCAL_JSON" '
    .skills[] |
    . as $up |
    ($local[0].skills // [] | map(select(.slug == $up.slug)) | first) as $loc |
    if $loc == null then [$up.slug, $up.name] | @tsv else empty end
  ' "$UPSTREAM_TMP"
)

echo "Local skills: $(jq '.total' "$LOCAL_JSON")"
echo "Upstream skills: $(jq '.total' "$UPSTREAM_TMP")"
echo ""

# Report outdated
if [[ ${#OUTDATED_SLUGS[@]} -eq 0 ]]; then
  echo "All installed skills are up-to-date with upstream."
else
  echo "Outdated skills (${#OUTDATED_SLUGS[@]}):"
  for info in "${OUTDATED_INFO[@]}"; do
    echo "  • $info"
  done
  echo ""

  if [[ "$DRY_RUN" == "false" ]]; then
    for slug in "${OUTDATED_SLUGS[@]}"; do
      if [[ "$AUTO" == "true" ]]; then
        echo "Updating: $slug"
        "$ROOT/add-skill" "$UPSTREAM" "$slug"
      else
        read -rp "Update $slug from upstream? [y/N] " confirm
        if [[ "$confirm" =~ ^[Yy] ]]; then
          "$ROOT/add-skill" "$UPSTREAM" "$slug"
        else
          echo "  Skipped: $slug"
        fi
      fi
    done
  fi
fi

# Report missing
if [[ ${#MISSING_SLUGS[@]} -gt 0 ]]; then
  echo ""
  echo "Skills available upstream but not installed (${#MISSING_SLUGS[@]}):"
  for slug in "${MISSING_SLUGS[@]}"; do
    echo "  • $slug"
  done

  if [[ "$INCLUDE_MISSING" == "true" && "$DRY_RUN" == "false" ]]; then
    echo ""
    for slug in "${MISSING_SLUGS[@]}"; do
      if [[ "$AUTO" == "true" ]]; then
        echo "Installing: $slug"
        "$ROOT/add-skill" "$UPSTREAM" "$slug"
      else
        read -rp "Install $slug? [y/N] " confirm
        if [[ "$confirm" =~ ^[Yy] ]]; then
          "$ROOT/add-skill" "$UPSTREAM" "$slug"
        else
          echo "  Skipped: $slug"
        fi
      fi
    done
  elif [[ "$INCLUDE_MISSING" == "false" ]]; then
    echo "Run with --missing to install missing skills."
  fi
fi

if [[ "$DRY_RUN" == "true" ]]; then
  echo ""
  echo "(Dry run — no changes made)"
fi

echo ""
echo "Done."
