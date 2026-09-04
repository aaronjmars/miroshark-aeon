#!/usr/bin/env python3
"""Decide whether a critical skill-health incident has recovered."""

import json
import sys
from datetime import datetime


def _timestamp(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def critical_incident_recovered(state, detected_at):
    """Return true after a successful run newer than a critical incident."""
    if not isinstance(state, dict):
        return False
    last_success = _timestamp(state.get("last_success"))
    detected = _timestamp(detected_at)
    return (
        state.get("last_status") == "success"
        and state.get("consecutive_failures") == 0
        and last_success is not None
        and detected is not None
        and last_success > detected
    )


def main():
    detected_at = sys.argv[1] if len(sys.argv) == 2 else None
    try:
        state = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        state = None
    print("recovered" if critical_incident_recovered(state, detected_at) else "active")


if __name__ == "__main__":
    main()
