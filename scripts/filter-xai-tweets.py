#!/usr/bin/env python3
"""Post-filter Grok x_search results and harvest URL-citation annotations.

Two responsibilities:

1. Drop tweets that don't contain any required token from the OR-separated
   `var` (guards against Grok returning bare-word matches).

2. Harvest URL citations from `output_text.annotations[]` and splice any
   URL that isn't already rendered in `output_text.text` back in as a
   synthesized tweet block. Grok's `output_text.text` has a length cap
   and can truncate mid-stream while still collecting all citation URLs
   as annotations — without this step those extra tweets are invisible
   to skills that only jq-extract `.text`.

Usage:
    filter-xai-tweets.py <cache_file> <var>

The cache file is rewritten in place.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


BLOCK_START = re.compile(r"^\s*\d+\.\s", re.MULTILINE)
TWEET_URL = re.compile(
    r"https?://(?:www\.)?(?:x\.com|twitter\.com)/[^/\s]+/status/(\d+)",
    re.IGNORECASE,
)


def extract_patterns(var: str) -> list[str]:
    parts = re.split(r"\s+OR\s+", var, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def split_blocks(text: str) -> tuple[str, list[str]]:
    """Return (preamble_before_first_number, [block_1, block_2, ...])."""
    matches = list(BLOCK_START.finditer(text))
    if not matches:
        return text, []
    preamble = text[: matches[0].start()]
    blocks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append(text[start:end].rstrip())
    return preamble, blocks


def keep_block(block: str, patterns: list[str]) -> bool:
    low = block.lower()
    return any(p.lower() in low for p in patterns)


def renumber(blocks: list[str]) -> list[str]:
    return [
        re.sub(r"^\s*\d+\.", f"{i + 1}.", b, count=1)
        for i, b in enumerate(blocks)
    ]


def filter_text(text: str, patterns: list[str]) -> tuple[str, int, int]:
    preamble, blocks = split_blocks(text)
    if not blocks:
        return text, 0, 0
    kept = [b for b in blocks if keep_block(b, patterns)]
    kept_body = "\n\n".join(renumber(kept))
    if preamble.strip():
        result = preamble.rstrip() + "\n\n" + kept_body
    else:
        result = kept_body
    return result, len(blocks), len(kept)


def tweet_ids_in(text: str) -> set[str]:
    return {m.group(1) for m in TWEET_URL.finditer(text)}


def handle_from_url(url: str) -> str | None:
    """Extract @handle from an x.com tweet URL. Returns None for /i/status/ URLs."""
    m = re.match(
        r"https?://(?:www\.)?(?:x\.com|twitter\.com)/([^/\s]+)/status/\d+",
        url,
        re.IGNORECASE,
    )
    if not m:
        return None
    handle = m.group(1)
    if handle.lower() in {"i", "web", "intent"}:
        return None
    return handle


def harvest_annotations(content: dict) -> list[dict]:
    """Return a list of {url, title, handle} dicts from content.annotations[].

    Shape-defensive: accepts any annotation that carries a URL pointing to a
    tweet, regardless of the annotation's declared `type`. Unknown fields
    are ignored; missing optional fields are tolerated.
    """
    harvested: list[dict] = []
    seen: set[str] = set()
    for ann in content.get("annotations", []) or []:
        if not isinstance(ann, dict):
            continue
        url = ann.get("url") or ann.get("href") or ""
        if not url or not TWEET_URL.search(url):
            continue
        m = TWEET_URL.search(url)
        if not m:
            continue
        tweet_id = m.group(1)
        if tweet_id in seen:
            continue
        seen.add(tweet_id)
        title = ann.get("title") or ann.get("text") or ""
        harvested.append(
            {
                "url": url,
                "tweet_id": tweet_id,
                "title": title.strip() if isinstance(title, str) else "",
                "handle": handle_from_url(url),
            }
        )
    return harvested


def format_annotation_block(n: int, ann: dict) -> str:
    """Render a harvested annotation as a numbered tweet block.

    The block carries the URL (so the skill's dedup and notification logic
    see it) and any title/handle metadata we have; it's flagged as a citation
    so downstream processors can tell it apart from a fully-rendered tweet.
    """
    handle = ann["handle"]
    header = f"x.com/{handle}" if handle else ann["url"]
    summary = ann["title"] or "(annotation citation — no text in cache)"
    lines = [
        f"{n}. {header} — {summary}",
        "Source: XAI annotation citation",
        f"Link: {ann['url']}",
    ]
    return "\n".join(lines)


def splice_annotations(text: str, annotations: list[dict]) -> tuple[str, int]:
    """Append synthesized blocks for any annotation URL not already present.

    Annotation-derived blocks are NOT pattern-filtered: Grok's `x_search`
    run is already scoped by the var, so any citation it surfaced is
    relevant by construction.
    """
    if not annotations:
        return text, 0
    present = tweet_ids_in(text)
    missing = [a for a in annotations if a["tweet_id"] not in present]
    if not missing:
        return text, 0

    preamble, existing_blocks = split_blocks(text)
    start_n = len(existing_blocks) + 1
    new_blocks = [
        format_annotation_block(start_n + i, ann) for i, ann in enumerate(missing)
    ]
    stitched = "\n\n".join(existing_blocks + new_blocks)
    if preamble.strip():
        result = preamble.rstrip() + "\n\n" + stitched
    else:
        result = stitched
    return result, len(missing)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: filter-xai-tweets.py <cache_file> <var>", file=sys.stderr)
        return 2
    cache_file = Path(argv[1])
    var = argv[2]
    patterns = extract_patterns(var)
    if not patterns:
        print("filter-xai-tweets: no patterns from var, skipping", file=sys.stderr)
        return 0
    try:
        data = json.loads(cache_file.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"filter-xai-tweets: cannot read {cache_file}: {exc}", file=sys.stderr)
        return 1

    total_orig = 0
    total_kept = 0
    total_harvested = 0
    for item in data.get("output", []) or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []) or []:
            if content.get("type") != "output_text":
                continue
            text = content.get("text", "") or ""
            filtered, orig, kept = filter_text(text, patterns)
            annotations = harvest_annotations(content)
            spliced, added = splice_annotations(filtered, annotations)
            content["text"] = spliced
            total_orig += orig
            total_kept += kept
            total_harvested += added

    cache_file.write_text(json.dumps(data))
    patterns_s = ", ".join(patterns)
    summary = (
        f"filter-xai-tweets: kept {total_kept}/{total_orig} tweets "
        f"(patterns: {patterns_s})"
    )
    if total_harvested:
        summary += f"; spliced {total_harvested} annotation citation(s)"
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
