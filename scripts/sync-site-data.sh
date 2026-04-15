#!/usr/bin/env bash
#
# sync-site-data.sh — Copy memory, logs, and article metadata into docs/_data/
# for Jekyll to render as activity, memory, and article index pages.
#
# Usage: bash scripts/sync-site-data.sh
#
# Output: docs/_data/{logs.json, memory.json, topics.json, articles.json}
#

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"
DATA_DIR="$REPO_ROOT/docs/_data"

mkdir -p "$DATA_DIR"

# --- Helpers ---

json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

# --- 1. Activity logs ---
# Collect all log files into a JSON array, most recent first

LOGS_FILE="$DATA_DIR/logs.json"
echo "[" > "$LOGS_FILE"

first=true
for logfile in $(find "$REPO_ROOT/memory/logs" -name "*.md" -type f 2>/dev/null | sort -r); do
    date_str="$(basename "$logfile" .md)"
    content="$(cat "$logfile")"

    if [[ "$first" == true ]]; then
        first=false
    else
        echo "," >> "$LOGS_FILE"
    fi

    cat >> "$LOGS_FILE" <<ENTRY
  {
    "date": "$(json_escape "$date_str")",
    "content": "$(json_escape "$content")"
  }
ENTRY
done

echo "]" >> "$LOGS_FILE"

# --- 2. Memory index ---
# Copy MEMORY.md content as JSON

MEMORY_FILE="$DATA_DIR/memory.json"
memory_content=""
if [[ -f "$REPO_ROOT/memory/MEMORY.md" ]]; then
    memory_content="$(cat "$REPO_ROOT/memory/MEMORY.md")"
fi

cat > "$MEMORY_FILE" <<MEMJSON
{
  "content": "$(json_escape "$memory_content")"
}
MEMJSON

# --- 3. Topics ---
# Collect all topic files into a JSON array

TOPICS_FILE="$DATA_DIR/topics.json"
echo "[" > "$TOPICS_FILE"

first=true
for topicfile in $(find "$REPO_ROOT/memory/topics" -name "*.md" -type f 2>/dev/null | sort); do
    name="$(basename "$topicfile" .md)"
    content="$(cat "$topicfile")"

    if [[ "$first" == true ]]; then
        first=false
    else
        echo "," >> "$TOPICS_FILE"
    fi

    cat >> "$TOPICS_FILE" <<ENTRY
  {
    "name": "$(json_escape "$name")",
    "content": "$(json_escape "$content")"
  }
ENTRY
done

echo "]" >> "$TOPICS_FILE"

# --- 4. Article index ---
# Build a metadata-only index of all articles (for the articles page)

ARTICLES_FILE="$DATA_DIR/articles.json"
echo "[" > "$ARTICLES_FILE"

first=true
for articlefile in $(find "$REPO_ROOT/articles" -name "*.md" -type f 2>/dev/null | sort -r); do
    filename="$(basename "$articlefile")"

    # Extract date from filename
    if [[ "$filename" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        date_str="${BASH_REMATCH[1]}"
    else
        date_str="$(git -C "$REPO_ROOT" log -1 --format="%as" -- "$articlefile" 2>/dev/null || date -u +%Y-%m-%d)"
    fi

    # Extract title from first # heading
    title=""
    while IFS= read -r line; do
        if [[ "$line" == "---" ]]; then
            while IFS= read -r line; do [[ "$line" == "---" ]] && break; done
            continue
        fi
        if [[ "$line" =~ ^#[[:space:]]+(.*) ]]; then
            title="${BASH_REMATCH[1]}"
            break
        fi
    done < "$articlefile"
    [[ -z "$title" ]] && title="$(basename "$articlefile" .md)"

    # Extract first paragraph as summary
    summary=""
    found_title=false
    in_fm=false
    while IFS= read -r line; do
        if [[ "$in_fm" == false && "$line" == "---" ]]; then in_fm=true; continue; fi
        if [[ "$in_fm" == true ]]; then [[ "$line" == "---" ]] && in_fm=false; continue; fi
        [[ -z "$line" ]] && continue
        if [[ "$found_title" == false && "$line" =~ ^#[[:space:]] ]]; then found_title=true; continue; fi
        [[ "$line" =~ ^#+ ]] && continue
        summary="${line:0:200}"
        break
    done < "$articlefile"

    if [[ "$first" == true ]]; then
        first=false
    else
        echo "," >> "$ARTICLES_FILE"
    fi

    cat >> "$ARTICLES_FILE" <<ENTRY
  {
    "filename": "$(json_escape "$filename")",
    "title": "$(json_escape "$title")",
    "date": "$(json_escape "$date_str")",
    "summary": "$(json_escape "$summary")"
  }
ENTRY
done

echo "]" >> "$ARTICLES_FILE"

# --- Done ---

log_count=$(find "$REPO_ROOT/memory/logs" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
topic_count=$(find "$REPO_ROOT/memory/topics" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
article_count=$(find "$REPO_ROOT/articles" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

echo "Site data synced to $DATA_DIR:"
echo "  logs:     $log_count entries"
echo "  topics:   $topic_count files"
echo "  articles: $article_count files"
echo "  memory:   MEMORY.md"
