#!/usr/bin/env python3
"""Unit tests for skill_health_recovery. Run: python3 scripts/tests/test_skill_health_recovery.py"""
import json
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import skill_health_recovery as shr  # noqa: E402


class TestCriticalIncidentRecovery(unittest.TestCase):
    def test_recovery_does_not_wait_for_lifetime_success_rate(self):
        state = {
            "last_status": "success",
            "consecutive_failures": 0,
            "last_success": "2026-08-25T19:42:58Z",
            "success_rate": 0.33,
        }
        self.assertTrue(
            shr.critical_incident_recovered(state, "2026-08-25T19:42:49Z")
        )

    def test_success_before_incident_does_not_resolve_it(self):
        state = {
            "last_status": "failed",
            "consecutive_failures": 3,
            "last_success": "2026-08-24T19:42:58Z",
            "success_rate": 0.75,
        }
        self.assertFalse(
            shr.critical_incident_recovered(state, "2026-08-25T19:42:49Z")
        )

    def test_dispatch_after_success_waits_for_run_outcome(self):
        state = {
            "last_status": "dispatched",
            "consecutive_failures": 0,
            "last_success": "2026-08-25T19:42:58Z",
            "success_rate": 0.33,
        }
        self.assertFalse(
            shr.critical_incident_recovered(state, "2026-08-25T19:42:49Z")
        )

    def test_invalid_or_missing_timestamps_fail_closed(self):
        state = {
            "last_status": "success",
            "consecutive_failures": 0,
            "last_success": "not-a-time",
        }
        self.assertFalse(shr.critical_incident_recovered(state, "2026-08-25T19:42:49Z"))
        self.assertFalse(shr.critical_incident_recovered(state, None))
        state["last_success"] = "2026-08-25T19:42:58"
        self.assertFalse(shr.critical_incident_recovered(state, "2026-08-25T19:42:49Z"))

    def test_cli_reports_recovery(self):
        result = subprocess.run(
            [sys.executable, "scripts/skill_health_recovery.py", "2026-08-25T19:42:49Z"],
            input=json.dumps({
                "last_status": "success",
                "consecutive_failures": 0,
                "last_success": "2026-08-25T19:42:58Z",
                "success_rate": 0.33,
            }),
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "recovered")


if __name__ == "__main__":
    unittest.main(verbosity=2)
