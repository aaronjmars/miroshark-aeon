"""Self-contained validation of surface_stats.py — no pytest needed.

Imports the local copy and exercises the full happy / sad path matrix,
including the one CI is going to run. Exits non-zero on any failure.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import surface_stats  # noqa: E402


def _check(label: str, cond: bool, *, detail: str = "") -> None:
    flag = "OK  " if cond else "FAIL"
    print(f"  {flag} {label}{(' — ' + detail) if detail else ''}")
    if not cond:
        raise SystemExit(f"FAILED: {label}")


def test_surface_keys_complete():
    expected = {
        "share_card", "replay_gif", "transcript_md", "transcript_json",
        "trajectory_csv", "trajectory_jsonl", "thread_txt", "thread_json",
        "watch_page", "feed_atom", "feed_rss",
    }
    _check("SURFACE_KEYS == expected set",
           set(surface_stats.SURFACE_KEYS) == expected)


def test_surface_stats_path_pure_join():
    with tempfile.TemporaryDirectory() as d:
        p = surface_stats.surface_stats_path(d)
        _check("surface_stats_path returns join", p == os.path.join(d, "surface-stats.json"))
        _check("surface_stats_path doesn't create file", not os.path.exists(p))


def test_increment_creates_file_at_one():
    with tempfile.TemporaryDirectory() as d:
        surface_stats.increment_surface_stat(d, "share_card")
        on_disk = json.loads(open(os.path.join(d, "surface-stats.json")).read())
        _check("share_card == 1 after one increment", on_disk["share_card"] == 1)


def test_repeated_increments_climb():
    with tempfile.TemporaryDirectory() as d:
        for _ in range(7):
            surface_stats.increment_surface_stat(d, "replay_gif")
        stats = surface_stats.read_surface_stats(d)
        _check("replay_gif == 7 after 7 increments", stats["replay_gif"] == 7)
        _check("share_card stays 0", stats["share_card"] == 0)
        _check("transcript_md stays 0", stats["transcript_md"] == 0)
        _check("total == 7", stats["total"] == 7)


def test_read_zero_defaults():
    with tempfile.TemporaryDirectory() as d:
        stats = surface_stats.read_surface_stats(d)
        for key in surface_stats.SURFACE_KEYS:
            _check(f"{key} zero-defaulted", stats[key] == 0)
        _check("total zero-defaulted", stats["total"] == 0)
        _check(
            "every SURFACE_KEY present",
            set(stats.keys()) >= set(surface_stats.SURFACE_KEYS) | {"total"},
        )


def test_increment_preserves_other_surfaces():
    with tempfile.TemporaryDirectory() as d:
        surface_stats.increment_surface_stat(d, "transcript_md")
        surface_stats.increment_surface_stat(d, "transcript_md")
        surface_stats.increment_surface_stat(d, "trajectory_csv")
        surface_stats.increment_surface_stat(d, "feed_rss")

        stats = surface_stats.read_surface_stats(d)
        _check("transcript_md == 2", stats["transcript_md"] == 2)
        _check("trajectory_csv == 1", stats["trajectory_csv"] == 1)
        _check("feed_rss == 1", stats["feed_rss"] == 1)
        _check("total == 4", stats["total"] == 4)


def test_unknown_key_dropped():
    with tempfile.TemporaryDirectory() as d:
        surface_stats.increment_surface_stat(d, "totally_made_up")
        _check(
            "no file written for unknown key",
            not os.path.exists(os.path.join(d, "surface-stats.json")),
        )
        stats = surface_stats.read_surface_stats(d)
        _check("totally_made_up not in stats", "totally_made_up" not in stats)
        _check("total == 0", stats["total"] == 0)


def test_falsy_sim_dir_no_op():
    surface_stats.increment_surface_stat(None, "share_card")
    surface_stats.increment_surface_stat("", "share_card")
    stats = surface_stats.read_surface_stats(None)
    _check("None sim_dir total == 0", stats["total"] == 0)
    for key in surface_stats.SURFACE_KEYS:
        _check(f"None sim_dir {key} == 0", stats[key] == 0)


def test_corrupt_json_resets():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "surface-stats.json"), "w") as fh:
            fh.write('{"share_card": 12, "replay_gif"')  # truncated
        stats = surface_stats.read_surface_stats(d)
        _check("share_card resets after corrupt read", stats["share_card"] == 0)
        _check("total resets after corrupt read", stats["total"] == 0)
        # Subsequent increment must succeed.
        surface_stats.increment_surface_stat(d, "share_card")
        stats = surface_stats.read_surface_stats(d)
        _check("share_card == 1 after re-write", stats["share_card"] == 1)


def test_negative_values_clamped():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "surface-stats.json"), "w") as fh:
            json.dump({"share_card": -5, "replay_gif": 3}, fh)
        stats = surface_stats.read_surface_stats(d)
        _check("negative clamped to 0", stats["share_card"] == 0)
        _check("positive preserved", stats["replay_gif"] == 3)
        _check("total reflects clamp", stats["total"] == 3)


def test_atomic_write_uses_replace():
    with tempfile.TemporaryDirectory() as d:
        with mock.patch.object(
            surface_stats.os, "replace", wraps=surface_stats.os.replace
        ) as spy:
            surface_stats.increment_surface_stat(d, "watch_page")
        _check("os.replace was called", spy.called)
        stats = surface_stats.read_surface_stats(d)
        _check("watch_page == 1", stats["watch_page"] == 1)


def test_replace_failure_swallowed():
    with tempfile.TemporaryDirectory() as d:
        with mock.patch.object(surface_stats.os, "replace", side_effect=OSError("disk full")):
            surface_stats.increment_surface_stat(d, "thread_txt")
        _check(
            "no canonical file left behind",
            not os.path.exists(os.path.join(d, "surface-stats.json")),
        )


def test_full_distribution_round_trip():
    with tempfile.TemporaryDirectory() as d:
        plan = [("share_card", 4), ("replay_gif", 2), ("transcript_md", 1),
                ("trajectory_csv", 3), ("watch_page", 1)]
        for key, n in plan:
            for _ in range(n):
                surface_stats.increment_surface_stat(d, key)
        stats = surface_stats.read_surface_stats(d)
        _check("share_card == 4", stats["share_card"] == 4)
        _check("replay_gif == 2", stats["replay_gif"] == 2)
        _check("transcript_md == 1", stats["transcript_md"] == 1)
        _check("trajectory_csv == 3", stats["trajectory_csv"] == 3)
        _check("watch_page == 1", stats["watch_page"] == 1)
        _check("total == 11", stats["total"] == 4 + 2 + 1 + 3 + 1)
        _check("thread_txt zero-default", stats["thread_txt"] == 0)
        _check("feed_atom zero-default", stats["feed_atom"] == 0)


def main():
    tests = [
        ("SURFACE_KEYS complete", test_surface_keys_complete),
        ("surface_stats_path is pure join", test_surface_stats_path_pure_join),
        ("increment creates file at 1", test_increment_creates_file_at_one),
        ("repeated increments climb", test_repeated_increments_climb),
        ("read zero-defaults every key", test_read_zero_defaults),
        ("increment preserves other surfaces", test_increment_preserves_other_surfaces),
        ("unknown surface key dropped", test_unknown_key_dropped),
        ("falsy sim_dir is no-op", test_falsy_sim_dir_no_op),
        ("corrupt JSON resets to zeros", test_corrupt_json_resets),
        ("negative on-disk values clamped", test_negative_values_clamped),
        ("atomic write uses os.replace", test_atomic_write_uses_replace),
        ("os.replace failure is swallowed", test_replace_failure_swallowed),
        ("full distribution round-trip", test_full_distribution_round_trip),
    ]
    print(f"Running {len(tests)} tests…")
    for label, fn in tests:
        print(f"\n[{label}]")
        fn()
    print(f"\nALL {len(tests)} tests passed.")


if __name__ == "__main__":
    main()
