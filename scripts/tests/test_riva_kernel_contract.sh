#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
KERNEL="$ROOT/skills/vuln-scanner/riva.md"
[ -s "$KERNEL" ]
for phrase in \
  'security history' \
  'attacker' \
  'Trust boundaries' \
  'invariants' \
  'source-to-sink' \
  'Construct' \
  'Invert' \
  'Propagate' \
  'known-good' \
  'PoC-verification'; do
  grep -qi "$phrase" "$KERNEL" || { echo "Riva contract missing: $phrase" >&2; exit 1; }
done
echo "ok - Riva kernel contract contains required research stages"
