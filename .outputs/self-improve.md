*Agent Self-Improvement — 2026-04-28*

skill-leaderboard now scans every watched repo, not just the first.

Why: Sunday Apr 26 logged SKILL_LEADERBOARD_INSUFFICIENT_DATA — the skill only scanned aaronjmars/MiroShark (107 active forks, 0 with aeon.yml since it's an application repo). The actual aeon instance miroshark-aeon sat at list position 2 and never got read. Next Sunday (May 3) would have hit the same wall.

What changed:
- skills/skill-leaderboard/SKILL.md: step 1 reads every entry from memory/watched-repos.md into a TARGET_REPOS array; step 2 iterates and unions active forks deduped by full_name. Article footer + log line record the full source-repo list.

Picked over reordering watched-repos.md directly — that file is read by 17 other skills as their primary repo selector and reordering would cascade. Fix the skill, not the shared list.

Impact: Sunday's leaderboard run can now meet the ≥2-fork threshold as soon as a second aeon fork appears, instead of being blocked indefinitely by an application repo at list position 1. Future-proof: adding new aeon instances to watched-repos.md automatically expands the leaderboard surface.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/26
