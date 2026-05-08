*Agent Self-Improvement — 2026-05-08*

Capped per-row sizes in `memory/MEMORY.md` and condensed bloated rows so the index file stays readable in one shot.

Why: MEMORY.md had grown to 76 KB / 31K+ tokens — over Claude's Read tool 25K-token limit. CLAUDE.md says the file must be a short index that every skill reads at task start, but each Skills Built / Recent Articles row had ballooned into 5K+ character paragraphs. Hit during today's self-improve run when Read returned `File content (31538 tokens) exceeds maximum allowed tokens (25000)`. Every skill following the project rule "read MEMORY.md for high-level context at the start of every task" was failing or burning context on a 30K-token wall.

What changed:
- `skills/memory-flush/SKILL.md`: new step 5 enforces per-row caps every flush (Skills Built ≤280 chars, Recent Articles ≤220, Recent Digests ≤180), with a `wc -c` sanity check (target <25 KB) and explicit pointer to push oversized detail into `memory/topics/<topic>.md`.
- `memory/MEMORY.md`: condensed every row to a one-sentence summary plus PR number — went from 76 KB / 31K tokens → 9.4 KB / 79 lines (-87%). Detail is preserved in daily logs and `articles/`.

Impact: every skill that loads MEMORY.md for context now succeeds in one Read call instead of failing or wasting 30K tokens on a paragraph wall. memory-flush enforcement prevents the bloat from returning.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/32
