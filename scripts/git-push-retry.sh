#!/usr/bin/env bash
# Shared rebase + conflict-resolve + push retry loop for aeon.yml's post-run
# git steps. Extracted from "Commit results" (unchanged behavior) so
# "Commit read-only failure log" can reuse the exact same fleet-safe push
# path instead of a second, drifting copy.
#
# Assumes the caller has already `git add`ed and `git commit`ed locally on
# the current branch — this script only gets that commit onto its remote
# counterpart under concurrent-writer contention (many skills push often).
set -uo pipefail

for i in 1 2 3 4 5 6 7 8 9 10; do
  # Pull and rebase onto latest remote
  if ! git pull --rebase origin "$(git branch --show-current)" 2>/dev/null; then
    echo "Rebase conflict on attempt $i, auto-resolving..."
    while true; do
      CONFLICTED=$(git diff --name-only --diff-filter=U) || true
      [ -z "$CONFLICTED" ] && break
      for f in $CONFLICTED; do
        if [[ "$f" == memory/logs/* ]] || [[ "$f" == memory/topics/* ]] || [[ "$f" == memory/MEMORY.md ]] || [[ "$f" == memory/skill-health/* ]] || [[ "$f" == apps/dashboard/outputs/* ]] || [[ "$f" == output/* ]]; then
          sed -i '/^<<<<<<< /d; /^=======/d; /^>>>>>>> /d' "$f"
          git add "$f"
        else
          git checkout --theirs "$f"
          git add "$f"
        fi
      done
      if git diff --cached --quiet; then
        git rebase --skip || true
      else
        GIT_EDITOR=true git rebase --continue || true
      fi
    done
  fi
  # Try to push — if it fails, another job beat us, loop and re-pull
  if git push -u origin HEAD 2>/dev/null; then
    echo "Pushed successfully on attempt $i"
    bash scripts/audit.sh "git.push" "${GITHUB_REPOSITORY:-}@$(git rev-parse --abbrev-ref HEAD)" 0 "GH_GLOBAL" || true
    exit 0
  fi
  echo "Push attempt $i failed (ref moved), retrying in ${i}s..."
  sleep "$(( (RANDOM % 4) + i ))"  # jittered backoff - a deterministic sleep re-collides lockstep writers under push contention
done
echo "Failed to push after 10 attempts"
exit 1
