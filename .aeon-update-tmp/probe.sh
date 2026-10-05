#!/usr/bin/env bash
set -euo pipefail
z=$(echo "subst-works")
echo "$z"
echo "redirect-works" > .aeon-update-tmp/probe.out
cat .aeon-update-tmp/probe.out
gh api repos/aeonfun/aeon --jq '.full_name'
