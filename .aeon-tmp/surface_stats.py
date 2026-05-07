"""Per-share-surface request counters.

Closes the **inbound** observability gap that paired with the outbound
webhook delivery log (PR #73). Every public share surface
(``share-card.png``, ``replay.gif``, ``transcript.md`` / ``.json``,
``trajectory.csv`` / ``.jsonl``, ``thread.txt`` / ``.json``,
``/watch/<id>``, ``/api/feed.atom`` + ``feed.rss``) increments a counter
on disk after it serves a successful response.
"""

from __future__ import annotations

import json
import os
import tempfile
from typing import Dict, Optional


SURFACE_STATS_FILENAME = "surface-stats.json"


SURFACE_KEYS: frozenset[str] = frozenset(
    {
        "share_card",
        "replay_gif",
        "transcript_md",
        "transcript_json",
        "trajectory_csv",
        "trajectory_jsonl",
        "thread_txt",
        "thread_json",
        "watch_page",
        "feed_atom",
        "feed_rss",
    }
)


def surface_stats_path(sim_dir: str) -> str:
    return os.path.join(sim_dir or "", SURFACE_STATS_FILENAME)


def _empty_stats() -> Dict[str, int]:
    return {key: 0 for key in SURFACE_KEYS}


def _load_raw(path: str) -> Dict[str, int]:
    if not path or not os.path.exists(path):
        return _empty_stats()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except Exception:
        return _empty_stats()

    if not isinstance(raw, dict):
        return _empty_stats()

    stats = _empty_stats()
    for key in SURFACE_KEYS:
        value = raw.get(key, 0)
        try:
            ivalue = int(value)
        except (TypeError, ValueError):
            ivalue = 0
        stats[key] = max(0, ivalue)
    return stats


def _atomic_write(path: str, payload: Dict[str, int]) -> None:
    parent = os.path.dirname(path) or "."
    os.makedirs(parent, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        prefix=".surface-stats-", suffix=".tmp", dir=parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, sort_keys=True, separators=(",", ":"))
        os.replace(tmp_path, path)
    except Exception:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def increment_surface_stat(sim_dir: Optional[str], surface_key: str) -> None:
    if not sim_dir:
        return
    if surface_key not in SURFACE_KEYS:
        return

    path = surface_stats_path(sim_dir)

    try:
        if not os.path.isdir(sim_dir):
            return
        stats = _load_raw(path)
        stats[surface_key] = max(0, int(stats.get(surface_key, 0))) + 1
        _atomic_write(path, stats)
    except Exception:
        return


def read_surface_stats(sim_dir: Optional[str]) -> Dict[str, int]:
    if not sim_dir:
        result = _empty_stats()
        result["total"] = 0
        return result

    stats = _load_raw(surface_stats_path(sim_dir))
    total = sum(stats.values())
    result = dict(stats)
    result["total"] = total
    return result
