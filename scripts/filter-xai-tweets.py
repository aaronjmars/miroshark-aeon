#!/usr/bin/env python3
"""Post-filter Grok x_search results to drop tweets missing required tokens.

Guards against Grok returning tweets that only use the bare word "aeon" /
"miroshark" without the $ cashtag, @ handle, or github URL from the var.

Usage:
    filter-xai-tweets.py <cache_file> <var>

The var is interpreted as the OR-separated set of tokens that define a match.
Each numbered tweet block in the Grok text output must contain (case-
insensitive substring match) at least one of those tokens, else it's dropped.
The file is rewritten in place with renumbered, filtered blocks.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


BLOCK_START = re.compile(r"^\s*\d+\.\s", re.MULTILINE)


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
    kept = renumber(kept)
    body = "\n\n".join(kept)
    if preamble.strip():
        result = preamble.rstrip() + "\n\n" + body
    else:
        result = body
    return result, len(blocks), len(kept)


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
    for item in data.get("output", []) or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []) or []:
            if content.get("type") != "output_text":
                continue
            text = content.get("text", "") or ""
            filtered, orig, kept = filter_text(text, patterns)
            content["text"] = filtered
            total_orig += orig
            total_kept += kept

    cache_file.write_text(json.dumps(data))
    patterns_s = ", ".join(patterns)
    print(
        f"filter-xai-tweets: kept {total_kept}/{total_orig} tweets (patterns: {patterns_s})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
