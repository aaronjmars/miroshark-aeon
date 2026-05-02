*Agent Self-Improvement — 2026-05-02*

Hyperstitions log-header resilience

The hyperstitions-ideas skill ran on schedule today (Sat 10:00 UTC) and produced its market question, but the LLM appended the bullet block to memory/logs/2026-05-02.md without writing the `## Hyperstitions Ideas` section header. That sets up a two-step cascade failure: the skill's own dedup guard keys off the header, and heartbeat's "did this run today?" check searches for the substring "hyperstitions" in the log — both would return empty. Tonight's 19:00 UTC heartbeat would conclude the skill never ran, dispatch it, and the operator would receive a second conflicting market question on the same coordination channel.

Why: Caught the missing header by `grep -i hyperstitions memory/logs/2026-05-02.md` returning empty after seeing only the bullet block in the day's log — every prior Saturday run (Mar 27, Mar 28, Apr 11, Apr 18, Apr 25) had carried the proper header. hyperstitions-ideas is not on heartbeat's auto-trigger skip-list, so a re-dispatch would have fired live. Picked over today's other minor drift (repo-pulse missing `**Notification sent:** yes` line) because the hyperstitions miss has a concrete duplicate-notification downstream consumer.

What changed:
- skills/hyperstitions-ideas/SKILL.md step 8: prepended an emphatic pre-block instruction — first appended line MUST be the literal `## Hyperstitions Ideas` header on its own line, with a footnote naming the dedup-guard / heartbeat / memory-flush consumers and citing today's failure as trigger.
- skills/hyperstitions-ideas/SKILL.md step 0: dedup guard now also matches a bare `- **Question:**` bullet when no Hyperstitions header sits above it — defensive backstop so even a future header-drop run is recognised as already-done by any subsequent dispatch attempt.
- memory/logs/2026-05-02.md: inserted the missing `## Hyperstitions Ideas` header above the existing bullet block so tonight's heartbeat sees the run as completed and doesn't re-dispatch.

Impact: prevents duplicate hyperstitions market questions in the operator channel on any day the LLM running the skill drops the header — both via the strengthened instruction (prevents the drop) and the bullet-pattern backstop (catches it if it still happens). Tonight's heartbeat will now find the patched header and stand down.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/28
