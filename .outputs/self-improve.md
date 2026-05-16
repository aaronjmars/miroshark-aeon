*Agent Self-Improvement — 2026-05-16*

Project-Lens PR Status Verification
The project-lens skill now requires `gh pr view --json state,mergedAt` for any PR it references by number, and asserts that the notification's PR-status verb (`opened`/`merged`/`closed`/`draft`) must match the article body word-for-word. If the two ever disagree, re-query gh and let the JSON win.

Why: The 2026-05-15 project-lens log self-reported a notification quality bug — the notification text said "merged" while the article body correctly said "opened". MiroShark PR #83 was still open at notify time (~16:10 UTC); it didn't merge until ~16:25 UTC. The skill had zero PR-state verification guidance, so the LLM's status assertion drifted between the two surfaces it produced in the same run.

What changed:
- skills/project-lens/SKILL.md: new PR-status verification bullet under step 5's writing guidelines (run gh pr view, cache the verb); pre-notification assertion at the top of step 6 (notification verbs must match article body; re-query on doubt).

Impact: Eliminates a class of factual error in the highest-visibility surface the skill emits (push to Telegram/Discord/Slack). One extra gh call per article (~30s) prevents a user-visible mismatch. Pattern is reusable — if repo-article or thread-formatter ever exhibit the same drift, the same two-line addition applies.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/40
