#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WORKFLOW="$ROOT/.github/workflows/aeon.yml"

choices=$(awk '
  /^      harness:$/ { in_harness=1; next }
  in_harness && /^      var:$/ { exit }
  in_harness && /^          - / { sub(/^          - /, ""); print }
' "$WORKFLOW")

if ! grep -qx 'fx' <<<"$choices"; then
  echo 'workflow_dispatch harness choices omit fx' >&2
  exit 1
fi

python3 - "$WORKFLOW" <<'PY'
import sys

import yaml

workflow = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
for job_name, job in workflow.get("jobs", {}).items():
    for step in job.get("steps", []):
        run = step.get("run") if isinstance(step, dict) else None
        if isinstance(run, str) and len(run) > 20_500:
            name = step.get("name", "unnamed")
            raise SystemExit(
                f"workflow run expression too large: {job_name}/{name} "
                f"is {len(run)} characters (limit 21000, guard 20500)"
            )
PY

echo 'workflow harness choice tests passed'
