"""Wrapper to run feed tests against the cloned target repo."""
import sys
import subprocess

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_unit_feed.py", "-x", "-v"],
    cwd="/tmp/build-target/backend",
    capture_output=True,
    text=True,
)
sys.stdout.write(result.stdout)
sys.stderr.write(result.stderr)
sys.exit(result.returncode)
